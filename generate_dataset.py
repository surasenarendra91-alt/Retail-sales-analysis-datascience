"""
Generates a realistic synthetic retail sales dataset (2 years of transactions)
mimicking a multi-region superstore, for the Retail Domain Data Science Project.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 6500

# --- Reference data ---
regions = ["North", "South", "East", "West", "Central"]
region_weights = [0.22, 0.18, 0.24, 0.20, 0.16]

categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels"],
    "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
}
category_list = list(categories.keys())
category_weights = [0.28, 0.42, 0.30]

segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.51, 0.30, 0.19]

ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
ship_mode_weights = [0.60, 0.19, 0.15, 0.06]

city_by_region = {
    "North": ["Manchester", "Leeds", "Newcastle", "Sheffield"],
    "South": ["Southampton", "Brighton", "Portsmouth", "Reading"],
    "East": ["Norwich", "Cambridge", "Ipswich", "Peterborough"],
    "West": ["Bristol", "Exeter", "Plymouth", "Cardiff"],
    "Central": ["Birmingham", "Coventry", "Leicester", "Nottingham"],
}

# base unit price ranges & typical cost margin per category (for realism)
price_ranges = {
    "Furniture": (60, 900),
    "Office Supplies": (3, 120),
    "Technology": (25, 1800),
}
margin_ranges = {  # profit margin as % of sales, varies by category
    "Furniture": (-0.05, 0.18),
    "Office Supplies": (0.05, 0.35),
    "Technology": (-0.10, 0.30),
}

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    order_id = f"ORD-{100000+i}"

    # seasonality: boost order likelihood around Nov-Dec (holiday) and back-to-school Aug-Sep
    day_offset = np.random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=day_offset)
    month = order_date.month

    # simple seasonal resample: re-roll some dates into peak months to create realistic seasonality
    if np.random.rand() < 0.18:
        peak_month = np.random.choice([11, 12, 9], p=[0.45, 0.4, 0.15])
        year = np.random.choice([2024, 2025])
        day = np.random.randint(1, 28)
        order_date = datetime(year, peak_month, day)

    ship_date = order_date + timedelta(days=int(np.random.choice([1, 2, 3, 4, 5, 6, 7],
                                                                  p=[0.05, 0.15, 0.25, 0.25, 0.15, 0.1, 0.05])))

    region = np.random.choice(regions, p=region_weights)
    city = np.random.choice(city_by_region[region])
    category = np.random.choice(category_list, p=category_weights)
    sub_category = np.random.choice(categories[category])
    segment = np.random.choice(segments, p=segment_weights)
    ship_mode = np.random.choice(ship_modes, p=ship_mode_weights)

    quantity = int(np.random.choice([1, 2, 3, 4, 5, 6], p=[0.35, 0.25, 0.18, 0.12, 0.06, 0.04]))
    unit_price = round(np.random.uniform(*price_ranges[category]), 2)

    discount = float(np.random.choice([0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5],
                                       p=[0.40, 0.20, 0.12, 0.12, 0.08, 0.05, 0.03]))

    gross_sales = round(unit_price * quantity, 2)
    sales = round(gross_sales * (1 - discount), 2)

    margin = np.random.uniform(*margin_ranges[category])
    # higher discount erodes margin further
    margin = margin - discount * 0.6
    profit = round(sales * margin, 2)

    customer_id = f"CUST-{np.random.randint(1000, 2500)}"

    rows.append({
        "Order_ID": order_id,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Ship_Date": ship_date.strftime("%Y-%m-%d"),
        "Ship_Mode": ship_mode,
        "Customer_ID": customer_id,
        "Segment": segment,
        "Region": region,
        "City": city,
        "Category": category,
        "Sub_Category": sub_category,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
    })

df = pd.DataFrame(rows)
df = df.sort_values("Order_Date").reset_index(drop=True)
df.to_csv("/home/claude/project/data/retail_sales_dataset.csv", index=False)
print("Saved:", df.shape)
print(df.head())
