# 📊 Sales Analytics Dashboard

A comprehensive, interactive sales analytics dashboard built with Python, Streamlit, Pandas, Matplotlib, Seaborn, and Squarify. Empower business users to explore sales, profit, customer, product, and logistics insights with ease.

---

## 🚀 Features

- **Dynamic Filters:** Date range, region, category, sub-category, customer segment
- **KPIs:** Total Sales, Total Profit, Total Orders, Average Order Value, Average Shipping Delay
- **Tabbed Visual Panels:**
  - Time Analysis (trends, seasonality, YoY)
  - Region Analysis (top/bottom regions, profit-loss)
  - Product Analysis (top products, category breakdown, treemap)
  - Customer Analysis (behavior, value, frequency)
  - Logistics (shipping delay, on-time vs. late)
- **Interactive Charts:** All visuals update with filters
- **Expandable Sections:** For focused insight per category

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) (dashboard UI)
- [Pandas](https://pandas.pydata.org/) (data wrangling)
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) (visualizations)
- [Squarify](https://github.com/laserson/squarify) (treemap)

---

## ⚡ Setup Instructions

1. **Clone the repository or download the code.**
2. **Install dependencies:**
   ```bash
   pip install streamlit pandas matplotlib seaborn squarify
   ```
3. **Place your sales data Excel file (e.g., `Amazon 2_Raw.xlsx`) in the project folder.**
4. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
5. **Upload your Excel file in the web app and start exploring!**

---

## 📂 Data Requirements

- The Excel file should have at least these columns:
  - `Order Date`, `Sales`
- For full features, include: `Profit`, `Product`, `Category`, `Sub-Category`, `Region`/`State`/`City`, `Customer`, `Ship Date`, `Segment`

---

## 🛠️ Customization

- Add or remove filters in the sidebar as needed.
- Place additional charts in the appropriate tab/expander in `dashboard.py`.
- Adjust color palettes or chart types for your brand or preferences.

---

## 💬 Support

For questions or feature requests, open an issue or contact the author.
