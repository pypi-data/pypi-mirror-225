use std::collections::{HashMap, HashSet};
use std::iter::zip;
use std::ops::Range;

use ndarray::{prelude::*, IntoDimension, IxDynImpl, concatenate, stack};
use optimisers::Convergence;
use pyo3::types::PyDict;
use rand::{distributions::Uniform, Rng};
use std::ops::Div;

use numpy::{PyReadonlyArray2, PyArray1, PyReadonlyArray1, IntoPyArray, PyReadonlyArrayDyn, PyReadonlyArray3};
use pyo3::prelude::*;
use rayon::prelude::*;

mod optimisers;
mod cost_utils;
// mod tests;
mod pre_processing;
use crate::optimisers::{best_optimiser, inertial_optimiser, best_optimiser_with_details, Results, gradient_descent};
use crate::cost_utils::{cost, coverage, Order, Term, cost_final, final_coverage};
use crate::pre_processing::{create_steps, create_space};



// fn make_function(usage: ArrayView2<f64>, prices: ArrayView2<f64>, current_levels: ArrayView2<f64>) -> Box<dyn Fn(ArrayView1<f64>) -> f64> {
//     let (i, j) = usage.dim();
//     let mut two_dim_levels = Array2::zeros((i, j  + 1));
//     let mut dump = Array2::zeros((i, j));
//     let mut last_x = Array1::zeros(j + 1);
//     let f = move |x: ArrayView1<f64>| {
//         let changed = &x - &last_x;
//         cost(usage.view(), prices, &current_levels + &x, &mut dump)
//     };
//     Box::new(f)
// }


#[pyclass(unsendable, frozen)]
#[derive(Clone)]
pub struct FinalResults {
    pub commitments: HashMap<String, ArrayBase<ndarray::OwnedRepr<usize>, Dim<[usize; 1]>>>,
    #[pyo3(get)]
    pub n_iter: usize,
    #[pyo3(get)]
    pub minimum: f64,
    #[pyo3(get)]
    pub coverage: f64,
    #[pyo3(get)]
    pub convergence: Convergence
}

#[pymethods]
impl FinalResults {
    #[getter]
    fn commitments<'py>(&self,  py: Python<'py>) -> HashMap<String, &'py numpy::PyArray<usize, Dim<[usize; 1]>>> {
        let mut dict: HashMap<String, &numpy::PyArray<usize, Dim<[usize; 1]>>> = HashMap::new();
        for (k, v) in self.commitments.clone() {
            dict.insert(k, v.into_pyarray(py));
        }

        dict
    }
}

