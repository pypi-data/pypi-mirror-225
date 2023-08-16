import numpy as np
import pandas as pd

# import the contents of the Rust library into the Python extension
# optional: include the documentation from the Rust module
# __all__ = __all__ + ["PythonClass"]

import finoptim.rust_as_backend as rs

from datetime import datetime, date, timedelta
from dataclasses import dataclass
from typing import Optional, List, Union, Callable, Dict


@dataclass
class FinalResults:
    """Class for keeping tidy results."""
    optimal_arangment: pd.DataFrame
    minimum: float
    coverage: float
    n_iter: int = 0
    convergence: Optional[List[float]] = None
    formatted: Optional[pd.DataFrame] = None

    def format(self, **kwargs: List[dict]) -> pd.DataFrame:
        """create a new `DataFrame` out of `self.optimal_arangment` with prettier values.
        it is sorted by price, and you can add any columns you want using a dictionnary mapping
        the *guid*s to your wanted values

        Returns:
            pd.DataFrame: prettier DataFrame

        Examples
        --------
        ```python
        res = fp.optimise(df_real, prices_df)
        guid_to_instance_name = {"K7YHHNFGTNN2DP28" : 'i3.large', 'SAHHHV5TXVX4DCTS' : 'r5.large'}
        res.format(instance_type=guid_to_instance_name)
        print(res)
        >>>
        ╭─────────────────┬──────────────────────────┬───────────────╮
        │ instance_type   │  three_year_commitments  │  price_per_D  │
        ├─────────────────┼──────────────────────────┼───────────────┤
        │ i3.large        │           1338           │     2,886     │
        │ r5.large        │           1570           │     2,564     │
        │ savings plans   │           1937           │     1,937     │
        ╰─────────────────┴──────────────────────────┴───────────────╯
        ```
        """
        res = self.optimal_arangment
        price_col, rest = res.columns[-1], res.columns[:-1]
        md = res.loc[res[price_col] != 0].drop_duplicates().sort_values(by=price_col, ascending=False)

        for k, mapping in kwargs.items():
            md[k] = md.index.map(mapping)
        md = md[list(kwargs) + list(rest) + [price_col]]
        self.formatted = md
        return md

    def __repr__(self) -> str:
        if self.formatted is None:
            return str(self.minimum)
        return self.formatted.to_markdown(index=False, tablefmt='rounded_outline', floatfmt=',.0f', numalign='center')

def add_one(x: int) -> int:
    """see if documentation works

    Args:
        x (int): your number

    Returns:
        int: numnber +1
    """
    return x + 1



def __validate__prices__(prices):

    if isinstance(prices, pd.DataFrame):
        assert(set(prices.index).issubset({'OD', 'RI1Y', 'SP1Y', 'RI3Y', 'SP3Y'}))

    if isinstance(prices, dict):
        prices = pd.DataFrame(prices)
        assert(set(prices.index).issubset({'OD', 'RI1Y', 'SP1Y', 'RI3Y', 'SP3Y'}))

    if callable(prices):
        raise NotImplemented("Not Implemented Yet")

    return prices

def __find_period__(df: pd.DataFrame) -> str:
        dates = pd.to_datetime(df.index)
        periods = np.diff(dates, 1)
        if periods.min() != periods.max():
            raise Warning("Careful, you have missing datas in your usage")
        return dates.inferred_freq



def cost(usage: Union[pd.DataFrame, np.ndarray],
         prices: Union[dict, list, np.ndarray],
         commitments: Optional[dict]=None,
         savings_plans: Union[None, float, int, np.ndarray]=None,
         reservations: Union[None, np.ndarray, dict]=None,
         period: Optional[str]=None,
         guid: Optional[List[str]]=None) -> float:
    """_summary_

    Args:
        usage (Union[pd.DataFrame, np.ndarray]): Cloud usage in hours or days. The DataFrame index must be the time.
        prices (Union[dict, list, np.ndarray]): Prices associated with different pricing models
        commitments (Optional[dict], optional): 
        A dictionnary of the different commitments. The keys must be RI or SP for reserved instances 
        and savings plans, followed by the term. in years. For exemple : 'RI3Y' or 'SP1Y'.
        If commitments is specified, `savings_plans` and `reservations` can be left to `None`
        savings_plans (Union[None, float, int, np.ndarray], optional): Savings plans commitment per hour or day
        reservations (Union[None, np.ndarray, dict], optional): Reservations levels per families. One per usage columns, or dict with keys same as usage columns
        period (Optional[str], optional): Time period of usage. Defaults to None.
        guid (Optional[List[str]], optional): to implement, column with guids in case of long DataFrame. Defaults to None.

    Raises:
        Exception: Negative reservation not allowed
        Exception: Can't infer the series period

    Returns:
        float: the cost associated with the usage, prices and input levels of commitments

        the savings plans levels must be the ammount of money spend per time period (hours or days)
    """

    return __general_entries__("cost", usage, prices, commitments, savings_plans, reservations, period, guid)



