def print_summary_table(history):
    header = (f"{'k':>2} | {'[a_k; b_k]':^20} | {'y_k':>8} | {'f(y_k)':>8} | "
              f"{'z_k':>8} | {'f(z_k)':>8} | {'Случай':^6} | {'Новый интервал':^20} | "
              f"{'Delta':>7}")
    print(header)
    for row in history:
        interval = f"[{row['a_k']:.4f}; {row['b_k']:.4f}]"
        new_interval = f"[{row['a_k1']:.4f}; {row['b_k1']:.4f}]"
        print(f"{row['k']:>2} | {interval:^20} | {row['y_k']:>8.4f} | {row['f_yk']:>8.4f} | "
              f"{row['z_k']:>8.4f} | {row['f_zk']:>8.4f} | {row['case']:^6} | "
              f"{new_interval:^20} | {row['delta']:>7.4f}")

def print_descent_table(history):
    headers = ["k", "x^k", "f(x^k)", "||grad||", "t_k", "x^(k+1)", "||norm_x||", "|mod_fx|", "Условия"]
    rows = []
    for row in history:
        rows.append([
            str(row["k"]),
            f"({row['x_k'][0]:8.4f}; {row['x_k'][1]:8.4f})",
            f"{row['f_xk']:.4f}",
            f"{row['grad_norm']:.4f}",
            f"{row['t_k']:.4f}",
            f"({row['x_k1'][0]:8.4f}; {row['x_k1'][1]:8.4f})",
            f"{row['norm_x']:.4f}",
            f"{row['mod_fx']:.4f}",
            "да" if row["ok"] else "нет",
        ])
    # ширина каждого столбца = самая длинная строка в нём (заголовок или значение)
    widths = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
    print(" | ".join(h.center(w) for h, w in zip(headers, widths)))
    for r in rows:
        # числа и координаты - по правому краю, "да/нет" - по центру
        print(" | ".join(c.center(w) if i == len(r) - 1 else c.rjust(w)
                         for i, (c, w) in enumerate(zip(r, widths))))
