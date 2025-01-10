# Global literals list (track all literals globally)
global_literals = [1, 2, 3]  # Example literals, you can modify this
computation_steps = 0  # Global counter for computation steps

def find_max_frequency_literal(clauses):
    global computation_steps

    # Calculate the frequency of each literal across all clauses
    freq = {}

    for clause in clauses:
        for literal in clause:
            if literal not in freq:
                freq[literal] = 0
            freq[literal] += 1

    # Find the literal with the maximum frequency
    max_literal = max(freq, key=freq.get)
    computation_steps += 1

    return max_literal, freq

def solve_3sat(clauses, literals):
    global computation_steps

    m = len(clauses)  # Number of clauses
    n = len(literals)  # Number of literals

    # Base case: No clauses, trivial solution
    if m == 0:
        return True  # No clauses to satisfy

    # Base case: No literals, unsolvable if there are clauses
    if n == 0:
        return False  # No literals to satisfy the clauses

    # Step 1: Find the literal with the max frequency
    max_literal, freq = find_max_frequency_literal(clauses)

    # Step 2: Try assigning true to the max_literal
    # Remove clauses that are satisfied by assigning the max_literal as True
    clauses_true = [clause for clause in clauses if max_literal not in clause]

    # Step 3: Try assigning false to the max_literal
    # Remove clauses that are satisfied by assigning the max_literal as False
    clauses_false = [clause for clause in clauses if -max_literal not in clause]

    # Step 4: Recursively solve the problem by reducing the number of clauses and literals
    # Case 1: Assign max_literal to true (local literals are updated)
    new_literals_true = [lit for lit in literals if lit != max_literal]  # Local literal update
    if solve_3sat(clauses_true, new_literals_true):
        computation_steps += 1
        return True

    # Case 2: Assign max_literal to false (local literals are updated)
    new_literals_false = [lit for lit in literals if lit != -max_literal]  # Local literal update
    if solve_3sat(clauses_false, new_literals_false):
        computation_steps += 1
        return True


    # If neither case works, return False
    return False

# Example input:
# Let's assume the 3SAT problem is represented as:
clauses = [[1, 2, 3], [1, -2, 3], [1, 2, -3], [-1, -2, 3]]

# Solve the 3SAT problem using global literals and local literals
solution = solve_3sat(clauses, global_literals)

if solution:
    print("3SAT is solvable")
else:
    print("3SAT is unsolvable")
print(f"Computation steps: {computation_steps}")


