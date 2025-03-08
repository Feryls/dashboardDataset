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

    st.markdown("---")
    st.markdown("### 📝 Pertanyaan Bisnis")
    st.markdown("""
    1. Apakah jumlah penyewaan sepeda lebih tinggi di hari kerja dibandingkan akhir pekan?
    2. Bagaimana perbedaan pola penggunaan sepeda antara pengguna biasa dan member?
    """)

# Filter data hanya berdasarkan tahun (tanpa musim)
filtered_df = df[df['yr'] == year - 2011]

# **Pertanyaan 2: Pengguna Biasa vs Member (Keseluruhan)**
st.markdown("### 📊 Analisis Pertanyaan 2: Pola Penggunaan Pengguna Biasa vs Member (Keseluruhan)")

# Kelompokkan data berdasarkan hari dalam seminggu
weekday_data = filtered_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()

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
- Tren ini konsisten sepanjang tahun, menunjukkan bahwa pengguna biasa lebih dipengaruhi oleh hari libur dibandingkan member.  
""")
