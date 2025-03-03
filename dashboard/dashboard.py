import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Data",
    page_icon="📊",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("/mnt/data/data_day.csv")
    return data

data = load_data()

# Judul Dashboard
st.title("Dashboard Analisis Data 📊")
st.write("Dashboard ini menampilkan analisis berdasarkan data yang diberikan.")

# Sidebar untuk filter
st.sidebar.header("📊 Filter Data")

# Menampilkan daftar kolom yang bisa difilter
column_filter = st.sidebar.selectbox("Pilih Kolom untuk Filter:", options=data.columns)

unique_values = data[column_filter].unique()
selected_values = st.sidebar.multiselect(f"Pilih Nilai dari {column_filter}:", options=unique_values, default=unique_values)

# Filter data
filtered_data = data[data[column_filter].isin(selected_values)]

# Tampilkan ringkasan statistik sederhana
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Data", f"{len(filtered_data):,}")
with col2:
    st.metric("Rata-rata", f"{filtered_data.mean(numeric_only=True).mean():.2f}")
with col3:
    st.metric("Maksimum", f"{filtered_data.max(numeric_only=True).max():.2f}")

# Buat dua kolom untuk visualisasi
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.subheader("📊 Histogram Data")
    selected_numeric_col = st.selectbox("Pilih Kolom Numerik:", options=data.select_dtypes(include=['number']).columns)
    fig, ax = plt.subplots()
    sns.histplot(filtered_data[selected_numeric_col], bins=20, kde=True, ax=ax)
    ax.set_title(f"Distribusi {selected_numeric_col}")
    st.pyplot(fig)

with graph_col2:
    st.subheader("📊 Scatter Plot")
    x_axis = st.selectbox("Pilih X Axis:", options=data.select_dtypes(include=['number']).columns, index=0)
    y_axis = st.selectbox("Pilih Y Axis:", options=data.select_dtypes(include=['number']).columns, index=1)
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_data, x=x_axis, y=y_axis, alpha=0.5)
    ax.set_title(f"Hubungan antara {x_axis} dan {y_axis}")
    st.pyplot(fig)

# Tampilkan tabel data
st.subheader("📋 Ringkasan Data")
st.dataframe(filtered_data.head(10), use_container_width=True)

# Tombol unduh data
st.sidebar.download_button(
    label="📥 Unduh Data (CSV)",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
