import random
import string
from tablipy.core import Tablipy


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


# Generate random column headers
num_columns = 10
col_headers = [generate_random_string(8) for _ in range(num_columns)]

# Generate random data for the table
num_rows = 20
data = [[generate_random_string(10) for _ in range(num_columns)]
        for _ in range(num_rows)]

# Create an instance of Tablipy
table_instance = Tablipy(col_headers=col_headers, data=data)

# Print the table
table_instance.print()
