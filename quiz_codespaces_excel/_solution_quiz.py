import os
import pandas as pd

DATA_PATH = "data/raw/encuestas_demo.csv"
OUT_DIR = "reports"
OUT_FILE = os.path.join(OUT_DIR, "quiz_result.xlsx")

def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out

def dist_departamento(df: pd.DataFrame) -> pd.DataFrame:
    vc = df["departamento"].value_counts(dropna=False)
    return vc.reset_index().rename(columns={"index":"departamento","departamento":"count"}).sort_values("count", ascending=False)

def top5_municipio(df: pd.DataFrame) -> pd.DataFrame:
    vc = df["municipio"].value_counts(dropna=False).head(5)
    return vc.reset_index().rename(columns={"index":"municipio","municipio":"count"}).sort_values("count", ascending=False)

def gasto_promedio_por_servicio(df: pd.DataFrame) -> pd.DataFrame:
    t = df.groupby("servicio", as_index=False)["gasto_estimado"].mean()
    t.rename(columns={"gasto_estimado":"gasto_promedio"}, inplace=True)
    return t.sort_values("gasto_promedio", ascending=False)

def pivot_municipio_x_punto(df: pd.DataFrame) -> pd.DataFrame:
    pvt = pd.pivot_table(df, index="municipio", columns="punto_atencion", values="id", aggfunc="count", fill_value=0)
    return pvt.reset_index()

def export_excel(tables: dict, out_file: str):
    with pd.ExcelWriter(out_file, engine="openpyxl") as xw:
        for sheet, tdf in tables.items():
            tdf.to_excel(xw, sheet_name=sheet, index=False)

def main():
    ensure_dirs()
    df = clean_columns(load_data(DATA_PATH))
    tables = {
        "dist_departamento": dist_departamento(df),
        "top5_municipio": top5_municipio(df),
        "gasto_promedio_por_servicio": gasto_promedio_por_servicio(df),
        "pivot_municipio_x_punto": pivot_municipio_x_punto(df),
    }
    export_excel(tables, OUT_FILE)
    print(f"[OK] Entregable: {os.path.abspath(OUT_FILE)}")

if __name__ == "__main__":
    main()
