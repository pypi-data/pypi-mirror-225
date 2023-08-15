
# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Numpy simulator backend."""

from .abstract_backend import AbstractBackend
from isq.simulate.simulator import simulate


class NumpySimBackend(AbstractBackend):

    def __init__(
        self,
        shots: int = 100,
    ) -> None:
        self.shots = shots

    def run(self, ir, **kw):
        """Run the quantum circuit by this method."""
        return dict(simulate(ir, run_time=self.shots, **kw))
