import ffn
import numpy as np

# reference: https://pmorissette.github.io/ffn/_modules/ffn/core.html#PerformanceStats


portfolio = {'spy': 0.5,
             'agg': 0.5,
             }

portfolio_list = list(portfolio.keys())
portfolio_weight = list(portfolio.values())

prices = ffn.get(portfolio_list, start='2010-01-01')
rebase = prices.rebase()

returns_rebase = rebase.to_returns().dropna()

weight = np.array(portfolio_weight)
weighted_rebase = rebase.mul(weight)
portfolio_rebase = weighted_rebase.sum(axis=1)

print(portfolio_rebase)

stats = portfolio_rebase.calc_stats()
dd_series = portfolio_rebase.to_drawdown_series()
mdd = portfolio_rebase.calc_max_drawdown()

print(stats.display())
print(dd_series)
print(mdd)
