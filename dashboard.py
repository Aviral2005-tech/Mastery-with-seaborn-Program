# ==============================================================================
# Interactive Sales Dashboard
# Author : Aviral Maheshwari
# ==============================================================================

import os
import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
print("Current Working Directory:")
print(os.getcwd())

# ==============================================================================
# Create folders
# ==============================================================================

os.makedirs("visualizations", exist_ok=True)

# ==============================================================================
# Visualization Theme
# ==============================================================================

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12,7)

# ==============================================================================
# Load Dataset
# ==============================================================================

print("="*60)
print("INTERACTIVE SALES DASHBOARD")
print("="*60)

df = pd.read_csv("sales_data (3).csv")

print("\nDataset Loaded Successfully")

print(df.head())

# ==============================================================================
# Data Cleaning
# ==============================================================================

df.columns = df.columns.str.strip()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df.dropna(inplace=True)

df["Month"] = df["Date"].dt.strftime("%b-%Y")

print("\nDataset Shape :",df.shape)

print("\nMissing Values")
print(df.isnull().sum())

# ==============================================================================
# Basic Statistics
# ==============================================================================

print("\nSummary Statistics")

print(df.describe())

# ==============================================================================
# Customer Analysis
# ==============================================================================

customer_sales = (
    df.groupby("Customer_ID")
    .agg(
        Total_Sales=("Total_Sales","sum"),
        Orders=("Customer_ID","count"),
        Avg_Order=("Total_Sales","mean")
    )
    .reset_index()
)

customer_sales = customer_sales.sort_values(
    by="Total_Sales",
    ascending=False
)

# ==============================================================================
# Product Analysis
# ==============================================================================

product_sales = (
    df.groupby("Product")
    .agg(
        Revenue=("Total_Sales","sum"),
        Quantity=("Quantity","sum")
    )
    .reset_index()
)

product_sales = product_sales.sort_values(
    by="Revenue",
    ascending=False
)

# ==============================================================================
# Region Analysis
# ==============================================================================

region_sales = (
    df.groupby("Region")["Total_Sales"]
    .sum()
    .reset_index()
)

# ==============================================================================
# Monthly Sales
# ==============================================================================

monthly_sales = (
    df.groupby("Month")["Total_Sales"]
    .sum()
    .reset_index()
)

# ==============================================================================
# Chart 1
# Monthly Sales Trend
# ==============================================================================

plt.figure(figsize=(12,6))

sns.lineplot(
    data=monthly_sales,
    x="Month",
    y="Total_Sales",
    marker="o",
    linewidth=3,
    color="royalblue"
)

plt.xticks(rotation=45)

plt.title("Monthly Sales Trend")

plt.tight_layout()

