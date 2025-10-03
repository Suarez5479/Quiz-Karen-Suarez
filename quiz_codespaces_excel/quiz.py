import os
import pandas as pd

DATA_PATH = "data/raw/encuestas_demo.csv"
OUT_DIR = "reports"
OUT_FILE = os.path.join(OUT_DIR, "quiz_result.xlsx")

def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)

def load_data(path: str) -> pd.DataFrame:
    """TODO(1): Carga el CSV y retorna un DataFrame."""
    df = pd.read_csv(path)
    return df

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(2): Devuelve copia con nombres de columnas en minúsculas y espacios->'_'."""
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out

def dist_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(3): Conteo por 'departamento' (desc), columna 'count'."""
    vc = df["departamento"].value_counts(dropna=False)
    return vc.reset_index().rename(columns={"departamento":"count", "count":"departamento"}).sort_values("count", ascending=False)

def top5_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(4): Top 5 municipios por cantidad (desc)."""
    vc = df["municipio"].value_counts(dropna=False).head(5)
    return vc.reset_index().rename(columns={"municipio":"count", "count":"municipio"})[["municipio", "count"]]

def gasto_promedio_por_servicio(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(5): Promedio de 'gasto_estimado' por 'servicio' (desc)."""
    resultado = df.groupby("servicio")["gasto_estimado"].mean().sort_values(ascending=False)
    return resultado.reset_index().rename(columns={"gasto_estimado":"gasto_promedio"})

def pivot_municipio_x_punto(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(6): Conteos municipio x punto_atencion como tabla dinámica."""
    pivot = pd.pivot_table(
        df,
        values="id",
        index="municipio",
        columns="punto_atencion",
        aggfunc="count",
        fill_value=0
    )
    return pivot.reset_index()

def export_excel(tables: dict, out_file: str):
    """TODO(7): Exporta a Excel con una hoja por cada clave del dict."""
    with pd.ExcelWriter(out_file, engine="openpyxl") as xw:
        for sheet, tdf in tables.items():
            tdf.to_excel(xw, sheet_name=sheet, index=False)

def main():
    ensure_dirs()
    df = load_data(DATA_PATH)
    df = clean_columns(df)
    t1 = dist_departamento(df)
    t2 = top5_municipio(df)
    t3 = gasto_promedio_por_servicio(df)
    t4 = pivot_municipio_x_punto(df)
    tables = {
        "dist_departamento": t1,
        "top5_municipio": t2,
        "gasto_promedio_por_servicio": t3,
        "pivot_municipio_x_punto": t4,
    }
    export_excel(tables, OUT_FILE)
    print(f"[OK] Entregable generado: {os.path.abspath(OUT_FILE)}")

if __name__ == "__main__":
    main()