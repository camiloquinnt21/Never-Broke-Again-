def add_technical_indicators_extended(df):
    import streamlit as st
    from ta.trend import MACD, ADXIndicator, PSARIndicator, IchimokuIndicator
    from ta.momentum import RSIIndicator, StochasticOscillator
    from ta.volatility import BollingerBands, AverageTrueRange

    df = df.copy()
    df.columns = [c.lower() for c in df.columns]

    # Medias móviles simples y exponenciales (requieren 'close')
    if 'close' in df.columns:
        df['sma20'] = df['close'].rolling(20).mean()
        df['ema20'] = df['close'].ewm(span=20).mean()
        if len(df) >= 50:
            df['ma50'] = df['close'].rolling(50).mean()
        else:
            st.warning("No hay suficientes datos para calcular MA50 (mínimo 50 datos requeridos).")
        if len(df) >= 200:
            df['ma200'] = df['close'].rolling(200).mean()
        else:
            st.warning("No hay suficientes datos para calcular MA200 (mínimo 200 datos requeridos).")

        # Bollinger Bands (mínimo 20 datos)
        if len(df) >= 20:
            bb = BollingerBands(df['close'], window=20)
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_lower'] = bb.bollinger_lband()
            df['bb_middle'] = bb.bollinger_mavg()
        else:
            st.warning("No hay suficientes datos para calcular Bollinger Bands (mínimo 20 datos requeridos).")

        # RSI (mínimo 14 datos)
        if len(df) >= 14:
            df['rsi14'] = RSIIndicator(df['close'], window=14).rsi()
        else:
            st.warning("No hay suficientes datos para calcular RSI (mínimo 14 datos requeridos).")

        # MACD (mínimo 26 datos)
        if len(df) >= 26:
            macd = MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
        else:
            st.warning("No hay suficientes datos para calcular MACD (mínimo 26 datos requeridos).")

    # Indicadores que requieren High, Low y Close
    have_hlc = all(x in df.columns for x in ['high', 'low', 'close'])

    # SAR (mínimo 2 datos)
    if have_hlc:
        if len(df) >= 2:
            psar = PSARIndicator(df['high'], df['low'], df['close'], step=0.02, max_step=0.2)
            df['sar'] = psar.psar()
        else:
            st.warning("No hay suficientes datos para calcular SAR (mínimo 2 datos requeridos).")

        # ADX, ATR (mínimo 15 datos)
        if len(df) >= 15:
            adx = ADXIndicator(high=df['high'], low=df['low'], close=df['close'])
            df['adx'] = adx.adx()
            df['+di'] = adx.adx_pos()
            df['-di'] = adx.adx_neg()
            df['atr'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
        else:
            st.warning("No hay suficientes datos para calcular ADX/ATR (mínimo 15 datos requeridos).")

        # Ichimoku (mínimo 52 datos)
        if len(df) >= 52:
            ichimoku = IchimokuIndicator(high=df['high'], low=df['low'], window1=9, window2=26, window3=52)
            df['tenkan_sen'] = ichimoku.ichimoku_conversion_line()
            df['kijun_sen'] = ichimoku.ichimoku_base_line()
            df['senkou_span_a'] = ichimoku.ichimoku_a()
            df['senkou_span_b'] = ichimoku.ichimoku_b()
        else:
            st.warning("No hay suficientes datos para calcular Ichimoku (mínimo 52 datos requeridos).")

        # Stochastic Oscillator (mínimo 5 datos)
        if len(df) >= 5:
            stoch = StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=5, smooth_window=3)
            df['stoch'] = stoch.stoch()
            df['stoch_signal'] = stoch.stoch_signal()
        else:
            st.warning("No hay suficientes datos para calcular Stochastic Oscillator (mínimo 5 datos requeridos).")

    return df
