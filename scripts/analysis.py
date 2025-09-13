# Step 1: Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 2: Load dataset
df = pd.read_csv("../data/sales.csv", parse_dates=["order_date"])

# Step 3: Compute Revenue column
df["revenue"] = df["quantity"] * df["price"]

# Step 4: Total revenue per category
revenue_per_category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
print("Total Revenue per Category:\n", revenue_per_category)

# Step 5: Best-selling product (by revenue)
best_product = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(1)
print("\nBest-Selling Product:\n", best_product)

# Step 6: Daily revenue trend
daily_revenue = df.groupby("order_date")["revenue"].sum()
print("\nDaily Revenue Trend:\n", daily_revenue)

# Step 7: Monthly revenue trend
monthly_revenue = df.groupby(df["order_date"].dt.to_period("M"))["revenue"].sum()
print("\nMonthly Revenue Trend:\n", monthly_revenue)

# Step 8: Plot trends
plt.figure(figsize=(12,5))
plt.plot(daily_revenue.index, daily_revenue.values, marker="o", label="Daily Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Daily Revenue Trend")
plt.legend()
plt.grid(True)
plt.show()

monthly_revenue.plot(kind="bar", figsize=(10,5), title="Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.show()

# Step 9: NumPy Statistical Analysis on Revenue
revenue_array = df["revenue"].values

mean_revenue = np.mean(revenue_array)
std_revenue = np.std(revenue_array)
percentiles = np.percentile(revenue_array, [25, 50, 75])

print("\nRevenue Statistics:")
print(f"Mean Revenue: {mean_revenue:.2f}")
print(f"Standard Deviation: {std_revenue:.2f}")
print(f"25th Percentile: {percentiles[0]:.2f}")
print(f"50th Percentile (Median): {percentiles[1]:.2f}")
print(f"75th Percentile: {percentiles[2]:.2f}")
