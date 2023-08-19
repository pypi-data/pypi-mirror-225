import sys
from pathlib import Path

import cirq
import pytest
import qiskit.circuit.library as qcl
from qiskit import QuantumCircuit
from qiskit_finance.circuit.library.probability_distributions import (
    LogNormalDistribution,
    NormalDistribution,
)

import bluequbit

sys.path.append(Path(__file__).parent)
from bluequbit_test_lib import cirq_textbook_algorithms as algos  # noqa: E402

nqubits = 3

# Should be equivalent to the circuits being tested in deqart_backend.
circuits = [
    qcl.QFT(nqubits),
    qcl.QuantumVolume(nqubits),
    qcl.ExactReciprocal(2, 0.5),
    # Disabled for now because Qiskit has serialization roundtrip problem.
    # qcl.FourierChecking([1, -1, -1, -1], [1, 1, -1, -1]),
    qcl.IQP([[6, 5, 3], [5, 4, 5], [3, 5, 1]]),
]

# Grover circuit.
oracle = QuantumCircuit(2)
oracle.z(0)  # good state = first qubit is |1>
grover = qcl.GroverOperator(oracle, insert_barriers=True)
circuits.append(grover)

# Adder circuit
qc_adder = QuantumCircuit(3)
qc_adder.rz(0.5, 0)
qc_adder.rz(0.6, 1)
# 1 + 1 qubits
adder = qcl.DraperQFTAdder(1, kind="half")
qc_adder.append(adder, range(adder.num_qubits))
circuits.append(qc_adder)

# Multiplier circuit
qc_multiplier = QuantumCircuit(5)
qc_multiplier.rz(0.5, 0)
qc_multiplier.rz(0.6, 1)
# 1 x 1 qubits
mul = qcl.HRSCumulativeMultiplier(1)
qc_multiplier.append(mul, range(mul.num_qubits))
circuits.append(qc_multiplier)

circuits.extend(
    [
        NormalDistribution(3, mu=1, sigma=1, bounds=(0, 2)),
        LogNormalDistribution(
            [2, 2, 2], [1, 0.9, 0.2], [[1, -0.2, 0.2], [-0.2, 1, 0.4], [0.2, 0.4, 1]]
        ),
    ]
)

# Now we add Cirq circuits
circuits.extend(
    [algos.make_qft(3), algos.phase_estimation(0.123456, 3), algos.make_grover(3)]
)


@pytest.mark.parametrize("circuit", circuits)
def test_bq_run_circuit(circuit):
    bq = bluequbit.init()
    bq.run(circuit)


def test_temporary_validate_productofsums_cirq():
    qs = cirq.LineQubit.range(2)
    c = cirq.Circuit([cirq.ry(0.5).on(qs[1]).controlled_by(qs[0])])
    bq = bluequbit.init()
    bq.run(c)


def test_qiskit_cy():
    # See https://trello.com/c/0SMvJuLV/266-productofsums-issue
    qc_qiskit = QuantumCircuit(2)
    qc_qiskit.cy(0, 1)
    bq = bluequbit.init()
    bq.run(qc_qiskit)


def test_cirq_controlled_ry():
    # See https://trello.com/c/0SMvJuLV/266-productofsums-issue
    # Basically same as test_cirq_cy, except in Cirq.
    qs = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([cirq.ry(0.5).on(qs[1]).controlled_by(qs[0])])
    bq = bluequbit.init()
    bq.run(circuit)


@pytest.mark.parametrize("seed", range(4))
def test_cirq_random_circuit(seed):
    qubits = [cirq.NamedQubit(f"q_{i}") for i in range(7)]
    circuit = cirq.testing.random_circuit(qubits, 5, 0.7, random_state=seed)
    bq = bluequbit.init()
    bq.run(circuit)


def test_cirq_circuit_with_non_terminal_measurements():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.measure(qubits, key="measure1"))
    circuit.append(cirq.X(qubits[0]))
    circuit.append(cirq.X(qubits[1]))
    circuit.append(cirq.measure(qubits, key="measure2"))
    bq = bluequbit.init()
    with pytest.raises(bluequbit.exceptions.BQJobNotCompleteError) as e_info:
        bq.run(circuit)
        assert "FAILED_VALIDATION. Mid-circuit measurements" in str(e_info)


def test_cirq_circuit_with_terminal_measurements_only():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[0]))
    circuit.append(cirq.X(qubits[1]))
    circuit.append(cirq.measure(qubits, key="measure1"))
    bq = bluequbit.init()
    bq.run(circuit)


@pytest.mark.parametrize("circuit", [None, 42, "42"])
def test_invalid_object(circuit):
    bq = bluequbit.init()
    with pytest.raises(Exception) as e_info:
        bq.run(circuit)
        assert "Unsupported circuit type" in str(e_info)


def test_empty_circuit():
    bq = bluequbit.init()
    circuit = cirq.Circuit()
    with pytest.raises(bluequbit.exceptions.BQJobNotCompleteError) as e_info:
        bq.run(circuit)
        assert "FAILED_VALIDATION. The circuit is empty" in str(e_info)
