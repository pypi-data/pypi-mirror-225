use std::{ops::Div, cmp::Ordering};

use ndarray::Axis;
use numpy::{IntoPyArray, PyArray1};
use pyo3::prelude::*;
use ndarray::prelude::*;
// use rayon::prelude::*;
use ndarray::parallel::prelude::*;
use argminmax::ArgMinMax;

use crate::cost_utils::{coverage, underutilisation, cost_scalar};


#[derive(Clone)]
#[pyclass(unsendable, frozen)]
pub struct Convergence {
    costs: Option<Array1<f64>>,
    coverages: Option<Array1<f64>>,
    discounts: Option<Array1<f64>>,
    choices: Option<Array1<usize>>,
    underutilisation_cost: Option<Array1<f64>>,
    speeds: Option<Array1<f64>>,
}

#[pymethods]
impl Convergence {

    fn get_underutilisation_cost<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.underutilisation_cost {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }

    fn get_costs<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.costs {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }

    fn get_coverages<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.coverages {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }

    fn get_discounts<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.discounts {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }

    fn get_speeds<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.speeds {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }

    fn get_choices<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<usize>> {
        match &self.choices {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }
}

#[pyclass(unsendable, frozen)]
#[derive(Clone)]
pub struct Results {
    pub argmin: Array1<usize>,
    #[pyo3(get)]
    pub n_iter: usize,
    #[pyo3(get)]
    pub minimum: f64,
    #[pyo3(get)]
    pub convergence: Convergence
}

impl Ord for Results {
    fn cmp(&self, other: &Self) -> Ordering {
        match self.minimum < other.minimum {
            true => Ordering::Less,
            false => if self.minimum == other.minimum {Ordering::Equal} else {Ordering::Greater}
        }
    }
}

impl PartialOrd for Results {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for Results {
    fn eq(&self, other: &Self) -> bool {
        self.minimum == other.minimum
    }
}

impl Eq for Results { }

#[pymethods]
impl Results {
    #[getter]
    fn argmin<'py>(&self,  py: Python<'py>) -> &'py PyArray1<usize> {
        self.argmin.clone().into_pyarray(py)
        // currently there's a copy here everytime Python wants to read this array
        // really not great
    }
}


fn l2_norm(x: ArrayView1<f64>) -> f64 {
    x.dot(&x).sqrt()
}

fn iterative_rounding(x: ArrayView1<f64>) -> Array1<f64> {
    let n = x.dim();
    let mut p = Array1::zeros(n);
    let mut indices = (0..n).collect::<Vec<_>>();
    indices.sort_by(|&a, &b| x[a].partial_cmp(&x[b]).expect("never empty"));
    indices.reverse();

    p[indices[0]] = 1.;
    let mut cos = 0.;
    let mut i = 1;
    let mut angle = p.dot(&x) / l2_norm(p.view());
    while (angle > cos) & (n > i) {
        p[indices[i]] = if x[indices[i]] < 0. {-1.} else {1.};
        cos = angle;
        angle = p.dot(&x) / l2_norm(p.view());
        i += 1;
    }
    p[indices[i]] = 0.;
    p
}

fn rounding<T: FnMut(ArrayView1<f64>)->f64>(
        function: &mut T,
        point: ArrayView1<f64>
        ) -> Array1<usize> {

    let mut x = point.to_owned();
    let n = point.len();

    let h: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 2]>> = Array2::from_diag(&Array1::ones(n));
    
    let mut grad = |x: ArrayView1<f64>| {
        let mut tmp = &h + &x;
        let c = function(x);
        tmp.map_axis_mut(Axis(1), |row| {
            function(row.view()) - c
        })
    };
    
    let cost_variations = grad(point.view());
    
    let mut indices = (0..n).collect::<Vec<_>>();
    indices.sort_by(|&a, &b| cost_variations[a].partial_cmp(&cost_variations[b]).expect("never empty"));
    indices.reverse();

    drop(grad);

    for i in indices {
        x[i] = x[i].floor();
        let cost_floor: f64 = function(x.view());
        x[i] += 1.;
        let cost_ceiling: f64 = function(x.view());
        x[i] -= if cost_floor < cost_ceiling {1.} else {0.};
    };

    x.mapv(|x: f64| x as usize)               
}


