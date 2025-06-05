"""Aplicación Streamlit para análisis y reporte de activos financieros."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# --------- Portafolios predefinidos ---------
PORTFOLIOS: dict[str, list[str]] = {
    "Majors_USD": ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'USDCHF=X', 'AUDUSD=X'],
    "Eurocéntrico": ['EURUSD=X', 'EURJPY=X', 'EURGBP=X', 'EURCHF=X', 'EURAUD=X'],
    "USD_vs_Mundo": ['EURUSD=X', 'USDJPY=X', 'USDCAD=X', 'USDCHF=X', 'AUDUSD=X', 'NZDUSD=X', 'USDSEK=X'],
    "Commodity FX": ['AUDUSD=X', 'NZDUSD=X', 'USDCAD=X', 'USDNOK=X', 'USDZAR=X'],
    "Asia FX": ['USDJPY=X', 'USDCNH=X', 'USDSGD=X', 'USDHKD=X', 'USDINR=X'],
    "S&P500 Big Tech": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA'],
    "Bancos USA": ['JPM', 'BAC', 'C', 'WFC', 'GS', 'MS', 'USB'],
    "Índices Globales": ['^GSPC', '^DJI', '^IXIC', '^FTSE', '^N225', '^HSI', '^BVSP'],
    "ETFs Diversificados": ['SPY', 'QQQ', 'EEM', 'IWM', 'VNQ', 'TLT', 'GLD'],
    "Latam Stocks": ['BBD', 'PBR', 'VALE', 'ITUB', 'CIB', 'EC', 'SQM'],
    "Crypto Majors (Spot ETF/Stock)": ['BTC-USD', 'ETH-USD', 'COIN', 'MSTR', 'RIOT'],
    "Energía Global": ['XOM', 'CVX', 'COP', 'BP', 'SHEL', 'TOT', 'ENB'],
    "Consumo Defensivo USA": ['PG', 'KO', 'PEP', 'WMT', 'COST', 'MDLZ', 'MO'],
    "Europa Blue Chips": ['NESN.SW', 'SAP.DE', 'OR.PA', 'ASML.AS', 'NOVN.SW', 'SIE.DE', 'DAI.DE'],
    "Healthcare USA": ['JNJ', 'PFE', 'UNH', 'MRK', 'ABT', 'LLY', 'CVS']
}


@dataclass
class Metrics:
    """Container for common financial metrics."""

    mean_daily_return: float
    volatility: float
    cumulative_return: float
    sharpe_ratio: float
    max_drawdown: float
    annualized_return: float
    annualized_volatility: float

# --------- Funciones Compartidas ---------
def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Calcula el Índice de Fuerza Relativa (RSI)."""

    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)

