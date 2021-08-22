# Chemical equation balancer

Balance your chemical equations with ease!

## Installation
```
$ git clone git@github.com:InCogNiTo124/chemeq.git && cd chemeq;
$ python3 -m venv venv
$ source venv/bin/activate
$ (venv) pip install -r requirements/main.txt
```

Optionally, install `dev` dependencies inside the virtual environment and check the code:
```
$ (venv) pip install -r requirements/dev.txt
$ (venv) make check
```

## Usage
```
python3 main.py -i ${INPUT_CHEM_1} ${INPUT_CHEM_2} ... -o ${OUTPUT_CHEM_1} ${OUTPUT_CHEM_2} ...
```
Note, there must be at least one input and at least one output.

### Examples:
```
$ (venv) python3 main.py -i CH4 Cl2 -o CH3Cl H2
2CH4 + Cl2 --> 2CH3Cl + H2
$ (venv) python3 main.py -i 'KOH' 'Co3(PO4)2' -o 'K3PO4' 'Co(OH)2'
6KOH + Co3(PO4)2 --> 2K3PO4 + 3Co(OH)2
$ (venv) python3 main.py -i CH3CH2OH O2 -o CO2 H2O
CH3CH2OH + 3O2 --> 2CO2 + 3H2O
```

## How it works?
The idea is to write every molecule as a vector, such that the first dimension corresponds to one atom, the second for another etc. Then, both the left side and the right side can be though of as linear combination of vectors.
After a short matrix calculation, it can be shown that the solution which balances the chemical equation is actually a basis vector in the nullspace of the system matrix.

For more details, try to figure out [https://en.wikipedia.org/wiki/Chemical\_equation#Balancing\_chemical\_equations](https://en.wikipedia.org/wiki/Chemical_equation#Balancing_chemical_equations)

I've actually come up with the idea on my own.

# TODO:
- Web deployment
- Simpler implementation?
- More docs? idk
- Bugfixes? idk
