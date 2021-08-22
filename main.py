"""
Main module
"""
from argparse import ArgumentParser
from argparse import Namespace
from collections import Counter
from typing import List
from typing import Set
from typing import Tuple
from typing import cast

from lark import Lark
from lark import Token
from lark import Transformer
from lark import v_args
from sympy import Matrix  # type: ignore
from sympy import lcm  # type: ignore

GRAMMAR = """
%import common.INT
%import common.UCASE_LETTER
%import common.LCASE_LETTER
%import common.WS

%ignore WS
start: molecule+

molecule: atom | molecule_group
molecule_group: "(" molecule+ ")" INT
?atom: single_atom | multiple_atoms
single_atom: ATOM
multiple_atoms: ATOM INT
ATOM: UCASE_LETTER LCASE_LETTER?
"""


@v_args(inline=True)
class ChemTransformer(Transformer):
    """
    A lark.Transformer performing tree reduction on the chemical tree.

    Reduces chemical formula to the atom counts
    """

    def single_atom(self, atom: Token) -> Counter[str]:
        """Reduction of the `single_atom` production rule"""
        return Counter({atom.value: 1})

    def multiple_atoms(self, atom: Token, count: Token) -> Counter[str]:
        """Reduction of the `multiple_atoms` production rule"""
        return Counter({atom.value: int(count.value)})

    def molecule(self, *children):
        """Reduction of the `molecule` production rule"""
        start: Counter[str] = Counter()
        return sum(children, start=start)

    def molecule_group(self, *children):
        """Reduction of the `molecule_group` production rule"""
        group_count = int(children[-1].value)
        counter: Counter[str] = sum(children[:-1], start=Counter())
        return Counter({key: value * group_count for key, value in counter.items()})

    def start(self, *children):
        """Reduction of the grammar's starting nonterminal symbol"""
        return self.molecule(*children)


def count_atoms(chemical_formula: str) -> Counter[str]:
    """
    Count the atoms in a chemical formula
    """
    parser = Lark(GRAMMAR, parser="lalr", transformer=ChemTransformer())
    reduced_tree = cast(Counter[str], parser.parse(chemical_formula))
    return reduced_tree


def build_equation_system(
    left_vectors: List[Matrix], right_vectors: List[Matrix]
) -> Matrix:
    """
    Builds the matrix of the system with molecules encoded as vectors
    """
    left = Matrix.hstack(*left_vectors)
    right = Matrix.hstack(*right_vectors)
    return Matrix.hstack(left, -right)


def balance_equation(
    input_molecules: List[str], output_molecules: List[str]
) -> Tuple[List[int], List[int]]:
    """
    Balance the equation containing `input_molecules` molecules in the left side of
    chemical equation, and `output_molecules` in the right side of the equation.
    """
    input_len = len(input_molecules)
    output_len = len(output_molecules)
    input_atom_counts = list(map(count_atoms, input_molecules))
    output_atom_counts = list(map(count_atoms, output_molecules))
    input_atom_set = atoms_set(input_atom_counts)
    output_atom_set = atoms_set(output_atom_counts)

    # sanity check
    # the set of all atoms appearing in the equation input
    # must match the set of all atoms appearing in the equation output
    assert input_atom_set == output_atom_set

    atom_order = sorted(input_atom_set)

    input_molecule_vectors = list(
        map(lambda m: vectorize(m, atom_order), input_atom_counts)
    )
    output_molecule_vectors = list(
        map(lambda m: vectorize(m, atom_order), output_atom_counts)
    )
    system_matrix = build_equation_system(
        input_molecule_vectors, output_molecule_vectors
    )

    nullspace = system_matrix.nullspace()

    # Sometimes there might be more than one vector in the basis of the nullspace.
    # I'm not sure if it is possible. I don't think it has any real world sense
    vector = nullspace[0]

    # sometimes nullspace basis comes up in fractional form
    # while technically correct, stechiometric coefficients are defined to
    # be integers. therefore, it is necessary to scale the vector s.t. all
    # the elements are integers
    #
    # note, one cannot just divide by the smallest element;
    # for example [2/3 3/4] would give [1 9/8] but it should give [8 9]
    vector *= lcm(list(fraction.denominator() for fraction in vector))
    coefficients = list(map(int, vector[:]))

    # sanity check: the length of the coefficients list should be
    # the sum of the lengts of the molecule lists
    assert len(coefficients) == input_len + output_len

    return coefficients[:input_len], coefficients[input_len:]


def parse_args() -> Namespace:
    """
    Argument parsing function
    """
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-molecules", nargs="+", type=str)
    parser.add_argument("-o", "--output-molecules", nargs="+", type=str)
    return parser.parse_args()


def atoms_set(atom_count_list: List[Counter[str]]) -> Set[str]:
    """
    Get a set of all (unique) atoms of all molecules in one side of chemical equation
    """
    return set(sum(atom_count_list, start=Counter()).keys())


def vectorize(molecule: Counter[str], atom_order: List[str]) -> Matrix:
    """
    Builds a vector from a molecule atom counts
    """
    molecule_vector = Matrix.zeros(len(atom_order), 1)
    for atom, count in molecule.items():
        molecule_vector[atom_order.index(atom)] = count
    return molecule_vector


def assemble_expression(coefficients: List[int], molecules: List[Matrix]) -> str:
    """
    Helper function for representation building.

    Takes a list of integer coefficients and a list of molecular formulae strings
    and builds a string representation of one side of chemical equation
    """
    assert len(coefficients) == len(molecules)
    return " + ".join(
        "{}{}".format("" if coef == 1 else coef, molecule)
        for coef, molecule in zip(coefficients, molecules)
    )


def main(arguments: Namespace) -> str:
    """
    Main function

    Consumes the command line arguments and calls the equation balancing function.
    """

    # print(input_molecule_vectors)
    # print(output_molecule_vectors)
    in_coefficients, out_coefficients = balance_equation(
        arguments.input_molecules, arguments.output_molecules
    )
    return "{} --> {}".format(
        assemble_expression(in_coefficients, arguments.input_molecules),
        assemble_expression(out_coefficients, arguments.output_molecules),
    )


if __name__ == "__main__":
    args = parse_args()
    print(main(args))
