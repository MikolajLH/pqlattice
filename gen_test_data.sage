from argparse import ArgumentParser
import importlib

# echo "* Integers" | sage gen_test_data.sage

args = input().split()

parser = ArgumentParser(
    add_help=True
)
parser.add_argument("module")
parser.add_argument("object")

args = parser.parse_args(args)

print(args)

try:
    if args.module == "*":
        obj = globals()[args.object]
        print(obj)
        R = obj(11)
        print(R)
        a = R(7)
        b = R(3)
        bi = b ** (-1)
        q1 = a // b
        q2 = a / b
        print(a, b, q1, q2, bi, bi * a)
    else:
        pass
        pkg = importlib.import_module(args.module)
        obj = getattr(pkg, args.object)
        print(obj)
except ImportError:
    print(f"No module {args.module}")