pub fn gradient_descent<T: FnMut(ArrayView1<f64>)->f64>(function: &mut T,
                                                        steps: ArrayView1<f64>,
                                                        start: ArrayView1<f64>) -> Results {

    let mut x = start.to_owned();
    let mut c = function(x.view());
    let h: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 2]>> = Array2::from_diag(&steps);

    let mut grad = |x: ArrayView1<f64>| {
        let mut tmp = &h + &x;
        let c = function(x);
        tmp.map_axis_mut(Axis(1), |row| {
            function(row.view()) - c
        })
    };
    
    let mut cost_variations = grad(x.view());

    let iter_max = 10_000;
    let mut n_iter = 0;
    let mut condition = true;
    let alpha = 0.001;
    // let mut costs = Vec::new();
    while condition && (n_iter < iter_max) {
        n_iter += 1;
        // print!("{c} \r");

        cost_variations = grad(x.view());
        x -= &(alpha * &cost_variations);
        x.mapv_inplace(|d| if d < 0. {0.} else {d});

        condition = l2_norm(cost_variations.view()) > 0.01;   
    }


    let argmin = rounding(function, x.view());
    Results {
        argmin: argmin.clone(),
        n_iter: n_iter,
        minimum: function(argmin.mapv(|x: usize| x as f64).view()),
        convergence : Convergence { costs: None,
                                    coverages: None,
                                    discounts: None,
                                    choices: None,
                                    underutilisation_cost: None,
                                    speeds: None }
    }
}



pub fn inertial_optimiser<T: FnMut(ArrayView1<f64>)->f64>(function: &mut T,
                                                            steps: ArrayView1<f64>,
                                                            start: ArrayView1<f64>) -> Results {

    let n = start.len();

    let mut x = start.to_owned();
    let mut c = function(x.view());
    let h: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 2]>> = Array2::from_diag(&steps);

    // let mut grad = |x: ArrayView1<f64>| {
    //     let mut tmp = &h + &x;
    //     let c = function(x);
    //     tmp.map_axis_mut(Axis(1), |row| {
    //         function(row.view()) - c
    //     })
    // };
    
    let mut speed =  Array::ones(n);
    // let mut cost_variations = grad(x.view());
    let mut tmp = &h + &x;
    let mut cost_variations = tmp.map_axis_mut(Axis(1), |row| {
        function(row.view()) - c
    });

    let drag = 0.8;
    let iter_max = 1_000;
    let mut n_iter = 0;
    let mut condition = true;
    let alpha = 0.001;
    let mut costs = Vec::new();
    while condition && (n_iter < iter_max) {
        n_iter += 1;
        // print!("{c} \r");

        tmp = &h + &x;
        cost_variations = tmp.map_axis_mut(Axis(1), |row| {
            function(row.view()) - c
        });

        // cost_variations = grad(x.view());
        speed = &speed * drag - &cost_variations;
        println!("{:?}", &(&speed * alpha));
        x += &(&speed * alpha);
        x.mapv_inplace(|d| if d < 0. {0.} else {d});

        c = function(x.view());
        costs.push(c);

        condition = l2_norm(speed.view()) > 0.1;   
    }


    let argmin = rounding(function, x.view());
    Results {
        argmin: argmin.clone(),
        n_iter: n_iter,
        minimum: function(argmin.mapv(|x: usize| x as f64).view()),
        convergence : Convergence { costs: Some(Array1::from_vec(costs)),
                                    coverages: None,
                                    discounts: None,
                                    choices: None,
                                    underutilisation_cost: None,
                                    speeds: None }
    }
}




