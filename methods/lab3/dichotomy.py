from helping.log import make_logger
from helping.types import IntervalResult

def dichotomy_method(f, a0, b0, l, eps=None, verbose = False):
    log = make_logger(verbose)

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

    # шаг 1
    a, b = a0, b0
    log("Метод дихотомии - подробное решение\n")
    log("Шаг 1. Задаём:")
    log(f"L0 = [a0; b0] = [{a0}; {b0}]")
    log(f"eps = {eps}")
    log(f"l = {l}")

    # шаг 2
    k = 0
    log(f"\nШаг 2. Положим k = 0.")

    history = []

    while True:
        # шаг 3
        y = (a + b - eps) / 2
        z = (a + b + eps) / 2
        fy = f(y)
        fz = f(z)

        log(f"\nШаг 3 (итерация k = {k}). Текущий интервал: [a{k}; b{k}] = [{a}; {b}]")
        log(f"y{k} = (a{k} + b{k} - eps) / 2 = ({a} + {b} - {eps}) / 2 = {y}")
        log(f"f(y{k}) = {fy}")
        log(f"z{k} = (a{k} + b{k} + eps) / 2 = ({a} + {b} + {eps}) / 2 = {z}")
        log(f"f(z{k}) = {fz}")

        # шаг 4
        if fy < fz:
            case = "a"
            new_a, new_b = a, z
            log(f"\nШаг 4. f(y{k}) < f(z{k}) : {fy} < {fz}")
            log(f"=> a{k + 1} = a{k} = {new_a},  b{k + 1} = z{k} = {new_b}")
        elif fy > fz:
            case = "b"
            new_a, new_b = y, b
            log(f"\nШаг 4. f(y{k}) > f(z{k}): {fy} > {fz}")
            log(f"=> a{k + 1} = y{k} = {new_a},  b{k + 1} = b{k} = {new_b}")
        else:
            case = "c"
            # f(y_k) == f(z_k): минимум находится между y_k и z_k
            new_a, new_b = y, z
            log(f"\nШаг 4. f(y{k}) = f(z{k}): {fy} = {fz}")
            log(f"=> a{k + 1} = y{k} = {new_a},  b{k + 1} = z{k} = {new_b}")

        a, b = new_a, new_b
        delta = abs(b - a)

        history.append({
            "k": k,
            "a_k": history[-1]["a_k1"] if history else a0,
            "b_k": history[-1]["b_k1"] if history else b0,
            "y_k": y,
            "f_yk": fy,
            "z_k": z,
            "f_zk": fz,
            "case": case,
            "a_k1": a,
            "b_k1": b,
            "delta": delta,
        })

        # шаг 5
        log(f"\nШаг 5. |L_{2 * (k + 1)}| = |b{k + 1} - a{k + 1}| = |{b} - {a}| = {delta}")

        if delta < l:
            log(f"{delta} < l = {l} - алгоритм завершён.")
            x_res = (a + b) / 2
            log(f"\nx* принадлежит [{a}; {b}]")
            log(f"x* = (a{k + 1} + b{k + 1}) / 2 = ({a} + {b}) / 2 = {x_res}")
            break
        else:
            log(f"{delta} >= l = {l} - полагаем k = {k + 1} и переходим к шагу 3.")
            k += 1

    x_res = (a + b) / 2
    return IntervalResult(
        a=a, b=b, x=x_res,
        n_evals=2 * (k + 1),
        history=history,
        extra={
            "R_fact": abs(b - a) / abs(b0 - a0),
               },
    )
