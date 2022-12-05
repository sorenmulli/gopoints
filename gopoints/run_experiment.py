import os
from pelutils import log, JobDescription

from gopoints.simulation import Simulation


def run(args: JobDescription):
    simulation = Simulation(
        args.n,
        args.p_a,
        args.p_b,
        args.p_c,
        args.p_d,
        args.r_s,
        args.r_a,
        args.r_b,
        args.c_a,
        args.c_b,
    )
    for _ in range(args.steps):
        simulation.step()


if __name__ == "__main__":
    from pelutils import Parser, Argument

    parser = Parser(
        Argument("steps", type=int),
        Argument("n", type=int),
        Argument("p_a", type=float),
        Argument("p_b", type=float),
        Argument("p_c", type=float),
        Argument("p_d", type=float),
        Argument("r_s", type=int),
        Argument("r_a", type=int),
        Argument("r_b", type=int),
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
