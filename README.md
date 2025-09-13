
```markdown
# 📊 E-commerce Sales Dashboard

An **Intermediate Python project** for analyzing and visualizing sales data.  
The dashboard computes **total revenue by category**, finds the **best-selling product**,  
shows **daily and monthly revenue trends**, and performs **statistical analysis with NumPy**.

---

## 📂 Project Structure
```

Ecommerce\_Sales\_Dashboard/
│
├── data/
│   └── sales.csv              # Dataset
│
├── scripts/
│   └── analysis.py            # Main analysis script
│
├── reports/
│   ├── figures/               # Plots will be saved here (optional)
│   └── summary.txt            # Insights (optional)
│
├── notebooks/
│   └── dashboard\_analysis.ipynb   # Jupyter notebook version
│
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation

````

---

## 📊 Features
- Compute **total revenue per category**
- Identify **best-selling product**
- Analyze **daily and monthly revenue trends**
- Generate **visualizations (line & bar plots)**
- Perform **statistical analysis**:
  - Mean revenue  
  - Standard deviation  
  - Percentiles (25th, 50th, 75th)  

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Ecommerce_Sales_Dashboard.git
cd Ecommerce_Sales_Dashboard
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Script

```bash
cd scripts
python analysis.py
```

---

## 📈 Example Output

**Total Revenue per Category**

```
Electronics    4225
Furniture       900
Stationery       70
```

**Best-Selling Product**

```
Laptop    2400
```

**Plots**

* Daily revenue trend (line chart)
* Monthly revenue trend (bar chart)

---

## 📦 Requirements

* Python 3.8+
* pandas
* numpy
* matplotlib

---

## 📝 License

This project is open-source. Feel free to use and modify.

```
