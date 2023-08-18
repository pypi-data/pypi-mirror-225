import numpy as np

from libcasm.composition import CompositionCalculator


def test_CompositionCalculator_1():
    components = ["A", "B"]
    allowed_occs = [["A", "B"]]
    n_sublat = len(allowed_occs)
    volume = 10
    occupation = [0] * n_sublat * volume

    comp_calculator = CompositionCalculator(components, allowed_occs)

    # check (a)
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([10, 0], dtype="int")
    assert np.all(total_n == expected_total_n)

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([1.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    # check (b)
    occupation[0] = 1
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([9, 1], dtype="int")
    assert np.all(total_n == expected_total_n)

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([0.9, 0.1])
    assert np.allclose(mean_n, expected_mean_n)


def test_CompositionCalculator_2():
    components = ["A", "B"]
    allowed_occs = [["A", "B"], ["A", "B"]]
    n_sublat = len(allowed_occs)
    volume = 10
    occupation = [0] * n_sublat * volume

    comp_calculator = CompositionCalculator(components, allowed_occs)

    # check (a)
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([20, 0], dtype="int")
    assert np.all(total_n == expected_total_n)

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([2.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    # check (b)
    occupation[0] = 1
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([19, 1], dtype="int")
    assert np.all(total_n == expected_total_n)

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([1.9, 0.1])
    assert np.allclose(mean_n, expected_mean_n)


def test_CompositionCalculator_3():
    components = ["A", "B"]
    allowed_occs = [["A", "B"], ["B", "A"]]
    n_sublat = len(allowed_occs)
    volume = 10
    occupation = [0] * n_sublat * volume

    comp_calculator = CompositionCalculator(components, allowed_occs)

    # check (a)
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([10, 10], dtype="int")
    assert np.all(total_n == expected_total_n)

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([1.0, 1.0])
    assert np.allclose(mean_n, expected_mean_n)

    # check (b)
    occupation[0] = 1
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([9, 11], dtype="int")
    assert (total_n == expected_total_n).all()

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([0.9, 1.1])
    assert np.allclose(mean_n, expected_mean_n)


def test_CompositionCalculator_4():
    components = ["Zr", "Va", "O"]
    allowed_occs = [["Zr"], ["Zr"], ["Va", "O"], ["Va", "O"]]
    n_sublat = len(allowed_occs)
    volume = 10
    occupation = [0] * n_sublat * volume

    comp_calculator = CompositionCalculator(components, allowed_occs)

    # check (a)
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([20, 20, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([2.0, 2.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    species_frac = comp_calculator.species_frac(occupation)
    expected_species_frac = np.array([1.0, 0.0, 0.0])
    assert np.allclose(species_frac, expected_species_frac)

    # check (a-0)
    total_n = comp_calculator.num_each_component(occupation, sublattice_index=0)
    expected_total_n = np.array([10, 0, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    total_n = comp_calculator.num_each_component(occupation, sublattice_index=1)
    expected_total_n = np.array([10, 0, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    total_n = comp_calculator.num_each_component(occupation, sublattice_index=2)
    expected_total_n = np.array([0, 10, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    total_n = comp_calculator.num_each_component(occupation, sublattice_index=3)
    expected_total_n = np.array([0, 10, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=0)
    expected_mean_n = np.array([1.0, 0.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=1)
    expected_mean_n = np.array([1.0, 0.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=2)
    expected_mean_n = np.array([0.0, 1.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=3)
    expected_mean_n = np.array([0.0, 1.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=0)
    expected_species_frac = np.array([1.0, 0.0, 0.0])
    assert np.allclose(species_frac, expected_species_frac)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=1)
    expected_species_frac = np.array([1.0, 0.0, 0.0])
    assert np.allclose(species_frac, expected_species_frac)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=2)
    assert all([np.isnan(species_frac[i]) for i in range(len(species_frac))])

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=3)
    assert all([np.isnan(species_frac[i]) for i in range(len(species_frac))])

    # check (b)
    occupation[20] = 1  # set an "O" on sublattice_index=2
    total_n = comp_calculator.num_each_component(occupation)
    expected_total_n = np.array([20, 19, 1], dtype="int")
    assert (total_n == expected_total_n).all()

    mean_n = comp_calculator.mean_num_each_component(occupation)
    expected_mean_n = np.array([2.0, 1.9, 0.1])
    assert np.allclose(mean_n, expected_mean_n)

    species_frac = comp_calculator.species_frac(occupation)
    expected_species_frac = np.array([20.0 / 21.0, 0.0, 1.0 / 21.0])
    assert np.allclose(species_frac, expected_species_frac)

    # check (b-0)
    total_n = comp_calculator.num_each_component(occupation, sublattice_index=0)
    expected_total_n = np.array([10, 0, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    total_n = comp_calculator.num_each_component(occupation, sublattice_index=1)
    expected_total_n = np.array([10, 0, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    total_n = comp_calculator.num_each_component(occupation, sublattice_index=2)
    expected_total_n = np.array([0, 9, 1], dtype="int")
    assert (total_n == expected_total_n).all()

    total_n = comp_calculator.num_each_component(occupation, sublattice_index=3)
    expected_total_n = np.array([0, 10, 0], dtype="int")
    assert (total_n == expected_total_n).all()

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=0)
    expected_mean_n = np.array([1.0, 0.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=1)
    expected_mean_n = np.array([1.0, 0.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=2)
    expected_mean_n = np.array([0.0, 0.9, 0.1])
    assert np.allclose(mean_n, expected_mean_n)

    mean_n = comp_calculator.mean_num_each_component(occupation, sublattice_index=3)
    expected_mean_n = np.array([0.0, 1.0, 0.0])
    assert np.allclose(mean_n, expected_mean_n)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=0)
    expected_species_frac = np.array([1.0, 0.0, 0.0])
    assert np.allclose(species_frac, expected_species_frac)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=1)
    expected_species_frac = np.array([1.0, 0.0, 0.0])
    assert np.allclose(species_frac, expected_species_frac)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=2)
    expected_species_frac = np.array([0.0, 0.0, 1.0])
    assert np.allclose(species_frac, expected_species_frac)

    species_frac = comp_calculator.species_frac(occupation, sublattice_index=3)
    assert all([np.isnan(species_frac[i]) for i in range(len(species_frac))])
