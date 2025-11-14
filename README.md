# 🌍 Global Economic Trends Dashboard

A comprehensive interactive dashboard for visualizing **119+ macroeconomic and development indicators** across **85+ countries** using World Bank Open Data.

## Features

- 📊 **119+ Indicators** across 11 categories
- 🌍 **85+ Countries** from all continents
- 📈 **Interactive Visualizations**: Line and bar charts with Plotly
- 🔮 **GDP Prediction**: Machine learning model to forecast next year's GDP
- 🌐 **Real-time Data**: Fetches latest data from World Bank API
- 💾 **Smart Caching**: Local caching for faster performance
- 📥 **Data Export**: Download data as CSV

## Data Categories

### 📊 11 Major Categories:

1. **POPULATION & DEMOGRAPHICS** (18 indicators)
   - Population totals, growth, life expectancy, fertility, urban/rural distribution

2. **ECONOMY & GDP** (14 indicators)
   - GDP, GNI, per capita metrics, growth rates, exports/imports

3. **PRICES, INFLATION & MONEY** (8 indicators)
   - Inflation, CPI, interest rates, money supply, stock market

4. **EMPLOYMENT & LABOR MARKET** (10 indicators)
   - Unemployment, labor force, sector employment, participation rates

5. **EDUCATION** (10 indicators)
   - Literacy, enrollment rates, completion rates, education spending

6. **HEALTH** (14 indicators)
   - Health expenditure, mortality rates, disease prevalence, immunization

7. **POVERTY & INEQUALITY** (8 indicators)
   - Poverty headcount, income distribution, Gini index

8. **ENVIRONMENT & CLIMATE** (12 indicators)
   - CO2 emissions, pollution, forest area, agricultural land

9. **ENERGY** (8 indicators)
   - Energy consumption, electricity access, renewable energy sources

10. **TRADE, BUSINESS & INDUSTRY** (9 indicators)
    - Ease of doing business, trade volumes, sector value added

11. **DIGITAL, INFRASTRUCTURE & INNOVATION** (9 indicators)
    - Internet users, mobile connectivity, patents, transportation

## Installation

```bash
# Clone the repository
cd open-source-eval

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## How to Use

1. **Select Countries**: Choose one or more countries from the sidebar (85+ available)
2. **Choose Category**: Select from 11 data categories
3. **Pick Indicator**: Choose specific indicator within that category
4. **Set Time Range**: Pick start and end years (1960-2024)
5. **View Charts**: Explore line charts, bar comparisons, and rankings
6. **Enable Features**: Toggle growth rates, year comparisons, or GDP predictions
7. **Download Data**: Export your data as CSV

## Data Source

All data is sourced from the [World Bank Open Data API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api)

## Project Structure

```
open-source-eval/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── data/                       # Cached API responses
├── models/                     # ML models
│   └── predictor.py           # GDP prediction model
└── src/
    ├── api/
    │   └── world_bank.py      # World Bank API client
    ├── visualizations/
    │   └── charts.py          # Chart generation functions
    └── utils/
        └── helpers.py         # Utility functions
```

## Technologies Used

- **Streamlit**: Interactive web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning for predictions
- **World Bank API**: Economic data source

## Future Enhancements

- Multi-indicator comparison on single chart
- Regional aggregations and continent-level analysis
- Time-series forecasting for all indicators
- Correlation analysis between indicators
- Custom indicator combinations
- Real-time alerts for data updates

## Sample Queries

Try these interesting comparisons:

- **COVID Impact**: Compare health expenditure 2015-2023 for USA, IND, BRA
- **Tech Leaders**: Internet users % for KOR, JPN, SGP, USA
- **Energy Transition**: Renewable electricity % for DEU, DNK, NOR
- **Emerging Markets**: GDP growth for VNM, IND, BGD, ETH
- **Life Expectancy**: Compare JPN, CHE, AUS, SGP over 40 years
- **Innovation Race**: Patent applications for USA, CHN, JPN, KOR

## License

MIT License

---

Built with ❤️ for data enthusiasts and economic analysis
