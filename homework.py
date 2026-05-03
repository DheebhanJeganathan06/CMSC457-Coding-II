from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def ghz_x_meas():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.x(0)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc

def superdense_alice(x, z):
    qc = QuantumCircuit(1)
    if x:
        qc.x(0)
    if z:
        qc.z(0)
    return qc

def superdense_bob():
    qc = QuantumCircuit(2, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
    return qc

def teleport_alice(qreg: QuantumRegister, creg: ClassicalRegister):
    qc = QuantumCircuit(qreg, creg)
    qc.cx(qreg[0], qreg[1])
    qc.h(qreg[0])
    qc.measure(qreg[0], creg[0])
    qc.measure(qreg[1], creg[1])
    return qc

def swap_charlie(qreg: QuantumRegister, creg: ClassicalRegister):
    qc = QuantumCircuit(qreg, creg)
    qc.h(qreg[0])
    qc.cx(qreg[0], qreg[1])
    return qc


def swap_alice(qreg: QuantumRegister, creg: ClassicalRegister):
    qc = QuantumCircuit(qreg, creg)
    qc.h(qreg[0])
    qc.measure(qreg[0], creg[0])
    return qc

def error_to_syndrome(pauli, wire):
    stabilizers = [
        "XZZXI",
        "IXZZX",
        "XIXZZ",
        "ZXIXZ",
        "ZZXIX",
    ]

    w = wire - 1
    syndrome = ""

    for stab in stabilizers:
        s = stab[w]
        bit = 0
        if pauli == "X":
            if s == "Z":
                bit = 1
        elif pauli == "Z":
            if s == "X":
                bit = 1
        elif pauli == "XZ":
            if s in ("X", "Z"):
                bit = 1
        syndrome += str(bit)

    return syndrome

def measure_one_syndrome(data, ancilla, creg, synd):
    qc = QuantumCircuit(data, ancilla, creg)
    qc.h(ancilla[0])

    for i, p in enumerate(synd):
        if p == 'X':
            qc.cx(ancilla[0], data[i])
        elif p == 'Z':
            qc.cz(ancilla[0], data[i])

    qc.h(ancilla[0])
    qc.measure(ancilla[0], creg[0])
    return qc