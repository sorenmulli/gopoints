from typing import Tuple
import numpy as np


class Simulation:
    """Handles state and transition for a single simulation"""

    def __init__(
        self,
        N: int,
        p_A: float,
        p_B: float,
        p_C: float,
        p_D: float,
        r_S: int,
        r_A: int,
        r_B: int,
        c_A: int,
        c_B: int,
    ):
        """
        See validation appendix for explanation of parameters
        """
        self.N = N

        self.p_A = p_A
        self.p_B = p_B
        self.p_C = p_C
        self.p_D = p_D

        self.r_S = r_S
        self.r_A = r_A
        self.r_B = r_B

        self.c_A = c_A
        self.c_B = c_B

        # Everyone starts as new users with signup amount of points
        self.X = np.ones(self.N) * self.r_S
        self.i = 0

    def sample(self, p: float) -> np.ndarray:
        return np.random.choice(2, self.N, p=[1 - p, p]).astype(bool)

    def do_matching(
        self, requester: np.ndarray, giver: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        diff = sum(giver) - sum(requester)
        ignored_requester = np.zeros(self.N, dtype=bool)
        ignored_giver = np.zeros(self.N, dtype=bool)
        # Some requesters will be ignored
        if diff < 0:
            ignored_requester[
                np.random.choice(np.where(requester)[0], abs(diff), replace=False)
            ] = True
            requester[ignored_requester] = False
        # Some givers will be ignored
        elif diff > 0:
            ignored_giver[
                np.random.choice(np.where(giver)[0], diff, replace=False)
            ] = True
            giver[ignored_giver] = False
        return ignored_requester, ignored_giver

    def step(self):

        mask_A = self.sample(self.p_A)
        mask_B = self.sample(self.p_B)
        mask_C = self.sample(self.p_C)
        mask_D = self.sample(self.p_D)

        # Exclude those that cannot afford it
        poor_A = self.X < self.c_A
        poor_B = self.X < self.c_B
        mask_A[poor_A] = False
        mask_B[poor_B] = False

        # Match conversation starts
        ignored_A, ignored_C = self.do_matching(mask_A, mask_C)
        # Match advice
        ignored_B, ignored_D = self.do_matching(mask_B, mask_D)

        assert mask_A.sum() == mask_C.sum(), self.i
        assert mask_B.sum() == mask_D.sum(), self.i

        self.i += 1


if __name__ == "__main__":
    # Test
    s = Simulation(100, 1 / 20, 1 / 10, 1 / 40, 1 / 20, 10, 5, 2, 2, 1)
    np.random.seed(0)
    for _ in range(100):
        s.step()
