
# 📊 market_data_analytics

**A complete Python ETL pipeline for financial market data analysis**  
Extraction • Transformation • Loading • Visualization • Dashboarding

---

## 🚀 Overview

This project builds an end-to-end data processing pipeline for financial market data, including:
- Extraction from APIs or files (e.g., stock prices, volumes, indicators)
- Data transformation (cleaning, feature engineering, technical indicators)
- Loading into **DuckDB** (an analytical database optimized for columnar storage)
- Interactive dashboards with **Streamlit** and **Evidence**

The goal is to showcase a reproducible and scalable workflow with **data quality checks**, suitable for asset management use cases.

---

## 💡 Features

- ✅ **Python ETL**: A script that extracts, transforms, and loads data into DuckDB  
- ✅ **Data validation**: Checks for schema consistency, missing values, and outliers  
- ✅ **Interactive dashboards**: Built with Streamlit and Evidence  
- ✅ **DuckDB caching**: Efficient storage with fast analytical SQL queries

---

## 🛠️ Tech Stack

| Component             | Technology                    |
|-----------------------|-------------------------------|
| Language              | Python 3.10+                  |
| ETL & Processing      | pandas, numpy                 |
| Analytical database   | DuckDB                        |
| Dashboarding          | Streamlit, Evidence           |

---

## 💾 Installation

```bash
# Clone the repo
git clone https://github.com/yvesco81/market_data_analytics.git
cd market_data_analytics

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

1. **Run the ETL process**  
   ```bash
   python etl_main.py
   ```

2. **Launch streamlit dashboard**  
   ```bash
   streamlit run streamlit_dashboard/index.py
   ```

3. Open your browser at http://localhost:8501 to explore stock prices, rolling indicators, volumes, and more.

4. **Launch evidence dashboard**  
   ```bash
   CD evidence_dashboard
   npm run dev
   ```

5. Open your browser at http://localhost:3000 to explore stock prices, rolling indicators, volumes, and more.


---

## ⚙️ Project Structure

```
market_data_analytics/
├── data/                          # Local data folder (input/output)
├── deployments/                  # Deployment configs
├── evidence_dashboard/           # Evidence-based dashboard
├── flows/                        # Prefect flows for ETL orchestration
├── stock_data/                   # Core data logic (extract, transform, load)
├── streamlit_dashboard/          # Streamlit dashboard app
├── tests/                        # Unit and integration tests
├── .gitignore
├── .prefectignore
├── logger.py                     # Custom logging logic
├── main.py                       # Entry point (optional)
├── prefect.yaml                  # Prefect configuration
├── pyproject.toml                # Poetry config
├── poetry.lock                   # Dependency lock file
├── README.md
└── requirements.txt              # Additional dependencies
```

---

## ✅ Data Quality Checks

The pipeline includes validations such as:
- Presence of required columns
- Value ranges (e.g., non-negative volumes)
- Primary key uniqueness (ticker + date)
- Statistical anomaly detection

---

## 📈 Output

- A persistent DuckDB database ready for analysis
- Clean, enriched datasets for modeling
- Interactive dashboards with market indicators
- Fully automated and modular pipeline

---

## ✨ Use Cases

- Quantitative research and signal processing
- Market data monitoring and watchlists
- Asset management platforms
- Portfolio data ingestion demos

---

## 🖼️ Streamlit Dashboard Preview
<p align="center">
   <img src="images/streamlit_index.png" width="900"/>
   <img src="images/streamlit_historical_data.png" width="900"/>
   <img src="images/streamlit_stock.png" width="900"/>
</p>


## 🖼️ Evidence Dashboard Preview

<p align="center">
   <img src="images/evidence_index.png" width="900"/>
   <img src="images/evidence_historical_data.png" width="900"/>
   <img src="images/evidence_stock.png" width="900"/>
</p>
---

## 🤝 Contributing

Feel free to fork and enhance:
- Add more tickers or financial indicators
- Integrate additional data sources
- Deploy on Streamlit Cloud or with Docker

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

Yves Courtel  
📧 yves@example.com  
GitHub: [@yvesco81](https://github.com/yvesco81)
