# FinOps package 

The best python package to help you optimise your cloud spendings




```python
import finoptim as fp
import pandas as pd


past_usage = pd.DataFrame(...)
guid_to_price = fp.cloud.load_aws_prices(as_dict=True)
prices = np.array(past_usqge.index.map(guid_to_price))

usage = fp.normalize(past_usage)

res = fp.optimise_past(usage, prices)
```


```python
predictions = pd.DataFrame(...) # some SQL query
current_reservations = pd.DataFrame(...) # some SQL query

normalize_reservations = fp.normalize(current_reservations)

res = fp.optimise_past(predictions, prices)
```



### TODO

- possibility to precise the period of the data in case it is not inferred correctly
- " call PyErr at suitable intervals inside your Rust function, and check the returned value. If it was -1, immediately return from your Rust function;"
- compute the better step size to avoid waiting too long
- coverage must folow the same inputs as cost
- allow for long DataFrame as input
- the cost function should return a gradient when evaluated (save some compute)

