import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("ecommerce_data.csv")   # use the CSV you built
df.head()

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

