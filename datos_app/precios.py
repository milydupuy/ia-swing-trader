from datos_app.precios_cedears import obtener_precios


PRECIOS = {}


def cargar_precios():

    global PRECIOS

    try:

        PRECIOS = obtener_precios()

        print(
            f"✔ Precios CEDEARs cargados: {len(PRECIOS)}"
        )

    except Exception as e:

        print(
            f"❌ Error cargando precios CEDEARs: {e}"
        )

        PRECIOS = {}

    return PRECIOS


def obtener_precio(ticker):

    ticker = str(ticker).upper().strip()

    return PRECIOS.get(ticker)