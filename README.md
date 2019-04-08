# SlurmEnvToHostfile

## Overview
Create an MPI hostfile from the Slurm environment variables

While OpenMPI can interpret basic Slurm resource allocations, specifically a list of hosts with some number of processes per host, it fails for more complicated resource allocations where different numbers of processes per host are required.

This code currently produces a hostfile, named `hostfile` by default, appropriate for passing to `mpirun` as

```
mpirun --hostfile hostfile MyMPI.exe
```

The name of the generated hostfile can be specified with the `--hostfile` option. Alternatively, the `--host` option of 
`mpirun` can be used by calling `SlurmEnvToHostfile` with the `--no-file` option:

```
mpirun --host `SlurmEnvToHostfile --no-file` MyMPI.exe
```

The script needs more extensive testing and would benefit from:
* being able to produce an MPICH-compliant hostfile.

## Contributors

This code is maintained by Eric Tittley.

Based on [Christopher Hoffman's code](https://github.com/pftool/pftool/blob/master/scripts/pfscripts.py)
but extended to parse `SLURM_JOB_CPUS_PER_NODE` correctly, not just as a single integer.
