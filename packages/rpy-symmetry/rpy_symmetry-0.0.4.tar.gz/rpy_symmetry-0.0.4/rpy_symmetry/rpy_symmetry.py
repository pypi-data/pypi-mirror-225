import numpy as np
import typing as ty
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import FloatVector


def symmetry_test(
    x: ty.Union[tuple, list, np.ndarray],
    test_statistic: str = 'MI',
    test_k: int = 1,
    _module: str = 'symmetry',
    _method: str = 'symmetry_test',
    **kw,
) -> dict:
    """Perform symmetry test of dataset x

    See https://cran.r-project.org/web/packages/symmetry/symmetry.pdf for more
    info.

    Args:
        x (ty.Union[tuple, list, np.ndarray]): Dataset to test
        test_statistic (str, optional): Which method to use (see ref). Defaults to 'MI'.
        test_k (int, optional): Required argument, only relevant for some test_statistics (but not
            MI, the default). Defaults to 1.
        _module (str, optional): Which module to load. Defaults to 'symmetry'.
        _method (str, optional): Wich function to call. Defaults to 'symmetry_test'.

    Returns:
        dict: results dictionary of the test.
    """
    test = getattr(get_module(_module), _method)
    result = test(
        x=FloatVector(x),
        stat=test_statistic,
        k=test_k,
        **kw,
    )
    return _result_to_dict(result)


def p_symmetry(x: np.ndarray, **kw) -> float:
    """Get the p-value of the symmetry test, see symmetry_test"""
    return float(symmetry_test(x, **kw)['p.value'])


def get_module(name: str = 'symmetry'):
    if not rpackages.isinstalled(name):
        if name == 'symmetry':
            _install_package_on_the_fly(name)
        else:
            # I'm not doing this for any package for safety reasons
            raise ModuleNotFoundError(
                f'{name} is not installed in R, you can use '
                f'_install_package_on_the_fly(\'{name}\')"'
            )
    return rpackages.importr(name)


def _install_package_on_the_fly(package: str) -> None:
    from rpy2.robjects.vectors import StrVector
    from rpy2.rinterface_lib.embedded import RRuntimeError

    utils = rpackages.importr('utils')
    packnames = (package,)
    utils.chooseCRANmirror(ind=1)
    try:
        utils.install_packages(StrVector(packnames))
    except RRuntimeError as e:
        raise RuntimeError(
            f'Cannot install {package} on the fly, please make sure that R is properly installed'
        ) from e


def _float_or_str(x) -> ty.Union[str, float]:
    """Try making x a float, or a string otherwise"""
    try:
        return float(x)
    except ValueError:
        pass
    return str(x)


def _result_to_dict(res) -> dict:
    """Extract htest results from a rpy2.robjects.vectors.ListVector object"""
    res_dict = {}
    for i, n in enumerate(res.names):
        v = res[i]
        if len(v) == 1:
            v = _float_or_str(v[0])
        res_dict[n] = v
    return res_dict
