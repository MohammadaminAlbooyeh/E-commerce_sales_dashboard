import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("ecommerce_data.csv")   # use the CSV you built
df.head()

# Basic checks & cleaning
# Types & nulls
print(df.dtypes)
print(df.isna().sum())

# Parse dates
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
df = df.dropna(subset=['OrderDate'])

# Ensure numerics
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
df['Price']    = pd.to_numeric(df['Price'], errors='coerce')

# Remove impossible rows
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

# Optional: drop exact duplicates
df = df.drop_duplicates()

# Sort by time
df = df.sort_values('OrderDate').reset_index(drop=True)

# Feature engineering
# Line-level revenue (euros)
df['TotalPrice'] = df['Quantity'] * df['Price']

# Time features
df['OrderMonth'] = df['OrderDate'].values.astype('datetime64[M]')
df['Year'] = df['OrderDate'].dt.year
df['Month'] = df['OrderDate'].dt.month
df['Weekday'] = df['OrderDate'].dt.day_name()

# Build order-level table (in case an order has multiple lines)
orders = (df.groupby('OrderID', as_index=False)
            .agg(CustomerID=('CustomerID','first'),
                 OrderDate=('OrderDate','min'),
                 Items=('Quantity','sum'),
                 OrderValue=('TotalPrice','sum')))

orders['OrderMonth'] = orders['OrderDate'].values.astype('datetime64[M]')

# Quick KPI snapshot
total_revenue = orders['OrderValue'].sum()
total_orders = orders['OrderID'].nunique()
unique_customers = orders['CustomerID'].nunique()
aov = total_revenue / total_orders                     # Average Order Value
purchase_freq = total_orders / unique_customers        # Orders per customer
repeat_rate = (orders.groupby('CustomerID')['OrderID']
                    .nunique().ge(2).mean())           # % of customers with ≥2 orders

kpis = {
    "Total revenue (€)": round(total_revenue, 2),
    "Total orders": int(total_orders),
    "Unique customers": int(unique_customers),
    "AOV (€ per order)": round(aov, 2),
    "Purchase frequency (orders/customer)": round(purchase_freq, 3),
    "Repeat customer rate": round(float(repeat_rate), 3),
}
kpis

# Most frequent buyers & top products
# Frequent buyers (by number of orders)
frequent_buyers = (orders.groupby('CustomerID')['OrderID']
                        .nunique().sort_values(ascending=False).head(10))

# Top products by units and by revenue
top_products_units = (df.groupby('ProductName')['Quantity']
                        .sum().sort_values(ascending=False).head(10))

top_products_revenue = (df.groupby('ProductName')['TotalPrice']
                          .sum().sort_values(ascending=False).head(10))

frequent_buyers, top_products_units, top_products_revenue

top_products_units.plot(kind='bar', title='Top Products by Units'); plt.ylabel('Units'); plt.tight_layout(); plt.show()
top_products_revenue.plot(kind='bar', title='Top Products by Revenue (€)'); plt.ylabel('Revenue (€)'); plt.tight_layout(); plt.show()

# Seasonal trends (month & weekday)
# Monthly revenue (order-level)
monthly_revenue = (orders.groupby('OrderMonth')['OrderValue']
                          .sum().rename('Revenue'))

# 3-month rolling average for smoothing
monthly_revenue_smooth = monthly_revenue.rolling(3, min_periods=1).mean()

# Weekday revenue
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday_revenue = (orders.assign(Weekday=orders['OrderDate'].dt.day_name())
                         .groupby('Weekday')['OrderValue'].sum()
                         .reindex(weekday_order))

monthly_revenue.plot(title='Monthly Revenue (€)'); plt.ylabel('€'); plt.tight_layout(); plt.show()
monthly_revenue_smooth.plot(title='Monthly Revenue (€) – 3M Rolling Avg'); plt.ylabel('€'); plt.tight_layout(); plt.show()
weekday_revenue.plot(kind='bar', title='Revenue by Weekday (€)'); plt.ylabel('€'); plt.tight_layout(); plt.show()

# Customer retention (cohort analysis)
# First purchase month (cohort) per customer
first_order_month = (orders.groupby('CustomerID')['OrderDate']
                            .min().dt.to_period('M'))

orders['Cohort'] = orders['CustomerID'].map(first_order_month).astype('period[M]')
orders['OrderPeriod'] = orders['OrderDate'].dt.to_period('M')

# Months since first purchase (1 = cohort month)
to_int = lambda p: p.year*12 + p.month
orders['CohortIndex'] = (orders['OrderPeriod'].apply(to_int)
                         - orders['Cohort'].apply(to_int) + 1)

# Count unique customers active in each cohort/index
cohort_counts = (orders.groupby(['Cohort','CohortIndex'])['CustomerID']
                        .nunique().reset_index())

cohort_pivot = cohort_counts.pivot(index='Cohort', columns='CohortIndex', values='CustomerID')

# Retention rates
cohort_size = cohort_pivot.iloc[:, 0]
retention = (cohort_pivot.div(cohort_size, axis=0)).round(3)

retention  # rows = cohorts by month, cols = months since first purchase

plt.imshow(retention.fillna(0).values, aspect='auto')
plt.title('Cohort Retention')
plt.xlabel('Months since first purchase')
plt.ylabel('Cohort (YYYY-MM)')
plt.colorbar(label='Retention rate')
plt.tight_layout(); plt.show()

# Extra: simple RFM segmentation
# Recency (days since last order), Frequency (# orders), Monetary (€ spent)
snapshot_date = orders['OrderDate'].max() + pd.Timedelta(days=1)

rfm = (orders.groupby('CustomerID')
             .agg(Recency=('OrderDate', lambda x: (snapshot_date - x.max()).days),
                  Frequency=('OrderID','nunique'),
                  Monetary=('OrderValue','sum'))
      )

# Simple quantile-based scoring (1=low, 5=high for F/M; reverse for R)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['RFM_Segment'] = rfm['R_Score'].astype(str)+rfm['F_Score'].astype(str)+rfm['M_Score'].astype(str)
rfm.head()

# Save outputs
monthly_revenue.to_csv("monthly_revenue.csv")
retention.to_csv("cohort_retention.csv")
rfm.to_csv("rfm_scores.csv")

