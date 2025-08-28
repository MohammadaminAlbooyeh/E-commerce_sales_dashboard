# E-commerce Customer Analysis

This project provides a comprehensive analysis of e-commerce customer behavior using transaction data. It includes data cleaning, feature engineering, key performance indicators (KPIs), product and customer insights, seasonal trends, cohort retention analysis, and RFM segmentation.

## Table of Contents

- [E-commerce Customer Analysis](#e-commerce-customer-analysis)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Data](#data)
  - [Analysis Steps](#analysis-steps)
  - [Key Outputs](#key-outputs)
  - [How to Run](#how-to-run)
  - [Dependencies](#dependencies)
  - [Results](#results)
  - [License](#license)

---

## Overview

The goal of this project is to extract actionable insights from e-commerce transaction data. The analysis covers:

- Data cleaning and preparation
- Calculation of business KPIs
- Identification of top customers and products
- Analysis of seasonal trends
- Customer retention via cohort analysis
- RFM (Recency, Frequency, Monetary) segmentation

## Data

- **Input:** `ecommerce_data.csv`  
  The dataset should contain at least the following columns:  
  `OrderID`, `CustomerID`, `OrderDate`, `ProductName`, `Quantity`, `Price`

- **Outputs:**  
  - `monthly_revenue.csv`: Monthly revenue data  
  - `cohort_retention.csv`: Customer retention matrix  
  - `rfm_scores.csv`: RFM segmentation scores

## Analysis Steps

1. **Data Loading & Cleaning**
	- Parse dates, ensure numeric types, remove invalid rows, drop duplicates, and sort by date.

2. **Feature Engineering**
	- Calculate line-level revenue, extract time features (month, year, weekday).

3. **Order-Level Aggregation**
	- Aggregate order data to compute total items and order value per order.

4. **KPI Calculation**
	- Total revenue, total orders, unique customers, average order value (AOV), purchase frequency, repeat customer rate.

5. **Customer & Product Insights**
	- Identify most frequent buyers and top products by units sold and revenue.

6. **Seasonal Trends**
	- Analyze monthly and weekday revenue, visualize trends and rolling averages.

7. **Cohort Retention Analysis**
	- Track customer retention by cohort (first purchase month) and visualize retention rates.

8. **RFM Segmentation**
	- Score customers based on recency, frequency, and monetary value for targeted marketing.

## Key Outputs

- **KPIs:**  
  - Total revenue (€)
  - Total orders
  - Unique customers
  - Average order value (AOV)
  - Purchase frequency (orders/customer)
  - Repeat customer rate

- **Top Customers & Products:**  
  - Top 10 frequent buyers
  - Top 10 products by units sold
  - Top 10 products by revenue

- **Visualizations:**  
  - Bar charts for top products
  - Monthly and weekday revenue trends
  - Cohort retention heatmap

- **Segmentation:**  
  - RFM scores for each customer

## How to Run

1. Place your `ecommerce_data.csv` file in the project directory.
2. Install the required Python packages (see below).
3. Run the analysis script:

	```bash
	python main.py
	```

4. The script will generate output CSV files and display plots.

## Dependencies

- Python 3.x
- pandas
- numpy
- matplotlib

Install dependencies with:

```bash
pip install pandas numpy matplotlib
```

## Results

- Output CSV files (`monthly_revenue.csv`, `cohort_retention.csv`, `rfm_scores.csv`) will be saved in the project directory.
- Visualizations will be displayed during script execution.

## License

This project is provided for educational and analytical purposes.

---
