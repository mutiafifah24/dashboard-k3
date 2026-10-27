import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Inspeksi K3", layout="wide")
st.title("🦺 Dashboard Inspeksi K3")

# Load Data
df = pd.read_csv("data_k3.csv")

# Filter Sidebar
st.sidebar.header("Filter Data")
lokasi = st.sidebar.multiselect(
    "Pilih Lokasi:",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
status = st.sidebar.multiselect(
    "Pilih Status:", options=df["Status"].unique(), default=df["Status"].unique()
)

df_filtered = df[(df["Location"].isin(lokasi)) & (df["Status"].isin(status))]

# Metrik Utama (Cards)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Temuan", len(df_filtered))
col2.metric("Open", len(df_filtered[df_filtered["Status"] == "Open"]))
col3.metric("On Progress", len(df_filtered[df_filtered["Status"] == "Progress"]))
col4.metric("Closed", len(df_filtered[df_filtered["Status"] == "Closed"]))

st.markdown("---")

# Grafik Visualisasi
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
  st.subheader("Temuan Berdasarkan Kategori")
  fig_cat = px.bar(
      df_filtered,
      x="Category",
      color="Status",
      barmode="group",
      title="Jumlah Temuan per Kategori",
  )
  st.plotly_chart(fig_cat, use_container_width=True)

with col_chart2:
  st.subheader("Distribusi Status Temuan")
  fig_pie = px.pie(
      df_filtered, names="Status", title="Persentase Status Temuan", hole=0.4
  )
  st.plotly_chart(fig_pie, use_container_width=True)

# Tabel Data
st.subheader("📋 Detail Data Temuan")
st.dataframe(df_filtered)
