import streamlit as st
from datetime import datetime
from data_utils import download_prices
from indicadores import add_technical_indicators_extended
from graficos import plot_conglomerate_chart

st.set_page_config(page_title="Never Broke Again – Análisis Individual", layout="wide")
st.title("🔎 Never Broke Again – Análisis Individual de Activos Financieros")

# Sidebar – selección de indicadores
st.sidebar.subheader("Indicadores técnicos a mostrar")
indicadores = st.sidebar.multiselect(
    "Selecciona indicadores para el gráfico",
    ["RSI", "MACD", "ADX", "Stochastic", "ATR", "Bollinger Bands", "SAR", "Ichimoku", "MA50/MA200"],
    default=["RSI", "Bollinger Bands", "MA50/MA200"]
)

symbol = st.text_input("Ticker o símbolo (ej: AAPL, MSFT, EURUSD=X, BTC-USD):", value="GBPUSD=X")
start = st.date_input("Fecha inicio", value=datetime(2023, 1, 1))
end = st.date_input("Fecha fin", value=datetime.today())

if st.button("🔍 Analizar activo individual"):
    with st.spinner(f"Descargando y analizando datos de {symbol}..."):
        df = download_prices([symbol], start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        st.write("--- DataFrame descargado ---")
        st.write(df.head())
        st.write("Columnas:", df.columns)
        if df.empty or 'close' not in df.columns:
            st.error("No se encontraron datos válidos para el símbolo ingresado.")
        else:
            df = add_technical_indicators_extended(df)
            # Advierte si faltan datos para algunos indicadores
            if len(df) < 52:
                st.warning("Atención: algunos indicadores avanzados requieren al menos 52 datos para su cálculo (Ichimoku, MA200...).")
            st.subheader("📈 Gráfico conglomerado con indicadores seleccionados")
            fig = plot_conglomerate_chart(df, symbol, indicadores)
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("📝 Datos diarios + indicadores (últimas 10 filas)")
            st.dataframe(df.tail(10))
            st.download_button("⬇️ Descargar datos (CSV)", df.to_csv(), file_name=f"{symbol}_report.csv")
