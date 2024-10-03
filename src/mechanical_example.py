import os
import sys
import glob
import multiprocessing
import time
import argparse

import coreform_utils
cubit = coreform_utils.import_cubit()
script_relative = coreform_utils.mk_script_relative( __file__ )
num_physical_cores = coreform_utils.get_physical_cores()

parser = argparse.ArgumentParser()
def input_args():
    parser.add_argument( "--num-proc", "-np", dest="num_proc", type=int, default=num_physical_cores )
    args = parser.parse_args()
    return args

## Base Model
def create_base_model():
    cubit.cmd( "reset" )
    filename = script_relative( "../cad/nist_mtc_crada_assembly_rev-D.sab" )
    cubit.cmd( f"import acis '{filename}'" )
    cubit.cmd( "save cub5 'base_model.cub5' overwrite" )

## Distribute and gather
def distribute( num_proc ):
    if os.path.isdir( 'tmp' ) == False:
        os.makedirs( 'tmp' )
    cubit.cmd( "reset" )
    cubit.cmd( "open 'base_model.cub5'" )
    B = cubit.get_entities( "body" )
    avg_size = len( B ) // num_proc
    remainder = len( B ) % num_proc
    # List comprehension to generate sublists
    sublists = [
        B[i * avg_size + min(i, remainder):(i + 1) * avg_size + min(i + 1, remainder)]
        for i in range( num_proc )
    ]
    filenames = []
    for p in range( 0, num_proc ):
        proc_body_list = cubit.get_id_string( sublists[p] )
        filenames.append( os.path.join( "tmp", f"proc_{p}.cub5" ) )
        cubit.cmd( f'export cubit "{filenames[-1]}" body {proc_body_list} overwrite' )
    return filenames

def gather():
    filesearch = os.path.join( "tmp", "*.cub5" )
    filenames = glob.glob( filesearch )
    cubit.cmd( "reset" )
    for filename in filenames:
        cubit.cmd( f"import cubit '{filename}'" )
    cubit.cmd( "save cub5 'base_model_meshed.cub5' overwrite" )

## Parallel Meshing
def mesh_entities( filename ):
    cubit.cmd( "reset" )
    cubit.cmd( f'open "{filename}"' )
    cubit.cmd( "compress ids" )
    cubit.cmd( "vol all scheme tetmesh" )
    cubit.cmd( "vol all size auto factor 5" )
    cubit.cmd( "mesh vol all" )
    cubit.cmd( f"save cub5 '{filename}' overwrite" )

## Script
if __name__ == "__main__":
    args = input_args()
    num_proc = int( args.num_proc )
    ### Create model
    t0 = time.time()
    create_base_model()
    t1 = time.time()
    print( f"Create elapsed time: {t1-t0} seconds" )
    ### Distribute
    t0 = time.time()
    filenames = distribute( num_proc )
    t1 = time.time()
    print( f"Distribute elapsed time: {t1-t0} seconds" )
    ### Mesh
    t0 = time.time()
    #### Create a pool of worker processes
    with multiprocessing.Pool( processes=num_proc ) as pool:
        #### Apply the mesh_entity function to each item in bid_list
        pool.map( mesh_entities, filenames )
    t1 = time.time()
    print( f"Parallel elapsed time: {t1-t0} seconds" )
    ### Gather
    t0 = time.time()
    gather()
    t1 = time.time()
    print( f"Gather elapsed time: {t1-t0} seconds" )