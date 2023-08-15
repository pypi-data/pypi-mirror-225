from qiskit import QuantumCircuit
from qiskit.primitives import Estimator
from qiskit.opflow import I, X, Y, Z

estimator = Estimator()
circuit = QuantumCircuit(4)
circuit.h(0)
circuit.cz(1, 2)
circuit.cx(0, 1)
circuit.x(2)

h_cost = '1 * ( 1 * (Y^Z^Y^I) + 1 * (I^X^Z^X) + 1 * (I^I^Z^Z) + 1 * (Z^I^I^Z)) / 2'

hamiltonian = eval(h_cost)

expectation_value = estimator.run(circuit, hamiltonian).result().values
print(expectation_value)