#[pymodule]
fn rust_as_backend(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    #[pyfn(m)]
    #[pyo3(name = "inertial_optimiser")]
    fn py_inertial_optimiser<'py>(usage: PyReadonlyArray2<f64>,
                                    prices: PyReadonlyArray2<f64>,
                                    n_starts: Option<usize>,
                                    starting_point: Option<PyReadonlyArray1<f64>>) -> Py<Results> {


        let usage = usage.as_array();
        let prices = prices.as_array();
        let n = usage.ncols();

        // each clojure here has its own memory to perform the cost computation
        // to make multiple threads, just call the factory ?
        let make_cost_function = move || {
            let mut dump = usage.to_owned();
            let (i, j) = usage.dim();
            println!("expensive copy");
            move |levels: ArrayView1<f64>| {
                let two_dim_levels = Array2::zeros((i, j  + 1)) + &levels;
                cost(usage.view(), prices.view(), two_dim_levels.view(), &mut dump)
            }
        };

        println!("starting optimiser");
        let steps = create_steps(prices.view(), 1.);


        let n_starts = match n_starts {
            Some(i) => i,
            None => 2
        };


        let res = match starting_point {
            Some(t) => inertial_optimiser(&mut make_cost_function(), steps.view(), t.as_array().view()),
            None  => {
                let space = create_space(usage.view(), prices.view(), 1.);

                let starts_vec: Vec<f64>= space.iter().map(|x| {
                    let range = Uniform::from(x.clone());
                    let tmp: Vec<f64> = rand::thread_rng().sample_iter(&range.clone()).take(n_starts).collect();
                    tmp.into_iter()
                }).flatten().collect();


                let starts = unsafe { Array2::from_shape_vec_unchecked((n + 1, n_starts), starts_vec) };


                let mut results = Vec::with_capacity(4);
                starts.axis_iter(Axis(1))
                    .into_par_iter()
                    .map_init(
                        make_cost_function,
                        |local_cost_function, start| inertial_optimiser(local_cost_function, steps.view(), start))
                    .collect_into_vec(&mut results);

                let res = results.iter().min().expect("not an empty set");

                (*res).to_owned()
            }
        };


        Python::with_gil(|py| Py::new(py, res).unwrap())
    }
    
    #[pyfn(m)]
    #[pyo3(name = "gradient_descent")]
    fn py_gradient_descent<'py>(usage: PyReadonlyArray2<f64>,
                                    prices: PyReadonlyArray2<f64>,
                                    n_starts: Option<usize>,
                                    starting_point: Option<PyReadonlyArray1<f64>>) -> Py<Results> {


        let usage = usage.as_array();
        let prices = prices.as_array();
        let n = usage.ncols();

        // each clojure here has its own memory to perform the cost computation
        // to make multiple threads, just call the factory ?
        let make_cost_function = move || {
            let mut dump = usage.to_owned();
            let (i, j) = usage.dim();
            println!("expensive copy");
            move |levels: ArrayView1<f64>| {
                let two_dim_levels = Array2::zeros((i, j  + 1)) + &levels;
                cost(usage.view(), prices.view(), two_dim_levels.view(), &mut dump)
            }
        };

        println!("starting optimiser");
        let steps = create_steps(prices.view(), 1.);


        let n_starts = match n_starts {
            Some(i) => i,
            None => 2
        };


        let res = match starting_point {
            Some(t) => gradient_descent(&mut make_cost_function(), steps.view(), t.as_array().view()),
            None  => {
                let space = create_space(usage.view(), prices.view(), 1.);

                let starts_vec: Vec<f64>= space.iter().map(|x| {
                    let range = Uniform::from(x.clone());
                    let tmp: Vec<f64> = rand::thread_rng().sample_iter(&range.clone()).take(n_starts).collect();
                    tmp.into_iter()
                }).flatten().collect();


                let starts = unsafe { Array2::from_shape_vec_unchecked((n + 1, n_starts), starts_vec) };

                let mut results = Vec::with_capacity(4);
                starts.axis_iter(Axis(1))
                    .into_par_iter()
                    .map_init(
                        make_cost_function,
                        |local_cost_function, start| gradient_descent(local_cost_function, steps.view(), start))
                    .collect_into_vec(&mut results);

                let res = results.iter().min().expect("not an empty set");

                (*res).to_owned()
            }
        };


        Python::with_gil(|py| Py::new(py, res).unwrap())
    }
    


    #[pyfn(m)]
    #[pyo3(name = "optimiser")]
    fn py_best_optimiser<'py>(usage: PyReadonlyArray2<f64>,
        prices: PyReadonlyArray2<f64>,
        period: String,
        step: Option<f64>,
        convergence_details: Option<bool>,
        starting_point: Option<PyReadonlyArray1<f64>>, 
    ) -> Py<Results> {

        let p = match period.as_str() {
            "D" => 24.,
            "H" => 1.,
            _ => {panic!("provide a valid period string : either D or H")}
        };

        let usage = usage.as_array();
        let prices = prices.as_array();
        // let mut s = prices.slice_mut(s![0, ..]);
        // s /= 24.;


        let t = match step {
            Some(t) => t,
            None => 1.
        };

        let space = create_space(usage.view(), prices.view(), p);
        let steps = create_steps(prices.view(), t);

        let start = match starting_point {
            Some(t) => t.as_array().to_owned(),
            None  => Array1::from_iter(space.iter().map(|x| x.start))
        };


        let make_cost_function = || {
            let (i, j) = usage.dim();
            let mut two_dim_levels = Array2::zeros((i, j  + 1));
            let mut dump = Array2::zeros((i, j));
            let prices = prices.to_owned();
            println!("expensive copies here");
            move |levels: ArrayView1<f64>| {
                two_dim_levels = Array2::zeros((i, j+1)) + &levels;
                cost(usage.view(), prices.view(), two_dim_levels.view(), &mut dump)
            }
        };



        let res = match convergence_details {
            Some(b) if b =>  best_optimiser_with_details(usage.to_owned(), prices.to_owned(), t, Some(start)),
            _ => best_optimiser(&mut make_cost_function(), steps.view(), start)
        };

        Python::with_gil(|py| Py::new(py, res).unwrap())
    }


    #[pyfn(m)]
    #[pyo3(name = "cost_distribution")]
    fn py_cost_distribution<'py>(
        py: Python<'py>,
        usage: PyReadonlyArray3<f64>,
        prices: PyReadonlyArray2<f64>,
        levels: PyReadonlyArray2<f64>) -> &'py PyArray1<f64> {
        let usage = usage.as_array();
        let prices = prices.as_array();
        let levels = levels.as_array();
    
        let (n, i, j) = usage.dim();
        let mut cost_samples = Vec::with_capacity(n+1);

        usage.axis_iter(Axis(0))
        .into_par_iter()
        .with_min_len(n/8)
        .map_init(
        || Array2::zeros((i, j)),
        |init, row| cost(row.view(), prices.view(), levels.view(), init))
        .collect_into_vec(&mut cost_samples);

        Array1::from_vec(cost_samples).into_pyarray(py)
    }


    #[pyfn(m)]
    #[pyo3(name = "optimise_predictions")]
    fn py_optimise_predictions<'py>(
        predictions: PyReadonlyArray3<f64>,
        prices: PyReadonlyArray2<f64>,
        levels: PyReadonlyArray2<isize>) -> Py<Results> {
        
        let predictions = predictions.as_array();
        let prices = prices.as_array();
        let current_levels = levels
        .as_array()
        .to_owned()
        .mapv(|x| usize::try_from(x).unwrap())
        .mapv(|x| x as f64);

        let (n, i, j) = predictions.dim();

        let make_cost_function = move || {
            let (_, i, j) = predictions.dim();
            let current_levels = current_levels.clone();
            let mut two_dim_levels = Array2::zeros((i, j  + 1));
            let mut dump = Array2::zeros((i, j));
            println!("expensive copies here");
            move |levels: ArrayView1<f64>| {
                two_dim_levels = &current_levels + &levels;
                predictions.axis_iter(Axis(0))
                .map(|pred| cost(pred.view(), prices.view(), two_dim_levels.view(), &mut dump))
                .sum() // here we just minimize the mean, but it could be a better idea to minimize the median or some quantile
                // but more compute intensive, as it implies one sort (but whatever)
            }
        };

        let space = predictions.fold_axis(
            Axis(2),
            Range { start: 0., end: 0. },
            |x, y| Range {
                start: y.min(x.start),
                end: y.max(x.end)
            }).into_raw_vec();
        
        let steps = create_steps(prices.view(), 1.);

        let res = best_optimiser(&mut make_cost_function(), steps.view(), Array1::from_iter(space.iter().map(|x| x.start)));

        Python::with_gil(|py| Py::new(py, res).unwrap())
    }

    #[pyfn(m)]
    #[pyo3(name = "cost")]
    fn py_cost(usage: PyReadonlyArray2<f64>, prices: PyReadonlyArray2<f64>, levels: PyReadonlyArrayDyn<'_, usize>) -> Option<f64> {
        let usage = usage.as_array();
        let prices = prices.as_array();

        let mut dump = usage.to_owned();
        let levels = levels
                            .as_array()
                            .to_owned()
                            .mapv(|x| x as f64);

        let z = match levels.dim().into_dimension().ndim() {
            1 => {
                let (i, j) = usage.dim();
                let one_dim_levels = levels.into_dimensionality::<Ix1>().unwrap();
                let two_dim_levels = Array2::zeros((i, j  + 1)) + &one_dim_levels;
                Some(cost(usage.view(),
                        prices.view(),
                        two_dim_levels.view(),
                        &mut dump))
                    },
            2 => Some(cost(usage.view(),
                        prices.view(),
                        levels.into_dimensionality::<Ix2>().unwrap().view(),
                        &mut dump)),
            _ => None
        };

        z
    }

    #[pyfn(m)]
    #[pyo3(name = "coverage")]
    fn py_coverage(usage: PyReadonlyArray2<f64>, prices: PyReadonlyArray2<f64>, levels: PyReadonlyArrayDyn<'_, usize>) -> Option<f64> {
        let usage = usage.as_array();
        let prices = prices.as_array();

        let levels = levels.as_array()
                            .to_owned()
                            .mapv(|x| x as f64);

        let z = match levels.dim().into_dimension().ndim() {
            1 => {
                let (i, j) = usage.dim();
                let one_dim_levels = levels.into_dimensionality::<Ix1>().unwrap();
                let two_dim_levels = Array2::zeros((i, j  + 1)) + &one_dim_levels;
                Some(coverage(usage.view(),
                        prices.view(),
                        two_dim_levels.view()))
            },
            2 => Some(coverage(usage.view(),
                        prices.view(),
                        levels.into_dimensionality::<Ix2>().unwrap().view())),
            _ => None
        };

        z
    }


    #[pyfn(m)]
    #[pyo3(name = "optim_final")]
    fn py_optim_final(usage: PyReadonlyArray2<f64>,
        prices: PyReadonlyArray2<f64>,
        pricing_models: Vec<&str>,
        period: &str) -> Py<FinalResults> {

        let b = period == "D";
        let usage = usage.as_array();
        let prices = prices.as_array();

        let mut models = Vec::with_capacity(pricing_models.len());
        let (timespan, n) = usage.dim();
        let mut j = 0;
        for (i, p) in pricing_models.into_iter().enumerate() {
            let model = match p {
                "OD" => Order::OnDemand(i),
                "RI1Y" => Order::Reservations(Term::OneYear, Range { start: j, end: j + n}, i),
                "RI3Y" => Order::Reservations(Term::ThreeYears, Range { start: j, end: j + n }, i),
                "SP1Y" => Order::SavingsPlans(Term::OneYear, j, i),
                "SP3Y" => Order::SavingsPlans(Term::ThreeYears, j, i),
                _ => panic!("Not a known priving model")
            };
            match model {
                Order::Reservations(_, _, _) => j += n,
                Order::SavingsPlans(_, _, _) => j += 1,
                _ => ()
            }

            models.push(model);
        }
        let levels = Array1::zeros(j);
        models.sort();

        let mut steps: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>>= Array::ones(j);
        let mut average_cost = 1000.;
        for i in models.iter() {
            match i {
                Order::Reservations(_, indexes, price_index) => {
                    let mut s =  steps.slice_mut(s![indexes.start..indexes.end]);
                    s.assign(&s.div(&prices.slice(s![*price_index, ..])));
                },
                Order::OnDemand(j) => {
                    average_cost = (&usage * &prices.slice(s!(*j, ..))).sum() / timespan as f64;
                },
                _ => ()
            }
        }
        steps *= average_cost / 5_000.;
        // println!("step size : {}", average_cost / 10_000.);

        let make_cost_function = || {
            let mut two_dim_levels = Array2::zeros((timespan, j));
            let mut dump = Array2::zeros((timespan, n));
            let prices = prices.to_owned();
            let models = models.clone();
            // println!("{:?}", models);
            println!("expensive copies here");
            move |levels: ArrayView1<f64>| {
                two_dim_levels = Array2::zeros((timespan, j)) + &levels;
                cost_final(usage.view(), prices.view(), &mut two_dim_levels, &models, b, &mut dump)
            }
        };

        let res = best_optimiser(&mut make_cost_function(), steps.view(), levels);
        
  
        let mut returned_df: HashMap<String, ArrayBase<ndarray::OwnedRepr<usize>, Dim<[usize; 1]>>> =  HashMap::new();
        // returned_df.insert("price", Array1::zeros(n + 1));

        for model in models {
            match model {
                Order::Reservations(t, indexes, price_index) => {
                    let mut r =  Array1::zeros(n + 1);
                    let mut s =  r.slice_mut(s![1..]);
                    s.assign(&res.argmin.slice(s![indexes.start..indexes.end]));
                    match t {
                        Term::OneYear => {
                            returned_df.insert(String::from("one_year_commitments"), r);
                        },
                        Term::ThreeYears => {
                            returned_df.insert(String::from("three_year_commitments"), r);
                        }
                    }
                }
                Order::SavingsPlans(t, index, price_index) => {
                    match t {
                        Term::OneYear => {
                            returned_df.get_mut("one_year_commitments").unwrap()[0] = res.argmin[index];
                        },
                        Term::ThreeYears => {
                            returned_df.get_mut("three_year_commitments").unwrap()[0] = res.argmin[index];
                        }
                    }
                },
                Order::OnDemand(_) => ()
            } 
        }


        let fres = FinalResults {
            commitments : returned_df,
            n_iter : res.n_iter,
            coverage : 2.,
            minimum : res.minimum,
            convergence : res.convergence

        };
        Python::with_gil(|py| Py::new(py, fres).unwrap())        
    }


    #[pyfn(m)]
    #[pyo3(name = "final_cost_or_coverage")]
    fn py_cost_final(usage: PyReadonlyArray2<f64>,
        prices: PyReadonlyArray2<f64>,
        levels: PyReadonlyArray2<f64>,
        pricing_models: Vec<&str>,
        period: &str,
        cost_or_coverage: bool) -> f64 {

            let b = period == "D";
            let usage = usage.as_array();
            let prices = prices.as_array();
            let mut levels = levels.as_array().to_owned().mapv(|x| x as f64);
    
            let mut models = Vec::with_capacity(pricing_models.len());
            let (timespan, n) = usage.dim();
            let mut dump = Array2::zeros((timespan, n));
            let mut j = 0;
            for (i, p) in pricing_models.into_iter().enumerate() {
                let model = match p {
                    "OD" => Order::OnDemand(i),
                    "RI1Y" => Order::Reservations(Term::OneYear, Range { start: j, end: j + n}, i),
                    "RI3Y" => Order::Reservations(Term::ThreeYears, Range { start: j, end: j + n }, i),
                    "SP1Y" => Order::SavingsPlans(Term::OneYear, j, i),
                    "SP3Y" => Order::SavingsPlans(Term::ThreeYears, j, i),
                    _ => panic!("Not a known priving model")
                };
                match model {
                    Order::Reservations(_, _, _) => j += n,
                    Order::SavingsPlans(_, _, _) => j += 1,
                    _ => ()
                }
    
                models.push(model);
            }

            if cost_or_coverage {
                cost_final(usage.view(), prices.view(), &mut levels, &models, b, &mut dump)
            } else {
                final_coverage(usage.view(), prices.view(), &mut levels, &models, b, &mut dump)
            }
        }


    m.add_class::<Results>()?;


    Ok(())
}


