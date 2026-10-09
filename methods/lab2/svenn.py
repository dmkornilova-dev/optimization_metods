from helping.log import make_logger
from helping.types import IntervalResult, NotUnimodalError

def svenn_method(func, x0, t, verbose=False):
    log = make_logger(verbose)

    # шаг 1
    log(f"\nШаг 1: x0 = {x0}, t = {t}")

    # шаг 2: k = 0, вычисляем f-, f0, f+ (три вычисления функции)
    k = 0
    f_minus = func(x0 - t)
    f0 = func(x0)
    f_plus = func(x0 + t)
    n_evals = 3
    log(f"\nШаг 2: k = {k}")
    log(f"f(x0 - t) = f({x0 - t}) = {f_minus}")
    log(f"f(x0) = f({x0}) = {f0}")
    log(f"f(x0 + t) = f({x0 + t}) = {f_plus}")

    # шаг 3: проверка условия окончания
    log("\nШаг 3: проверка условия окончания")
    if f_minus >= f0 <= f_plus:  # случай a)
        a0, b0 = x0 - t, x0 + t
        log(f"Случай a): f- >= f0 <= f+: {f_minus} >= {f0} <= {f_plus}")
        log(f"-> интервал найден: [a0, b0] = [{a0}, {b0}]")
        return IntervalResult(a=a0, b=b0, x=(a0 + b0) / 2,
                              n_evals=n_evals, history=[])
    elif f_minus < f0 > f_plus:  # случай b) функция не унимодальна ! Исправлено
        raise NotUnimodalError(
            f"Случай b): f- <= f0 >= f+: {f_minus} <= {f0} >= {f_plus}. "
            "Функция не является унимодальной, "
            "требуемый интервал неопределённости не может быть найден."
        )
    else:
        log(f"Случай c): условие окончания не выполняется: "
            f"f- = {f_minus}, f0 = {f0}, f+ = {f_plus}")
        log("-> переходим к шагу 4")

    # шаг 4: определение Delta и начальных границ.
    # f(x1) уже вычислено на шаге 2 (это f_plus или f_minus), повторно не считаем.
    if f_minus >= f0 >= f_plus:  # функция убывает вправо
        right = True
        delta = t
        a0, b0 = x0, None
        x_curr, f_curr = x0 + t, f_plus
        dir_name = "вправо"
    elif f_minus <= f0 <= f_plus:  # функция убывает влево
        right = False
        delta = -t
        a0, b0 = None, x0
        x_curr, f_curr = x0 - t, f_minus
        dir_name = "влево"
    else:
        raise NotUnimodalError("Не удалось определить направление убывания функции.")
    k = 1
    log(f"\nШаг 4: функция убывает {dir_name}, Delta = {delta}, x1 = {x_curr}, k = {k}")

    # шаги 5-6
    while True:
        x_next = x_curr + (2 ** k) * delta
        f_next = func(x_next)  # единственное новое вычисление на итерации
        n_evals += 1

        log(f"\nШаг 5 (k={k}): x{k + 1} = x{k} + 2^{k} * Delta = "
            f"{x_curr} + {2 ** k} * ({delta}) = {x_next}")
        log(f"Шаг 6 (k={k}): f(x{k}) = f({x_curr}) = {f_curr} (уже вычислено);\n"
            f"f(x{k + 1}) = f({x_next}) = {f_next}")

        if f_next < f_curr:  # случай а) - функция продолжает убывать
            if right:
                a0 = x_curr
            else:
                b0 = x_curr
            log(f"f(x{k + 1}) < f(x{k})  =>  функция продолжает убывать. Обновляем границу.")
            x_curr, f_curr = x_next, f_next  # переносим значение, не пересчитываем
            k += 1
        else:  # случай б) - функция перестала убывать
            if right:
                b0 = x_next
            else:
                a0 = x_next
            log(f"f(x{k + 1}) >= f(x{k})  =>  функция перестала убывать. "
                f"Алгоритм завершён.")
            break

    log(f"\nРезультат: интервал, содержащий минимум функции: [a0, b0] = [{a0}, {b0}]")
    log(f"Число вычислений функции: {n_evals}\n")
    return IntervalResult(a=a0, b=b0, x=(a0 + b0) / 2,
                          n_evals=n_evals, history=[])