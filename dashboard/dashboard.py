import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🚲",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("hour.csv")
    return data

data = load_data()

# Judul Dashboard
st.title("Dashboard Analisis Penggunaan Sepeda Berbagi 🚲")
st.write("Dashboard ini menampilkan analisis pola penggunaan sepeda berbagi berdasarkan musim dan cuaca")

# Sidebar untuk filter
st.sidebar.header("📊 Filter Data")

season_labels = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_labels = {1: "Cerah ☀️", 2: "Berkabut 🌫️", 3: "Hujan Ringan 🌧️", 4: "Cuaca Buruk ⛈️"}

season_filter = st.sidebar.multiselect(
    "Pilih Musim:", list(season_labels.keys()), default=list(season_labels.keys()), format_func=lambda x: season_labels[x]
)
weather_filter = st.sidebar.multiselect(
    "Pilih Cuaca:", list(weather_labels.keys()), default=list(weather_labels.keys()), format_func=lambda x: weather_labels[x]
)

# Filter data
filtered_data = data[(data["season"].isin(season_filter)) & (data["weathersit"].isin(weather_filter))]

# Tampilkan ringkasan statistik sederhana
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pengguna", f"{filtered_data['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Per Jam", f"{filtered_data['cnt'].mean():.0f}")
with col3:
    st.metric("Maksimum Per Jam", f"{filtered_data['cnt'].max():,}")
with col4:
    st.metric("Jam Teramai", filtered_data.loc[filtered_data['cnt'].idxmax(), 'hr'])

# Visualisasi Tren Penggunaan Sepeda per Jam
st.subheader("⏳ Pola Penggunaan Sepeda Per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, x='hr', y='cnt', estimator='mean', ci=None, marker='o', color='b', ax=ax)
ax.set_title("Rata-Rata Penggunaan Sepeda Per Jam", fontsize=12)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Visualisasi Penggunaan Berdasarkan Cuaca
st.subheader("🌤️ Distribusi Penggunaan Berdasarkan Cuaca")
weather_analysis = filtered_data.groupby('weathersit')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=weather_analysis, y='weathersit', x='cnt', palette="Greens_r", ax=ax)
ax.set_title("Rata-Rata Pengguna Berdasarkan Cuaca")
ax.set_xlabel("Rata-Rata Jumlah Pengguna")
ax.set_yticks(range(len(weather_filter)))
ax.set_yticklabels([weather_labels[i] for i in sorted(weather_filter)])
st.pyplot(fig)

# Tabel ringkasan
st.subheader("📋 Ringkasan Data")
st.dataframe(filtered_data[['hr', 'season', 'weathersit', 'cnt']].head(10))

# Tombol unduh data
st.sidebar.download_button(
    label="📥 Unduh Data Hasil Filter (CSV)",
    data=filtered_data.to_csv(index=False),
    file_name="bike_sharing_data.csv",
    mime="text/csv"
)
st.sidebar.markdown("[Sumber Data](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/code)")
