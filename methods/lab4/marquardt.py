from math import sqrt
from helping.log import make_logger
from helping.types import MultivarResult


def marquardt_method(f, grad, hess, x0, eps1, M, mu0, verbose=False):
    # метод Марквардта: d_k = -(H(x^k) + mu_k * E)^-1 * grad f(x^k), x^{k+1} = x^k + d^k.
    # Линейный поиск шага не нужен: длину шага регулирует параметр mu_k
    # (если f не уменьшилась - mu_k удваивается, если уменьшилась - mu_{k+1} = mu_k / 2).
    if eps1 <= 0:
        raise ValueError("eps1 должно быть положительным числом")
    if M <= 0:
        raise ValueError("M должно быть положительным числом")
    if mu0 <= 0:
        raise ValueError("mu0 должно быть положительным числом")
    if len(x0) != 2:
        raise ValueError("Реализация рассчитана на функцию двух переменных")

    log = make_logger(verbose)

    # шаг 1
    x = list(x0)
    log("Метод Марквардта - подробное решение\n")
    log("Шаг 1. Задаём:")
    log(f"x0 = {x}")
    log(f"eps1 = {eps1}")
    log(f"M = {M}")

    # шаг 2
    k = 0
    mu = mu0
    log(f"\nШаг 2. Положим k = 0, mu0 = {mu0}.")

    fx = f(*x)  # для проверки f(x^{k+1}) < f(x^k) на шаге 11
    n_evals = 1  # f(x0)
    history = []

    while True:
        # шаг 3
        g = grad(*x)  # частные производные при данном x=(x1;x2)
        log(f"\nШаг 3 (итерация k = {k}). x{k} = {x}, f(x{k}) = {fx:.6f}")
        log(f"grad f(x{k}) = {g}")

        # шаг 4
        norm_g = sqrt(sum(gi ** 2 for gi in g))
        log(f"\nШаг 4. ||grad f(x{k})|| = {norm_g:.6f}")
        if norm_g <= eps1:
            reason = "step4"
            log(f"{norm_g:.6f} <= eps1 = {eps1} - алгоритм завершён, x* = x{k}.")
            break
        log(f"{norm_g:.6f} > eps1 = {eps1} - переходим к шагу 5.")

        # шаг 5
        if k >= M:
            reason = "step5"
            log(f"\nШаг 5. k = {k} >= M = {M} - алгоритм завершён, x* = x{k}.")
            break
        log(f"\nШаг 5. k = {k} < M = {M} - переходим к шагу 6.")

        # шаг 6 - матрица Гессе
        (h11, h12), (h21, h22) = hess(*x)
        log(f"\nШаг 6. H(x{k}) = [[{h11}, {h12}], [{h21}, {h22}]]")

        mu_k = mu  # mu_k на начале итерации (до возможных удвоений на шаге 13)
        trials = 0
        while True:
            trials += 1
            # шаг 7 - матрица H(x^k) + mu_k * E
            a11, a12, a21, a22 = h11 + mu, h12, h21, h22 + mu
            log(f"\nШаг 7 (попытка {trials}). mu{k} = {mu}, "
                f"H(x{k}) + mu{k}*E = [[{a11}, {a12}], [{a21}, {a22}]]")

            # шаг 8 - обратная матрица (H + mu*E)^-1 = 1/|A| * (A*)^T
            det = a11 * a22 - a12 * a21
            if det == 0:
                # обратной матрицы нет - увеличиваем mu (как на шаге 13) и повторяем шаг 7
                log(f"Шаг 8. |H + mu*E| = 0 - обратной матрицы не существует, mu{k} = 2*mu{k}.")
                mu *= 2
                continue
            inv = [[a22 / det, -a12 / det],
                   [-a21 / det, a11 / det]]
            log(f"Шаг 8. |H + mu*E| = {det}, (H + mu*E)^-1 = 1/{det} * [[{a22}, {-a12}], [{-a21}, {a11}]] = {inv}")

            # шаг 9 - направление d^k = -(H + mu*E)^-1 * grad f(x^k)
            d = [-(inv[0][0] * g[0] + inv[0][1] * g[1]),
                 -(inv[1][0] * g[0] + inv[1][1] * g[1])]
            log(f"Шаг 9. d{k} = -(H + mu*E)^-1 * grad f(x{k}) = {d}")

            # шаг 10 - новая точка
            x_new = [xi + di for xi, di in zip(x, d)]
            f_new = f(*x_new)
            n_evals += 1
            log(f"Шаг 10. x{k + 1} = x{k} + d{k} = {x_new}")
            log(f"f(x{k + 1}) = {f_new:.6f}")

            # шаг 11 - проверка f(x^{k+1}) < f(x^k)
            if f_new < fx:
                log(f"Шаг 11. f(x{k + 1}) = {f_new:.6f} < f(x{k}) = {fx:.6f} - переходим к шагу 12.")
                break
            # шаг 13 - mu_k = 2 * mu_k и возврат к шагу 7
            log(f"Шаг 11. f(x{k + 1}) = {f_new:.6f} >= f(x{k}) = {fx:.6f} - переходим к шагу 13.")
            mu *= 2
            log(f"Шаг 13. mu{k} = 2*mu{k} = {mu}, возвращаемся к шагу 7.")
            if mu > 1e300:
                raise RuntimeError("mu_k неограниченно растёт: f не убывает вдоль найденных направлений")

        norm_x = sqrt(sum((a - b) ** 2 for a, b in zip(x_new, x)))
        mod_fx = abs(f_new - fx)

        history.append({
            "k": k,
            "x_k": x,
            "f_xk": fx,
            "grad_norm": norm_g,
            "mu_k": mu,          # mu, при котором шаг принят (после удвоений)
            "mu_start": mu_k,    # mu в начале итерации
            "trials": trials,    # число попыток (шагов 7-11) на этой итерации
            "d": d,
            "x_k1": x_new,
            "f_xk1": f_new,
            "norm_x": norm_x,
            "mod_fx": mod_fx,
        })

        # шаг 12 - k = k + 1, mu_{k+1} = mu_k / 2
        x, fx = x_new, f_new
        log(f"\nШаг 12. k = {k + 1}, mu{k + 1} = mu{k} / 2 = {mu} / 2 = {mu / 2}. Переходим к шагу 3.")
        mu = mu / 2
        k += 1

    log(f"\nx* = {x}, f(x*) = {fx:.6f}")

    return MultivarResult(
        x=x, f_x=fx,
        n_iter=len(history),
        n_evals=n_evals,
        history=history,
        extra={"reason": reason, "mu_final": mu},
    )
