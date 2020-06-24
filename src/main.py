import sys
from solve import read_file, solve

try:
    filename = sys.argv[1]
except IndexError:
    print(f'Usage: {__file__} <ingredients_file.json>')
    exit(1)

with open(filename) as f:
    try:
        names, amounts = read_file(f)
    except ValueError as e:
        print(e)
        exit(1)
try:
    res = solve(amounts)
except ValueError as e:
    print(f'Error solving: {e}')
    print('Make sure that the amounts are correct and sorted from largest to smallest.')
    exit(1)

for name,(low,high) in zip(names,res):
    if low < high:
        print(f"{name+':':20} {low: >7.2%} -{high: >7.2%}")
    else:
        print(f"{name+':':20}      {low: >7.2%}")