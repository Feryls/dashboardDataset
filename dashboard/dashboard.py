import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("/mnt/data/data_day (1).csv")

df['dteday'] = pd.to_datetime(df['dteday'])

# Sidebar
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal", [df['dteday'].min(), df['dteday'].max()],
    min_value=df['dteday'].min(), max_value=df['dteday'].max()
)
filtered_df = df[(df['dteday'] >= pd.Timestamp(start_date)) & (df['dteday'] <= pd.Timestamp(end_date))]

# Dashboard Title
st.title("Dashboard Peminjaman Sepeda")

# Metric
st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Peminjaman", filtered_df['cnt'].sum())
col2.metric("Peminjaman oleh Pengguna Terdaftar", filtered_df['registered'].sum())
col3.metric("Peminjaman oleh Pengguna Biasa", filtered_df['casual'].sum())

# Grafik Tren Harian
st.subheader("Tren Peminjaman Harian")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_df['dteday'], filtered_df['cnt'], marker='o', linestyle='-')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Tren Peminjaman Harian")
st.pyplot(fig)

# Grafik Peminjaman Berdasarkan Musim
st.subheader("Peminjaman Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=filtered_df['season'], y=filtered_df['cnt'], ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Jumlah Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Grafik Peminjaman Berdasarkan Hari Kerja
st.subheader("Peminjaman Berdasarkan Hari Kerja")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=filtered_df['workingday'], y=filtered_df['cnt'], ax=ax)
ax.set_xlabel("Hari Kerja (0 = Libur, 1 = Kerja)")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Jumlah Peminjaman Sepeda Berdasarkan Hari Kerja")
st.pyplot(fig)

st.caption("Dashboard dibuat dengan Streamlit")
