import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset
df = pd.read_csv("/mnt/data/data_day(1).csv")

# Pastikan kolom tanggal dalam format datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Sidebar untuk rentang waktu
st.sidebar.header("Filter Waktu")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Waktu", [df['order_date'].min(), df['order_date'].max()]
)

# Filter data berdasarkan rentang waktu
filtered_df = df[(df['order_date'] >= str(start_date)) & (df['order_date'] <= str(end_date))]

# Analisis jumlah pesanan per hari
daily_orders_df = filtered_df.resample(rule='D', on='order_date').agg({
    "order_id": "nunique",
    "total_price": "sum"
}).reset_index()
daily_orders_df.rename(columns={
    "order_id": "order_count",
    "total_price": "revenue"
}, inplace=True)

# Tampilkan metrik utama
st.header("Dashboard Analisis Data")
st.subheader("Ringkasan Penjualan")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Pesanan", daily_orders_df['order_count'].sum())

with col2:
    total_revenue = format_currency(daily_orders_df['revenue'].sum(), "IDR", locale='id_ID')
    st.metric("Total Pendapatan", total_revenue)

# Visualisasi pesanan harian
st.subheader("Jumlah Pesanan Harian")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_orders_df["order_date"], daily_orders_df["order_count"], marker='o', color='b')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Produk dengan penjualan terbaik
st.subheader("Produk dengan Penjualan Terbaik")
sum_order_items_df = filtered_df.groupby("product_name")["quantity_x"].sum().reset_index()
sum_order_items_df = sum_order_items_df.sort_values(by="quantity_x", ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=sum_order_items_df['product_name'], x=sum_order_items_df['quantity_x'], ax=ax, palette='Blues_r')
ax.set_xlabel("Jumlah Terjual")
st.pyplot(fig)

st.caption("Dibuat dengan Streamlit")