def coverage(usage: Union[pd.DataFrame, np.ndarray],
         prices: Union[dict, list, np.ndarray],
         commitments: Optional[dict]=None,
         savings_plans: Union[None, float, int, np.ndarray]=None,
         reservations: Union[None, np.ndarray, dict]=None,
         period: Optional[str]=None,
         guid: Optional[List[str]]=None) -> float:
    """compute coverage based on usage

    Args:
        usage (Union[pd.DataFrame, np.ndarray]): Cloud usage in hours or days. The DataFrame index must be the time.
        prices (Union[dict, list, np.ndarray]): Prices associated with different pricing models
        commitments (Optional[dict], optional): 
        A dictionnary of the different commitments. The keys must be RI or SP for reserved instances 
        and savings plans, followed by the term. in years. For exemple : 'RI3Y' or 'SP1Y'.
        If commitments is specified, `savings_plans` and `reservations` can be left to `None`
        savings_plans (Union[None, float, int, np.ndarray], optional): Savings plans commitment per hour or day
        reservations (Union[None, np.ndarray, dict], optional): Reservations levels per families. One per usage columns, or dict with keys same as usage columns
        period (Optional[str], optional): Time period of usage. Defaults to None.
        guid (Optional[List[str]], optional): to implement, column with guids in case of long DataFrame. Defaults to None.

    Raises:
        Exception: Negative reservation not allowed
        Exception: Can't infer the series period

    Returns:
        float: the coverage associated with the usage, prices and input levels of commitments

        the savings plans levels must be the ammount of money spend per time period (hours or days)
    """
    return __general_entries__("coverage", usage, prices, commitments, savings_plans, reservations, period, guid)



def under_utilisation(usage, prices, levels) -> float:
    pass




def optimise(usage: pd.DataFrame,
             prices: Union[Dict, pd.DataFrame, Callable]) -> FinalResults:
    """_summary_

    Args:
        usage (pd.DataFrame): The usage in hours or days of cloud compute
        prices (Union[Dict, pd.DataFrame, Callable]): A `DataFrame` of prices

            Columns must be the same as usage, and index must be pricing models names in:
            `{'OD'|'RI1Y'|'SP1Y'|'RI3Y'|'SP3Y'}`

    Raises:
        TypeError: If the entry is not a DataFrame
        Exception: If the time period can't be infered

    Returns:
        FinalResults: The optimal commitments on the time period given in a `FinalResult` object
    """

    if not isinstance(usage, pd.DataFrame):
        raise TypeError("You need to provide a time series DataFrame with a time index")
    
    prices = __validate__prices__(prices)

    if "SP1Y" in prices.index:
        correct_order = prices.loc['SP1Y'].div(prices.loc['OD'])
    else:
        correct_order = prices.loc['SP3Y'].div(prices.loc['OD'])

    correct_order = np.argsort(correct_order.values)

    usage = usage.reindex(columns=usage.columns[correct_order])
    prices = prices.reindex(columns=prices.columns[correct_order])


    X = usage.values.astype(float)
    period = __find_period__(usage)
    if period not in {'D', 'H'}:
        raise Exception("Can't infer time_period, please provide period={'days'|'hours'}")
        
    usage.index = pd.to_datetime(usage.index).to_pydatetime()

    res = rs.optim_final(X, prices.values, list(prices.index), period)

    arangment = pd.DataFrame(res.commitments, index=["savings plans"] + list(usage.columns))
    p = np.zeros(len(usage.columns) + 1)
    for d in arangment.columns:
        k = "RI3Y" if d == 'three_year_commitments' else 'RI1Y'
        p += np.append(1, prices.loc[k] * (23 * (period == "D") + 1)) * arangment[d]
    arangment[f"price_per_{period}"] = p

    fres = FinalResults(
        optimal_arangment=arangment,
        minimum=res.minimum,
        coverage=0,
        n_iter=res.n_iter,
        convergence=res.convergence
    )
    return fres


