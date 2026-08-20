import pandas as pd


ARCHIVO = "datos_app/cedears.csv"


def cargar_universo():

    try:

        df = pd.read_csv(
    ARCHIVO,
    encoding="utf-8-sig"
        )

    except FileNotFoundError:

        print(
            f"\n❌ No se encontró el archivo: {ARCHIVO}"
        )

        return pd.DataFrame()

    # -----------------------------------------
    # NORMALIZAR COLUMNAS
    # -----------------------------------------

    df.columns = (
        df.columns
        .str.strip()
    )

    # -----------------------------------------
    # SOLO CEDEARs ACTIVOS
    # -----------------------------------------

    if "Activo" in df.columns:

        df = df[
            df["Activo"]
            .astype(str)
            .str.upper()
            .str.strip()
            == "SI"
        ]

    # -----------------------------------------
    # ELIMINAR DUPLICADOS
    # -----------------------------------------

    df = df.drop_duplicates(
        subset=["Ticker"]
    )

    df = df.reset_index(
        drop=True
    )

    print(
        f"\nCEDEARs de acciones "
        f"en el universo: {len(df)}"
    )

    return df