import itertools   
import sys

def generate_tables(n, opp):
    # index's s1, s2, ...
    symbols = [f's{i}' for i in range(n)]
    # create empty table
    table = [[None for j in range(n)] for i in range(n)]

    # a + 0 = a for addition, a * 1 = a for multipliation
    identity = 0 if opp == "add" else 1
    # fill in identities
    for i in range(n):
        table[identity][i] = symbols[i] 
        table[i][identity] = symbols[i]  

    # get indices that need to be filled in 
    # j from i to n leaves out half of the columns, which can be populated according the the commutative axiom
    none_indices = [(i, j) for i in range(n) for j in range(i, n) if table[i][j] is None]

    # fill in other entries and add to table list
    def generate_combos():
        # Generate all possible completions of the None cells
        for combo in itertools.product(symbols, repeat=len(none_indices)):
            filled_table = [row[:] for row in table]  # copy table into new one
            for index, value in zip(none_indices, combo): # fill in empty entries
                i, j = index
                # fill in entry and commutative entry
                filled_table[i][j] = value
                filled_table[j][i] = value 

            yield filled_table

    return generate_combos()


def is_commutative(table):
    # check commutativity for each pair
    for row in range(len(table)):
        for col in range(len(table)):
            if table[row][col] != table[col][row]: # check if a ~ b = b ~ a
                return False
    
    return True

def is_associative(table):
    n = len(table)  
    element_dict = {f's{i}': i for i in range(n)}
    for a in range(n):  # Iterate over all possible 'a'
        for b in range(n):  # Iterate over all possible 'b'
            for c in range(n):  # Iterate over all possible 'c'
                # Check if a ~ (b ~ c) == (a ~ b) ~ c
                ab = element_dict[table[a][b]]
                bc = element_dict[table[b][c]]
                if table[a][bc] != table[ab][c]:
                    return False  
    return True  

def has_identity(table, opp):
    # a + 0 = a for addition, a * 1 = a for multipliation
    identity = 0 if opp == "add" else 1
    
    for a in range(len(table)):
        expected = f's{a}'
        # Check 0 + a = a and a + 0 = a for each a (or a * 1 = a and 1 * a = a)
        if table[identity][a] != expected or table[a][identity] != expected: 
            return False
    return True

def has_inverse(table, opp):
    # check if each number has an inverse
    for a in range(len(table)):
        # for multiplicative, only non zero elements 
        if (opp == "mult" and a == 0):
            break

        has_inverse = False
        # a + b = 0 for additive, a * b = 1 for multiplicative
        identity = 's0' if opp == "add" else 's1'
        # check if each element has an inverse
        for b in range(len(table)):
            if table[a][b] == identity and table[b][a] == identity:
                has_inverse = True
        # return false if one was not found
        if not has_inverse:
            return False
        
    return True

def is_distributive(add_table, mult_table):
    n = len(add_table)
    element_dict = {f's{i}': i for i in range(n)} # for converting to index

    # for each a, b, and c, check if distributive property holds
    for a in range(n):
        for b in range(n):
            for c in range(n):
                bc_sum = element_dict[add_table[b][c]]
                ab_prod = element_dict[mult_table[a][b]]
                ac_prod = element_dict[mult_table[a][c]]
                if mult_table[a][bc_sum] != add_table[ab_prod][ac_prod]:
                    return False
    return True

def find_rings(n):
    # get all possible sum and multiplication tables
    sum_tables = generate_tables(n, "add")
    mult_tables = generate_tables(n, "mult")
    
    # check validity of each table 
    valid_sum_tables = []
    valid_mult_tables = []
    for table in sum_tables:
        if is_commutative(table) and is_associative(table) and has_identity(table, "add") and has_inverse(table, "add"):
            valid_sum_tables += [table]

    for table in mult_tables:
        if is_commutative(table) and is_associative(table) and has_identity(table, "mult") and has_inverse(table, "mult"):
            valid_mult_tables += [table]

    # check distributive property for each add/multiplaication table pair
    valid_combos = []
    for add_table in valid_sum_tables:
        for mult_table in valid_mult_tables:
            if is_distributive(add_table, mult_table):
                valid_combos += [(add_table, mult_table)]

    return valid_combos

def display_rings(n):
    valid_rings = find_rings(n)  # get the rings

    # for each add/multiplaication table pair
    for idx, (add_table, mult_table) in enumerate(valid_rings):
        print(f"Ring {idx + 1}:\n")

        # Display the addition table
        print("Addition Table:")
        for row in add_table:
            print(row)
        print()

        # display multiplication table
        print("Multiplaication Table:")
        for row in mult_table:
            print(row)
        print()


if __name__ == '__main__':
    n = int(sys.argv[1])
    display_rings(n)
        