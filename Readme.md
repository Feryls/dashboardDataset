# <ins>Proyek Analisis Data Bike Sharing Dataset<ins>
## <ins>Deskripsi Proyek<ins>
Proyek ini adalah proyek yang dimana bertujuan untuk menganalisa tentang dataset yang didapat dari bike sharing dengan menggunakan teknik data analisis dan visualisasi.

## <ins>Struktur Folder<ins>
```
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt
```

## <ins>Langkah-langkah Menjalankan Dashboard<ins>

### 1. Git Clone
```
cd documents
```
```
git clone https://github.com/Feryls/dashboardDataset
```

Note: cd documents yang diawal itu untuk memilih dimana akan di clone

### 2. Instalasi Dependecies
```
pip install -r requirements.txt
```

Note: Pastikan dependencies yang diperlukan sudah terinstal

### 3. Menjalankan Dashboard
```
streamlit run dashboard.py
```

Note: Setelah menjalankan dashboard biasanya akan masuk ke localhost:8501

### 4. Push Proyek ke Github
commit semua file lalu jalankan perintah ini
```
git push
```

Note: Jika tidak bisa di push biasanya git belum ada nama dan email anda, yang perlu dilakukan masukan perintah berikut
```
git config --global user.name
```
```
git config --global user.email
```

Note: contoh user.name -> user.randy || user.email -> user.randyputra7012@gmail.com

### 5. Menghubungkan Repository Github ke Streamlit
1. Buka website resmi [streamlit](https://streamlit.io/)
2. Pilih deploy with streamlit community cloud
3. Hubungkan ke github
4. Buat App baru
5. Isi kriteria yang sesuai dengan proyek

### 6. Salin URL Streamlit
Setelah berhasil terdeploy, salin url streamlit proyek analisis data ke dalam file url.txt
