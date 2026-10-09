from helping.log import make_logger
from helping.types import IntervalResult

def fibonacci_method(f, a0, b0, l, eps=None, verbose = False):

    if eps is None:
        raise ValueError("Нужно задать eps")
    if eps <= 0:
        raise ValueError("eps должно быть положительным числом")
    if l <= 0:
        raise ValueError("l должно быть положительным числом")
    if eps >= l:
        raise ValueError("Должно выполняться 0 < eps < l")
    if a0 >= b0:
        raise ValueError("Должно выполняться a0 < b0")

    log = make_logger(verbose)

    # шаг 1
    a, b = a0, b0
    log("Метод Фибоначчи - подробное решение\n")
    log("Шаг 1. Задаём:")
    log(f"L0 = [a0; b0] = [{a0}; {b0}]")
    log(f"l = {l}")
    log(f"eps = {eps}")

    # шаг 2
    F = [1, 1]  # F0 = F1 = 1
    N = 1
    while F[N] < (b0 - a0) / l:
        F.append(F[-1] + F[-2])
        N += 1
    if N < 3:
        raise ValueError("Требуется N >= 3 (уменьшите l)")
    log(f"\nШаг 2. Находим наименьшее N, при котором F_N >= |L0| / l = {b0 - a0} / {l} = {(b0 - a0) / l:.6f}")
    log(f"Числа Фибоначчи: {', '.join(f'F{i} = {F[i]}' for i in range(N + 1))}")
    log(f"F{N} = {F[N]} >= {(b0 - a0) / l:.6f} => N = {N} вычислений функции")

    # шаг 3
    k = 0
    log("\nШаг 3. Положим k = 0.")

    # шаг 4
    y = a + F[N - 2] / F[N] * (b - a)
    z = a + F[N - 1] / F[N] * (b - a)
    log(f"\nШаг 4. y0 = a0 + F{N - 2} / F{N} * (b0 - a0) = {a0} + {F[N - 2]} / {F[N]} * ({b0} - ({a0})) = {y:.6f}")
    log(f"z0 = a0 + F{N - 1} / F{N} * (b0 - a0) = {a0} + {F[N - 1]} / {F[N]} * ({b0} - ({a0})) = {z:.6f}")

    fy, fz = None, None  # значения функции в y_k, z_k
    n_eval = 0  # общее число вычислений функции
    history = []

    while True:
        # шаг 5: вычисляем только те значения, которых ещё нет
        log(f"\nШаг 5 (итерация k = {k}). Текущий интервал: [a{k}; b{k}] = [{a:.6f}; {b:.6f}]")
        if fy is None:
            fy = f(y)
            n_eval += 1
            log(f"f(y{k}) = f({y:.6f}) = {fy:.6f}")
        else:
            log(f"f(y{k}) = f({y:.6f}) = {fy:.6f} (уже вычислено)")
        if fz is None:
            fz = f(z)
            n_eval += 1
            log(f"f(z{k}) = f({z:.6f}) = {fz:.6f}")
        else:
            log(f"f(z{k}) = f({z:.6f}) = {fz:.6f} (уже вычислено)")

        # шаг 6
        if fy <= fz:
            case = "a"
            new_a, new_b = a, z
            new_y = new_a + F[N - k - 3] / F[N - k - 1] * (new_b - new_a)
            new_z = y
            new_fy, new_fz = None, fy
            log(f"\nШаг 6. f(y{k}) <= f(z{k}): {fy:.6f} <= {fz:.6f} => случай a)")
            log(f"a{k + 1} = a{k} = {new_a:.6f},")
            log(f"b{k + 1} = z{k} = {new_b:.6f},")
            log(f"y{k + 1} = a{k + 1} + F{N - k - 3} / F{N - k - 1} * (b{k + 1} - a{k + 1}) = {new_y:.6f},")
            log(f"z{k + 1} = y{k} = {new_z:.6f}")
        else:
            case = "b"
            new_a, new_b = y, b
            new_y = z
            new_z = new_a + F[N - k - 2] / F[N - k - 1] * (new_b - new_a)
            new_fy, new_fz = fz, None
            log(f"\nШаг 6. f(y{k}) > f(z{k}): {fy:.6f} > {fz:.6f} => случай b)")
            log(f"a{k + 1} = y{k} = {new_a:.6f},")
            log(f"b{k + 1} = b{k} = {new_b:.6f},")
            log(f"y{k + 1} = z{k} = {new_y:.6f},")
            log(f"z{k + 1} = a{k + 1} + F{N - k - 2} / F{N - k - 1} * (b{k + 1} - a{k + 1}) = {new_z:.6f}")

        history.append({
            "k": str(k),
            "a_k": a,
            "b_k": b,
            "y_k": y,
            "f_yk": fy,
            "z_k": z,
            "f_zk": fz,
            "case": case,
            "a_k1": new_a,
            "b_k1": new_b,
            "delta": abs(new_b - new_a),
        })

        a, b = new_a, new_b
        y, z = new_y, new_z
        fy, fz = new_fy, new_fz

        # шаг 7
        if k != N - 3:
            log(f"\nШаг 7. k = {k} != N - 3 = {N} - 3 = {N - 3} => положим k = {k + 1} и переходим к шагу 5.")
            k += 1
            continue

        log(f"\nШаг 7. k = N - 3 = {N} - 3 = {N - 3} => отсутствует точка нового вычисления функции")
        break

    # шаг 7 (б)
    y_last = (a + b) / 2
    f_y_last = fy if fy is not None else fz  # значение в этой точке уже вычислено
    z_last = y_last + eps
    f_z_last = f(z_last)
    n_eval += 1

    log(f"y{N - 2} = z{N - 2} = (a{N - 2} + b{N - 2}) / 2 = ({a:.6f} + ({b:.6f})) / 2 = {y_last:.6f}")
    log(f"y{N - 1} = y{N - 2} = z{N - 2} = {y_last:.6f},")
    log(f"z{N - 1} = y{N - 1} + eps = {y_last:.6f} + {eps} = {z_last:.6f}")
    log(f"f(y{N - 1}) = {f_y_last:.6f} (уже вычислено)")
    log(f"f(z{N - 1}) = {f_z_last:.6f}")

    if f_y_last <= f_z_last:
        case = "a"
        new_a, new_b = a, z_last
        log(f"f(y{N - 1}) <= f(z{N - 1}): {f_y_last:.6f} <= {f_z_last:.6f} => "
            f"a{N - 1} = a{N - 2} = {new_a:.6f}, b{N - 1} = z{N - 1} = {new_b:.6f}")
    else:
        case = "b"
        new_a, new_b = y_last, b
        log(f"f(y{N - 1}) > f(z{N - 1}): {f_y_last:.6f} > {f_z_last:.6f} => "
            f"a{N - 1} = y{N - 1} = {new_a:.6f}, b{N - 1} = b{N - 2} = {new_b:.6f}")

    history.append({
        "k": N-1,
        "a_k": a,
        "b_k": b,
        "y_k": y_last,
        "f_yk": f_y_last,
        "z_k": z_last,
        "f_zk": f_z_last,
        "case": case,
        "a_k1": new_a,
        "b_k1": new_b,
        "delta": abs(new_b - new_a),
    })

    a, b = new_a, new_b
    delta = abs(b - a)
    x_res = (a + b) / 2

    log(f"\nАлгоритм завершён.")
    log(f"x* принадлежит [{a:.6f}; {b:.6f}]")
    log(f"Длина конечного интервала: {delta:.6f}")
    log(f"x* = (a{N - 1} + b{N - 1}) / 2 = ({a:.6f} + ({b:.6f})) / 2 = {x_res:.6f}")

    # сходимость
    R = 1 / F[N]
    log("\nСходимость:")
    log(f"N = {n_eval} - количество вычислений функции")
    log(f"R(N) = 1 / F{N} = 1 / {F[N]} = {R:.6f}")
    log(f"Проверка: (b - a) / (b0 - a0) = {delta:.6f} / {b0 - a0} = {delta / (b0 - a0):.6f}")
    if abs(delta - R * (b0 - a0)) <= eps:
        log(f"Разница между предполагаемой и фактической длиной "
            f"итогового отрезка не более eps = {eps:.4f}\n")
        r = True
    else:
        log(f"Разница между предполагаемой и фактической длиной "
            f"итогового отрезка БОЛЬШЕ eps = {eps:.4f}\n")
        r = False

    return IntervalResult(
        a=a, b=b, x=x_res,
        n_evals=n_eval,
        history=history,
        extra={
            "F_N": F[N],
            "R": R,
            "R_fact": abs(b-a) / abs(b0-a0),
            "R_ok": r},
    )