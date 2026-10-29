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

def print_table_multivar(history):
    marq = bool(history) and "mu_k" in history[0]
    head = [f"{'k':>2}", f"{'x^k':^22}", f"{'f(x^k)':>9}", f"{'||grad||':>9}"]
    if marq:
        head += [f"{'mu_k':>9}", f"{'Попыток':>7}", f"{'d^k':^22}", f"{'x^(k+1)':^22}", f"{'f(x^(k+1))':>10}"]
    else:
        head += [f"{'d^k':^8}", f"{'t_k':>8}", f"{'x^(k+1)':^22}", f"{'||norm_x||':>8}",
                 f"{'|mod_fx|':>8}", f"{'Условия':^7}"]
    print(" | ".join(head))
    for row in history:
        xk = f"({row['x_k'][0]:.4f}; {row['x_k'][1]:.4f})"
        xk1 = f"({row['x_k1'][0]:.4f}; {row['x_k1'][1]:.4f})"
        cells = [f"{row['k']:>2}", f"{xk:^22}", f"{row['f_xk']:>9.4f}", f"{row['grad_norm']:>9.4f}"]
        if marq:
            dk = f"({row['d'][0]:.4f}; {row['d'][1]:.4f})"
            cells += [f"{row['mu_k']:>9.4f}", f"{row['trials']:>7}", f"{dk:^22}", f"{xk1:^22}",
                      f"{row['f_xk1']:>10.4f}"]
        else:
            ok = "да" if row["ok"] else "нет"
            cells += [f"{row.get('direction', ''):^8}", f"{row['t_k']:>8.4f}", f"{xk1:^22}",
                      f"{row['norm_x']:>8.4f}", f"{row['mod_fx']:>8.4f}", f"{ok:^7}"]
        print(" | ".join(cells))
