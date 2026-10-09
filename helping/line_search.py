from helping.log import make_logger
from methods.lab2.svenn import svenn_method

# линейный поиск минимума функции f
# метод Свенна определяет отрезок, на котором производится поиск
# метод дихотомии / золотого сечения / чисел Фибоначчи находит на этом отрезке минимум
def line_search(f, step_method, svenn_t, verbose=False):
    log = make_logger(verbose)
    params = dict(step_method) # копия параметров
    method = params.pop("func")

    sv = svenn_method(f, 0, svenn_t, verbose=False)
    log(f"Свенн (x0 = 0, t = {svenn_t}): [{sv.a}; {sv.b}], вычислений: {sv.n_evals}")

    res = method(f, sv.a, sv.b, verbose=False, **params)
    log(f"{method.__name__}: [{res.a:.6f}; {res.b:.6f}], t* = {res.x:.6f}, "
        f"вычислений: {res.n_evals}")

    return res.x, sv.n_evals + res.n_evals
