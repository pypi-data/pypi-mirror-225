# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""JAX backend."""

from .abstract_backend import AbstractBackend
from isq.simulate.simulator import getprobs


class JaxBackend(AbstractBackend):

    def run(self, ir, **kw):
        """Run the quantum circuit by this method."""
        return getprobs(ir, mod=1, **kw)
