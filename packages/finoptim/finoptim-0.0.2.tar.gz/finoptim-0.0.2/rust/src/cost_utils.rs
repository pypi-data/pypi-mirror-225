use std::cmp::Ordering;
use std::ops::Range;

use ndarray::Zip;
use ndarray::prelude::*;


#[derive(PartialEq, Eq, Clone, Debug)]
pub enum Term {
    ThreeYears,
    OneYear
}

#[derive(PartialEq, Eq, Clone, Debug)]
pub enum Order {
    OnDemand(usize),
    Reservations(Term, Range<usize>, usize),
    SavingsPlans(Term, usize, usize)
}

impl Order {
    fn norm(&self) -> isize {
        match self {
            Order::OnDemand(_) => 4,
            Order::SavingsPlans(t, _, _) => if *t == Term::OneYear {3} else {2},
            Order::Reservations(t, _, _) => if *t == Term::OneYear {1} else {0},
        }
    }
}

impl PartialOrd for Order {
    fn partial_cmp(&self, other: &Order) -> Option<Ordering> {
        match self.norm() - other.norm() {
            -4..=-1 => Some(Ordering::Less),
            0 => Some(Ordering::Equal),
            1..=4 => Some(Ordering::Greater),
            _ => panic!("not supposed to happend anyway"),
        }
    }
}

impl Ord for Order {
    fn cmp(&self, other: &Self) -> Ordering {
        match self.norm() - other.norm() {
            -4..=-1 => Ordering::Greater,
            0 => Ordering::Equal,
            1..=4 => Ordering::Less,
            _ => panic!("not supposed to happen anyway"),
        }
    }
}

pub fn cost_scalar(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: ArrayView1<f64>,
    dump: &mut Array2<f64>) -> f64 {
    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![1..]);
    let s = levels[0];
    let timespan = usage.nrows();

    let mut cost = (&reservations * &ri_price).sum() + s;
    cost *= 24. * timespan as f64;
    
    *dump = &usage - &reservations;
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    let mut s: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::ones(timespan) * s * 24.;
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };

    *dump *= &od_price;

    cost + dump.sum()
}



pub fn cost(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: ArrayView2<f64>,
    dump: &mut Array2<f64>)
     -> f64 {
    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![.., 1..]);
    let mut s = levels.slice(s![.., 0]).to_owned();

    let cost = (&reservations * &ri_price).sum() + s.sum();
    
    *dump = &usage - &reservations;
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };


    *dump *= &od_price;

    cost + dump.sum()
}

pub fn coverage(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: ArrayView2<f64>)
    -> f64 {


    let od_price = prices.slice(s![0, ..]);
    let sp_price = prices.slice(s![1, ..]);
    let reservations = levels.slice(s![.., 1..]);
    let mut s = levels.slice(s![.., 0]).to_owned();

    let denum = (&usage * &od_price).sum();
    let mut num = reservations.sum_axis(Axis(0));
    
    let mut col_i = usage.column(0).to_owned();

    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        col_i = 0. + &usage.column(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        num[i] += min.sum(); // hours of savings plans used
        min *= sp_price[i];
        s -= &min;
    };

    // ((num * od_price).sum() + s.sum()) / denum
    (num * od_price).sum() / denum

}


pub fn underutilisation(usage: ArrayView2<f64>, prices: ArrayView2<f64>, levels: ArrayView1<f64>, dump: &mut Array2<f64>) -> f64 {
    let sp_price = prices.slice(s![1, ..]);
    let ri_price = prices.slice(s![2, ..]);
    let reservations = levels.slice(s![1..]);
    let s = levels[0];
    let timespan = usage.nrows();

    let mut underutilisation = 0.;
    
    *dump = &usage - &reservations;
    underutilisation += ((*dump).mapv(|d| if d < 0. {-d} else {0.}) * ri_price).sum();
    (*dump).mapv_inplace(|d| if d < 0. {0.} else {d});
    
    let mut s: ArrayBase<ndarray::OwnedRepr<f64>, Dim<[usize; 1]>> = Array::ones(timespan) * s * 24.;
    for i in 0..usage.ncols() {
        let ss = &s / sp_price[i];
        let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
        let mut min = col_i.to_owned();
        Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});

        col_i -= &min;
        min *= sp_price[i];
        s -= &min;
    };

    underutilisation + s.sum()
}



