# 🏭 Factory Optimisation System

A machine learning-powered Streamlit web application that analyzes manufacturing and sales data, forecasts sales, and estimates gross profit to support production planning and factory optimisation decisions.

## Project Overview

The Factory Optimisation System turns raw production and sales records from the **Nassau Candy Distributor** dataset into interactive dashboards, sales forecasts, profit estimates and optimisation recommendations. It is a multi-page Streamlit app with a shared, clean corporate design across all pages.

## Objectives

- Forecast future sales using machine learning
- Estimate gross profit for production planning
- Analyze historical manufacturing performance
- Support factory optimisation decisions
- Visualize key business metrics
- Demonstrate practical applications of AI in manufacturing

## Key Features

- **Interactive Dashboard:** KPI cards, sidebar filters and Plotly charts for exploring sales and profit
- **Factory Optimization:** recommendations that support production planning
- **Machine Learning Models:** trained models loaded with Joblib
- **Sales Prediction:** ML-based sales forecasting
- **Business Analytics and Performance Insights:** charts and summaries of key metrics

## App Pages

| Page | Purpose |
|---|---|
| Home (`app.py`) | Project overview, objectives, features, tech stack, dataset and workflow |
| Dashboard | KPIs and interactive charts with filters |
| Factory Optimization | Optimisation recommendations for production |
| Sales Prediction | ML forecasting of sales and gross profit |
| Visualization | Additional charts and analytics |

> Update this table so it matches the pages that exist in your repository.

## Dataset

The project uses the **Nassau Candy Distributor Dataset**, which contains historical manufacturing and sales records, including:

- Order information
- Product categories
- Sales
- Manufacturing cost
- Gross profit
- Units sold
- Regional sales
- Shipping details

Dataset source: `<add the link to where you got the dataset>`

## Project Workflow

Data Collection → Data Cleaning → EDA → Feature Engineering → Model Training → Sales Prediction → Factory Optimization → Business Insights

## Tech Stack

| Area | Tools |
|---|---|
| Core | Python, Streamlit, Pandas, NumPy |
| Machine Learning | Scikit-learn, Joblib |
| Visualization | Plotly, Matplotlib |
| Tooling | VS Code, Jupyter, Git |

## Machine Learning

- **Model(s) used:** `<for example Random Forest Regressor, Linear Regression, etc.>`
- **Target:** `<for example Sales / Gross Profit>`
- **Evaluation metrics:** `<for example R², MAE, RMSE with your actual values>`

> Fill in the real model and results. Specific numbers make the project much more convincing than general claims.

## Project Structure

```
factory-optimisation-system/
├── app.py                      # Home page (project overview)
├── pages/
│   ├── Dashboard.py
│   ├── Factory_Optimization.py
│   ├── Sales_Prediction.py
│   └── Visualization.py
├── data/                       # Nassau Candy dataset
├── models/                     # Saved ML models (.joblib)
├── requirements.txt
└── README.md
```

> Adjust the folder and file names to match your repository.

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Screenshots

Add screenshots of the Home page, Dashboard and Sales Prediction page here:

```markdown
![Dashboard](screenshots/dashboard.png)
```

## Future Improvements

- `<add the next features you plan to build>`

## Author

**Sujal Kaler**, BCA (AI/ML), Lovely Professional University
