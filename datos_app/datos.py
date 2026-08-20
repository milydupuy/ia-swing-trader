import yfinance as yf


def descargar_datos(simbolo, periodo="10y"):

    try:

        datos = yf.download(
            simbolo,
            period=periodo,
            progress=False,
            auto_adjust=False
        )

        if datos is None or datos.empty:
            return None

        # -----------------------------------------
        # NORMALIZAR COLUMNAS DE YFINANCE
        # -----------------------------------------

        if hasattr(datos.columns, "nlevels"):

            if datos.columns.nlevels > 1:

                datos.columns = (
                    datos.columns
                    .get_level_values(0)
                )

        # -----------------------------------------
        # VERIFICAR CLOSE
        # -----------------------------------------

        if "Close" not in datos.columns:

            print(
                f"⚠ No se encontró Close para {simbolo}"
            )

            return None

        return datos

    except Exception as e:

        print(
            f"⚠ Error descargando {simbolo}: {e}"
        )

        return None