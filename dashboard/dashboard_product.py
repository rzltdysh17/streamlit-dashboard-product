import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setting style
sns.set(style="darkgrid")
st.set_page_config(page_title="Dashboard Produk", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/product_final.csv")
    df.dropna(subset=['product_category_name_english', 'product_length_cm', 
                      'product_height_cm', 'product_width_cm', 'product_photos_qty'], inplace=True)
    df["volume_cm3"] = df["product_length_cm"] * df["product_height_cm"] * df["product_width_cm"]
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("🔍 Filter Kategori Produk")

# Urutkan kategori per abjad
all_categories = sorted(df['product_category_name_english'].dropna().unique())

# Tambahkan opsi 'Pilih Semua' dan 'Reset'
select_all = st.sidebar.checkbox("Pilih Semua Kategori", value=True)

selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk (A-Z)", all_categories,
    default=all_categories if select_all else [])

# Filter data
df_filtered = df[df['product_category_name_english'].isin(selected_categories)]

st.title("📊 Dashboard Analisis Produk")

# Tabs
tab1, tab2, tab3 = st.tabs(["📦 Jumlah Produk", "📸 Rata-rata Foto", "📐 Rata-rata Volume"])

with tab1:
    st.subheader("Top 10 Kategori dengan Jumlah Produk Terbanyak")
    top_categories = df_filtered['product_category_name_english'].value_counts().head(10)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(y=top_categories.index, x=top_categories.values, palette="viridis", ax=ax1)
    ax1.set_xlabel("Jumlah Produk")
    ax1.set_ylabel("Kategori Produk")
    st.pyplot(fig1)

with tab2:
    st.subheader("Top 10 Kategori dengan Rata-rata Jumlah Foto Produk Terbanyak")
    photo_categories = df_filtered.groupby('product_category_name_english')['product_photos_qty'].mean().sort_values(ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(y=photo_categories.index, x=photo_categories.values, palette="crest", ax=ax2)
    ax2.set_xlabel("Rata-rata Jumlah Foto")
    ax2.set_ylabel("Kategori Produk")
    st.pyplot(fig2)

with tab3:
    st.subheader("Top 10 Kategori dengan Rata-rata Volume Produk Terbesar")
    volume_categories = df_filtered.groupby('product_category_name_english')['volume_cm3'].mean().sort_values(ascending=False).head(10)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(y=volume_categories.index, x=volume_categories.values, palette="mako", ax=ax3)
    ax3.set_xlabel("Rata-rata Volume (cm³)")
    ax3.set_ylabel("Kategori Produk")
    st.pyplot(fig3)

# Watermark / Footer
st.markdown("""
---
<div style='text-align: center; font-size: 14px; color: gray;'>
    © Rizal Teddyansyah | 
    <a href='https://github.com/' target='https://github.com/rzltdysh17'>GitHub</a> • 
    <a href='https://linkedin.com/' target='https://www.linkedin.com/in/rizal-teddyansyah/'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
