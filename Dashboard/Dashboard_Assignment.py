# Loading semua libraries yang diperlukan
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import os

# Mengatur halaman Streamlit
st.set_page_config(page_title="E-Commerce Dashboard", layout="centered")
st.title("E-Commerce Sales Dashboard")

# Import data yang digunakan
ecommerce_data = pd.read_csv('Dashboard/ecommerce_cleaned.csv')

# Pre-process data yang akan digunakan untuk visualisasi
ecommerce_data['order_approved_at'] = pd.to_datetime(ecommerce_data['order_approved_at'])
ecommerce_data['order_year'] = ecommerce_data['order_approved_at'].dt.year
ecommerce_data['order_month'] = ecommerce_data['order_approved_at'].dt.month
ecommerce_data['profit'] = ecommerce_data['price'] - ecommerce_data['freight_value']

# Membuat filter pada halaman
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox("Pilih Tahun", sorted(ecommerce_data['order_year'].unique()))
data_filtered = ecommerce_data[ecommerce_data['order_year'] == year_filter]

# 10 kota dengan penjualan tertinggi (2016-2018)
st.subheader(f"10 Kota Dengan Penjualan Tertinggi ({year_filter})")
top10_cities = data_filtered.groupby('customer_city')['price'].sum().sort_values(ascending=False).head(10)
colors = ['#FF5733'] + ['#3498DB'] * (len(top10_cities) - 1)
fig1, ax1 = plt.subplots()
sns.barplot(x=top10_cities.index, y=top10_cities.values, palette=colors, ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# 5 produk yang paling banyak terjual
filtered_profit = data_filtered.dropna(subset=['product_category_name'])
most_profitable = filtered_profit.groupby('product_category_name').apply(
    lambda x: (x['price'] - x['freight_value']).sum()
).sort_values(ascending=False).head(5)

st.subheader(f"5 Produk Dengan Penjualan Terbanyak ({year_filter})")
colors_profitable = ['#FF5733'] + ['#3498DB'] * (len(most_profitable) - 1)
fig4, ax4 = plt.subplots()
sns.barplot(x=most_profitable.index, y=most_profitable.values, palette=colors_profitable, ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

# MoM growth per tahun
st.subheader(f"Month-on-Month Sales Growth (%) - {year_filter}")
penjualan_bulanan = data_filtered.groupby(['order_year', 'order_month'])['price'].sum().reset_index()
penjualan_bulanan = penjualan_bulanan.sort_values(['order_year', 'order_month'])
penjualan_bulanan['mom_growth_percent'] = penjualan_bulanan['price'].pct_change() * 100

nama_bulan = [calendar.month_name[m] for m in penjualan_bulanan['order_month']]
colors_growth = ['#FF5733' if growth > 0 else '#3498DB' for growth in penjualan_bulanan['mom_growth_percent']]

fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.barplot(x=nama_bulan, y=penjualan_bulanan['mom_growth_percent'], palette=colors_growth, ax=ax5)
plt.title(f"Month-on-Month Sales Growth (%) - {year_filter}", fontsize=14)
plt.xlabel("Bulan")
plt.ylabel("MoM Growth (%)")
plt.xticks(rotation=45)
plt.axhline(0, color='black', linestyle='--', linewidth=1)
st.pyplot(fig5)

st.caption("Maulana Muhammad Ikhsan")