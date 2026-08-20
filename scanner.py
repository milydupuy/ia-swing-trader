import pandas as pd

from indicadores import (
    calcular_rsi,
    media_50,
    media_200,
    macd_alcista
)

from score import calcular_score

from config import (
    SCORE_COMPRAR,
    SCORE_VIGILAR
)


def obtener_cierre(datos):

    cierre = datos["Close"]

    # Yahoo puede devolver un DataFrame
    if isinstance(cierre, pd.DataFrame):
        cierre = cierre.iloc[:, 0]

    cierre = pd.to_numeric(
        cierre,
        errors="coerce"
    )

    cierre = cierre.dropna()

    if cierre.empty:
        return None

    return float(cierre.iloc[-1])


def analizar_accion(ticker, datos):

    try:

        if datos is None or datos.empty:
            return None

        precio = obtener_cierre(datos)

        if precio is None:
            return None

        m50 = media_50(datos)
        m200 = media_200(datos)
        rsi = calcular_rsi(datos)
        macd = macd_alcista(datos)

        # -----------------------------------------
        # VALIDAR INDICADORES
        # -----------------------------------------

        if pd.isna(m50):
            return None

        if pd.isna(m200):
            return None

        if pd.isna(rsi):
            return None

        # -----------------------------------------
        # CALCULAR SCORE
        # -----------------------------------------

        score, motivos = calcular_score(
            precio,
            m50,
            m200,
            rsi,
            macd
        )

        # -----------------------------------------
        # RECOMENDACIÓN
        # -----------------------------------------

        if score >= SCORE_COMPRAR:

            estado = "COMPRAR"

        elif score >= SCORE_VIGILAR:

            estado = "VIGILAR"

        else:

            estado = "DESCARTAR"

        # -----------------------------------------
        # RESULTADO
        # -----------------------------------------

        return {

            "simbolo": ticker,

            "ticker": ticker,

            "precio": round(precio, 2),

            "m50": round(m50, 2),

            "m200": round(m200, 2),

            "rsi": round(rsi, 2),

            "macd": macd,

            "score": score,

            "estado": estado,

            "motivos": motivos

        }

    except Exception as e:

        print(
            f"⚠ Error analizando {ticker}: {e}"
        )

        return None