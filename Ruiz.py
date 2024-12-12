import numpy as np
from itertools import product
from collections import defaultdict
from tqdm import tqdm  # Import progress bar library

def generate_spin_configurations(n):
    """
    Generate all possible spin configurations for an n x n lattice.
    Returns an iterator over flat configurations.
    """
    total_spins = n * n
    return product([-1, 1], repeat=total_spins)

def calculate_energy(configuration, n):
    """
    Calculate the energy of a given spin configuration.
    Assumes periodic boundary conditions.
    """
    lattice = np.array(configuration).reshape(n, n)
    energy = 0

    # Iterate over each spin in the lattice
    for i in range(n):
        for j in range(n):
            # Add interaction with right neighbor (periodic boundary)
            if lattice[i, j] == lattice[i, (j + 1) % n]:
                energy += 1
            # Add interaction with bottom neighbor (periodic boundary)
            if lattice[i, j] == lattice[(i + 1) % n, j]:
                energy += 1


    return energy

def get_canonical_form(configuration):
    """
    Get the canonical form of a configuration by choosing the lexicographically
    smaller of the configuration and its spin-reversed version.
    """
    spin_reversed = tuple(-s for s in configuration)
    return min(configuration, spin_reversed)

def enumerate_configurations_and_dos_with_symmetry(n):
    """
    Enumerate configurations using spin reversal symmetry and calculate the
    density of states (number of configurations for each energy level).
    """
    equivalence_classes = defaultdict(int)  # Store count of configurations in each equivalence class
    energy_counts = defaultdict(int)       # Store density of states for each energy level

    # Generate all configurations
    total_configs = 2 ** (n * n)  # Total number of configurations
    map(get_canonical_form, tqdm(generate_spin_configurations(n), total=total_configs, desc="Enumerating configurations"))
    # NB: convert to dictionary of numbers using Counter instead
    for cf in map(get_canonical_form, tqdm(generate_spin_configurations(n), total=total_configs, desc="Enumerating configurations")):
        equivalence_classes[cf] += 1


    # Calculate energy for each equivalence class
    for canonical_config, count in equivalence_classes.items():
        energy = calculate_energy(canonical_config, n)
        energy_counts[energy] += count

    return energy_counts


# Lattice size (n x n)
n = 6  # Adjust this for larger sizes (e.g., 6 for a 6x6 lattice)

print(f"Enumerating configurations for a {n}x{n} lattice using spin reversal symmetry...")
    
# Enumerate configurations and calculate density of states
energy_counts = enumerate_configurations_and_dos_with_symmetry(n)

# Display results
print("\nDensity of States (Energy Levels):")
for energy, count in sorted(energy_counts.items()):
    print(f"Energy: {energy}, Count: {count}")

