# Exploring parallel execution of Coreform Cubit
## Setup
Recommend creating a virtual environment.
Below are instructions for Windows 11, Powershell.

```powershell
python3.11.exe -m venv env
.\env\Scripts\Activate.ps1
python.exe -m pip install -r requirements.txt
```

## Executing
There are three examples:

1. Array
    * `src/array_example.py`
    * This example builds an NxNxN array of bricks and hex-meshes them in parallel
2. Mechanical
    * `src/mechanical_example.py`
    * This example builds a tetmesh on a mechanical assembly from NIST
3. Nuclear
    * `src/nuclear_example.py`
    * This example builds a surface mesh on the ITER example from Paramak

To execute, recommend creating a separate working directory and running the script from that location:

```powershell
mkdir path\to\workdir\array
cd path\to\workdir\array
python.exe path\to\array_example.py --num-proc 8 --array-size 8

mkdir path\to\workdir\mechanical
cd path\to\workdir\mechanical
python.exe path\to\mechanical_example.py --num-proc 8

mkdir path\to\workdir\nuclear
cd path\to\workdir\nuclear
python.exe path\to\nuclear_example.py --num-proc 8
```

When these execute they do the following:

1. Create a base model, either via CAD generation or importing a CAD file.
    * Saves this base model as `base_model.cub5` in the working directory
2. Distributes bodies in `num_proc` lists of approximately quantity of bodies
    * Exports a temporary file for each of the `num_proc` lists to `./tmp/proc_{p}.cub5` -- where `{p}` is an integer for the worker id.
3. Uses the [`multiprocessing`](https://docs.python.org/3.11/library/multiprocessing.html) library to map each temporary file to a worker within a `Pool`.
    * Each worker meshes its temporary file and saves the temporary file, overwriting it.
4. After completion, the main process creates a new Cubit file and imports each of the meshed temporary files.
    * Saves this meshed model as `base_model_meshed.cub5`

## Benchmark results

### Array

| Num Proc | Time (sec) | Speedup  | Expected Time (sec) |
|----------|------------|----------|---------------------|
| 1        | 23.79288   | 1        | 23.79288            |
| 2        | 15.29146   | 1.555958 | 11.89644            |
| 3        | 11.44965   | 2.078045 | 7.930959            |
| 4        | 8.893886   | 2.675195 | 5.94822             |
| 5        | 7.981742   | 2.980913 | 4.758576            |
| 6        | 7.33141    | 3.245335 | 3.96548             |
| 7        | 7.066741   | 3.366881 | 3.398983            |
| 8        | 6.751833   | 3.523914 | 2.97411             |

### Mechanical

| Num Proc | Time (sec) | Speedup  | Expected Time |
|----------|------------|----------|---------------|
| 1        | 36.40587   | 1        | 36.40587      |
| 2        | 30.80655   | 1.181758 | 18.20293      |
| 3        | 23.1821    | 1.57043  | 12.13529      |
| 4        | 19.451     | 1.871671 | 9.101467      |
| 5        | 19.12655   | 1.903421 | 7.281174      |
| 6        | 17.77591   | 2.048045 | 6.067645      |
| 7        | 19.75792   | 1.842596 | 5.200838      |
| 8        | 17.34634   | 2.098764 | 4.550734      |

### Nuclear

| Num Proc | Time (sec) | Speedup  | Expected Time |
|----------|------------|----------|---------------|
| 1        | 14.78449   | 1        | 14.78449      |
| 2        | 13.6472    | 1.083335 | 7.392244      |
| 3        | 12.97859   | 1.139145 | 4.928163      |
| 4        | 13.94882   | 1.05991  | 3.696122      |
| 5        | 11.18191   | 1.322179 | 2.956898      |
| 6        | 8.82909    | 1.67452  | 2.464081      |
| 7        | 9.088693   | 1.62669  | 2.11207       |
| 8        | 9.598481   | 1.540295 | 1.848061      |

## Discussion

The results above demonstrate that *it is* possible to use Python to perform parallel, process-based operations using Coreform Cubit's Python API, however the speedups in these examples are minimal to moderate.
It may be that a more sophisticated approach to distributing entities in order to better load-balance the workers would improve performance in the mechanical and nuclear examples.
It should also be noted that there is additional overhead that may not be encountered in a more traditional serial processing usage of Coreform Cubit: exporting multiple CUB5 files, reading them in and re-exporting after meshing, gathering all the partial files into a new monolithic file, etc.
This overhead cost may be alleviated by skipping the final gather in Coreform Cubit, instead exporting Exodus mesh files and using SEACAS tools (e.g., `ejoin`) to combine them.
Overhead may also be reduced if that parallel execution is performed across unique cases (e.g., a DoE sweep) wherein each case would need to be loaded separately even in the serial case.