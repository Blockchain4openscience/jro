import numpy as np
from surfinpy import mu_vs_mu
from surfinpy import utils as ut
import unittest
from numpy.testing import assert_almost_equal
import os

test_data = os.path.join(os.path.dirname(__file__), 'H2O.txt')


class Testmu_vs_mu(unittest.TestCase):

    def test_calculate_excess(self):
        bulk = {'Cation': 1, 'Anion': 2, 'Energy': -100.00, 'F-Units': 1}
        x1 = mu_vs_mu.calculate_excess(1, 2, 3, bulk)
        x2 = mu_vs_mu.calculate_excess(2, 2, 3, bulk, nspecies=1, check=True)
        expected1 = 0.16666666666
        expected2 = -0.3333333333
        assert_almost_equal(expected1, x1, decimal=4)
        assert_almost_equal(expected2, x2, decimal=4)

    def test_calculete_normalisation(self):
        bulk = {'Cation': 1, 'Anion': 2, 'Energy': -100.00, 'F-Units': 1}
        x = mu_vs_mu.calculate_normalisation(1, 2, bulk, 3)
        expected = 33.5
        assert_almost_equal(expected, x, decimal=4)

    def test_calculate_surface_energy(self):
        x = mu_vs_mu.calculate_surface_energy(1, 2, 3, 4, 5, 6, 7)
        expected = -49
        assert x == expected

    def test_evaluate_phases(self):
        xshiftval = 0
        yshiftval = 0
        deltaX = {'Range': [0, 10], 'Label': 'O'}
        deltaY = {'Range': [0, 10], 'Label': 'H_2O'}
        bulk = {'Cation': 1, 'Anion': 2, 'Energy': -100.00, 'F-Units': 1}
        pure = {'Cation': 24, 'X': 48, 'Y': 0, 'Area': 60.22, 'Energy': -570.0,
                'Label': 'Stoich', 'nSpecies': 1}
        H2O = {'Cation': 24, 'X': 48, 'Y': 2, 'Area': 60.22, 'Energy': -600.0,
               'Label': '1 Water', 'nSpecies': 1}
        data = [pure, H2O]
        data = sorted(data, key=lambda k: (k['Y']))
        nsurfaces = len(data)
        X = np.arange(deltaX['Range'][0], deltaX['Range'][1], 0.025,
                      dtype="float")
        Y = np.arange(deltaY['Range'][0], deltaY['Range'][1], 0.025,
                      dtype="float")
        X = X - xshiftval
        Y = Y - yshiftval
        phase, SE = mu_vs_mu.evaluate_phases(data, bulk, X, Y,
                                         nsurfaces, xshiftval, yshiftval)
        expected_phase = np.zeros(X.size * Y.size)
        expected_phase = expected_phase + 2
        assert_almost_equal(phase, expected_phase)

    def test_temperature_correction(self):
        y = mu_vs_mu.temperature_correction(test_data, 100)
        assert_almost_equal(y, 0.006078349650349607)