import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="🚲 Analisis Data: Bike Sharing Dataset",
    page_icon="🚴",
    layout="wide"
)

# Header
st.markdown('# 🚴‍♂️ Analisis Data: Bike Sharing Dataset')

# Author Info
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.write("👤 **Nama:** Randy")
with col2:
    st.write("📧 **Email:** randyputra7012@gmail.com")
with col3:
    st.write("🆔 **ID Dicoding:** MS119D5Y0656")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/data_day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Sidebar Filter
with st.sidebar:
    st.header("📊 Filter Data")

    # Tahun Filter
    year = st.selectbox(
        "Pilih Tahun",
        options=[2011, 2012],
        format_func=lambda x: f"Tahun {x}"
    )

    # Musim Filter
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

# **Pertanyaan 1: Hari Kerja vs Akhir Pekan**
st.markdown("### 📈 Analisis Pertanyaan 1: Penyewaan Sepeda di Hari Kerja vs Akhir Pekan")
col1, col2 = st.columns([2, 1])

with col1:
    workingday_avg = filtered_df.groupby('workingday')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=['Akhir Pekan', 'Hari Kerja'], y=workingday_avg.values,
                palette=['royalblue', 'lightcoral'])
    plt.title('Perbandingan Penyewaan Sepeda: Hari Kerja vs Akhir Pekan', fontsize=14)
    plt.ylabel('Rata-rata Penyewaan')
    plt.xlabel('Kategori Hari')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

with col2:
    st.markdown("""
    **📌 Insight:**  
    - Penyewaan lebih tinggi pada **hari kerja** dibanding akhir pekan.  
    - Indikasi kuat bahwa sepeda digunakan untuk **transportasi harian (commuting)**.  
    - **Akhir pekan** masih memiliki penggunaan yang cukup tinggi, kemungkinan besar untuk **rekreasi**.  
    """)

# **Pertanyaan 2: Pengguna Biasa vs Member**
st.markdown("### 📊 Analisis Pertanyaan 2: Pola Penggunaan Pengguna Biasa vs Member")

fig, ax = plt.subplots(figsize=(12, 6))
weekday_data = filtered_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()

# Buat bar plot
# Pastikan data tidak kosong
if not filtered_df.empty:
    weekday_data = filtered_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()
    
    # Pastikan index weekday dalam urutan yang benar (0=Minggu, ..., 6=Sabtu)
    weekday_data = weekday_data.sort_values(by='weekday')
    
    # Buat x-axis index
    x = range(len(weekday_data))  # Harus sesuai dengan jumlah kategori

    # Pastikan jumlah label sesuai dengan x
    labels = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    labels = labels[:len(x)]  # Sesuaikan jumlah label dengan x
    
    fig, ax = plt.subplots(figsize=(12, 6))

    width = 0.35
    ax.bar([i - width/2 for i in x], weekday_data['casual'], width, label='Pengguna Biasa', color='royalblue')
    ax.bar([i + width/2 for i in x], weekday_data['registered'], width, label='Member', color='lightcoral')

    plt.xticks(x, labels)  # Pastikan jumlah x sesuai dengan labels
    plt.title('Pola Penggunaan Sepeda: Pengguna Biasa vs Member', fontsize=14)
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Rata-rata Jumlah Pengguna')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang tersedia untuk filter yang dipilih.")


st.markdown("""
**📌 Insight:**  
- **Pengguna Biasa (Casual Users)** lebih aktif di **akhir pekan**, yang menunjukkan tujuan rekreasi.  
- **Member (Registered Users)** lebih banyak menggunakan sepeda di **hari kerja**, yang menunjukkan pola transportasi harian.  
- Peningkatan penyewaan pada **Senin-Jumat** mendukung tren bahwa **member lebih stabil** dibanding pengguna biasa.  
""")

# **Analisis Musim**
st.markdown("### 🌤️ Analisis Berdasarkan Musim")

col1, col2 = st.columns(2)

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
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.markdown("""
    **📌 Insight Pengguna Biasa:**  
    - Penggunaan tertinggi di **musim panas**, kemungkinan karena cuaca yang mendukung.  
    - Penyewaan **menurun drastis di musim dingin**.  
    """)

with col2:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=['Semi', 'Panas', 'Gugur', 'Dingin'],
                y=season_registered.values,
                palette='Reds')
    plt.title('Penggunaan oleh Member per Musim')
    plt.ylabel('Total Member')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.markdown("""
    **📌 Insight Member:**  
    - Pola **lebih stabil** dibanding pengguna biasa.  
    - **Puncak penggunaan di musim gugur**, mungkin karena kondisi kerja & sekolah.  
    """)

# **Kesimpulan**
st.markdown("### 📋 Kesimpulan Akhir")
st.markdown("""
1. **Hari Kerja vs Akhir Pekan:** Penyewaan lebih tinggi pada hari kerja, menunjukkan pola commuting.  
2. **Casual vs Member:** Pengguna biasa dominan di akhir pekan, member lebih stabil sepanjang minggu.  
3. **Musim:** Pengguna biasa dipengaruhi cuaca, sedangkan member lebih stabil sepanjang tahun.  
""")

# Tampilkan data mentah
if st.checkbox("🔍 Lihat Data Mentah"):
    st.dataframe(filtered_df)
