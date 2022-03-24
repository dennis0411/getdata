import ffn

list = ['aapl', 'msft', 'spy']

prices = ffn.get(list, start='2010-01-01')
print(prices)
rebase = prices.rebase()
print(rebase)
stats = rebase.calc_stats()
dd_series = rebase.to_drawdown_series()
dd = rebase.calc_max_drawdown()

# reference: https://pmorissette.github.io/ffn/_modules/ffn/core.html#PerformanceStats

print("try:", [stats[x].mtd for x in list])


returns_rebase = rebase.to_returns().dropna()

print(returns_rebase)
