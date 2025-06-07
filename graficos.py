# graficos.py

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_conglomerate_chart(df, symbol, indicadores):
    rows = 1
    subplot_titles = ["Precio"]
    for ind in ["RSI", "MACD", "ADX", "Stochastic", "ATR"]:
        if ind in indicadores:
            rows += 1
            subplot_titles.append(ind)
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03, 
                        subplot_titles=subplot_titles, row_heights=[0.5]+[0.12]*(rows-1))
    r = 1
    fig.add_trace(go.Scatter(x=df.index, y=df.get('close'), name='Close', line=dict(color='blue')), row=r, col=1)
    if "MA50/MA200" in indicadores:
        if 'ma50' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['ma50'], name='MA50', line=dict(color='orange')), row=r, col=1)
        if 'ma200' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['ma200'], name='MA200', line=dict(color='purple')), row=r, col=1)
    if "Bollinger Bands" in indicadores:
        if 'bb_upper' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['bb_upper'], name='BB Upper', line=dict(color='grey', dash='dash')), row=r, col=1)
        if 'bb_lower' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['bb_lower'], name='BB Lower', line=dict(color='grey', dash='dash')), row=r, col=1)
    if "SAR" in indicadores and 'sar' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['sar'], name='SAR', mode='markers', marker=dict(color='black', size=5, symbol="circle")), row=r, col=1)
    if "Ichimoku" in indicadores and all(x in df.columns for x in ['tenkan_sen','kijun_sen','senkou_span_a','senkou_span_b']):
        fig.add_trace(go.Scatter(x=df.index, y=df['tenkan_sen'], name='Tenkan-sen', line=dict(color='red')), row=r, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['kijun_sen'], name='Kijun-sen', line=dict(color='green')), row=r, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['senkou_span_a'], name='Senkou Span A', line=dict(color='brown', dash='dot')), row=r, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['senkou_span_b'], name='Senkou Span B', line=dict(color='brown', dash='dash')), row=r, col=1)
    idx = 2
    if "RSI" in indicadores and 'rsi14' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['rsi14'], name='RSI', line=dict(color='teal')), row=idx, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=idx, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=idx, col=1)
        idx += 1
    if "MACD" in indicadores and 'macd' in df.columns and 'macd_signal' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['macd'], name='MACD', line=dict(color='navy')), row=idx, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['macd_signal'], name='MACD Signal', line=dict(color='orange')), row=idx, col=1)
        idx += 1
    if "ADX" in indicadores and 'adx' in df.columns and '+di' in df.columns and '-di' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['adx'], name='ADX', line=dict(color='black')), row=idx, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['+di'], name='+DI', line=dict(color='green', dash='dash')), row=idx, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['-di'], name='-DI', line=dict(color='red', dash='dash')), row=idx, col=1)
        idx += 1
    if "Stochastic" in indicadores and 'stoch' in df.columns and 'stoch_signal' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['stoch'], name='Stoch', line=dict(color='magenta')), row=idx, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['stoch_signal'], name='Stoch Signal', line=dict(color='darkmagenta')), row=idx, col=1)
        idx += 1
    if "ATR" in indicadores and 'atr' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['atr'], name='ATR', line=dict(color='brown')), row=idx, col=1)
        idx += 1
    fig.update_layout(height=350 + 150*(rows-1), title=f"{symbol} – Gráfico interactivo conglomerado", hovermode="x unified")
    return fig
