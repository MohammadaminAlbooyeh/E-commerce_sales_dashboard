# Step 1: Import necessary libraries
import pandas as pd

# Step 2: Load the dataset
df = pd.read_csv("../data/sales.csv", parse_dates=["order_date"])

# Step 3: Compute Revenue column
df["revenue"] = df["quantity"] * df["price"]

# Step 4: Compute total revenue per category
revenue_per_category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)

# Step 5: Print the result
print("Total Revenue per Category:")
print(revenue_per_category)