pub fn best_optimiser_with_details(usage: Array2<f64>, prices: Array2<f64>, step_size:f64, start: Option<Array1<f64>>) -> Results {
    let n = usage.ncols();
    let timespan = usage.nrows();
    let ri_price = prices.slice(s![2, ..]);
    let mut dump = usage.to_owned(); // malloc here
    

    let mut up: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::ones(n+1);
    let mut s =  up.slice_mut(s![1..]);
    s.assign(&s.div(&ri_price));
    up *= step_size;

    let mut levels: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::zeros(n + 1);
    let mut returned_levels: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::zeros(n + 1);
    let min_usage = usage.fold_axis(Axis(0), f64::INFINITY, |a, &x| a.min(x)) / 24.;
    let mut s: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = levels.slice_mut(s![1..]);
    s.assign(&min_usage);

    levels = match start {
        Some(t) => t,
        None =>  levels
    };

    let mut c = cost_scalar(usage.view(), prices.view(), levels.view(), &mut dump);

    let h: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 2]>> = Array2::from_diag(&up);
    let mut b = true;
    let mut i = 0;
    let mut cost_variations = Vec::with_capacity(n+1);
    let mut costs: Vec<f64> = Vec::new();
    let mut coverages: Vec<f64> = Vec::new();
    let mut discounts: Vec<f64> = Vec::new();
    let mut choices: Vec<usize> = Vec::new();
    let mut underutilisations: Vec<f64> = Vec::new();

    let mut j = 0;
    while j < 500 {
        i += 1;
        // print!("iteration {i}\r");
        // also it is slower than the single-threaded version 🤡
        let g = &h + &levels;
        g.axis_iter(Axis(0))
                            .into_par_iter()
                            .with_min_len(n/8)
                            .map_init(
                            || dump.clone(),
                            |init, row| cost_scalar(usage.view(), prices.view(), row.view(), init) - c)
                            .collect_into_vec(&mut cost_variations);

        // println!("new_line");
        // let mut g = &h + &levels;
        // let trucs = g.map_axis_mut(Axis(1), |row| {
        //     cost(usage.view(), prices.view(), row.view(), &mut dump) - c
        // });
        // cost_variations = trucs.to_vec();
        let (arg_min, _) =  cost_variations.argminmax();
        b = cost_variations[arg_min] < 0.;
        if !b {
            j += 1;
        } else {
            returned_levels = levels.clone();
        }

        levels[arg_min] += up[arg_min];
        c += cost_variations[arg_min];

        costs.push(c);
        choices.push(arg_min);
        let two_dim_levels = Array2::zeros((timespan, levels.len())) + &levels;
        coverages.push(coverage(usage.view(), prices.view(), two_dim_levels.view()));
        discounts.push(cost_variations[arg_min] / (step_size * 24. * timespan as f64));
        underutilisations.push(underutilisation(usage.view(), prices.view(), levels.view(), &mut dump));

    }

    println!("done in {i} iterations !");

    let argmin = returned_levels.mapv(|x: f64| x as usize);
    Results {
        argmin: argmin.clone(),
        n_iter: i,
        minimum: cost_scalar(usage.view(), prices.view(), argmin.mapv(|x: usize| x as f64).view(), &mut dump.clone()),
        convergence : Convergence { costs: Some(Array1::from_vec(costs)),
                                    coverages: Some(Array1::from_vec(coverages)),
                                    discounts: Some(Array1::from_vec(discounts)),
                                    choices: Some(Array1::from_vec(choices)),
                                    underutilisation_cost: Some(Array1::from_vec(underutilisations)),
                                    speeds: None }
    }


}

pub fn best_optimiser<T: FnMut(ArrayView1<f64>)->f64>(
    function: &mut T,
    steps: ArrayView1<f64>,
    start: Array1<f64>)-> Results {

    let mut c = function(start.view());
    let n = start.len();
    let mut x = start.to_owned();

    let h: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 2]>> = Array2::from_diag(&steps);
    let mut b = true;
    let mut i = 0;
    let mut cost_variations = Vec::with_capacity(n+1);
    while b {
        i += 1;
        // print!("iteration {i}\r");

        let mut g = &h + &x;
        cost_variations = g.map_axis_mut(Axis(1), |row| {
            function(row.view()) - c
        }).to_vec();
        let (arg_min, _) =  cost_variations.argminmax();
        // println!("{}", cost_variations[arg_min]);
        b = cost_variations[arg_min] < 0.;

        if b {
            x[arg_min] += steps[arg_min];
            c += cost_variations[arg_min];
        }
    }


    println!("done in {i} iterations !");
    let argmin = rounding(function, x.view());
    Results {
        argmin: argmin.clone(),
        n_iter: i,
        minimum: function(argmin.mapv(|x: usize| x as f64).view()),
        convergence : Convergence { costs: None,
                                    coverages: None,
                                    discounts: None,
                                    choices: None,
                                    underutilisation_cost: None,
                                    speeds: None }
    }
}