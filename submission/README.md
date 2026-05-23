# Bike Sharing Analysis Dashboard
## Project Overview
Dashboard ini dibuat untuk menganalisis data penyewaan sepeda, khususnya mengenai pengaruh kondisi cuaca terhadap jumlah penyewa. proyek ini merupakan bagian terakhir dari tugas analisis data.

## Struktur Folder
- `dashboard`: Berisi data yang sudah dibersihkan dan file 'dashboard.py'.
- `data`: Berisi dataset mentah (day.csv & hour.csv)
- `Proyek_Analisis_Data.ipynb`: Proses analisis data dari Wrangling hingga Exploratory Sata Analysis (EDA).
- `requirement`: Daftar library yang dibutuhkan.
- `url.txt`: link dashboard yang sudah di deploy menggunakan streamlit


## Setup Environment - Terminal/Shell
Jika kamu ingin menjalankan proyek ini secara lokal, pastikan sudah menginstal python di komputermu, lalu ikuti langkah berikut
1. **Download atau clone project**
   Pastikan folder proyek sudah tersimpan di laptop kamu.
2. **Instal Library yang dibutuhkan**
   ```bash
   pip install pandas matplotlib seaborn streamlit
## Menjalankan dashboard
pyhton -m streamlit run dashboard.py

## Link Dashboard yang sudah di deploy
**https://deploy-app-pitacdc15scientist.streamlit.app/**

