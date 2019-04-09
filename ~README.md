# SlurmEnvToHostfile

## Overview
Create an MPI hostfile from the Slurm environment variables

While OpenMPI can interpret basic Slurm resource allocations, specifically a list of hosts with some number of processes per host, it fails for more complicated resource allocations where different numbers of processes per host are required.

This code produces a hostfile, named `hostfile` by default, appropriate for passing to `mpirun` as

```
mpirun --hostfile hostfile MyMPI.exe
```

## Usage

From within a Slurm-provided environment:
```
SlurmEnvToHostfile
mpirun --hostfile hostfile MyMPI.exe
```

If arguments are passed to `SlurmEnvToHostfile.py``
```
python3 SlurmEnvToHostfile.py [OPTIONS]
mpirun --hostfile hostfile MyMPI.exe
```

### Options

`--hostfile` The name of the generated hostfile. Default `hostfile`

`--no-file`  Output to stdout
```
mpirun --host `python3 SlurmEnvToHostfile --no-file` MyMPI.exe
```   

`--style` The style of the hostfile can be set with the `--style` argument. Valid forms are
 * `--style=openmpi` OpenMPI-compliant [default]
 * `--style=mpich`   MPICH-compliant

## TODO

The script needs more extensive testing. Please report issues.

## Contributors

This code is maintained by Eric Tittley.

Contributors:
 Tilman Troester

Originally based on [Christopher Hoffman's code](https://github.com/pftool/pftool/blob/master/scripts/pfscripts.py)
but extended to parse `SLURM_JOB_CPUS_PER_NODE` correctly, not just as a single integer.
