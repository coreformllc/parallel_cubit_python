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