plt.savefig(
    "visualizations/sales_trend.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Chart 2
# Product Performance
# ==============================================================================

plt.figure(figsize=(10,6))

sns.barplot(
    data=product_sales,
    x="Product",
    y="Revenue",
    palette="viridis"
)

plt.title("Revenue by Product")

plt.tight_layout()

plt.savefig(
    "visualizations/product_performance.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Chart 3
# Box Plot
# ==============================================================================

plt.figure(figsize=(10,6))

sns.boxplot(
    data=df,
    x="Product",
    y="Total_Sales",
    palette="Set2"
)

plt.title("Sales Distribution")

plt.tight_layout()

plt.savefig(
    "visualizations/boxplot.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Chart 4
# Violin Plot
# ==============================================================================

plt.figure(figsize=(10,6))

sns.violinplot(
    data=df,
    x="Region",
    y="Total_Sales",
    palette="coolwarm"
)

plt.title("Regional Sales Distribution")

plt.tight_layout()

plt.savefig(
    "visualizations/violinplot.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Chart 5
# Histogram
# ==============================================================================

plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="Total_Sales",
    kde=True,
    bins=20,
    color="purple"
)

plt.title("Sales Distribution")

plt.tight_layout()

plt.savefig(
    "visualizations/histogram.png",
    dpi=300
)

plt.show()

print("\nFive charts created successfully.")
# ==============================================================================
# Chart 6
# Correlation Heatmap
# ==============================================================================

print("\nGenerating Correlation Heatmap...")

numeric_df = df.select_dtypes(include=["number"])

plt.figure(figsize=(10,8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    linewidths=0.5,
    fmt=".2f"
)

plt.title("Correlation Matrix")

plt.tight_layout()

plt.savefig(
    "visualizations/correlation_heatmap.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Chart 7
# Scatter Plot
# ==============================================================================

plt.figure(figsize=(10,6))

sns.scatterplot(
    data=df,
    x="Quantity",
    y="Total_Sales",
    hue="Product",
    s=120
)

plt.title("Quantity vs Total Sales")

plt.tight_layout()

plt.savefig(
    "visualizations/scatterplot.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Chart 8
# Customer Spending
# ==============================================================================

top10 = customer_sales.head(10)

plt.figure(figsize=(12,6))

sns.barplot(
    data=top10,
    x="Customer_ID",
    y="Total_Sales",
    palette="magma"
)

plt.title("Top 10 Customers")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "visualizations/top_customers.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Professional Dashboard (2x2)
# ==============================================================================

print("\nCreating Dashboard...")

fig, axes = plt.subplots(2,2,figsize=(16,12))

# -------------------- Chart 1 --------------------

sns.lineplot(
    ax=axes[0,0],
    data=monthly_sales,
    x="Month",
    y="Total_Sales",
    marker="o",
    linewidth=3
)

axes[0,0].set_title("Monthly Sales Trend")
axes[0,0].tick_params(axis="x",rotation=45)

# -------------------- Chart 2 --------------------

sns.barplot(
    ax=axes[0,1],
    data=product_sales,
    x="Product",
    y="Revenue",
    palette="viridis"
)

axes[0,1].set_title("Revenue by Product")

# -------------------- Chart 3 --------------------

axes[1,0].pie(
    region_sales["Total_Sales"],
    labels=region_sales["Region"],
    autopct="%1.1f%%",
    startangle=90
)

axes[1,0].set_title("Regional Revenue")

# -------------------- Chart 4 --------------------

sns.barplot(
    ax=axes[1,1],
    data=top10,
    x="Customer_ID",
    y="Total_Sales",
    palette="rocket"
)

axes[1,1].set_title("Top Customers")

axes[1,1].tick_params(axis="x",rotation=45)

plt.suptitle(
    "Interactive Sales Dashboard",
    fontsize=20,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "visualizations/dashboard.png",
    dpi=300
)

plt.show()

# ==============================================================================
# Plotly Interactive Dashboard
# ==============================================================================

print("\nCreating Interactive Plotly Charts...")

# -------------------- Monthly Sales --------------------

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Total_Sales",
    markers=True,
    title="Monthly Sales Trend",
    color_discrete_sequence=["royalblue"]
)

fig1.update_layout(
    template="plotly_white",
    hovermode="x unified"
)

fig1.write_html(
    "visualizations/monthly_sales.html"
)

# -------------------- Product Revenue --------------------

fig2 = px.bar(
    product_sales,
    x="Product",
    y="Revenue",
    color="Revenue",
    text_auto=True,
    title="Product Performance"
)

fig2.update_layout(
    template="plotly_white"
)

fig2.write_html(
    "visualizations/product_performance.html"
)

# -------------------- Region Pie --------------------

fig3 = px.pie(
    region_sales,
    names="Region",
    values="Total_Sales",
    hole=0.45,
    title="Regional Sales Distribution"
)

fig3.update_layout(
    template="plotly_white"
)

fig3.write_html(
    "visualizations/region_sales.html"
)

# -------------------- Scatter --------------------

fig4 = px.scatter(
    df,
    x="Quantity",
    y="Total_Sales",
    color="Product",
    hover_data=["Customer_ID","Region"],
    size="Total_Sales",
    title="Quantity vs Sales"
)

fig4.update_layout(
    template="plotly_white"
)

fig4.write_html(
    "visualizations/scatter_plot.html"
)

# -------------------- Histogram --------------------

fig5 = px.histogram(
    df,
    x="Total_Sales",
    color="Product",
    nbins=20,
    title="Sales Distribution"
)

fig5.update_layout(
    template="plotly_white"
)

fig5.write_html(
    "visualizations/sales_distribution.html"
)

print("Interactive charts saved.")

# ==============================================================================
# Animated Dashboard
# ==============================================================================

animated = px.bar(
    df,
    x="Product",
    y="Total_Sales",
    color="Region",
    animation_frame="Month",
    title="Monthly Product Sales Animation"
)

animated.write_html(
    "visualizations/animated_dashboard.html"
)

print("Animation saved.")

# ==============================================================================
# Interactive Dashboard (4-in-1)
# ==============================================================================

dashboard = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Monthly Sales",
        "Product Revenue",
        "Regional Sales",
        "Top Customers"
    ),
    specs=[
        [{"type":"scatter"},{"type":"bar"}],
        [{"type":"pie"},{"type":"bar"}]
    ]
)

dashboard.add_trace(
    go.Scatter(
        x=monthly_sales["Month"],
        y=monthly_sales["Total_Sales"],
        mode="lines+markers",
        name="Sales"
    ),
    row=1,
    col=1
)

dashboard.add_trace(
    go.Bar(
        x=product_sales["Product"],
        y=product_sales["Revenue"],
        name="Revenue"
    ),
    row=1,
    col=2
)

dashboard.add_trace(
    go.Pie(
        labels=region_sales["Region"],
        values=region_sales["Total_Sales"],
        hole=0.45
    ),
    row=2,
    col=1
)

dashboard.add_trace(
    go.Bar(
        x=top10["Customer_ID"],
        y=top10["Total_Sales"],
        name="Customers"
    ),
    row=2,
    col=2
)

dashboard.update_layout(
    height=800,
    width=1200,
    title="Professional Interactive Sales Dashboard",
    template="plotly_white"
)

dashboard.write_html(
    "visualizations/interactive_dashboard.html"
)

print("\nDashboard HTML created successfully.")

# ==============================================================================
# EXPORT SUMMARY REPORTS
# ==============================================================================

print("\nExporting Summary Reports...")

# Customer Summary
customer_sales.to_csv(
    "visualizations/customer_sales_summary.csv",
    index=False
)

# Product Summary
product_sales.to_csv(
    "visualizations/product_sales_summary.csv",
    index=False
)

# Region Summary
region_sales.to_csv(
    "visualizations/region_sales_summary.csv",
    index=False
)

# Monthly Summary
monthly_sales.to_csv(
    "visualizations/monthly_sales_summary.csv",
    index=False
)

# ==============================================================================
# SALES METRICS
# ==============================================================================

total_revenue = df["Total_Sales"].sum()

average_sale = df["Total_Sales"].mean()

highest_sale = df["Total_Sales"].max()

lowest_sale = df["Total_Sales"].min()

total_orders = len(df)

unique_customers = df["Customer_ID"].nunique()

best_product = (
    product_sales.sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]["Product"]
)

best_region = (
    region_sales.sort_values(
        "Total_Sales",
        ascending=False
    )
    .iloc[0]["Region"]
)

top_customer = (
    customer_sales.iloc[0]["Customer_ID"]
)

top_customer_sales = (
    customer_sales.iloc[0]["Total_Sales"]
)

# ==============================================================================
# KPI Dashboard
# ==============================================================================

print("\n" + "="*65)
print("             INTERACTIVE SALES DASHBOARD REPORT")
print("="*65)

print(f"Total Revenue              : ${total_revenue:,.2f}")
print(f"Average Sale               : ${average_sale:,.2f}")
print(f"Highest Sale               : ${highest_sale:,.2f}")
print(f"Lowest Sale                : ${lowest_sale:,.2f}")
print(f"Total Orders               : {total_orders}")
print(f"Unique Customers           : {unique_customers}")
print(f"Best Performing Product    : {best_product}")
print(f"Best Performing Region     : {best_region}")
print(f"Top Customer               : {top_customer}")
print(f"Top Customer Spending      : ${top_customer_sales:,.2f}")

print("="*65)

# ==============================================================================
# BUSINESS INSIGHTS
# ==============================================================================

print("\nBUSINESS INSIGHTS")
print("-"*65)

print(f"• Total revenue generated is ${total_revenue:,.2f}.")
print(f"• '{best_product}' is the highest revenue generating product.")
print(f"• '{best_region}' contributes the highest sales.")
print(f"• Customer {top_customer} is the most valuable customer.")
print("• Monthly sales trend helps identify seasonal demand.")
print("• Product comparison supports inventory planning.")
print("• Customer segmentation assists in targeted marketing.")
print("• Interactive dashboards improve business decision making.")

# ==============================================================================
# RECOMMENDATIONS
# ==============================================================================

print("\nBUSINESS RECOMMENDATIONS")
print("-"*65)

print("1. Reward top customers with loyalty programs.")
print("2. Increase inventory for best-selling products.")
print("3. Improve promotions in low-performing regions.")
print("4. Analyze seasonal trends before inventory planning.")
print("5. Monitor customer purchasing behaviour regularly.")
print("6. Use dashboards for monthly performance reviews.")

# ==============================================================================
# SAVE FINAL DASHBOARD IMAGE
# ==============================================================================

print("\nSaving Final Dashboard Summary...")

summary = pd.DataFrame({

    "Metric":[
        "Total Revenue",
        "Average Sale",
        "Highest Sale",
        "Lowest Sale",
        "Total Orders",
        "Unique Customers",
        "Best Product",
        "Best Region",
        "Top Customer"
    ],

    "Value":[
        total_revenue,
        average_sale,
        highest_sale,
        lowest_sale,
        total_orders,
        unique_customers,
        best_product,
        best_region,
        top_customer
    ]

})

summary.to_csv(
    "visualizations/dashboard_summary.csv",
    index=False
)

# ==============================================================================
# PROJECT COMPLETION
# ==============================================================================

print("\n" + "="*65)
print("PROJECT COMPLETED SUCCESSFULLY")
print("="*65)

print("\nGenerated Files")

print("""
✔ sales_trend.png
✔ product_performance.png
✔ boxplot.png
✔ violinplot.png
✔ histogram.png
✔ scatterplot.png
✔ correlation_heatmap.png
✔ dashboard.png

✔ monthly_sales.html
✔ product_performance.html
✔ region_sales.html
✔ scatter_plot.html
✔ sales_distribution.html
✔ animated_dashboard.html
✔ interactive_dashboard.html

✔ customer_sales_summary.csv
✔ product_sales_summary.csv
✔ region_sales_summary.csv
✔ monthly_sales_summary.csv
✔ dashboard_summary.csv
""")

print("="*65)
print("Interactive Sales Dashboard Successfully Generated")
print("="*65)