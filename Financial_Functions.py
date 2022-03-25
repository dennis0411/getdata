import ffn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# reference: https://pmorissette.github.io/ffn/_modules/ffn/core.html#PerformanceStats


portfolio = {'spy': 0.5,
             'agg': 0.5,
             }

start_date = '2010-01-01'
end_date = '2022-03-24'

benchmark_index = "spy"

portfolio_list = list(portfolio.keys())
portfolio_weight = list(portfolio.values())

prices = ffn.get(portfolio_list, start=start_date, end=end_date)
benchmark_rebase = ffn.get(benchmark_index, start=start_date, end=end_date).rebase()

rebase = prices.rebase()

# returns_rebase = rebase.to_returns().dropna()

weight = np.array(portfolio_weight)
weighted_rebase = rebase.mul(weight)
portfolio_rebase = weighted_rebase.sum(axis=1)
portfolio_rebase = pd.DataFrame(portfolio_rebase, columns=["portfolio"])

print(portfolio_rebase)

portfolio_stats = portfolio_rebase.calc_stats()
portfolio_dd_series = portfolio_rebase.to_drawdown_series()

print(portfolio_stats.display())
print(portfolio_dd_series)

comparison = pd.concat([portfolio_rebase, benchmark_rebase], axis=1)
comparison_stats = comparison.calc_stats()
comparison_dd_series = comparison.to_drawdown_series()

print(comparison_stats.display())
print(comparison_dd_series)
