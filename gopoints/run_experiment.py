import os
import numpy as np
from pelutils import log, JobDescription
import matplotlib.pyplot as plt
from tqdm import tqdm

from gopoints.simulation import Simulation

def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq: http://www.statsdirect.com/help/content/image/stat0206_wmf.gif
    # from: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    array = array.astype(float)
    if np.amin(array) < 0:
        array -= np.amin(array) #values cannot be negative
    array += 0.0000001 #values cannot be 0
    array = np.sort(array) #values must be sorted
    index = np.arange(1,array.shape[0]+1) #index per array element
    n = array.shape[0]#number of array elements
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) #Gini coefficient

def run(args: JobDescription):
    simulation = Simulation(
        args.n,
        args.yn_a / 365,
        args.yn_b / 365,
        args.yn_c / 365,
        args.yn_d / 365,
        args.p_f,
        args.r_s,
        args.r_a,
        args.r_b,
        args.r_f,
        args.c_a,
        args.c_b,
    )
    for _ in tqdm(range(args.years * 365)):
        simulation.step()
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    axes = axes.flatten()
    axes[0].plot(
        [100 * (x | y).sum() / args.n for x, y in zip(simulation.pA, simulation.pB)]
    )
    axes[0].set_xlabel("Days")
    axes[0].set_ylabel(r"% users that do not have enough gopoints")
    axes[0].set_title("Users not affording action")

    axes[1].plot([np.mean(x) for x in simulation.x])
    axes[1].plot([np.quantile(x, 0.25) for x in simulation.x], ls="--", color="red", alpha=0.5)
    axes[1].plot([np.quantile(x, 0.75) for x in simulation.x], ls="--", color="red", alpha=0.5)
    axes[1].set_xlabel("Days")
    axes[1].set_ylabel(r"Mean and IQR wealth")
    axes[1].set_title("gopoint wealth")

    axes[2].plot(
        [100 * (x | y).sum() / args.n for x, y in zip(simulation.iA, simulation.iB)]
    )
    axes[2].set_xlabel("Days")
    axes[2].set_ylabel(r"% users not receiving wanted help")
    axes[2].set_title("Users not getting a match")

    axes[3].plot([100*gini(x) for x in simulation.x])
    axes[3].set_xlabel("Days")
    axes[3].set_ylabel(r"Gini coefficient [%]")
    axes[3].set_title("Inequality in gopoint economy")


    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    from pelutils import Parser, Argument

    parser = Parser(
        Argument("years", type=int),
        Argument("n", type=int),
        Argument("yn_a", type=int),
        Argument("yn_b", type=int),
        Argument("yn_c", type=int),
        Argument("yn_d", type=int),
        Argument("p_f", type=float),
        Argument("r_s", type=int),
        Argument("r_a", type=int),
        Argument("r_b", type=int),
        Argument("r_f", type=int),
        Argument("c_a", type=int),
        Argument("c_b", type=int),
        multiple_jobs=True,
    )

    jobs = parser.parse_args()
    parser.document()
    for job in jobs:
        log.configure(os.path.join(job.location, "simulation.log"))
        log.log_repo()
        log(f"Starting {job.name}")
        with log.log_errors:
            run(job)