def __general_entries__(
        action: str,
        usage: Union[pd.DataFrame, np.ndarray],
        prices: Union[dict, list, np.ndarray],
        commitments: Optional[dict]=None,
        savings_plans: Union[None, float, int, np.ndarray]=None,
        reservations: Union[None, np.ndarray, dict]=None,
        period: Optional[str]=None,
        guid: Optional[List[str]]=None) -> float:

    if period is not None:
        assert(period in {'hours', 'hrs', 'H', 'days', 'D', 'd', 'h'})
        changes = {'days' : "D", "hours" : "H", "hrs" : 'H', 'day' : 'D', 'h' : 'H', 'd' : 'D'}
        try:
            period = changes[period.lower()]
        except KeyError:
            raise Exception("Period not in {'hours'|'hrs'|'H'|'days'|'D'|'d'|'h'}")

    # here detect if long or wide DataFrame
    if guid is not None:
        assert(guid in usage.columns)
        usage = pd.pivot_table()

           
    if isinstance(usage, pd.DataFrame):
        X = usage.values.astype(float)
        timespan, n = X.shape
        period = __find_period__(usage)
        usage.index = pd.to_datetime(usage.index).to_pydatetime()
        
    if isinstance(usage, (np.ndarray, np.generic)):
        assert period is not None
        X = usage.astype(float)
        timespan, n = X.shape
  

    if commitments is not None:
        assert isinstance(prices, dict)
        assert isinstance(commitments, dict)

        assert set(prices.keys()).issubset({'OD', 'RI1Y', 'SP1Y', 'RI3Y', 'SP3Y'})
        assert set(commitments.keys()).issubset({'OD', 'RI1Y', 'SP1Y', 'RI3Y', 'SP3Y'})
        assert set(commitments).issubset(set(prices))
        assert 'OD' in prices.keys()

        models = [i for i in prices.keys()]
        match action:
            case "cost":
                return rs.final_cost_or_coverage(
                    X,
                    np.array([prices[i] for i in models]),
                    np.hstack([np.zeros((timespan, 1 + (n - 1) * ('RI' == k[:2]))) + np.array(commitments[k]) for k in models if k in commitments.keys()]), # this syntax is to ensure the same order
                    models,
                    period,
                    True
                )
            case "coverage":
                return rs.final_cost_or_coverage(
                    X,
                    np.array([prices[i] for i in models]),
                    np.hstack([np.zeros((timespan, 1 + (n - 1) * ('RI' == k[:2]))) + np.array(commitments[k]) for k in models if k in commitments.keys()]), # this syntax is to ensure the same order
                    models,
                    period,
                    False
                )

    if isinstance(reservations, dict):
        assert isinstance(usage, pd.DataFrame)
        reservations = np.array([reservations.get(guid, 0) for guid in usage.columns])
    else:
        reservations = np.array(reservations)
    if (reservations < 0).any():
        raise Exception("Negative reservation not allowed")
    match period:
        case 'D':
            reservations *= 24
        case 'H':
            pass
        case _:
            raise Exception("Can't infer time_period, please provide period={'days'|'hours'}")
    levels = np.array(np.append(savings_plans, reservations)).astype(np.uint64) # here check if it must use uint32 instead

    match action:
        case "cost":
            return rs.cost(X, np.array(prices), levels)
        case "coverage":
            return rs.coverage(X, np.array(prices), levels)
        


def optimise_prediction(prediction: np.ndarray,
                        current_prices: Union[Dict, pd.DataFrame, Callable[[str], dict]],
                        current_levels: Union[None, Dict, pd.DataFrame] = None) -> FinalResults:


     
    prices = __validate__prices__(current_prices)

    print(prices)
    correct_order = prices.loc[['SP1Y']].div(prices.loc[['OD']])
    print(correct_order)
    correct_order = np.argsort(correct_order.values)

    prediction = prediction.reindex(columns=prediction.columns[correct_order])
    prices = prices.reindex(columns=prices.columns[correct_order])

    # here substract the current commitment to the usage and save the associated cost somewhere
    # or no ? because SP and RI can interact ? should add it everytime to the proposed commitments ?

    if prices.any():
        return True
    return False