def compute_bollinger(series: pd.Series, window: int = 20) -> tuple[pd.Series, pd.Series]:
    """Devuelve bandas de Bollinger superior e inferior."""

    sma = series.rolling(window).mean()
    std = series.rolling(window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    return upper, lower

def compute_metrics(asset_ret: pd.Series) -> Metrics:
    """Calcula métricas financieras básicas para una serie de retornos logarítmicos."""

    mean_return = float(asset_ret.mean())
    volatility = float(asset_ret.std())
    cumulative = float(np.exp(asset_ret.cumsum().iloc[-1]) - 1)
    sharpe = mean_return / volatility * np.sqrt(252) if volatility > 0 else np.nan
    max_drawdown = float((asset_ret.cumsum().expanding().max() - asset_ret.cumsum()).max())
    ann_return = mean_return * 252
    ann_vol = volatility * np.sqrt(252)
    return Metrics(
        mean_daily_return=mean_return,
        volatility=volatility,
        cumulative_return=cumulative,
        sharpe_ratio=sharpe,
        max_drawdown=max_drawdown,
        annualized_return=ann_return,
        annualized_volatility=ann_vol,
    )

def plot_portfolio(data: pd.DataFrame, returns: pd.DataFrame, port_ret: pd.Series, portfolio_name: str) -> plt.Figure:
    """Grafica la evolución de un portafolio."""

    fig, ax = plt.subplots(figsize=(10, 5))
    (data / data.iloc[0]).plot(ax=ax, alpha=0.4)
    ((1 + port_ret).cumprod()).plot(ax=ax, label="Portafolio (pesos iguales)", color="black", lw=2)
    plt.title(f"Evolución del portafolio: {portfolio_name}")
    plt.ylabel("Crecimiento acumulado")
    plt.legend()
    plt.tight_layout()
    return fig

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega indicadores técnicos básicos a un DataFrame de precios."""

    df = df.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["RSI14"] = compute_rsi(df["Close"], window=14)
    bb_upper, bb_lower = compute_bollinger(df["Close"], 20)
    df["BB_upper"], df["BB_lower"] = bb_upper, bb_lower
    return df

def plot_price_chart(df: pd.DataFrame, symbol: str) -> plt.Figure:
    """Grafica precio e indicadores técnicos de un activo."""

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close"], label="Close")
    ax.plot(df.index, df["SMA20"], label="SMA20")
    ax.plot(df.index, df["EMA20"], label="EMA20")
    ax.fill_between(df.index, df["BB_upper"], df["BB_lower"], color="lightgray", alpha=0.3, label="Bollinger Bands")
    ax.set_title(f"{symbol} Price Chart")
    ax.legend()
    plt.tight_layout()
    return fig

def extract_features_for_IA(prices: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Genera features estadísticos y técnicos para IA o backtesting."""

    panel_features: List[pd.DataFrame] = []
    for symbol in prices.columns:
        close = prices[symbol].dropna()
        if len(close) < window + 2:
            continue
        df = pd.DataFrame({'date': close.index, 'symbol': symbol, 'Close': close})
        df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
        df['volatility'] = df['log_return'].rolling(window).std() * np.sqrt(252)
        df['sharpe'] = df['log_return'].rolling(window).mean() / df['log_return'].rolling(window).std() * np.sqrt(252)
        df['VaR'] = df['log_return'].rolling(window).quantile(0.05)
        df['ES'] = df['log_return'].rolling(window).apply(
            lambda x: x[x <= np.quantile(x, 0.05)].mean() if np.any(x <= np.quantile(x, 0.05)) else np.nan)
        df['skew'] = df['log_return'].rolling(window).skew()
        df['kurtosis'] = df['log_return'].rolling(window).kurt()
        df['RSI14'] = compute_rsi(df['Close'], window=14)
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['EMA20'] = df['Close'].ewm(span=20).mean()
        sma = df['SMA20']
        std = df['Close'].rolling(20).std()
        df['BB_upper'] = sma + 2 * std
        df['BB_lower'] = sma - 2 * std
        df['drawdown'] = (df['Close'] - df['Close'].cummax()) / df['Close'].cummax()
        df = df.dropna(subset=['log_return'])
        panel_features.append(df)
    if not panel_features:
        return pd.DataFrame()
    features_df = pd.concat(panel_features, ignore_index=True)
    features_df = features_df.drop_duplicates(subset=['date', 'symbol'])
    features_df = features_df.sort_values(['symbol', 'date'])
    return features_df


def download_prices(symbols: Iterable[str], start: str, end: str) -> pd.DataFrame:
    """Descarga precios de cierre usando yfinance."""

    data = yf.download(list(symbols), start=start, end=end, progress=False)
    if 'Close' in data.columns:
        data = data['Close']
    return data.dropna(how="all")

# --------- STREAMLIT APP ---------


def main() -> None:
    """Despliega la interfaz de usuario en Streamlit."""

    st.set_page_config(page_title="Plataforma de Análisis Financiero", layout="centered")
    st.title("📊 Plataforma Integral de Análisis Financiero")

    tab1, tab2 = st.tabs(["Análisis de Portafolio", "Análisis Individual"])

# ---------- TAB 1: PORTAFOLIO COMPLETO -------------

    # ---------- TAB 1: PORTAFOLIO COMPLETO -------------
    with tab1:
        st.header("Análisis de Portafolios (Múltiples Activos)")

        portfolio_name = st.selectbox("Selecciona Portafolio", list(PORTFOLIOS.keys()), key="portfolio_tab1")
        symbols = PORTFOLIOS[portfolio_name]
    
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Fecha inicio", value=datetime(2022, 1, 1), key="start_tab1")
        with col2:
            end = st.date_input("Fecha fin", value=datetime.today(), key="end_tab1")
    
        if st.button("Lanzar análisis de portafolio"):
            start_str = start.strftime('%Y-%m-%d')
            end_str = end.strftime('%Y-%m-%d')
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            folder = os.path.join("portafolios_excel", f"{portfolio_name}_{now}")
            os.makedirs(folder, exist_ok=True)
            
            st.info("⏳ Descargando precios y calculando... (puede tardar unos segundos)")
            data = download_prices(symbols, start_str, end_str)
            if data.empty or len(data) < 2:
                st.error("❌ No hay datos suficientes para este portafolio.")
            else:
                returns = np.log(data / data.shift(1)).dropna()
                returns_csv = returns.to_csv().encode()
                port_ret = returns.mean(axis=1)
                port_ret.name = 'retorno_portafolio'
                metrics_port = compute_metrics(port_ret)
                stats_df = pd.DataFrame({
                    "Retorno Medio (%)": returns.mean() * 252 * 100,
                    "Volatilidad (%)": returns.std() * np.sqrt(252) * 100,
                    "Retorno Total (%)": (data.iloc[-1]/data.iloc[0] - 1) * 100
                }).round(2)
                stats_csv = stats_df.to_csv().encode()
                stats_portfolio = pd.DataFrame([metrics_port])
                corr = returns.corr()
                corr_csv = corr.to_csv().encode()
    
                # Resultados principales
                st.subheader("📊 Retornos individuales (primeros 5)")
                st.dataframe(returns.head())
                st.download_button("⬇️ Descargar retornos individuales (CSV)", returns_csv, file_name="retornos_individuales.csv")
                
                st.subheader("📈 Estadísticas individuales")
                st.dataframe(stats_df)
                st.download_button("⬇️ Descargar estadísticas individuales (CSV)", stats_csv, file_name="estadisticas_individuales.csv")
    
                st.subheader("📉 Estadísticas del portafolio combinado")
                st.json(metrics_port)
                
                st.subheader("🔗 Matriz de correlación")
                st.dataframe(corr)
                st.download_button("⬇️ Descargar matriz de correlación (CSV)", corr_csv, file_name="correlacion.csv")
    
                # Gráfico
                st.subheader("📈 Evolución del portafolio")
                fig = plot_portfolio(data, returns, port_ret, portfolio_name)
                st.pyplot(fig)
    
                # Correlaciones extremas (con fix para error de duplicados)
                corr_vals = corr.where(~np.eye(corr.shape[0],dtype=bool)).stack()
                corr_vals.index = corr_vals.index.set_names(['Activo 1', 'Activo 2'])
                most_negative = corr_vals.nsmallest(3).reset_index()
                most_positive = corr_vals.nlargest(3).reset_index()
                most_negative = most_negative.loc[:,~most_negative.columns.duplicated()]
                most_positive = most_positive.loc[:,~most_positive.columns.duplicated()]
    
                st.markdown("#### Correlaciones más negativas")
                st.dataframe(most_negative)
                st.markdown("#### Correlaciones más positivas")
                st.dataframe(most_positive)
    
                # Extracción de features para IA
                st.info("🔬 Extrayendo features avanzados para IA/trading automático...")
                features_df = extract_features_for_IA(data, window=20)
                if not features_df.empty:
                    features_csv = features_df.to_csv(index=False).encode()
                    st.success("✅ Features extraídos para IA/trading automático (primeras 5 filas):")
                    st.dataframe(features_df.head())
                    st.download_button("⬇️ Descargar features para IA (CSV)", features_csv, file_name="features_para_IA.csv")
                else:
                    st.warning("No hay suficientes datos para calcular features de IA en todos los activos.")
    
                st.success("✅ Análisis completo realizado. Archivos generados localmente en:")
                st.code(folder)

    # ---------- TAB 2: INDIVIDUAL -------------
    with tab2:
        st.header("Análisis Individual de Activos Financieros")
        with st.form("analyze_form"):
            symbol = st.text_input(
                "Ticker o símbolo (ej: AAPL, MSFT, TSLA, EURUSD=X, BTC-USD):",
                value="AAPL",
            )
            col1, col2 = st.columns(2)
            with col1:
                start_ind = st.date_input("Fecha inicio", value=datetime(2022, 1, 1), key="start_tab2")
            with col2:
                end_ind = st.date_input("Fecha fin", value=datetime.today(), key="end_tab2")
            submitted = st.form_submit_button("Lanzar análisis individual")

    if submitted:
        start_str = start_ind.strftime('%Y-%m-%d')
        end_str = end_ind.strftime('%Y-%m-%d')
        asset_folder = os.path.join("analisis_individual", symbol.upper() + "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(asset_folder, exist_ok=True)
        st.info(f"Descargando y analizando {symbol.upper()} ...")
        df = download_prices([symbol], start_str, end_str)
        if df.empty:
            st.error("❌ No hay datos para ese ticker y fechas seleccionadas.")
        else:
            df = add_technical_indicators(df)
            ret = np.log(df['Close']).diff().dropna()
            metrics = compute_metrics(ret)
            # Exporta datos diarios
            csv_path = os.path.join(asset_folder, f"{symbol}_report.csv")
            df.to_csv(csv_path)
            # Exporta métricas resumen
            metrics_path = os.path.join(asset_folder, f"{symbol}_metrics.csv")
            pd.DataFrame([metrics]).to_csv(metrics_path, index=False)
            # Gráfico
            fig = plot_price_chart(df, symbol)
            chart_path = os.path.join(asset_folder, f"{symbol}_price_chart.png")
            fig.savefig(chart_path)
            plt.close(fig)

            # --- Mostrar resultados en pantalla ---
            st.success(f"✅ Análisis completado para {symbol.upper()}")
            st.subheader("📊 Métricas principales")
            st.json(metrics)

            st.subheader("📈 Gráfico de precio e indicadores")
            st.pyplot(fig)

            st.subheader("📝 Datos diarios (primeras 10 filas)")
            st.dataframe(df.head(10))

            # --- Descarga directa de archivos ---
            with open(csv_path, "rb") as f:
                st.download_button("⬇️ Descargar datos diarios (CSV)", f, file_name=f"{symbol}_report.csv")
            with open(metrics_path, "rb") as f:
                st.download_button("⬇️ Descargar métricas (CSV)", f, file_name=f"{symbol}_metrics.csv")
            with open(chart_path, "rb") as f:
                st.download_button("⬇️ Descargar gráfico (PNG)", f, file_name=f"{symbol}_price_chart.png")

            st.info(f"Todos los archivos han sido guardados en la carpeta local: {asset_folder}")


if __name__ == "__main__":
    main()

