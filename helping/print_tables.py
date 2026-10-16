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
    # общая таблица для методов спуска; столбец d^k заполняется только в методе Ньютона
    # (в истории метода наискорейшего спуска ключа "direction" нет - столбец остаётся пустым)
    header = (f"{'k':>2} | {'x^k':^22} | {'f(x^k)':>9} | {'||grad||':>9} | {'d^k':^8} | {'t_k':>8} | "
              f"{'x^(k+1)':^22} | {'||norm_x||':>8} | {'|mod_fx|':>8} | {'Условия':^7}")
    print(header)
    for row in history:
        xk = f"({row['x_k'][0]:.4f}; {row['x_k'][1]:.4f})"
        xk1 = f"({row['x_k1'][0]:.4f}; {row['x_k1'][1]:.4f})"
        ok = "да" if row["ok"] else "нет"
        direction = row.get("direction", "")
        print(f"{row['k']:>2} | {xk:^22} | {row['f_xk']:>9.4f} | {row['grad_norm']:>9.4f} | "
              f"{direction:^8} | {row['t_k']:>8.4f} | {xk1:^22} | {row['norm_x']:>8.4f} | "
              f"{row['mod_fx']:>8.4f} | {ok:^7}")