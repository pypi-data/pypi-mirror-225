import numpy as np

from ocean_science_utilities.tools.solvers import fixed_point_iteration


def test_fixed_point():
    # set_log_to_console()

    def _func(x: np.ndarray) -> np.ndarray:
        return 6.28 + np.sin(x)

    x0 = np.zeros(10)
    rtol = 1e-4
    atol = 1e-4

    res1 = fixed_point_iteration(_func, x0)
    res2 = fixed_point_iteration(_func, x0)

    np.testing.assert_allclose(res1, _func(res1), rtol=rtol, atol=atol)
    np.testing.assert_allclose(res2, _func(res2), rtol=rtol, atol=atol)


if __name__ == "__main__":
    test_fixed_point()
