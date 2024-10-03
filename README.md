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