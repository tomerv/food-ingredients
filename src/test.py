from solve import solve, read_file
from io import StringIO

with open('data/rice_drink.txt', 'rb') as f:
    file_contents = f.read().decode('utf-8')

print(file_contents)

f = StringIO(file_contents)
print(read_file(f))
