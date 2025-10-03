# Quiz práctico — VS Code (GitHub Codespaces) → Entregable en Excel

**Objetivo:** Seguir instrucciones, cargar una base de datos pequeña, hacer cálculos básicos y **exportar un Excel** con varias hojas como entregable.

## Pasos (en Codespaces)
1) Crear y activar entorno:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2) Abrir `quiz.py` y completar los **TODO**.
3) Ejecutar:
```bash
python quiz.py
```
4) Verifica `reports/quiz_result.xlsx` y súbelo en tu PR.

## Lo que debes lograr
- Cargar `data/raw/encuestas_demo.csv`.
- Estandarizar nombres de columnas (minúsculas y `_`).
- Generar 4 tablas:
  - `dist_departamento`: conteo por `departamento` (desc).
  - `top5_municipio`: top 5 por `municipio` (desc).
  - `gasto_promedio_por_servicio`: promedio de `gasto_estimado` por `servicio` (desc).
  - `pivot_municipio_x_punto`: conteos `municipio` × `punto_atencion`.
- Exportar un Excel con **4 hojas** (una por tabla) en `reports/quiz_result.xlsx`.