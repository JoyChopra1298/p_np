import csv

import random
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(50000)


# Global literals list (track all literals globally)
def generate_random_3sat(m, n):
    """
    Generate a random 3-SAT problem with m clauses and n literals.
    Each clause has exactly 3 literals, chosen randomly from 1 to n and their negations.
    """
    clauses = []
    for _ in range(m):
        clause = random.sample(range(1, n + 1), 3)  # Choose 3 distinct literals
        clause = [random.choice([lit, -lit]) for lit in clause]  # Randomly negate literals
        clauses.append(clause)
    return clauses


# Track computation steps for solving the 3SAT problem
computation_steps = 0


def find_max_frequency_literal(clauses):
    # Calculate the frequency of each literal across all clauses
    freq = {}

    for clause in clauses:
        for literal in clause:
            if literal not in freq:
                freq[literal] = 0
            freq[literal] += 1

    # Find the literal with the maximum frequency
    max_literal = max(freq, key=freq.get)
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
    clauses_true = [clause for clause in clauses if max_literal not in clause]

    # Step 3: Try assigning false to the max_literal
    clauses_false = [clause for clause in clauses if -max_literal not in clause]

    # Step 4: Recursively solve the problem by reducing the number of clauses and literals
    computation_steps += 1  # Track computation step for every recursive call

    # Case 1: Assign max_literal to true (local literals are updated)
    new_literals_true = [lit for lit in literals if lit != max_literal]
    if solve_3sat(clauses_true, new_literals_true):
        return True

    # Case 2: Assign max_literal to false (local literals are updated)
    new_literals_false = [lit for lit in literals if lit != -max_literal]
    if solve_3sat(clauses_false, new_literals_false):
        return True

    # If neither case works, return False
    return False


# Function to generate random problems and plot computation steps
def generate_and_plot(m_values, n_values):
    steps_data = []  # List to store computation data

    for m in m_values:
        for n in n_values:
            global computation_steps
            # Generate random 3-SAT problem
            clauses = generate_random_3sat(m, n)
            literals = list(range(1, n + 1))  # Literals from 1 to n
            computation_steps = 0  # Reset computation steps
            # Solve the 3-SAT problem
            solve_3sat(clauses, literals)

            # Store the results in steps_data
            steps_data.append([m, n, m + n, computation_steps])
            print(f"m={m}, n={n}, m+n={m+n}, steps={computation_steps}")  # Optional: Debugging output

    # Save the data to a CSV file
    with open('computation_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["m", "n", "m+n", "computation_steps"])
        writer.writerows(steps_data)

    # Plotting m vs computation steps and save as PNG
    m_vals, m_steps = zip(*[(m, comp) for m, _, _, comp in steps_data])
    plt.figure(figsize=(10, 6))
    plt.scatter(m_vals, m_steps, c=m_steps, cmap='viridis', s=50)
    plt.colorbar(label='Computation Steps')
    plt.xlabel('Number of Clauses (m)')
    plt.ylabel('Computation Steps')
    plt.title('Number of Clauses vs Computation Steps')
    plt.savefig('m_vs_computation.png')  # Save plot as PNG

    # Plotting n vs computation steps and save as PNG
    n_vals, n_steps = zip(*[(n, comp) for _, n, _, comp in steps_data])
    plt.figure(figsize=(10, 6))
    plt.scatter(n_vals, n_steps, c=n_steps, cmap='viridis', s=50)
    plt.colorbar(label='Computation Steps')
    plt.xlabel('Number of Literals (n)')
    plt.ylabel('Computation Steps')
    plt.title('Number of Literals vs Computation Steps')
    plt.savefig('n_vs_computation.png')  # Save plot as PNG

    # Plotting m + n vs computation steps and save as PNG
    mn_vals, mn_steps = zip(*[(m + n, comp) for m, n, _, comp in steps_data])
    plt.figure(figsize=(10, 6))
    plt.scatter(mn_vals, mn_steps, c=mn_steps, cmap='viridis', s=50)
    plt.colorbar(label='Computation Steps')
    plt.xlabel('m + n')
    plt.ylabel('Computation Steps')
    plt.title('m + n vs Computation Steps')
    plt.savefig('mn_vs_computation.png')  # Save plot as PNG

    print("Plots and computation data saved successfully!")

# Test the generation and plot with random SAT problems of varying size
m_values = range(5, 1001, 100)
n_values = range(5, 1001, 100)

generate_and_plot(m_values, n_values)
