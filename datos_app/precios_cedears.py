import requests


URL = "https://data912.com/live/arg_cedears"


def obtener_precios():

    try:

        respuesta = requests.get(
            URL,
            timeout=10
        )

        if respuesta.status_code != 200:
            print(
                f"Error HTTP: {respuesta.status_code}"
            )
            return {}

        datos = respuesta.json()

        precios = {}

        for activo in datos:

            ticker = str(
                activo.get("symbol", "")
            ).upper().strip()

            precio = activo.get("c")

            if not ticker or precio is None:
                continue

            try:
                precio = float(precio)
            except (ValueError, TypeError):
                continue

            precios[ticker] = precio

        print(
            f"✔ Precios CEDEARs cargados: "
            f"{len(precios)}"
        )

        return precios

    except requests.RequestException as e:

        print(
            f"❌ Error conectando al mercado: {e}"
        )

        return {}

    except Exception as e:

        print(
            f"❌ Error procesando precios: {e}"
        )

        return {}