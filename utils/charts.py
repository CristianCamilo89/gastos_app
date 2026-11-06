"""Generación de gráficas con matplotlib (backend Agg -> imagen PNG)."""


def build_category_chart(data, path: str, title: str) -> bool:
    """
    Dibuja un gráfico de barras horizontales con los gastos por categoría
    y lo guarda como PNG en `path`.

    data: lista de tuplas (categoria, total)
    Devuelve True si se generó la imagen; False si matplotlib no está disponible
    (la pantalla usará entonces una gráfica nativa de Kivy).
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # backend sin ventana: genera imágenes
        import matplotlib.pyplot as plt
    except Exception:
        return False

    labels = [c for c, _ in data][::-1]
    values = [v for _, v in data][::-1]

    fig, ax = plt.subplots(figsize=(5, 4.5), dpi=110)
    bars = ax.barh(labels, values, color="#2563EB")
    ax.set_title(title)
    ax.set_xlabel("Monto")
    for bar, val in zip(bars, values):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f" {val:,.0f}", va="center", fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return True
