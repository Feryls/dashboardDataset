import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Proyek Analisis Data: Bike Sharing Dataset",
    page_icon="🚲",
    layout="wide"
)

# Header section
st.markdown('# 🚲 Analisis Data: Bike Sharing Dataset')

# Author information
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.write("👤 **Nama:** Randy")
with col2:
    st.write("📧 **Email:** randyputra7012@gmail.com")
with col3:
    st.write("🆔 **ID Dicoding:** MS119D5Y0656")


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/data_day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df


df = load_data()

# Sidebar
with st.sidebar:
    st.header("📊 Filter Data")

    # Year filter
    year = st.selectbox(
        "Pilih Tahun",
        options=[2011, 2012],
        format_func=lambda x: f"Tahun {x}"
    )

    # Season filter
    season_map = {
        1: "Musim Semi",
        2: "Musim Panas",
        3: "Musim Gugur",
        4: "Musim Dingin"
    }
    season = st.selectbox(
        "Pilih Musim",
        options=list(season_map.keys()),
        format_func=lambda x: season_map[x]
    )

    st.markdown("---")
    st.markdown("### 📝 Pertanyaan Bisnis")
    st.markdown("""
    1. Apakah jumlah penyewaan sepeda lebih tinggi di hari kerja dibandingkan akhir pekan?
    2. Bagaimana perbedaan pola penggunaan sepeda antara pengguna biasa dan member?
    """)

# Filter data
filtered_df = df[
    (df['yr'] == year - 2011) &
    (df['season'] == season)
    ]

# Main content
st.markdown("### 📈 Analisis Pertanyaan Bisnis 1")
st.write("Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan")

# Workingday vs Weekend analysis
col1, col2 = st.columns([2, 1])

with col1:
    workingday_avg = filtered_df.groupby('workingday')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=['Akhir Pekan', 'Hari Kerja'], y=workingday_avg.values,
                palette=['royalblue', 'lightcoral'])
    plt.title('Perbandingan Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
    plt.ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

with col2:
    st.markdown("""
    **Insight:**
    - Penyewaan lebih tinggi pada hari kerja
    - Menunjukkan penggunaan untuk transportasi harian
    - Pola yang konsisten untuk kebutuhan komuter
    """)

st.markdown("### 📊 Analisis Pertanyaan Bisnis 2")
st.write("Pola Penggunaan: Pengguna Biasa vs Member")

# Weekly pattern analysis using bar plot instead of line plot
fig, ax = plt.subplots(figsize=(12, 6))
weekday_data = filtered_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()

# Create bar plot
x = range(len(weekday_data))
width = 0.35

ax.bar([i - width/2 for i in x], weekday_data['casual'], width,
       label='Pengguna Biasa', color='royalblue')
ax.bar([i + width/2 for i in x], weekday_data['registered'], width,
       label='Member', color='lightcoral')

plt.xticks(x, ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
plt.title('Pola Penggunaan Sepeda: Pengguna Biasa vs Member')
plt.xlabel('Hari')
plt.ylabel('Rata-rata Jumlah Pengguna')
plt.legend()
st.pyplot(fig)

# Add insights
st.markdown("""
**Insight:**
- Member memiliki jumlah penyewaan yang lebih tinggi di hari kerja
- Pengguna biasa menunjukkan peningkatan di akhir pekan
- Perbedaan paling signifikan terlihat pada hari kerja
""")

# Seasonal analysis - Fixed to show all seasons
st.markdown("### 🌤️ Analisis Berdasarkan Musim")
col1, col2 = st.columns(2)

# Create season aggregation for all seasons
season_casual = df.groupby('season')['casual'].sum().reindex(range(1, 5))
season_registered = df.groupby('season')['registered'].sum().reindex(range(1, 5))

with col1:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=['Semi', 'Panas', 'Gugur', 'Dingin'],
                y=season_casual.values,
                palette='Blues')
    plt.title('Penggunaan oleh Pengguna Biasa per Musim')
    plt.ylabel('Total Pengguna Biasa')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    st.markdown("""
    **Insight Pengguna Biasa:**
    - Penyewaan tertinggi pada musim panas
    - Musim dingin menunjukkan penyewaan terendah
    - Tren meningkat dari musim semi ke musim panas
    """)

with col2:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=['Semi', 'Panas', 'Gugur', 'Dingin'],
                y=season_registered.values,
                palette='Reds')
    plt.title('Penggunaan oleh Member per Musim')
    plt.ylabel('Total Member')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    st.markdown("""
    **Insight Member:**
    - Pola yang lebih stabil antar musim
    - Sedikit penurunan di musim dingin
    - Puncak penggunaan di musim gugur
    """)

# Add overall seasonal insight
st.markdown("""
**Insight Musiman:**
- Kedua tipe pengguna menunjukkan penurunan di musim dingin
- Member memiliki pola penggunaan yang lebih konsisten
- Cuaca sangat mempengaruhi pengguna biasa
""")

# Conclusions
st.markdown("### 📋 Kesimpulan")
st.markdown("""
**Kesimpulan Utama:**

1. **Pola Penggunaan Hari Kerja vs Akhir Pekan**
   - Penyewaan lebih tinggi pada hari kerja
   - Menunjukkan penggunaan utama untuk transportasi harian
   - Member lebih dominan pada hari kerja

2. **Perbedaan Pola Pengguna Biasa vs Member**
   - Pengguna biasa lebih aktif di akhir pekan
   - Member menunjukkan penggunaan yang lebih stabil
   - Pola musiman lebih mempengaruhi pengguna biasa

3. **Implikasi Bisnis**
   - Fokuskan promosi akhir pekan untuk pengguna biasa
   - Tingkatkan layanan di rute komuter untuk member
   - Sesuaikan jumlah sepeda berdasarkan pola penggunaan
""")

# Show raw data option
if st.checkbox("🔍 Lihat Data Mentah"):
    st.dataframe(filtered_df)
