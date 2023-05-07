import random
import sympy


def generate_instances(length, nb_variables, nb_instances):
    _, *x = sympy.polys.rings.ring(
        ",".join([f"x{i}" for i in range(nb_variables)]), sympy.GF(2)
    )
    for _ in range(nb_instances):
        l = []
        for _ in range(length):
            while True:
                factors = []
                for _ in range(random.randrange(1, min(4, nb_variables + 1))):
                    while True:
                        factor = random.choice(x)
                        if factor not in factors:
                            break
                    factors.append(factor)
                monomial = sympy.prod(factors)
                if monomial != 1 and monomial not in l:
                    break
            l.append(monomial)
        print(sum(l))


for variables in range(2, 30):
    length = variables
    print(f"# length: {length}, variables: {variables}")
    if (
        variables
        + variables * (variables - 1) / 2
        + variables * (variables - 1) * (variables - 2) / (3 * 2)
        < length
    ):
        continue
    generate_instances(length, variables, 8)
    print()
