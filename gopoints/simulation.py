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
