import numpy as np


def get_path(res):
    # все пройденные точки x^0, x^1, ..., x^n по истории метода
    if not res.history:
        return [list(res.x)]  # остановка на шаге 4 сразу в x^0
    return [list(res.history[0]["x_k"])] + [list(h["x_k1"]) for h in res.history]


def plot_path(f, res, title="Путь метода", x_min=None, label_points=True,
              save_path=None, show=True):
    import matplotlib.pyplot as plt

    path = np.array(get_path(res), dtype=float)
    pts = path if x_min is None else np.vstack([path, np.array(x_min, dtype=float)])
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    pad = 0.25 * max((hi - lo).max(), 1e-6)

    xs = np.linspace(lo[0] - pad, hi[0] + pad, 400)
    ys = np.linspace(lo[1] - pad, hi[1] + pad, 400)
    X1, X2 = np.meshgrid(xs, ys)
    Z = f(X1, X2)
    zmin, zmax = Z.min(), Z.max()
    levels = zmin + (zmax - zmin) * np.geomspace(1e-3, 1, 16)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.contour(X1, X2, Z, levels=levels, cmap="Blues_r", linewidths=0.9)

    # стрелки между последовательными точками
    for p, q in zip(path[:-1], path[1:]):
        ax.annotate("", xy=q, xytext=p,
                    arrowprops=dict(arrowstyle="->", color="tab:orange", lw=1.6))
    ax.plot(path[:, 0], path[:, 1], "o", color="tab:orange", ms=5, zorder=3)

    if label_points and len(path) <= 30:
        for i, p in enumerate(path):
            ax.annotate(f"$x^{{({i})}}$", p, textcoords="offset points",
                        xytext=(6, 6), fontsize=10)

    ax.plot(*path[0], "s", color="tab:green", ms=8, zorder=4, label="старт $x^{(0)}$")
    ax.plot(*path[-1], "D", color="tab:red", ms=7, zorder=4, label="найденная точка $x^*$")
    if x_min is not None:
        ax.plot(*x_min, "*", color="black", ms=13, zorder=5, label="аналитический минимум")

    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title(title)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig, ax


def plot_paths_compare(f, results, title="Сравнение методов поиска шага", x_min=None,
                       save_path=None, show=True):
    """Пути нескольких запусков (dict {имя: res}) на одном графике + увеличенный фрагмент
    вокруг финальных точек."""
    import matplotlib.pyplot as plt

    paths = {name: np.array(get_path(res), dtype=float) for name, res in results.items()}
    styles = [("o", "tab:blue", 12), ("s", "tab:orange", 8), ("^", "tab:green", 5)]

    all_pts = np.vstack(list(paths.values()) + ([np.array([x_min], dtype=float)] if x_min is not None else []))
    lo, hi = all_pts.min(axis=0), all_pts.max(axis=0)
    pad = 0.25 * max((hi - lo).max(), 1e-6)
    xs = np.linspace(lo[0] - pad, hi[0] + pad, 400)
    ys = np.linspace(lo[1] - pad, hi[1] + pad, 400)
    X1, X2 = np.meshgrid(xs, ys)
    Z = f(X1, X2)
    levels = Z.min() + (Z.max() - Z.min()) * np.geomspace(1e-3, 1, 16)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # слева: общий вид
    ax1.contour(X1, X2, Z, levels=levels, cmap="Blues_r", linewidths=0.9)
    for (name, path), (mk, color, ms) in zip(paths.items(), styles):
        ax1.plot(path[:, 0], path[:, 1], "-", color=color, lw=1.2, alpha=0.7)
        ax1.plot(path[:, 0], path[:, 1], mk, color=color, ms=ms, mfc="none",
                 mew=1.6, label=name, zorder=3)
    first = next(iter(paths.values()))[0]
    ax1.plot(*first, "k*", ms=12, zorder=5, label="старт $x^{(0)}$")
    if x_min is not None:
        ax1.plot(*x_min, "r*", ms=13, zorder=5, label="аналитический минимум")
    ax1.set_xlabel("$x_1$")
    ax1.set_ylabel("$x_2$")
    ax1.set_title(title)
    ax1.set_aspect("equal", adjustable="box")
    ax1.legend(fontsize=9)

    # справа: увеличение вокруг финальных точек
    finals = np.array([p[-1] for p in paths.values()])
    center = np.array(x_min, dtype=float) if x_min is not None else finals.mean(axis=0)
    ref = np.vstack([finals, center])
    r = 1.5 * np.abs(ref - center).max()
    r = max(r, 1e-9)
    ax2.set_xlim(center[0] - r, center[0] + r)
    ax2.set_ylim(center[1] - r, center[1] + r)
    xl, yl = ax2.get_xlim(), ax2.get_ylim()

    # точки для проекций: найденные точки методов + аналитический минимум
    marks = [(name, path[-1], mk, color, ms + 2)
             for (name, path), (mk, color, ms) in zip(paths.items(), styles)]
    if x_min is not None:
        marks.append(("аналитический минимум", np.array(x_min, dtype=float), "*", "red", 14))
    for name, p, mk, color, ms in marks:
        # проекции на оси (пунктир) и маркеры на самих осях
        ax2.plot([p[0], p[0]], [yl[0], p[1]], "--", color=color, lw=1, alpha=0.8)
        ax2.plot([xl[0], p[0]], [p[1], p[1]], "--", color=color, lw=1, alpha=0.8)
        ax2.plot(p[0], yl[0], mk, color=color, ms=5, clip_on=False, zorder=6)
        ax2.plot(xl[0], p[1], mk, color=color, ms=5, clip_on=False, zorder=6)
        ax2.plot(*p, mk, color=color, ms=ms, mfc="none", mew=1.8, zorder=5,
                 label=f"{name} ({p[0]:.6f}; {p[1]:.6f})")
    ax2.set_xlabel("$x_1$")
    ax2.set_ylabel("$x_2$")
    ax2.set_title("Увеличение вокруг найденных точек")
    ax2.ticklabel_format(useOffset=False)
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=8)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig, (ax1, ax2)