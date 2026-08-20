import streamlit as st

from universo import cargar_universo
from datos_app.datos import descargar_datos
from scanner import analizar_accion


st.set_page_config(
    page_title="IA Swing Trader",
    page_icon="📈",
    layout="wide"
)


st.title("📈 IA Swing Trader")
st.write("Sistema de análisis de CEDEARs")


st.sidebar.title("MENU")

opcion = st.sidebar.radio(
    "Seleccioná una opción:",
    [
        "🏆 Escanear mercado",
        "🔎 Analizar empresa"
    ]
)


# =====================================================
# ESCANEAR MERCADO
# =====================================================

if opcion == "🏆 Escanear mercado":

    st.header("🏆 Ranking del mercado")

    if st.button("🔄 Ejecutar scanner"):

        empresas = cargar_universo()

        if empresas.empty:

            st.error(
                "No se encontraron empresas."
            )

        else:

            resultados = []

            barra = st.progress(0)

            total = len(empresas)

            for i, (_, empresa) in enumerate(
                empresas.iterrows()
            ):

                ticker = str(
                    empresa["Ticker"]
                ).upper().strip()

                try:

                    datos = descargar_datos(
                        ticker
                    )

                    if datos is None or datos.empty:
                        continue

                    resultado = analizar_accion(
                        ticker,
                        datos
                    )

                    if resultado is None:
                        continue

                    # ---------------------------------
                    # SOLO MOSTRAR COMPRAR
                    # ---------------------------------

                    if resultado["score"] < 70:
                        continue

                    resultado["nombre"] = (
                        empresa["Nombre"]
                    )

                    resultado["sector"] = (
                        empresa["Sector"]
                    )

                    resultado["industria"] = (
                        empresa["Industria"]
                    )

                    resultados.append(
                        resultado
                    )

                except Exception:
                    continue

                barra.progress(
                    (i + 1) / total
                )

            # =========================================
            # ORDENAR
            # =========================================

            resultados.sort(
                key=lambda x: x["score"],
                reverse=True
            )

            # =========================================
            # RESULTADOS
            # =========================================

            if not resultados:

                st.warning(
                    "No se encontraron empresas con score de COMPRAR."
                )

            else:

                st.success(
                    f"Se encontraron {len(resultados)} empresas para COMPRAR."
                )

                st.subheader(
                    "🏆 Ranking general"
                )

                for posicion, empresa in enumerate(
                    resultados,
                    start=1
                ):

                    st.markdown(
                        f"### {posicion}. "
                        f"{empresa['ticker']} — "
                        f"{empresa['nombre']}"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Score",
                        f"{empresa['score']}/85"
                    )

                    col2.metric(
                        "Precio",
                        f"${empresa['precio']:.2f}"
                    )

                    col3.metric(
                        "RSI",
                        f"{empresa['rsi']:.1f}"
                    )

                    col4.metric(
                        "Estado",
                        "COMPRAR"
                    )

                    st.write(
                        f"**Sector:** {empresa['sector']}"
                    )

                    st.write(
                        f"**Industria:** {empresa['industria']}"
                    )

                    with st.expander(
                        "Ver análisis"
                    ):

                        for motivo in empresa[
                            "motivos"
                        ]:

                            st.write(motivo)

                    st.divider()

                # =====================================
                # MEJOR EMPRESA POR SECTOR
                # =====================================

                st.header(
                    "🏆 Mejor empresa por sector"
                )

                sectores = {}

                for empresa in resultados:

                    sector = empresa[
                        "sector"
                    ]

                    if sector not in sectores:

                        sectores[sector] = []

                    sectores[sector].append(
                        empresa
                    )

                for sector, empresas_sector in sectores.items():

                    mejor = max(
                        empresas_sector,
                        key=lambda x: x["score"]
                    )

                    st.subheader(
                        f"📂 {sector}"
                    )

                    st.write(
                        f"🥇 **{mejor['ticker']} — "
                        f"{mejor['nombre']}**"
                    )

                    st.write(
                        f"Score: **{mejor['score']}/85**"
                    )


# =====================================================
# ANALIZAR EMPRESA
# =====================================================

elif opcion == "🔎 Analizar empresa":

    st.header("🔎 Analizar empresa")

    ticker = st.text_input(
        "Ingrese el ticker",
        placeholder="Ejemplo: AAPL"
    )

    if st.button("Analizar"):

        if not ticker:

            st.warning(
                "Ingresá un ticker."
            )

        else:

            ticker = ticker.upper().strip()

            datos = descargar_datos(
                ticker
            )

            if datos is None or datos.empty:

                st.error(
                    "No se pudieron descargar los datos."
                )

            else:

                resultado = analizar_accion(
                    ticker,
                    datos
                )

                if resultado is None:

                    st.error(
                        "No se pudo analizar la empresa."
                    )

                elif resultado["score"] < 70:

                    st.warning(
                        "Esta empresa no cumple "
                        "las condiciones para COMPRAR."
                    )

                else:

                    st.success(
                        "🟢 COMPRAR"
                    )

                    st.metric(
                        "Score",
                        f"{resultado['score']}/85"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Precio",
                        f"${resultado['precio']:.2f}"
                    )

                    col2.metric(
                        "Media 50",
                        f"${resultado['m50']:.2f}"
                    )

                    col3.metric(
                        "Media 200",
                        f"${resultado['m200']:.2f}"
                    )

                    st.metric(
                        "RSI",
                        f"{resultado['rsi']:.1f}"
                    )

                    st.write(
                        "### Análisis"
                    )

                    for motivo in resultado[
                        "motivos"
                    ]:

                        st.write(motivo)