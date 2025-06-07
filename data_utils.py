# data_utils.py

import yfinance as yf
import pandas as pd

def download_prices(symbols, start, end, interval="1d"):
    data = yf.download(
        tickers=symbols,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=False,
        group_by='ticker'
    )
    # ↓↓↓ NUEVO: debug
    print("\n--- DEBUG: DataFrame descargado ---")
    print(data.head())
    print("Columnas:", data.columns)
    # ↑↑↑

    # Si es un solo símbolo
    if isinstance(data.columns, pd.MultiIndex):
        if len(symbols) == 1:
            symbol = symbols[0]
            df = data[symbol].copy()
            df.columns = [col.lower() for col in df.columns]
            df = df.dropna(how='all')
        else:
            frames = []
            for symbol in symbols:
                if symbol in data.columns.get_level_values(1):
                    temp = data.xs(symbol, axis=1, level=1, drop_level=False)
                    temp.columns = [f"{col[0].lower()}_{col[1]}" for col in temp.columns]
                    frames.append(temp)
            df = pd.concat(frames, axis=1)
    else:
        df = data.copy()
        df.columns = [col.lower() for col in df.columns]
        df = df.dropna(how='all')

    # ↓↓↓ NUEVO: debug después de limpieza
    print("\n--- DEBUG: DataFrame procesado ---")
    print(df.head())
    print("Columnas finales:", df.columns)
    # ↑↑↑

    return df
