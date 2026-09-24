"""
End-to-End Retail Sales Analysis
Real-world Data Project — Retail Domain
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.dpi": 140,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "font.family": "DejaVu Sans",
})

OUT = "/home/claude/project/visuals"

df = pd.read_csv("/home/claude/project/data/retail_sales_dataset.csv", parse_dates=["Order_Date", "Ship_Date"])
df["Month"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()
df["Year"] = df["Order_Date"].dt.year
df["MonthName"] = df["Order_Date"].dt.strftime("%b")
df["Profit_Margin"] = df["Profit"] / df["Sales"]
df["Delivery_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days

# ============================================================
# 1. DATA QUALITY / OVERVIEW
# ============================================================
summary = {
    "rows": len(df),
    "date_min": df["Order_Date"].min(),
    "date_max": df["Order_Date"].max(),
    "total_sales": df["Sales"].sum(),
    "total_profit": df["Profit"].sum(),
    "avg_order_value": df["Sales"].mean(),
    "overall_margin": df["Profit"].sum() / df["Sales"].sum(),
    "unique_customers": df["Customer_ID"].nunique(),
    "missing_values": df.isna().sum().sum(),
}
print("=== SUMMARY ===")
for k, v in summary.items():
    print(f"{k}: {v}")

# ============================================================
# 2. MONTHLY SALES & PROFIT TREND
# ============================================================
monthly = df.groupby("Month").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()

fig, ax1 = plt.subplots(figsize=(11, 5.5))
ax1.bar(monthly["Month"], monthly["Sales"], width=20, color="#2563eb", alpha=0.85, label="Sales")
ax1.set_ylabel("Sales (£)", color="#2563eb")
ax1.tick_params(axis='y', labelcolor="#2563eb")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))

ax2 = ax1.twinx()
ax2.plot(monthly["Month"], monthly["Profit"], color="#f97316", marker="o", linewidth=2.5, label="Profit")
ax2.set_ylabel("Profit (£)", color="#f97316")
ax2.tick_params(axis='y', labelcolor="#f97316")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))
ax2.grid(False)

plt.title("Monthly Sales & Profit Trend (2024–2025)")
fig.autofmt_xdate()
fig.tight_layout()
plt.savefig(f"{OUT}/01_monthly_sales_profit_trend.png", bbox_inches="tight")
plt.close()

# ============================================================
# 3. SALES BY CATEGORY & SUB-CATEGORY
# ============================================================
cat_sales = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Sales", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
colors = ["#2563eb", "#f97316", "#10b981"]
axes[0].bar(cat_sales.index, cat_sales["Sales"], color=colors)
axes[0].set_title("Total Sales by Category")
axes[0].set_ylabel("Sales (£)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))
for i, v in enumerate(cat_sales["Sales"]):
    axes[0].text(i, v, f"£{v/1000:.0f}k", ha="center", va="bottom", fontsize=9)

axes[1].bar(cat_sales.index, cat_sales["Profit"], color=colors)
axes[1].set_title("Total Profit by Category")
axes[1].set_ylabel("Profit (£)")
axes[1].axhline(0, color="grey", linewidth=0.8)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))
for i, v in enumerate(cat_sales["Profit"]):
    axes[1].text(i, v, f"£{v/1000:.0f}k", ha="center", va="bottom" if v >= 0 else "top", fontsize=9)

fig.suptitle("Category Performance: Sales vs. Profit", fontweight="bold", fontsize=14)
fig.tight_layout()
plt.savefig(f"{OUT}/02_category_sales_profit.png", bbox_inches="tight")
plt.close()

# ============================================================
# 4. SUB-CATEGORY PROFITABILITY (highlighting loss-makers)
# ============================================================
sub = df.groupby("Sub_Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Profit")
colors_sub = ["#ef4444" if p < 0 else "#10b981" for p in sub["Profit"]]

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(sub.index, sub["Profit"], color=colors_sub)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Profit by Sub-Category (Red = Loss-Making)")
ax.set_xlabel("Profit (£)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))
fig.tight_layout()
plt.savefig(f"{OUT}/03_subcategory_profit.png", bbox_inches="tight")
plt.close()

# ============================================================
# 5. REGIONAL PERFORMANCE
# ============================================================
region_perf = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                                         Orders=("Order_ID", "nunique")).sort_values("Sales", ascending=False)

fig, ax = plt.subplots(figsize=(9, 5.5))
x = np.arange(len(region_perf))
width = 0.38
b1 = ax.bar(x - width/2, region_perf["Sales"], width, label="Sales", color="#2563eb")
b2 = ax.bar(x + width/2, region_perf["Profit"], width, label="Profit", color="#f97316")
ax.set_xticks(x)
ax.set_xticklabels(region_perf.index)
ax.set_title("Sales vs. Profit by Region")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))
ax.legend()
fig.tight_layout()
plt.savefig(f"{OUT}/04_region_performance.png", bbox_inches="tight")
plt.close()

# ============================================================
# 6. CUSTOMER SEGMENT ANALYSIS
# ============================================================
seg = df.groupby("Segment").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                                 AOV=("Sales", "mean")).sort_values("Sales", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].pie(seg["Sales"], labels=seg.index, autopct="%1.1f%%", startangle=90,
            colors=["#2563eb", "#f97316", "#10b981"], wedgeprops={"edgecolor": "white", "linewidth": 1.5})
axes[0].set_title("Share of Sales by Customer Segment")

axes[1].bar(seg.index, seg["AOV"], color=["#2563eb", "#f97316", "#10b981"])
axes[1].set_title("Average Order Value by Segment")
axes[1].set_ylabel("Avg. Sales per Order (£)")
for i, v in enumerate(seg["AOV"]):
    axes[1].text(i, v, f"£{v:.0f}", ha="center", va="bottom", fontsize=9)

fig.tight_layout()
plt.savefig(f"{OUT}/05_segment_analysis.png", bbox_inches="tight")
plt.close()

# ============================================================
# 7. DISCOUNT vs PROFIT MARGIN (relationship)
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5.5))
sample = df.sample(min(1500, len(df)), random_state=1)
sns.scatterplot(data=sample, x="Discount", y="Profit_Margin", hue="Category", alpha=0.6, ax=ax,
                 palette=["#2563eb", "#f97316", "#10b981"], s=35)
ax.axhline(0, color="grey", linestyle="--", linewidth=1)
ax.set_title("Discount Level vs. Profit Margin")
ax.set_xlabel("Discount Applied")
ax.set_ylabel("Profit Margin")
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
fig.tight_layout()
plt.savefig(f"{OUT}/06_discount_vs_margin.png", bbox_inches="tight")
plt.close()

# ============================================================
# 8. CORRELATION HEATMAP
# ============================================================
corr_cols = ["Sales", "Profit", "Quantity", "Discount", "Unit_Price", "Profit_Margin", "Delivery_Days"]
corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(7.5, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Matrix of Key Metrics")
fig.tight_layout()
plt.savefig(f"{OUT}/07_correlation_heatmap.png", bbox_inches="tight")
plt.close()

# ============================================================
# 9. PREDICTIVE MODEL: Forecast next-month sales (linear trend)
#    + Regression to predict Profit from order attributes
# ============================================================
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# --- 9a. Simple monthly sales forecast (linear regression on time index) ---
monthly_sorted = monthly.sort_values("Month").reset_index(drop=True)
monthly_sorted["t"] = np.arange(len(monthly_sorted))
lr = LinearRegression()
lr.fit(monthly_sorted[["t"]], monthly_sorted["Sales"])

future_t = np.arange(len(monthly_sorted), len(monthly_sorted) + 3).reshape(-1, 1)
future_preds = lr.predict(future_t)
future_months = pd.date_range(monthly_sorted["Month"].max() + pd.offsets.MonthBegin(1), periods=3, freq="MS")

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(monthly_sorted["Month"], monthly_sorted["Sales"], marker="o", color="#2563eb", label="Actual Sales")
ax.plot(future_months, future_preds, marker="o", linestyle="--", color="#ef4444", label="Forecast (Next 3 Months)")
ax.fill_between(future_months, future_preds * 0.85, future_preds * 1.15, color="#ef4444", alpha=0.15)
ax.set_title("Sales Forecast — Next 3 Months (Linear Trend Model)")
ax.set_ylabel("Sales (£)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x/1000:.0f}k"))
ax.legend()
fig.autofmt_xdate()
fig.tight_layout()
plt.savefig(f"{OUT}/08_sales_forecast.png", bbox_inches="tight")
plt.close()

# --- 9b. Random Forest to predict Profit from order features ---
features = ["Quantity", "Unit_Price", "Discount", "Category", "Region", "Segment", "Ship_Mode"]
X = df[features]
y = df["Profit"]

cat_features = ["Category", "Region", "Segment", "Ship_Mode"]
num_features = ["Quantity", "Unit_Price", "Discount"]

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
], remainder="passthrough")

model = Pipeline([
    ("prep", preprocess),
    ("rf", RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
print(f"\n=== PROFIT PREDICTION MODEL ===\nMAE: £{mae:.2f}\nR²: {r2:.3f}")

# Feature importance (aggregate one-hot back to original feature groups)
ohe = model.named_steps["prep"].named_transformers_["cat"]
ohe_names = ohe.get_feature_names_out(cat_features)
all_names = list(ohe_names) + num_features
importances = model.named_steps["rf"].feature_importances_

imp_df = pd.DataFrame({"feature": all_names, "importance": importances})
def base_feature(f):
    for c in cat_features:
        if f.startswith(c + "_"):
            return c
    return f
imp_df["group"] = imp_df["feature"].apply(base_feature)
grouped_imp = imp_df.groupby("group")["importance"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(grouped_imp.index, grouped_imp.values, color="#2563eb")
ax.set_title("Feature Importance — Predicting Order Profit\n(Random Forest Regressor)")
ax.set_xlabel("Relative Importance")
fig.tight_layout()
plt.savefig(f"{OUT}/09_feature_importance.png", bbox_inches="tight")
plt.close()

# ============================================================
# 10. Actual vs Predicted Profit scatter
# ============================================================
fig, ax = plt.subplots(figsize=(7, 6.5))
ax.scatter(y_test, preds, alpha=0.4, color="#2563eb", s=20)
lims = [min(y_test.min(), preds.min()), max(y_test.max(), preds.max())]
ax.plot(lims, lims, color="#ef4444", linestyle="--", linewidth=1.5, label="Perfect Prediction")
ax.set_xlabel("Actual Profit (£)")
ax.set_ylabel("Predicted Profit (£)")
ax.set_title(f"Model Performance: Actual vs. Predicted Profit\nR² = {r2:.3f}  |  MAE = £{mae:.2f}")
ax.legend()
fig.tight_layout()
plt.savefig(f"{OUT}/10_actual_vs_predicted.png", bbox_inches="tight")
plt.close()

# ============================================================
# Save summary stats for the report
# ============================================================
top_subcats_loss = sub[sub["Profit"] < 0].sort_values("Profit").head(3)
top_region = region_perf["Sales"].idxmax()
top_category = cat_sales["Sales"].idxmax()
best_segment = seg["Sales"].idxmax()

with open("/home/claude/project/report/key_findings.txt", "w") as f:
    f.write(f"Total Sales: £{summary['total_sales']:,.0f}\n")
    f.write(f"Total Profit: £{summary['total_profit']:,.0f}\n")
    f.write(f"Overall Margin: {summary['overall_margin']*100:.1f}%\n")
    f.write(f"Average Order Value: £{summary['avg_order_value']:,.2f}\n")
    f.write(f"Unique Customers: {summary['unique_customers']}\n")
    f.write(f"Total Orders: {summary['rows']}\n")
    f.write(f"Top Region by Sales: {top_region}\n")
    f.write(f"Top Category by Sales: {top_category}\n")
    f.write(f"Best Segment by Sales: {best_segment}\n")
    f.write(f"Loss-making sub-categories: {', '.join(top_subcats_loss.index.tolist())}\n")
    f.write(f"Forecast next 3 months sales: {[f'£{p:,.0f}' for p in future_preds]}\n")
    f.write(f"Profit Model MAE: £{mae:.2f}\n")
    f.write(f"Profit Model R2: {r2:.3f}\n")

print("\nAll visuals saved to", OUT)
print("Key findings saved to report/key_findings.txt")
