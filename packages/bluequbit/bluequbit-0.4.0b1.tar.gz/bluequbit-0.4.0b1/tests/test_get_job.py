import pytest
import qiskit

import bluequbit


def test_get_job():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    result = dq_client.run(qc_qiskit)

    assert result.num_qubits == 2
    print(result)

    assert result.get_statevector().shape == (4,)
    assert len(result.get_counts()) == 2
    assert sum(result.get_counts().values()) == 1.0


def test_get_job2():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    result = dq_client.run(qc_qiskit)

    result = dq_client.get(result)

    assert result.circuit is not None
    assert result.circuit["circuit_type"] == "Qiskit"
    assert result.num_qubits == 2

    assert result.get_statevector().shape == (4,)
    assert len(result.get_counts()) == 2
    assert sum(result.get_counts().values()) == 1.0


def test_get_job_counts():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    qc_qiskit.measure_all()
    result = dq_client.run(qc_qiskit, shots=6)

    assert result.num_qubits == 2
    assert sum(result.get_counts().values()) == 6

    with pytest.raises(bluequbit.exceptions.BQJobStatevectorNotAvailableError) as e:
        result.get_statevector()
    assert (
        e.value.message
        == "Job run with shots > 0 or statevector is too large for"
        f" {result.num_qubits} qubits (job: {result.job_id}). Please use .get_counts()"
        " instead."
    )
