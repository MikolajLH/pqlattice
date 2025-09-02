import json
from fpylll import *
from argparse import ArgumentParser



parser = ArgumentParser(
    add_help=True
)

parser.add_argument("out")
parser.add_argument("d")
parser.add_argument("n")

args = input().split()
args = parser.parse_args(args)
print(args)

file_path = f"{args.out}{args.d}x{args.d}.json"
N = int(args.n)
D = int(args.d)


def toList(A):
    A_list = []
    for row in A:
        row_list = []
        for el in row:
            row_list.append(int(el.str()))
        A_list.append(row_list)
    return A_list


res = []
for i in range(N):
    A = IntegerMatrix(D, D)
    A.randomize("uniform", bits=32)
    res.append(toList(A))

with open(file_path, mode='w', encoding='utf-8') as f:
    # print(json.dumps(res, indent=4))
    json.dump(res, f, indent=2)

print(file_path)
print(len(res))

# echo "<path> <dim> <num>" | sage gen_lattice.sage
# echo "./tests/sage_data/lattice/ 5 10" | sage gen_lattice.sage
