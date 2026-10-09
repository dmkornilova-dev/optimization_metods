from math import sqrt
from helping.log import make_logger
from helping.types import IntervalResult

def golden_section_method(f, a0, b0, l, eps = None, verbose = False):

    if l <= 0:
        raise ValueError("l должно быть положительным числом")
    if a0 >= b0:
        raise ValueError("Должно выполняться a0 < b0")

    log = make_logger(verbose)

    # шаг 1
    a, b = a0, b0
    log("Метод золотого сечения - подробное решение\n")
    log("Шаг 1. Задаём:")
    log(f"L0 = [a0; b0] = [{a0}; {b0}]")
    log(f"l = {l}")

    # шаг 2
    k = 0
    log("\nШаг 2. Положим k = 0.")

    # шаг 3
    coef = (3 - sqrt(5)) / 2  # 0.38196...
    y = a + coef * (b - a)
    z = a + b - y
    log(f"\nШаг 3. y0 = a0 + (3 - sqrt(5)) / 2 * (b0 - a0) = {a0} + {coef:.6f} * ({b0} - ({a0})) = {y:.6f}")
    log(f"z0 = a0 + b0 - y0 = {a0} + {b0} - ({y:.6f}) = {z:.6f}")

    fy, fz = None, None  # значения функции в y_k, z_k (None - ещё не вычислено)
    N = 0 # общее число вычислений функции
    history = []

    while True:
        # шаг 4: вычисляем только те значения, которых ещё нет
        log(f"\nШаг 4 (итерация k = {k}). Текущий интервал: [a{k}; b{k}] = [{a:.6f}; {b:.6f}]")
        if fy is None:
            fy = f(y)
            N += 1
            log(f"f(y{k}) = f({y:.6f}) = {fy:.6f}")
        else:
            log(f"f(y{k}) = f({y:.6f}) = {fy:.6f} (уже вычислено)")
        if fz is None:
            fz = f(z)
            N += 1
            log(f"f(z{k}) = f({z:.6f}) = {fz:.6f}")
        else:
            log(f"f(z{k}) = f({z:.6f}) = {fz:.6f} (уже вычислено)")

        # шаг 5
        if fy <= fz:
            case = "a"
            new_a, new_b = a, z
            new_y = new_a + new_b - y
            new_z = y
            new_fy, new_fz = None, fy
            log(f"\nШаг 5. f(y{k}) <= f(z{k}): {fy:.6f} <= {fz:.6f} => случай a)")
            log(f"a{k + 1} = a{k} = {new_a:.6f},")
            log(f"b{k + 1} = z{k} = {new_b:.6f},")
            log(f"y{k + 1} = a{k + 1} + b{k + 1} - y{k} = {new_y:.6f},")
            log(f"z{k + 1} = y{k} = {new_z:.6f}")
        else:
            case = "b"
            new_a, new_b = y, b
            new_y = z
            new_z = new_a + new_b - z
            new_fy, new_fz = fz, None
            log(f"\nШаг 5. f(y{k}) > f(z{k}): {fy:.4f} > {fz:.4f} => случай b)")
            log(f"a{k + 1} = y{k} = {new_a:.6f},")
            log(f"b{k + 1} = b{k} = {new_b:.6f},")
            log(f"y{k + 1} = z{k} = {new_y:.6f}, ")
            log(f"z{k + 1} = a{k + 1} + b{k + 1} - z{k} = {new_z:.6f}")

        #шаг 6
        delta = abs(new_a - new_b)

        history.append({
            "k": k,
            "a_k": a,
            "b_k": b,
            "y_k": y,
            "f_yk": fy,
            "z_k": z,
            "f_zk": fz,
            "case": case,
            "a_k1": new_a,
            "b_k1": new_b,
            "delta": delta
        })

        a, b = new_a, new_b
        y, z = new_y, new_z
        fy, fz = new_fy, new_fz

        log(f"\nШаг 6. Delta = |a{k + 1} - b{k + 1}| = |{a:.6f} - ({b:.6f})| = {delta:.6f}")

        if delta <= l:
            log(f"{delta:.6f} <= l = {l} - алгоритм завершён.")
            x_res = (a + b) / 2
            log(f"\nx* принадлежит [{a:.6f}; {b:.6f}]")
            log(f"x* = (a{k + 1} + b{k + 1}) / 2 = ({a:.6f} + {b:.6f}) / 2 = {x_res:.6f}")
            break
        else:
            log(f"{delta:.6f} > l = {l} - полагаем k = {k + 1} и переходим к шагу 4.")
            k += 1

    x_res = (a + b) / 2

    # сходимость
    R = ((sqrt(5)-1)/2.0) ** (N - 1)
    log("\nСходимость:")
    log(f"N = {N} - количество вычислений функции")
    log(f"R(N) = 0.618^(N-1) = 0.618^{N - 1} = {R:.6f}")
    log(f"Проверка: (b - a) / (b0 - a0) = {delta:.4f} / {b0 - a0} = {delta / (b0 - a0):.6f}\n")

    return IntervalResult(
        a=a, b=b, x=x_res,
        n_evals=N,
        history=history,
        extra={
            "R": R,
            "R_fact": abs(b-a) / abs(b0-a0)},
    )