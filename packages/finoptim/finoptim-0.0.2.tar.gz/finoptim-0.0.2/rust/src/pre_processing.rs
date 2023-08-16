use ndarray::prelude::*;
use std::{ops::{Div, Range}, iter::zip};



pub fn create_steps(prices: ArrayView2<f64>, t: f64) -> Array1<f64>  {
    let (_, n) = prices.dim();
    let ri_price = prices.slice(s![2, ..]);
    let mut steps= Array::ones(n+1);
    let mut s =  steps.slice_mut(s![1..]);
    s.assign(&s.div(&ri_price));
    steps *= t;

    steps
}


pub fn create_space(usage: ArrayView2<f64>, prices: ArrayView2<f64>, p: f64) -> Vec<Range<f64>> {
    let min_usage = usage.fold_axis(Axis(0), f64::INFINITY, |a, &x| a.min(x));
    let max_usage = usage.fold_axis(Axis(0), -f64::INFINITY, |a, &x| a.max(x));
    let sp_prices = prices.slice(s![1, ..]);
    let max_sp = (&usage * &sp_prices).sum_axis(Axis(1)).fold(-f64::INFINITY, |a, &b| a.max(b));

    let mut space = Vec::with_capacity(usage.ncols() + 1);
    space.push(Range { start: 0., end: max_sp / p });

    for (borne_inf, borne_sup) in zip(min_usage, max_usage) {
        space.push(Range{ start: borne_inf / p, end: borne_sup / p});
    }
    
    space
}