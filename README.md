# SlurmEnvToHostfile
Create an MPI hostfile from the Slurm environment variables

While OpenMPI can interpret basic Slurm resource allocations, specifically a list of hosts with some number of processes per host, it fails for more complicated resource allocations where different numbers of processes per host are required.

This code currently produces a hostfile, named hostfile, appropriate for passing to mpirun as

mpirun -hostfile hostfile MyMPI.exe

The script needs more extensive testing and would benefit from:
* being able to produce an MPICH-compliant hostfile.
* accepting a flag for the hostfile name.
