import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Carga y preparación de datos ---
df = pd.read_csv("ventas.csv")
df["fecha"] = pd.to_datetime(df["fecha"])
df["venta_total"] = df["unidades_vendidas"] * df["precio_unitario"]
df["mes"] = df["fecha"].dt.to_period("M")

COLORES = ["#2196F3", "#FF5722", "#4CAF50", "#FFC107"]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Dashboard de Ventas Retail México — 1er Semestre 2024", fontsize=16, fontweight="bold", y=1.01)
plt.subplots_adjust(hspace=0.45, wspace=0.35)

# --- Gráfica 1: Ventas totales por categoría (barras verticales) ---
ax1 = axes[0, 0]
ventas_cat = df.groupby("categoria")["venta_total"].sum().sort_values(ascending=False)
bars = ax1.bar(ventas_cat.index, ventas_cat.values, color=COLORES)
ax1.set_title("Ventas Totales por Categoría", fontweight="bold")
ax1.set_xlabel("Categoría")
ax1.set_ylabel("Ventas (MXN)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
             f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9)

# --- Gráfica 2: Tendencia de ventas por mes (línea) ---
ax2 = axes[0, 1]
ventas_mes = df.groupby("mes")["venta_total"].sum()
meses_label = [str(m) for m in ventas_mes.index]
ax2.plot(meses_label, ventas_mes.values, marker="o", color="#2196F3", linewidth=2.5, markersize=7)
ax2.fill_between(meses_label, ventas_mes.values, alpha=0.15, color="#2196F3")
ax2.set_title("Tendencia de Ventas por Mes", fontweight="bold")
ax2.set_xlabel("Mes")
ax2.set_ylabel("Ventas (MXN)")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax2.tick_params(axis="x", rotation=30)
for x, y in zip(meses_label, ventas_mes.values):
    ax2.text(x, y + 150, f"${y:,.0f}", ha="center", va="bottom", fontsize=8)

# --- Gráfica 3: Ventas por estado (barras horizontales) ---
ax3 = axes[1, 0]
ventas_estado = df.groupby("estado")["venta_total"].sum().sort_values()
ax3.barh(ventas_estado.index, ventas_estado.values, color="#4CAF50")
ax3.set_title("Ventas por Estado", fontweight="bold")
ax3.set_xlabel("Ventas (MXN)")
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for i, (val, label) in enumerate(zip(ventas_estado.values, ventas_estado.index)):
    ax3.text(val + 100, i, f"${val:,.0f}", va="center", fontsize=8)
ax3.set_xlim(0, ventas_estado.max() * 1.22)

# --- Gráfica 4: Participación por categoría (pie chart) ---
ax4 = axes[1, 1]
ventas_pie = df.groupby("categoria")["venta_total"].sum()
wedges, texts, autotexts = ax4.pie(
    ventas_pie.values,
    labels=ventas_pie.index,
    autopct="%1.1f%%",
    colors=COLORES,
    startangle=140,
    pctdistance=0.78,
)
for text in autotexts:
    text.set_fontsize(10)
    text.set_fontweight("bold")
ax4.set_title("Participación por Categoría", fontweight="bold")

plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
print("Dashboard guardado como dashboard.png")
