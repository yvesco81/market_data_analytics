---
title: Historical Data
---

This table provides historical stock data for all selected tickers from the full dataset.
It includes open, high, low, close prices and traded volume by day.
Use the pagination controls below to explore the data.


```sql all_prices
-- This query retrieves all data from the stock_data.stocks table
SELECT
   *
FROM stock_data.stocks
ORDER BY date, ticker
```

<DataTable data={all_prices} title="All Stock Prices" rows=30/>