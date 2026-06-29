import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Paleta tech / dark blue ---
BG_DARK   = "#0d1117"
BG_PANEL  = "#161b27"
GRID_CLR  = "#1e2a3a"
TEXT_CLR  = "#cdd9e5"
ACCENT    = "#58a6ff"
BLUE_GRAD = ["#1565C0", "#1976D2", "#42A5F5", "#90CAF9"]  # degradado para donut

plt.rcParams.update({
    "figure.facecolor":  BG_DARK,
    "axes.facecolor":    BG_PANEL,
    "axes.edgecolor":    GRID_CLR,
    "axes.labelcolor":   TEXT_CLR,
    "xtick.color":       TEXT_CLR,
    "ytick.color":       TEXT_CLR,
    "text.color":        TEXT_CLR,
    "grid.color":        GRID_CLR,
    "grid.linestyle":    "--",
    "grid.linewidth":    0.5,
    "font.family":       "DejaVu Sans",
})

# --- Carga y preparación de datos ---
df = pd.read_csv("ventas.csv")
df["fecha"] = pd.to_datetime(df["fecha"])
df["venta_total"] = df["unidades_vendidas"] * df["precio_unitario"]
df["mes"] = df["fecha"].dt.to_period("M")

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle("Dashboard de Ventas Retail México — 1er Semestre 2024",
             fontsize=15, fontweight="bold", color=TEXT_CLR, y=1.01)
plt.subplots_adjust(hspace=0.50, wspace=0.38)

# --- Gráfica 1: Ventas totales por categoría (barras delgadas, valores en $K) ---
ax1 = axes[0, 0]
ventas_cat = df.groupby("categoria")["venta_total"].sum().sort_values(ascending=False)
ventas_cat_k = ventas_cat / 1000
bars = ax1.bar(ventas_cat.index, ventas_cat_k.values, width=0.4, color=ACCENT,
               edgecolor=BG_DARK, linewidth=0.8)
ax1.set_title("Ventas Totales por Categoría", fontweight="bold", color=TEXT_CLR, pad=10)
ax1.set_xlabel("Categoría", labelpad=6)
ax1.set_ylabel("Ventas ($K MXN)", labelpad=6)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax1.yaxis.grid(True)
ax1.set_axisbelow(True)
for bar, val in zip(bars, ventas_cat_k.values):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
             f"${val:.1f}K", ha="center", va="bottom", fontsize=8.5, color=TEXT_CLR)

# --- Gráfica 2: Tendencia de ventas por mes (línea leaner, valores en $K) ---
ax2 = axes[0, 1]
ventas_mes = df.groupby("mes")["venta_total"].sum()
ventas_mes_k = ventas_mes / 1000
meses_label = [str(m) for m in ventas_mes.index]
ax2.plot(meses_label, ventas_mes_k.values, marker="o", color=ACCENT,
         linewidth=2, markersize=5, markerfacecolor=BG_DARK, markeredgewidth=2)
ax2.fill_between(meses_label, ventas_mes_k.values, alpha=0.12, color=ACCENT)
ax2.set_title("Tendencia de Ventas por Mes", fontweight="bold", color=TEXT_CLR, pad=10)
ax2.set_xlabel("Mes", labelpad=6)
ax2.set_ylabel("Ventas ($K MXN)", labelpad=6)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax2.tick_params(axis="x", rotation=30, labelsize=8)
ax2.yaxis.grid(True)
ax2.set_axisbelow(True)
for x, y in zip(meses_label, ventas_mes_k.values):
    ax2.text(x, y + 0.25, f"${y:.1f}K", ha="center", va="bottom", fontsize=8, color=TEXT_CLR)

# --- Gráfica 3: Ventas por estado (barras horizontales, valores en $K) ---
ax3 = axes[1, 0]
ventas_estado = df.groupby("estado")["venta_total"].sum().sort_values()
ventas_estado_k = ventas_estado / 1000
ax3.barh(ventas_estado.index, ventas_estado_k.values, height=0.55,
         color=ACCENT, edgecolor=BG_DARK, linewidth=0.8)
ax3.set_title("Ventas por Estado", fontweight="bold", color=TEXT_CLR, pad=10)
ax3.set_xlabel("Ventas ($K MXN)", labelpad=6)
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax3.xaxis.grid(True)
ax3.set_axisbelow(True)
for val, label in zip(ventas_estado_k.values, ventas_estado.index):
    ax3.text(val + 0.1, label, f"${val:.1f}K", va="center", fontsize=8, color=TEXT_CLR)
ax3.set_xlim(0, ventas_estado_k.max() * 1.22)

# --- Gráfica 4: Donut chart en azules degradados ---
ax4 = axes[1, 1]
ventas_donut = df.groupby("categoria")["venta_total"].sum()
wedges, texts, autotexts = ax4.pie(
    ventas_donut.values,
    labels=ventas_donut.index,
    autopct="%1.1f%%",
    colors=BLUE_GRAD,
    startangle=140,
    pctdistance=0.78,
    wedgeprops=dict(width=0.52, edgecolor=BG_DARK, linewidth=2),
)
for t in texts:
    t.set_color(TEXT_CLR)
    t.set_fontsize(9.5)
for at in autotexts:
    at.set_color(BG_DARK)
    at.set_fontsize(9)
    at.set_fontweight("bold")
ax4.set_title("Participación por Categoría", fontweight="bold", color=TEXT_CLR, pad=10)

plt.savefig("dashboard.png", dpi=150, bbox_inches="tight", facecolor=BG_DARK)
print("Dashboard guardado como dashboard.png")
