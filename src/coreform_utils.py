import os
import sys
import pathlib
import psutil

def mk_script_relative( filepath ):
    path_to_this_script = os.path.dirname( os.path.realpath( filepath ) )
    def script_relative( relpath ):
        return pathlib.Path(os.path.normpath( os.path.join( path_to_this_script, relpath ))).as_posix()
    return script_relative

# Get the number of physical cores (excluding hyper-threading)
def get_physical_cores():
    return psutil.cpu_count( logical=False )

# Get the number of logical cores (including hyper-threading)
def get_logical_cores():
    return psutil.cpu_count( logical=True )

# Import Coreform Cubit module
def import_cubit( verbose=False ):
    if "win" in sys.platform:
        path_to_cubit = r"C:\Program Files\Coreform Cubit 2024.8\bin"
    elif "lin" in sys.platform:
        path_to_cubit = "/opt/Coreform-Cubit-2024.8/bin"
    sys.path.append( path_to_cubit )
    import cubit
    if verbose:
        cubit.init( [] )
    else:
        cubit.init( [ "cubit", "-noecho", "-nojournal", "-information", "off", "-warning", "off" ])
    return cubit
