import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")

# Fungsi untuk mengelompokkan dan menghitung penyewaan bulanan pada tahun 2011 dan 2012
def create_monthly_comparison(df):
    df['dateday'] = pd.to_datetime(df['dateday'])  # Pastikan kolom 'dateday' bertipe datetime
    df['year'] = df['dateday'].dt.year
    df['month'] = df['dateday'].dt.strftime('%b')

    # Mengatur urutan bulan yang benar
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    # Filter data berdasarkan tahun 2011 dan 2012
    monthly_rentals_2012 = df[df['year'] == 2012].groupby('month')['count'].sum().reindex(month_order)
    monthly_rentals_2011 = df[df['year'] == 2011].groupby('month')['count'].sum().reindex(month_order)

    return monthly_rentals_2011, monthly_rentals_2012

# Fungsi untuk menghitung pengaruh kecepatan angin
def create_windspeed_effect(df):
    df['dateday'] = pd.to_datetime(df['dateday'])  # Pastikan kolom 'dateday' bertipe datetime
    df_2011 = df[df['dateday'].dt.year == 2011]  # Memfilter data untuk tahun 2011
    windspeed_data = df_2011[['windspeed', 'count']].dropna()  # Mengambil kolom 'windspeed' dan 'count' dan menghapus nilai yang hilang
    return windspeed_data

# Fungsi untuk menghitung penyewaan berdasarkan weekday dan weekend dalam 5 bulan
def create_weekday_vs_weekend_comparison(df):
    df['weekday'] = df['dateday'].dt.day_name()
    df['day_type'] = df['weekday'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
    day_type_data = df.groupby(['day_type', df['dateday'].dt.strftime('%b')]).agg({'count': 'mean'}).reset_index()
    day_type_data = day_type_data.rename(columns={'dateday': 'month'})  # Ganti nama kolom agar lebih deskriptif
    return day_type_data

# Sidebar untuk logo dan judul
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Baim: Bike Sharing Dashboard")

# Load dataset
df = pd.read_csv("clean_data.csv")

# Menghitung data yang diperlukan untuk visualisasi
monthly_rentals_2011, monthly_rentals_2012  = create_monthly_comparison(df)
windspeed_data = create_windspeed_effect(df)
weekday_data = create_weekday_vs_weekend_comparison(df)

# ----- MAIN PAGE -----
st.title("Baim: Bike Sharing Dashboard")
st.markdown("## Selamat datang di dashboard analisis penyewaan sepeda!")
st.markdown("Dashboard ini menyajikan analisis mendalam mengenai data penyewaan sepeda, termasuk tren bulanan, pengaruh kecepatan angin, dan variasi berdasarkan weekday dan weekend.")

# Visualisasi Tren Penyewaan Bulanan
st.markdown("### Tren Penyewaan Bulanan")
plt.figure(figsize=(10, 6))
# Plot untuk data 2012
plt.plot(monthly_rentals_2012.index, monthly_rentals_2012, marker='o', label='2012', color='green')
# Plot untuk data 2011
plt.plot(monthly_rentals_2011.index, monthly_rentals_2011, marker='o', label='2011', color='blue')
plt.title('Penyewaan Sepeda 2011 vs 2012', fontsize=16)
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Tahun')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#caption
st.caption("Penyewaan sepeda pada tahun 2012 secara umum mengalami peningkatan dibandingkan dengan tahun 2011. Setiap bulannya, terlihat bahwa jumlah penyewaan sepeda lebih tinggi di hampir semua bulan pada tahun 2012. Tren ini juga menunjukkan pola yang mirip, di mana pada pertengahan bulan terjadi kenaikan signifikan, terutama di bulan Juni. Misalnya, di bulan Juni 2012, jumlah penyewaan sepeda meningkat dibandingkan dengan Juni 2011, menunjukkan adanya tren kenaikan dalam popularitas penggunaan sepeda di tahun 2012 dibandingkan tahun sebelumnya.")

# Visualisasi Pengaruh Kecepatan Angin
st.markdown("### Pengaruh Kecepatan Angin Terhadap Penyewaan")
plt.figure(figsize=(10, 5))
plt.scatter(windspeed_data['windspeed'], windspeed_data['count'], alpha=0.6, color='blue', edgecolors='k',  marker='x')
plt.title('Pengaruh Kecepatan Angin Terhadap Penyewaan', fontsize=16)
plt.xlabel('Kecepatan Angin')
plt.ylabel('Jumlah Penyewaan')
plt.grid(True)
st.pyplot(plt)

#caption
st.caption("Berdasarkan analisis korelasi antara kecepatan angin (windspeed) dan jumlah penyewaan sepeda (count) pada tahun 2011, ditemukan korelasi yang lemah dan negatif. Ini menunjukkan bahwa kecepatan angin tidak memiliki pengaruh yang signifikan terhadap penyewaan sepeda. Dengan kata lain, meskipun ada sedikit penurunan jumlah penyewaan pada hari-hari dengan kecepatan angin lebih tinggi, pengaruhnya sangat kecil.")

# Visualisasi Penyewaan Berdasarkan Weekday vs Weekend
st.markdown("### Perbandingan Sewa Sepeda Weekday dan Weekend (Mei-September 2012)")
plt.figure(figsize=(10, 6))
sns.barplot(x='day_type', y='count', hue='month', data=weekday_data, palette='Set2', 
            hue_order=['May', 'Jun', 'Jul', 'Aug', 'Sep'])

# Judul dan label
plt.title('Perbandingan Sewa Sepeda Weekday dan Weekend (Mei-September 2012)', fontsize=16)
plt.ylabel('Jumlah Penyewaan')
plt.xlabel('Kategori Hari')
plt.legend(title='Bulan', loc='upper right')
plt.grid(axis='y')

# Tampilkan grafik
plt.tight_layout()
st.pyplot(plt)

#caption
st.caption("Secara umum, penyewaan sepeda pada weekend cenderung lebih tinggi dibandingkan weekday pada bulan Mei hingga September 2012, kecuali pada bulan Juli dan Agustus. Pada bulan Mei, Juni, dan September penyewaan sepeda saat weekend lebih banyak, sedangkan di bulan Juli dan Agustus, penyewaan sepeda pada weekday justru lebih tinggi dibandingkan weekend. Hal ini menunjukkan fluktuasi dalam pola penyewaan sepeda berdasarkan hari dalam seminggu.")
st.caption("Copyright © 2024 by Muhammad Ibrahim")
