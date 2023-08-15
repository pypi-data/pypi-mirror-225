# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Quantum circuit object."""

from isq import LocalDevice, quantumCor, TaskState
from isq.device.device import Device, AwsDevice, QcisDevice, ScQDevice
from typing import Callable, Union, Sequence, Literal, Optional, Any
from functools import partial
import numpy as np
import itertools
import time
import re


try:
    import jax.numpy as jnp
    HAS_JAX = True
except Exception:
    HAS_JAX = False

try:
    import torch
    HAS_TORCH = True
except Exception:
    HAS_TORCH = False

try:
    from autograd import numpy as anp
    HAS_AUTOGRAD = True
except Exception:
    HAS_AUTOGRAD = False

SIMULATOR_METHOD = Literal["simulator", "autograd", "jax", "torch", "pytorch"]
Tensor = Any


class QuantumCircuitError(Exception):
    """Quantum circuits error."""


class QuantumCircuit:
    """Quantum circuit class."""

    def __init__(
        self,
        num_qubits: Optional[int] = 1,
        backend: Device = None,
        method: SIMULATOR_METHOD = "autograd",
        dict_format: bool = False,
        sleep_time: int = 3,
        run_time: Optional[int] = None,
        init_circuit: bool = True,
        qubit_var: str = "q",
    ) -> None:

        if backend is None:
            backend = LocalDevice()

        self.use_hardware = False
        self.run_time = None
        self.sleep_time = None
        if isinstance(backend, (AwsDevice, QcisDevice, ScQDevice)):
            self.use_hardware = True
            self.run_time = run_time
            self.sleep_time = sleep_time
        # When using hardware, `method` is invalid

        if method == "jax":
            if not HAS_JAX:
                raise QuantumCircuitError("Jax is not installed.")

        if method == "autograd":
            if not HAS_AUTOGRAD:
                raise QuantumCircuitError("Autograd is not installed.")

        if method in ["torch", "pytorch"]:
            if not HAS_TORCH:
                raise QuantumCircuitError("Pytorch is not installed.")

        self._circuit_recording = []  # to record isqfile
        self._measure_recording = []  # to recoed measurement
        self.is_pauli_measure = False

        self.backend = backend
        self.method = method
        self.dict_format = dict_format

        self.qubit_var = qubit_var
        self.num_qubits = num_qubits
        if init_circuit:
            self._qbit_init(num_qubits)

    def __repr__(self) -> str:  # print isqfile
        return "\n".join(self.circuit)

    __str__ = __repr__

    def __len__(self) -> int:
        return len(self.circuit)

    @property
    def idx(self) -> int:
        return len(self.circuit)

    def __getitem__(self, key: int) -> str:
        return self.circuit[key]

    def __iter__(self):
        return (item for item in self.circuit)

    @property
    def circuit(self) -> list:
        return self._circuit_recording + self._measure_recording

    def qir(self, **kw) -> str:
        if kw is None:
            return self.backend.compile_to_ir(self.__repr__())
        self.backend.compile_with_par(self.__repr__(), **kw)
        return self.backend.get_ir()

    def extend(
        self,
        circuit: "QuantumCircuit",
    ) -> None:
        self._circuit_recording.extend(circuit._circuit_recording)

    def insert(
        self,
        start: int,
        end: int,
        reverse: bool = True
    ) -> None:
        """
        insert part of circuits inversely.
        """

        insert_list = self[start:end]
        if reverse:
            insert_list = insert_list[::-1]
        self._circuit_recording.extend(insert_list)

    def inv(
        self,
        func: Callable,
        *args,
        **kw
    ) -> None:
        """
        Insert a part of circuit inversely from a function.
        """
        start = self.idx
        func(*args, **kw)
        end = self.idx
        insert_list = self[start:end][::-1]
        for i in range(end-start):
            _ = self._circuit_recording.pop()
        self._circuit_recording.extend(insert_list)

    def _qbit_init(
        self,
        num_qubits: int,
    ) -> None:
        """
        Qubits initialization.
        """
        if num_qubits < 0:
            raise QuantumCircuitError(
                f"Number of inputs cannot be negative: {num_qubits}!")

        self._circuit_recording.append(f"qbit {self.qubit_var}[{num_qubits}];")

    def _one_qubit_op(
        self,
        qubit_idx: int,
        operation: str,
    ) -> None:
        """
        General one qubit operations.
        """
        self._circuit_recording.append(
            f"{operation}({self.qubit_var}[{qubit_idx}]);")

    def h(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "H"
        self._one_qubit_op(qubit_idx, operation)

    def x(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "X"
        self._one_qubit_op(qubit_idx, operation)

    def y(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Y"
        self._one_qubit_op(qubit_idx, operation)

    def z(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Z"
        self._one_qubit_op(qubit_idx, operation)

    def s(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "S"
        self._one_qubit_op(qubit_idx, operation)

    def sd(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "SD"
        self._one_qubit_op(qubit_idx, operation)

    def t(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "T"
        self._one_qubit_op(qubit_idx, operation)

    def td(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "TD"
        self._one_qubit_op(qubit_idx, operation)

    def x2p(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate pi/2"""
        operation = "X2P"
        self._one_qubit_op(qubit_idx, operation)

    def x2m(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate -pi/2"""
        operation = "X2M"
        self._one_qubit_op(qubit_idx, operation)

    def y2p(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate pi/2"""
        operation = "Y2P"
        self._one_qubit_op(qubit_idx, operation)

    def y2m(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate -pi/2"""
        operation = "Y2M"
        self._one_qubit_op(qubit_idx, operation)

    def m(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "M"
        self._one_qubit_op(qubit_idx, operation)

    def H(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "H"
        self._one_qubit_op(qubit_idx, operation)

    def X(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "X"
        self._one_qubit_op(qubit_idx, operation)

    def Y(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Y"
        self._one_qubit_op(qubit_idx, operation)

    def Z(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Z"
        self._one_qubit_op(qubit_idx, operation)

    def S(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "S"
        self._one_qubit_op(qubit_idx, operation)

    def SD(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "SD"
        self._one_qubit_op(qubit_idx, operation)

    def T(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "T"
        self._one_qubit_op(qubit_idx, operation)

    def TD(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "TD"
        self._one_qubit_op(qubit_idx, operation)

    def X2P(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate pi/2"""
        operation = "X2P"
        self._one_qubit_op(qubit_idx, operation)

    def X2M(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate -pi/2"""
        operation = "X2M"
        self._one_qubit_op(qubit_idx, operation)

    def Y2P(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate pi/2"""
        operation = "Y2P"
        self._one_qubit_op(qubit_idx, operation)

    def Y2M(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate -pi/2"""
        operation = "Y2M"
        self._one_qubit_op(qubit_idx, operation)

    def M(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "M"
        self._one_qubit_op(qubit_idx, operation)

    def _two_qubits_op(
        self,
        qubit_control: int,
        qubit_target: int,
        operation: str,
    ) -> None:
        """
        General two qubit operations.
        """
        self._circuit_recording.append(
            f"{operation}({self.qubit_var}[{qubit_control}], {self.qubit_var}[{qubit_target}]);")

    def cnot(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CNOT"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def cx(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CX"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def cy(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CY"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def cz(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CZ"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CNOT(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CNOT"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CX(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CX"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CY(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CY"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CZ(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CZ"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def _rotate_gate(
        self,
        param: Union[float, str],
        qubit_idx: int,
        operation: str,
    ) -> None:
        """
        General rotion operations.
        """
        self._circuit_recording.append(
            f"{operation}({param}, {self.qubit_var}[{qubit_idx}]);")

    def rx(
        self,
        param: Union[float, str],
        qubit_idx: int,
    ) -> None:
        operation = "RX"
        self._rotate_gate(param, qubit_idx, operation)

    def ry(
        self,
        param: Union[float, str],
        qubit_idx: int,
    ) -> None:
        operation = "RY"
        self._rotate_gate(param, qubit_idx, operation)

    def rz(
        self,
        param: Union[float, str],
        qubit_idx: int,
    ) -> None:
        operation = "RZ"
        self._rotate_gate(param, qubit_idx, operation)

    def RX(
        self,
        param: Union[float, str],
        qubit_idx: int,
    ) -> None:
        operation = "RX"
        self._rotate_gate(param, qubit_idx, operation)

    def RY(
        self,
        param: Union[float, str],
        qubit_idx: int,
    ) -> None:
        operation = "RY"
        self._rotate_gate(param, qubit_idx, operation)

    def RZ(
        self,
        param: Union[float, str],
        qubit_idx: int,
    ) -> None:
        operation = "RZ"
        self._rotate_gate(param, qubit_idx, operation)

    def rxy(
        self,
        phi: Union[float, str],
        theta: Union[float, str],
        qubit_idx: int,
    ) -> None:
        self._circuit_recording.append(
            f"RXY({phi}, {theta}, {self.qubit_var}[{qubit_idx}]);")

    RXY = rxy

    def add_gate(
        self,
        gate_name: str,
        matrix: Union[list, np.ndarray],
    ) -> None:
        """add gates manually"""
        quantumCor.addGate(gate_name, matrix)
        cm_gate_name = partial(self.cm, gate_name)
        setattr(self, gate_name, cm_gate_name)

    def cm(
        self,
        gate_name: str,
        *qubit_idx: Union[Sequence[int], int],
    ) -> None:
        """
        Customized gates.
        """
        para_list = []
        for idx in qubit_idx:
            para_list.append(f"{self.qubit_var}[{idx}]")
        para_str = ", ".join(para_list)
        self._circuit_recording.append(f"{gate_name}({para_str});")

    def measure_qubit(
        self,
        *qubit_idx: Union[Sequence[int], int],
    ) -> None:
        """
        Specifies the object to be measured.
        """

        self.is_pauli_measure = False
        self._len_qubit_measure = len(qubit_idx)
        # reset measurement
        self._measure_recording = []

        for idx in qubit_idx:
            self._measure_recording.append(f"M({self.qubit_var}[{idx}]);")

    # these abbr are for brother Long
    measu_qubit = measure_qubit
    mqbit = measure_qubit
    # these abbr are for brother Long

    def measure(
        self,
        **params,
    ) -> Sequence[Tensor]:
        """
        Forward calculation.
        """

        if self.is_pauli_measure:
            print("Warning: don't use pauli measurement after giving pauli operators.")

        if self.use_hardware:
            task = self._measure_hardware(**params)
            if self.dict_format:
                return task.result()
            return self._dict2array(task.result())

        if self.method == "simulator":
            results_dict = self.backend.run(self.__repr__(), **params)
            if self.dict_format:
                return results_dict
            return self._dict2array(results_dict)

        elif self.method == "autograd":
            return self.backend.probs(self.__repr__(), mod=0, **params)

        elif self.method == "jax":
            return self.backend.probs(self.__repr__(), mod=1, **params)

        elif self.method in ["torch", "pytorch"]:
            return self.backend.probs(self.__repr__(), mod=2, **params)

        else:
            raise NotImplementedError("Undefined method.")

    def _measure_hardware(self, **params) -> dict:
        """Using quantum hardwares."""
        task = self.backend.run(self.__repr__(), **params)
        # TODO:Expose the cancel API
        # self.task_cancel = task.cancel
        start_time = time.time()
        while task.state == TaskState.WAIT:
            task.result()
            # Wait for a period of time before doing an http request
            time.sleep(self.sleep_time)
            if self.run_time is not None:
                if time.time() > start_time + self.run_time:
                    break
        return task

    def _dict2array(
        self,
        result_dicts: dict,
    ) -> np.ndarray:
        """
        Transfer measurement results from Dict to Array.
        """
        shots = self.backend.shots
        # results_list = [0.0] * (2 ** self._len_qubit_measure)
        results_arrays = np.zeros(2 ** self._len_qubit_measure)

        for bin_idx, freq in result_dicts.items():
            results_arrays[int(bin_idx, 2)] = float(freq/shots)
        return results_arrays

    def pauli(
        self,
        gates: Union[str, tuple],
        format: str = "str",
    ) -> None:
        """
        Pauli measurement.
        """

        self._measure_recording = []  # reset measurement
        self.is_pauli_measure = True

        if format == "str":
            if not isinstance(gates, str):
                raise TypeError(f"Strings are needs but get f{type(gates)}")
            gate_op = re.findall("[a-zA-Z]+", gates)
            gate_idx = [int(idx) for idx in re.findall("[0-9]+", gates)]
            if len(gate_op) != len(gate_idx):
                raise ValueError("Illegal pauli measurement.")
            gates = zip(gate_idx, gate_op)

        elif format == "openfermion":
            pass

        else:
            raise QuantumCircuitError(f"Unsupported format {format!s}")

        for gate in gates:
            if gate[1].upper() == "X":
                self._measure_recording.append(
                    f"H({self.qubit_var}[{gate[0]}]);",
                )
                self._measure_recording.append(
                    f"M({self.qubit_var}[{gate[0]}]);",
                )
            elif gate[1].upper() == "Y":
                self._measure_recording.append(
                    f"X2P({self.qubit_var}[{gate[0]}]);",
                )
                self._measure_recording.append(
                    f"M({self.qubit_var}[{gate[0]}]);",
                )
            elif gate[1].upper() == "Z":
                self._measure_recording.append(
                    f"M({self.qubit_var}[{gate[0]}]);",
                )
            else:
                raise ValueError("Please input correct Pauli gates.")

    def pauli_measure(self, **params) -> Tensor:
        """
        Pauli measurement.
        """

        if not self.is_pauli_measure:
            print("Warning: using pauli measurement without giving pauli operators.")

        if self.use_hardware:
            task = self._measure_hardware(**params)
            measure_result_dict = task.result()
            result = 0
            for res_index, frequency in measure_result_dict.items():
                parity = (-1) ** (res_index.count("1") % 2)
                # e.g. {"011": 222}, to count "1"
                result += parity * frequency / self.backend.shots
            return result

        if self.method == "simulator":
            measure_result_dict = self.backend.run(self.__repr__(), **params)
            result = 0
            for res_index, frequency in measure_result_dict.items():
                parity = (-1) ** (res_index.count("1") % 2)
                # e.g. {"011": 222}, to count "1"
                result += parity * frequency / self.backend.shots
            return result

        elif self.method == "autograd":
            measure_result_list = self.backend.probs(
                self.__repr__(), mod=0, **params)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return anp.dot(measure_result_list, anp.array(parity))

        elif self.method == "jax":
            measure_result_list = self.backend.probs(
                self.__repr__(), mod=1, **params)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return jnp.vdot(jnp.array(measure_result_list), jnp.array(parity))

        elif self.method in ["torch", "pytorch"]:
            measure_result_list = self.backend.probs(
                self.__repr__(), mod=2, **params)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return torch.dot(
                measure_result_list,
                torch.tensor(parity).type_as(measure_result_list),
            )

        else:
            raise NotImplementedError("Undefined method.")

    def state(self, **params) -> Tensor:
        """To get state by simulation."""

        if self.use_hardware or self.method == "simulator":
            raise QuantumCircuitError(
                "Current method do not support state output!")

        if self.method == "autograd":
            return self.backend.state(self.__repr__(), mod=0, **params)

        elif self.method == "jax":
            return self.backend.state(self.__repr__(), mod=1, **params)

        elif self.method in ["torch", "pytorch"]:
            return self.backend.state(self.__repr__(), mod=2, **params)

        else:
            raise NotImplementedError("Undefined method.")

    def append_isqstr(
        self,
        isq_str: str,
    ) -> None:
        """Append strings to quantum circuit object."""
        for isq_line in isq_str.splitlines():
            if len(isq_line) != 0:
                self._circuit_recording.append(isq_line.strip())

    @classmethod
    def str2circuit(
        cls,
        isq_str: str,
    ) -> "QuantumCircuit":
        """Convert strings to quantum circuits."""
        circuit = cls(init_circuit=False)
        circuit.append_isqstr(isq_str)
        return circuit

    def append_isqfile(
        self,
        filename: str,
        mode: str = "r",
    ) -> None:
        """Append a file to quantum circuits."""
        with open(filename, mode) as isqfile:
            self.append_isqstr(isqfile.read())

    @classmethod
    def file2circuit(
        cls,
        filename: str,
        mode: str = "r",
    ) -> "QuantumCircuit":
        """Convert a file to quantum circuit object."""
        circuit = cls(init_circuit=False)
        circuit.append_isqfile(filename, mode)
        return circuit

    def circuit2file(
        self,
        filename: str,
        mode: str = "x",
    ) -> None:
        """Convert a quantum circuits to a file."""
        with open(filename, mode) as isqfile:
            isqfile.write(self.__repr__())

    def chain(
        self,
        gate_name: str,
        qubit_idx: Optional[Sequence] = None,
    ) -> None:
        """Act on each qubit and the next in turn"""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits - 1))
        operation = getattr(self, gate_name)
        for idx in qubit_idx:
            # self._two_qubits_op(idx, idx+1, gate_name)
            operation(idx, idx+1)

    def ring(
        self,
        gate_name: str,
        num_qubits: Optional[int] = None,
    ) -> None:
        """Act on all qubits via a ring"""
        if num_qubits is None:
            num_qubits = self.num_qubits
        if num_qubits < 2:
            raise ValueError(
                f"Number of qubits have to be larger than 1 but given {num_qubits}")
        operation = getattr(self, gate_name)
        for num_qubit in range(num_qubits-1):
            operation(num_qubit, num_qubit+1)
        operation(num_qubits-1, 0)

    def single(
        self,
        gate_name: str,
        qubit_idx: Optional[Sequence] = None,
    ) -> None:
        """Act on each qubit in turn"""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        operation = getattr(self, gate_name)
        for idx in qubit_idx:
            # self._one_qubit_op(idx, gate_name)
            operation(idx)

    def perm(
        self,
        gate_name: str,
        qubit_idx: Optional[Sequence] = None,
    ) -> None:
        """Permutation of all."""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        operation = getattr(self, gate_name)
        for idx in itertools.permutations(qubit_idx, 2):
            operation(*idx)

    def comb(
        self,
        gate_name: str,
        qubit_idx: Optional[Sequence] = None,
    ) -> None:
        """combinations of all."""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        operation = getattr(self, gate_name)
        for idx in itertools.combinations(qubit_idx, 2):
            operation(*idx)

    def param(
        self,
        gate_name: str,
        qubit_idx: Optional[Sequence] = None,
        param_name: str = "x",
        param_idx: Optional[Sequence] = None,
    ) -> None:
        """Quickly build parameterized circuits"""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        if param_idx is None:
            param_idx = qubit_idx
        operation = getattr(self, gate_name)
        for pidx, qidx in zip(param_idx, qubit_idx):
            operation(f"{param_name}[{pidx}]", qidx)

    def cmt(self, comments: Optional[str] = None) -> None:
        """Add comments"""
        if comments is None:
            self._circuit_recording.append("")
        elif isinstance(comments, str):
            self._circuit_recording.append(f"// {comments}")

    def draw(
        self,
        show_param: bool = False,
        **kw,
    ) -> None:
        from isq import Drawer
        drawer = Drawer(showparam=show_param)
        drawer.plot(self.qir(**kw))
