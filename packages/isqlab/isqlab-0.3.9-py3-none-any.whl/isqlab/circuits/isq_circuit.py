# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Isq quantum circuit object."""

from isqlab.backend import (
    AbstractBackend,
    TorchBackend,
    AutogradBackend,
    JaxBackend,
    NumpySimBackend,
)
import os
import numpy as np

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


class IsqCircuitError(Exception):
    """IsQ quantum circuits error."""


class IsqCircuit:
    """IsQ quantum circuit class."""

    def __init__(
        self,
        isq_file: str,
        backend: AbstractBackend,
        dict_format: bool = False,
    ) -> None:

        cwd = os.getcwd()

        if isq_file.endswith(".isq"):
            compile_cmd = f"isqc compile --target qcis {isq_file}"
            return_val = os.system(compile_cmd)
            if return_val != 0:
                raise IsqCircuitError(
                    f"Compile failed! Error code: {return_val}.")
            qcis_path = os.path.join(
                cwd,
                os.path.splitext(isq_file)[0] + ".qcis",
            )
        elif isq_file.endswith(".qcis"):
            qcis_path = os.path.join(cwd, isq_file)

        with open(qcis_path, "r") as qcis:
            self.qcis = qcis.read()

        self.backend = backend
        self.dict_format = dict_format

    def __repr__(self) -> str:
        return self.qcis

    __str__ = __repr__

    def measure(self, **kw):
        measure_result = self.backend.run(self.qcis, **kw)
        if isinstance(measure_result, dict):
            if self.dict_format:
                return measure_result
            return self._dict2array(measure_result)
        return measure_result

    def pauli_measure(self, **kw):

        if self.dict_format:
            measure_result_dict = self.measure(**kw)
            if not isinstance(measure_result_dict, dict):
                raise IsqCircuitError(
                    f"Dict format is not supported with the {self.backend}",
                )
            result = 0
            for res_index, frequency in measure_result_dict.items():
                parity = (-1) ** (res_index.count("1") % 2)
                # e.g. {"011": 222}, to count "1"
                result += parity * frequency / self.backend.shots
            return result

        if isinstance(self.backend, AutogradBackend):
            measure_result_list = self.measure(**kw)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return anp.dot(measure_result_list, anp.array(parity))

        elif isinstance(self.backend, JaxBackend):
            measure_result_list = self.measure(**kw)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return jnp.vdot(jnp.array(measure_result_list), jnp.array(parity))

        elif isinstance(self.backend, TorchBackend):
            measure_result_list = self.measure(**kw)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return torch.dot(
                measure_result_list,
                torch.tensor(parity).type_as(measure_result_list),
            )
        else:
            measure_result_list = self.measure(**kw)
            parity = [(-1) ** (str(bin(int(index))).count("1") % 2)
                      for index in range(len(measure_result_list))]
            return np.dot(measure_result_list, np.array(parity))

    def _dict2array(
        self,
        result_dicts: dict,
    ) -> np.ndarray:
        """Transfer measurement results from Dict to Array."""
        shots = self.backend.shots
        len_array = len(list(result_dicts.keys())[0])
        results_arrays = np.zeros(2 ** len_array)

        for bin_idx, freq in result_dicts.items():
            results_arrays[int(bin_idx, 2)] = float(freq/shots)
        return results_arrays
