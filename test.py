"""
Tests for chemical equation balancing script
"""
import pytest

from main import balance_equation
from main import count_atoms


@pytest.mark.parametrize(
    "molecule,target",
    [
        ("Na", {"Na": 1}),
        ("CO2", {"C": 1, "O": 2}),
        ("H2O", {"H": 2, "O": 1}),
        ("Mg(OH)2", {"Mg": 1, "O": 2, "H": 2}),
        ("Ba(NO2)2", {"Ba": 1, "N": 2, "O": 4}),
        ("Ba(PO3)2", {"Ba": 1, "P": 2, "O": 6}),
        ("C13H18O2", {"C": 13, "H": 18, "O": 2}),
        ("K4(ON(SO3)2)2", {"K": 4, "O": 14, "N": 2, "S": 4}),
        ("(CH3)3COOC(CH3)3", {"C": 8, "H": 18, "O": 2}),
        ("(C2H5)2NH", {"C": 4, "H": 11, "N": 1}),
        ("Co3(Fe(CN)6)2", {"Co": 3, "Fe": 2, "C": 12, "N": 12}),
    ],
)
def test_count_atoms(molecule, target):
    """
    Test `count_atoms` function with various inputs
    """
    count = count_atoms(molecule)
    assert count == target
    return


@pytest.mark.parametrize(
    "input_molecules,output_molecules,target",
    [
        (["P4O10", "H2O"], ["H3PO4"], ([1, 6], [4])),
        (["N2", "H2"], ["NH3"], ([1, 3], [2])),
        (["CH4", "Cl2"], ["CCl4", "H2"], ([1, 2], [1, 2])),
        (["CH3CH2OH", "O2"], ["CO2", "H2O"], ([1, 3], [2, 3])),
        (["KOH", "Co3(PO4)2"], ["K3PO4", "Co(OH)2"], ([6, 1], [2, 3])),
    ],
)
def test_balance_equation(input_molecules, output_molecules, target):
    """
    Test equation balancer
    """
    balanced_equation = balance_equation(input_molecules, output_molecules)
    assert balanced_equation == target