pub fn cost_final(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: &mut Array2<f64>,
    models: &Vec<Order>,
    days: bool,
    dump: &mut Array2<f64>)-> f64  {

    let timespan = usage.nrows();
    let mut cost = Array1::zeros(timespan);

    for model in models.iter() {
        match model {
            Order::Reservations(term, level_indexes, price_index) => {
                let mut max_duration = if *term == Term::OneYear {365} else {1095};
                // substract the reservations to the usage and add them to the cost vector
                let (start, end) = (level_indexes.start, level_indexes.end);
                let mut reservations = levels.slice_mut(s![.., start..end]);
                if days {reservations *= 24.;} else {max_duration *= 24;}
                let mut unvalid_res = reservations.slice_mut(s![max_duration.min(timespan).., ..]);
                unvalid_res *= 0.;
                let jjj = prices.slice(s![*price_index, ..]);
                cost += &(&reservations * &jjj).sum_axis(Axis(1));

                *dump = &usage - &reservations;
                (*dump).mapv_inplace(|d| if d < 0. {0.} else {d}); // find a way to only make this once if there are two RI fields
            },
            Order::SavingsPlans(term, level_index, price_index) => {
                let mut max_duration = if *term == Term::OneYear {365} else {1095};
                if !days {max_duration *= 24;}
                let mut s = levels.slice(s![.., *level_index]).to_owned();
                let mut unvalid_sp = s.slice_mut(s![max_duration.min(timespan)..]);
                unvalid_sp *= 0.;
                cost += &s;
                for i in 0..usage.ncols() {
                    let ss = &s / prices[[*price_index, i]];
                    let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
                    let mut min = col_i.to_owned();
                    Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});
                    col_i -= &min;
                    min *= prices[[*price_index, i]];
                    s -= &min;
                };
            },
            Order::OnDemand(price_index) => {
                let od_price = prices.slice(s![*price_index, ..]);
                *dump *= &od_price;
                cost += &dump.sum_axis(Axis(1));
            }
        }
    }

    cost.sum()
}


pub fn final_coverage(
    usage: ArrayView2<f64>,
    prices: ArrayView2<f64>,
    levels: &mut Array2<f64>,
    models: &Vec<Order>,
    days: bool,
    dump: &mut Array2<f64>)-> f64  {

    let timespan = usage.nrows();
    let mut cost = Array1::zeros(timespan);

    let mut num = 0.;
    let mut denum = Array1::zeros(timespan);
    let mut unused_sp = 0.;

    for model in models.iter() {
        match model {
            Order::Reservations(term, level_indexes, price_index) => {
                let mut max_duration = if *term == Term::OneYear {365} else {1095};
                // substract the reservations to the usage and add them to the cost vector
                let (start, end) = (level_indexes.start, level_indexes.end);
                let mut reservations = levels.slice_mut(s![.., start..end]);
                if days {reservations *= 24.;} else {max_duration *= 24;}
                let mut unvalid_res = reservations.slice_mut(s![max_duration.min(timespan).., ..]);
                unvalid_res *= 0.;

                denum = reservations.sum_axis(Axis(0));

                *dump = &usage - &reservations;
                (*dump).mapv_inplace(|d| if d < 0. {0.} else {d}); // find a way to only make this once if there are two RI fields
            },
            Order::SavingsPlans(term, level_index, price_index) => {
                let mut max_duration = if *term == Term::OneYear {365} else {1095};
                if !days {max_duration *= 24;}
                let mut s = levels.slice(s![.., *level_index]).to_owned();
                let mut unvalid_sp = s.slice_mut(s![max_duration.min(timespan)..]);
                unvalid_sp *= 0.;

                cost += &s;
                for i in 0..usage.ncols() {
                    let ss = &s / prices[[*price_index, i]];
                    let mut col_i: ArrayBase<ndarray::ViewRepr<&mut f64>, Dim<[usize; 1]>> = (*dump).column_mut(i);
                    let mut min = col_i.to_owned();
                    Zip::from(&mut min).and(&ss).for_each(|z, &y| {*z = z.min(y)});
                    col_i -= &min;
                    denum[i] += min.sum();
                    min *= prices[[*price_index, i]];
                    s -= &min;
                };
                unused_sp += s.sum();
            },
            Order::OnDemand(price_index) => {
                let od_price = prices.slice(s![*price_index, ..]);
                num = (&usage * &od_price).sum();
                denum *= &od_price;
            }
        }
    }

    num / (denum.sum() + unused_sp)
}