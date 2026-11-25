"""Análisis exploratorio de las inspecciones de seguridad alimentaria en Madrid (2018-2019).

Fuente: Civio Datos / Madrid Salud (Ayuntamiento de Madrid).
Uso:  python analisis.py
Genera un resumen por consola y las figuras en la carpeta figuras/.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA = Path(__file__).parent / "data" / "inspecciones_madrid.csv"
FIG_DIR = Path(__file__).parent / "figuras"
FIG_DIR.mkdir(exist_ok=True)

COL_ESTADO = "Estado higiénico sanitario"
COL_TIPO = "macroetiquetas"
COL_DISTRITO = "final_district"
COL_FECHA = "Fecha de la inspección"
COL_EPIGRAFE = "Epígrafe de actividad"

ORDEN_ESTADO = ["Favorable", "Favorable condicionado", "Desfavorable"]
COLORES_ESTADO = {"Favorable": "#2a9d8f", "Favorable condicionado": "#e9c46a", "Desfavorable": "#e76f51"}


def cargar() -> pd.DataFrame:
    df = pd.read_csv(DATA, encoding="utf-8")
    df[COL_FECHA] = pd.to_datetime(df[COL_FECHA], format="%d/%m/%Y", errors="coerce")
    return df


def resumen(df: pd.DataFrame) -> None:
    print("=" * 70)
    print("RESUMEN GENERAL")
    print("=" * 70)
    print(f"Número de filas:    {df.shape[0]:,}")
    print(f"Número de columnas: {df.shape[1]}")
    print(f"Rango de fechas:    {df[COL_FECHA].min():%d/%m/%Y} - {df[COL_FECHA].max():%d/%m/%Y}")
    print(f"Distritos:          {df[COL_DISTRITO].nunique()}")
    print(f"Epígrafes de actividad distintos: {df[COL_EPIGRAFE].nunique()}")

    print("\nValores nulos por columna (solo las que tienen):")
    nulos = df.isna().sum()
    print(nulos[nulos > 0].to_string())

    print("\n--- Variables numéricas (latitud / longitud) ---")
    print(df[["latitude", "longitude"]].describe().loc[["mean", "min", "max"]].round(4).to_string())

    print("\n--- Valores más frecuentes de las variables categóricas ---")
    for col in ["year", "Tipo de actuación", "Perfil de la actividad", COL_ESTADO,
                "Frecuencia de inspección", COL_TIPO, COL_DISTRITO, "mejora o empeora"]:
        vc = df[col].value_counts()
        print(f"\n{col}: {df[col].nunique()} valores distintos; moda = '{vc.index[0]}' ({vc.iloc[0]:,})")
        print((vc.head(5) / len(df) * 100).round(1).astype(str).add(" %").to_string())

    print("\n--- % de inspecciones desfavorables por tipo de establecimiento ---")
    print((pd.crosstab(df[COL_TIPO], df[COL_ESTADO], normalize="index") * 100).round(1).to_string())

    print("\n--- Distritos con mayor % de inspecciones desfavorables ---")
    pct = (df[COL_ESTADO] == "Desfavorable").groupby(df[COL_DISTRITO]).mean().mul(100).round(1)
    print(pct.sort_values(ascending=False).head(5).to_string())


def fig_estado(df):
    conteo = df[COL_ESTADO].value_counts().reindex(ORDEN_ESTADO)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(conteo.index, conteo.values, color=[COLORES_ESTADO[e] for e in conteo.index])
    for i, v in enumerate(conteo.values):
        ax.text(i, v, f"{v:,}\n({v / len(df):.0%})", ha="center", va="bottom")
    ax.set_title("Resultado de las inspecciones")
    ax.set_ylabel("Nº de inspecciones")
    ax.set_ylim(0, conteo.max() * 1.18)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "01_estado_higienico.png", dpi=120)
    plt.close(fig)


def fig_estado_por_tipo(df):
    tabla = pd.crosstab(df[COL_TIPO], df[COL_ESTADO], normalize="index")[ORDEN_ESTADO] * 100
    fig, ax = plt.subplots(figsize=(8, 4))
    tabla.plot(kind="barh", stacked=True, ax=ax, color=[COLORES_ESTADO[e] for e in ORDEN_ESTADO])
    ax.set_xlabel("% de inspecciones")
    ax.set_ylabel("")
    ax.set_title("Resultado según tipo de establecimiento")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "02_estado_por_tipo.png", dpi=120)
    plt.close(fig)


def fig_distritos(df):
    d = df[df[COL_DISTRITO].notna() & (df[COL_DISTRITO] != "Desconocido")]
    pct = (d[COL_ESTADO] == "Desfavorable").groupby(d[COL_DISTRITO]).mean().mul(100).sort_values()
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.barh(pct.index, pct.values, color="#e76f51")
    ax.axvline((df[COL_ESTADO] == "Desfavorable").mean() * 100, color="gray", ls="--", label="Media Madrid")
    ax.set_xlabel("% de inspecciones desfavorables")
    ax.set_title("Inspecciones desfavorables por distrito")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "03_desfavorables_por_distrito.png", dpi=120)
    plt.close(fig)


def fig_por_mes(df):
    serie = df.set_index(COL_FECHA).resample("MS").size()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(serie.index, serie.values, marker="o", color="#264653")
    ax.set_title("Inspecciones por mes")
    ax.set_ylabel("Nº de inspecciones")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "04_inspecciones_por_mes.png", dpi=120)
    plt.close(fig)


def fig_mapa(df):
    fig, ax = plt.subplots(figsize=(7, 7))
    for estado in ORDEN_ESTADO:
        sub = df[df[COL_ESTADO] == estado]
        ax.scatter(sub["longitude"], sub["latitude"], s=3, alpha=0.5, color=COLORES_ESTADO[estado], label=estado)
    ax.set_title("Ubicación de los establecimientos inspeccionados")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.legend(markerscale=4, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "05_mapa.png", dpi=120)
    plt.close(fig)


def fig_top_epigrafes(df):
    top = df[COL_EPIGRAFE].str.split(" - ", n=1).str[1].str.capitalize().value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh([t[:55] for t in top.index], top.values, color="#264653")
    ax.set_title("Las 10 actividades más inspeccionadas")
    ax.set_xlabel("Nº de inspecciones")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "06_top_actividades.png", dpi=120)
    plt.close(fig)

def calidad_datos() -> None:
    """Diagnostica faltantes y duplicados sin limpiar el dataset original."""
    # Comprobar duplicados antes de convertir fechas o normalizar blancos.
    original = pd.read_csv(DATA, encoding="utf-8")
    df = original.replace(r"^\s*$", pd.NA, regex=True)
    total = len(df)
    salida = DATA.parent.parent / "resultados"
    salida.mkdir(exist_ok=True)

    tabla = pd.DataFrame({
        "faltantes": df.isna().sum(),
        "porcentaje": (df.isna().mean().mul(100) if total else
                       pd.Series(0.0, index=df.columns)).round(2),
    }).sort_values("faltantes", ascending=False)
    tabla.index.name = "variable"
    tabla.to_csv(salida / "valores_faltantes.csv", encoding="utf-8")

    incompletas = int(df.isna().any(axis=1).sum())
    extras = int(original.duplicated().sum())
    implicadas = int(original.duplicated(keep=False).sum())
    fechas = pd.to_datetime(df[COL_FECHA], format="%d/%m/%Y", errors="coerce")
    invalidas = df[COL_FECHA].notna() & fechas.isna()
    sin_coordenadas = df[["latitude", "longitude"]].isna().any(axis=1)
    desconocidos = df[COL_DISTRITO].astype("string").str.strip().eq("Desconocido")

    metricas = {
        "filas": total,
        "columnas": len(df.columns),
        "filas_con_faltantes": incompletas,
        "copias_duplicadas_adicionales": extras,
        "filas_implicadas_en_duplicados": implicadas,
        "fechas_ausentes": int(df[COL_FECHA].isna().sum()),
        "fechas_no_interpretables": int(invalidas.sum()),
        "filas_sin_par_completo_de_coordenadas": int(sin_coordenadas.sum()),
        "distritos_desconocidos": int(desconocidos.sum()),
        "estados_ausentes": int(df[COL_ESTADO].isna().sum()),
    }
    pd.Series(metricas, name="cantidad").rename_axis("metrica").to_csv(
        salida / "resumen_calidad.csv", encoding="utf-8"
    )

    print("\n--- CALIDAD DE LOS DATOS ---")
    print(tabla.to_string())
    porcentaje = incompletas / total * 100 if total else 0.0
    print(f"\nFilas con algun faltante: {incompletas:,} ({porcentaje:.2f} %)")
    print(f"Copias repetidas adicionales: {extras:,}")
    print(f"Filas implicadas en duplicados: {implicadas:,}")
    print(f"Fechas ausentes: {metricas['fechas_ausentes']:,}")
    print(f"Fechas presentes no interpretables: {invalidas.sum():,}")
    print(f"Filas sin coordenadas completas: {sin_coordenadas.sum():,}")
    print(f"Distritos etiquetados como Desconocido: {desconocidos.sum():,}")

    con_faltantes = tabla[tabla["faltantes"] > 0]
    fig, ax = plt.subplots(figsize=(10, max(4, len(con_faltantes) * 0.4)))
    if not con_faltantes.empty:
        con_faltantes["porcentaje"].sort_values().plot.barh(ax=ax, color="#264653")
        ax.set_xlabel("Valores faltantes (%) sobre el total de filas")
        ax.set_ylabel("")
    else:
        ax.text(0.5, 0.5, "No se detectaron valores faltantes",
                ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
    ax.set_title("Valores faltantes por variable")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "07_valores_faltantes.png", dpi=120)
    plt.close(fig)
    print(f"Diagnostico guardado en {salida}")

if __name__ == "__main__":
    calidad_datos()
    datos = cargar()
    resumen(datos)
    for f in (fig_estado, fig_estado_por_tipo, fig_distritos, fig_por_mes, fig_mapa, fig_top_epigrafes):
        f(datos)
    print(f"\nFiguras guardadas en {FIG_DIR}")
