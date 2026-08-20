from ta.trend import MACD
from ta.momentum import RSIIndicator


def calcular_rsi(datos):

    close = datos["Close"].squeeze()

    rsi = RSIIndicator(
        close=close,
        window=14
    ).rsi()

    return float(rsi.iloc[-1])


def media_50(datos):

    close = datos["Close"].squeeze()

    return float(close.rolling(50).mean().iloc[-1])


def media_200(datos):

    close = datos["Close"].squeeze()

    return float(close.rolling(200).mean().iloc[-1])
def macd_alcista(datos):

    close = datos["Close"].squeeze()

    macd = MACD(close)

    macd_linea = float(macd.macd().iloc[-1])
    signal_linea = float(macd.macd_signal().iloc[-1])

    return macd_linea > signal_linea