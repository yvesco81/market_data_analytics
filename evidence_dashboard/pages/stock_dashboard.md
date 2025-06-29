---
title: Stock Dashboard
---

This dashboard provides detailed insights into selected stock tickers. It includes:
- Company metadata
- Price trends
- Volume patterns
- Daily variation
- Moving averages
- High-low spread analysis

Use the dropdown and date selector above to customize the view.

```sql range_dates
-- This query retrieves distinct dates from the stock_data.stocks table
SELECT
  date
FROM stock_data.stocks
GROUP BY date
ORDER BY date
```

```sql tickers
-- This query retrieves distinct stock tickers from the stock_data.stocks table
SELECT
   ticker
FROM stock_data.stocks
GROUP BY ticker
ORDER BY ticker
```

```sql ticker_prices
-- This query retrieves stock prices for the selected ticker
SELECT *
FROM stock_data.stocks
WHERE ticker LIKE '${inputs.ticker.value}'
   AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
ORDER BY date
```

```sql price_distribution
-- This query calculates the distribution of stock prices for the selected ticker
-- It groups the prices into buckets rounded to the nearest 10 and counts the frequency of each
SELECT
  ROUND(close, -1) AS price_bucket,  -- Round to nearest 10
  COUNT(*) AS frequency
FROM stock_data.stocks
WHERE ticker LIKE '${inputs.ticker.value}'
  AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
GROUP BY price_bucket
ORDER BY price_bucket
```


```sql growth
-- This query calculates the latest and previous day's closing prices for the selected ticker
-- and computes the percentage change between them
WITH ranked AS (
  SELECT
    date,
    close,
    ROW_NUMBER() OVER (ORDER BY date DESC) AS rn
  FROM stock_data.stocks
  WHERE ticker LIKE '${inputs.ticker.value}'
    AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
),
latest_two AS (
  SELECT rn, close
  FROM ranked
  WHERE rn IN (1, 2)
)
SELECT
  MAX(CASE WHEN rn = 1 THEN close END) AS latest_close,
  MAX(CASE WHEN rn = 2 THEN close END) AS previous_close,
  CASE
    WHEN MAX(CASE WHEN rn = 2 THEN close END) = 0 THEN NULL
    ELSE
      (MAX(CASE WHEN rn = 1 THEN close END) - MAX(CASE WHEN rn = 2 THEN close END))
      / MAX(CASE WHEN rn = 2 THEN close END)
  END AS pct_change
FROM latest_two
```

```sql company_info
-- This query retrieves company information based on the selected ticker
-- It includes the company's name, sector, industry, and a summary description
SELECT
  name,
  sector,
  industry,
  summary
FROM companies
WHERE ticker LIKE '${inputs.ticker.value}'
```

```sql rolling_avg
-- This query calculates the 7-day rolling average of closing prices for the selected ticker
SELECT
  date,
  close,
  AVG(close) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_avg
FROM stock_data.stocks
WHERE ticker LIKE '${inputs.ticker.value}'
   AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
ORDER BY date
```

```sql price_volume
-- This query retrieves both stock prices and volume traded for the selected ticker
-- It combines the two datasets to provide a comprehensive view of stock performance
SELECT
  date,
  close,
  volume / 1_000_000 AS volume_millions
FROM stock_data.stocks
WHERE ticker LIKE '${inputs.ticker.value}'
  AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
ORDER BY date
```

```sql spread_data
-- This query calculates the spread between the high and low prices for the selected ticker
-- It provides insight into the volatility of the stock during the selected date range
SELECT
  date,
  high - low AS spread
FROM stock_data.stocks
WHERE ticker LIKE '${inputs.ticker.value}'
  AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
ORDER BY date
```

```sql moving_avg_30
-- This query calculates the 30-day moving average of closing prices for the selected ticker
-- It helps to smooth out price fluctuations and identify trends over a longer period
SELECT
  date,
  close,
  AVG(close) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS ma_30
FROM stock_data.stocks
WHERE ticker LIKE '${inputs.ticker.value}'
  AND date::DATE BETWEEN '${inputs.selected_date.start}' AND '${inputs.selected_date.end}'
ORDER BY date
```

<Dropdown data={tickers} name=ticker value=ticker> <DropdownOption value="%" valueLabel="All Tickers" /> </Dropdown>
<DateRange  name="selected_date" data={range_dates} dates=date />


**Name**: {company_info[0].name}
**Sector**: {company_info[0].sector}
**Industry**: {company_info[0].industry}

<Details title="Description">
  {company_info[0].summary}
</Details>


<Grid cols=1>
  <BigValue
    data={growth}
    value=latest_close
    valueFmt="0.00"
    comparison=pct_change
    comparisonFmt="+0.0%;-0.0%;0.0%"
    comparisonTitle="vs. Previous Day"
  />
  <Grid cols=2>
    {#if ticker_prices.length > 0}
      <AreaChart
        data={ticker_prices}
        title="Stock Prices"
        x=date
        y=close
        fillColor=#b8645e
        lineColor=#b8645e
      />
    {:else}
      results found for this ticker/date range.
    {/if}
    {#if ticker_prices.length > 0}
    <BarChart
      data={price_distribution}
      title="Distribution of Closing Prices"
      x=price_bucket
      y=frequency
      fillColor=#00b4e0
    />
    {:else}
      results found for this ticker/date range.
    {/if}
    {#if ticker_prices.length > 0}
      <LineChart
        data={rolling_avg}
        title="7-Day Rolling Average"
        x=date
        y=rolling_avg
      />
    {:else}
      results found for this ticker/date range.
    {/if}
    {#if ticker_prices.length > 0}
      <LineChart
        data={moving_avg_30}
        title="30-Day Moving Average"
        x=date
        y=ma_30
        lineColor=#2ecc71
      />
    {:else}
      results found for this ticker/date range.
    {/if}
    {#if ticker_prices.length > 0}
      <Chart data={price_volume} title="Price vs Volume">
        <Bar y=volume_millions />
        <Line y=close />
      </Chart>
    {:else}
      results found for this ticker/date range.
    {/if}
    {#if ticker_prices.length > 0}
      <LineChart
        data={spread_data}
        title="Daily High-Low Spread"
        x=date
        y=spread
        lineColor=#e67e22
      />
    {:else}
      results found for this ticker/date range.
    {/if}
  </Grid>
</Grid>