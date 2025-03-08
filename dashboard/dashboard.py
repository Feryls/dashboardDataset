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

# **PERTANYAAN 1: Hari Kerja vs Akhir Pekan**
st.markdown("### 📈 Analisis Pertanyaan 1: Penyewaan Sepeda di Hari Kerja vs Akhir Pekan")

# Filter data untuk pertanyaan 1 (berdasarkan tahun & musim)
filtered_df_1 = df[
    (df['yr'] == year - 2011) & 
    (df['season'] == season)
]

col1, col2 = st.columns([2, 1])

with col1:
    workingday_avg = filtered_df_1.groupby('workingday')['cnt'].mean()
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

# **PERTANYAAN 2: Pengguna Biasa vs Member (Keseluruhan)**
st.markdown("### 📊 Analisis Pertanyaan 2: Pola Penggunaan Pengguna Biasa vs Member (Keseluruhan)")

# Filter data untuk pertanyaan 2 (hanya berdasarkan tahun, tidak musim)
filtered_df_2 = df[df['yr'] == year - 2011]

# Kelompokkan data berdasarkan hari dalam seminggu
weekday_data = filtered_df_2.groupby('weekday')[['casual', 'registered']].mean().reset_index()

# Pastikan urutan hari benar (0 = Minggu, ..., 6 = Sabtu)
weekday_data = weekday_data.sort_values(by='weekday')

# Buat x-axis index
x = range(len(weekday_data))
labels = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']

fig, ax = plt.subplots(figsize=(12, 6))

width = 0.35
ax.bar([i - width/2 for i in x], weekday_data['casual'], width, label='Pengguna Biasa', color='royalblue')
ax.bar([i + width/2 for i in x], weekday_data['registered'], width, label='Member', color='lightcoral')

plt.xticks(x, labels)
plt.title('Pola Penggunaan Sepeda: Pengguna Biasa vs Member (Keseluruhan)', fontsize=14)
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Rata-rata Jumlah Pengguna')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# **Insight**
st.markdown("""
**📌 Insight:**  
- **Pengguna Biasa (Casual Users)** lebih aktif di **akhir pekan**, menunjukkan tujuan rekreasi.  
- **Member (Registered Users)** lebih banyak menggunakan sepeda di **hari kerja**, yang menunjukkan pola transportasi harian.  
- Tren ini **konsisten sepanjang tahun**, menunjukkan bahwa pengguna biasa lebih dipengaruhi oleh hari libur dibandingkan member.  
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
