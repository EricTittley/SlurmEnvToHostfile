# SlurmEnvToHostfile

## Overview
Create an MPI hostfile from the Slurm environment variables

While OpenMPI can interpret basic Slurm resource allocations, specifically a list of hosts with some number of processes per host, it fails for more complicated resource allocations where different numbers of processes per host are required.

This code currently produces a hostfile, named `hostfile`, appropriate for passing to `mpirun` as

```
mpirun -hostfile hostfile MyMPI.exe
```

The script needs more extensive testing and would benefit from:
* being able to produce an MPICH-compliant hostfile.
* accepting a flag for the hostfile name.

## Contributors

This code is maintained by Eric Tittley.

Based on [Christopher Hoffman's code](https://github.com/pftool/pftool/blob/master/scripts/pfscripts.py)
but extended to parse `SLURM_JOB_CPUS_PER_NODE correctly`, not just as a single integer.
