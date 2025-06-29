-- sources/stock_data/company.sql
SELECT
  ticker,
  long_name AS name,
  sector,
  industry,
  summary
FROM companies
ORDER BY ticker
