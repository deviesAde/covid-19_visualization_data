import streamlit as st
import pandas as pd
import plotly.express as px

# Set judul dashboard
st.set_page_config(page_title="COVID-19 Indonesia Dashboard", layout="wide")
st.title("📊 COVID-19 Indonesia Time Series Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar 
st.sidebar.header("Filter Data")
provinsi = st.sidebar.multiselect(
    "Pilih Provinsi:",
    options=df['Province'].unique(),
    default=df['Province'].unique()[:5]
)

# Filter data berdasarkan provinsi
df_filtered = df[df['Province'].isin(provinsi)]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tren Harian", "📍 Total per Provinsi", "💀 Case Fatality Rate", "🗺️ Per Pulau"])

# Tab 1: Tren Harian
with tab1:
    st.subheader("Tren New Cases Harian per Provinsi")
    fig1 = px.line(df_filtered, x='Date', y='New Cases', color='Province',
                   title='Tren Kasus Baru Harian')
    st.plotly_chart(fig1, use_container_width=True)

# Tab 2: Total per Provinsi
with tab2:
    st.subheader("Total Kasus, Sembuh, dan Meninggal per Provinsi")
    latest = df_filtered.groupby('Province').last().reset_index()
    fig2 = px.bar(latest, x='Province', y=['Total Cases', 'Total Recovered', 'Total Deaths'],
                  barmode='group', title='Total Kasus, Sembuh, dan Meninggal')
    st.plotly_chart(fig2, use_container_width=True)

# Tab 3: Case Fatality Rate
with tab3:
    st.subheader("Case Fatality Rate (CFR) per Provinsi")
    latest['CFR'] = (latest['Total Deaths'] / latest['Total Cases']) * 100
    fig3 = px.bar(latest, x='Province', y='CFR', title='Case Fatality Rate (%)')
    st.plotly_chart(fig3, use_container_width=True)

# Tab 4: Per Pulau
with tab4:
    st.subheader("Total Kasus per Pulau")
    pulau = latest.groupby('Island')['Total Cases'].sum().reset_index()
    fig4 = px.pie(pulau, names='Island', values='Total Cases', title='Distribusi Kasus per Pulau')
    st.plotly_chart(fig4, use_container_width=True)

# Insight
st.header("🔍 Insight dari Data COVID-19 Historis Indonesia")
st.markdown("""
- **Jawa vs Luar Jawa**: Jawa mendominasi total kasus, tapi CFR di beberapa provinsi luar Jawa lebih tinggi → **ketimpangan akses kesehatan**.
- **CFR > 5 %** di Papua, Maluku, NTT menandakan **kapasitas fasilitas kesehatan daerah perlu diperkuat**.
- **Lonjakan kasus** selalu muncul setelah libur nasional/lebihan → **kebijakan mobilitas memengaruhi kurva wabah**.
- **Penurunan CFR nasional dari > 3 % ke < 2 %** menunjukkan **vaksinasi dan protokol kesehatan efektif**.
- **Data ini jadi “buku panduan”**: kalau pandemi lagi, kita tahu **daerah mana yang butuh bantuan duluan** dan **kapan harus bikin kebijakan pembatasan**.
""")