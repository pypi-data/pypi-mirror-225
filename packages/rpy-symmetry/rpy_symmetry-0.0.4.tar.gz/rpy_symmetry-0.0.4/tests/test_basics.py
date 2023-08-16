import unittest


def test_minimal():
    import rpy_symmetry as rsym

    pval = rsym.p_symmetry([1, 2, 3])
    assert pval


class RaiseMod(unittest.TestCase):
    def test_raises(self):
        import rpy_symmetry as rsym

        with self.assertRaises(ModuleNotFoundError):
            rsym.get_module('no_such_module')
