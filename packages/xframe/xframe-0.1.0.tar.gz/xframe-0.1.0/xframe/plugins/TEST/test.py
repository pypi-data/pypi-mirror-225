import logging
import sys
import os
import numpy as np
import traceback
file_path = os.path.realpath(__file__)
plugin_dir = os.path.dirname(file_path)
os.chdir(plugin_dir)
import time

#from analysisLibrary.classes import ReciprocalProjectionData
from xframe.library.gridLibrary import SampledFunction,NestedArray
from xframe.library.mathLibrary import nearest_positive_semidefinite_matrix
from xframe.analysis.analysisWorker import AnalysisWorker
from xframe import database,settings
from xframe.presenters.matplolibPresenter import plot1D
from xframe import Multiprocessing
log=logging.getLogger('root')

#class Worker(RecipeInterface):
class Worker(AnalysisWorker):
    def __init__(self):
        pass
    
    def start_working(self):
        from multiprocessing import Process
        
        p = Process(target=self.send_string)
        p2 = Process(target=self.send_string)
        p.start()
        #p2.start()
        p.join()
        #p2.join()
        return {},locals()

    def generate_GPU_function(self):
        kernel_str =  """
        __kernel void
        reduce(__global double* buffer,
        __global double* result,
        __const int length,
        __local double* scratch
        ) {
        int global_index = get_global_id(0);
        double accumulator = 0; //INFINITY;
        // Loop sequentially over chunks of input vector
        while (global_index < length) {
        double element = buffer[global_index];
        accumulator +=element; //  (accumulator < element) ?
        //accumulator : element;
        global_index += get_global_size(0);
        }
        // Perform parallel reduction
        int local_id = get_local_id(0);
        scratch[local_id]=accumulator;
        barrier(CLK_LOCAL_MEM_FENCE);
        
        for(int offset = get_local_size(0)/2;
        offset > 0;
        offset = offset / 2) {
        if (local_id<offset){
        //double other = scratch[local_id+offset];
        scratch[local_id]= scratch[local_id+offset]+scratch[local_id];;//(mine<other) ? mine : other;
        }
        barrier(CLK_LOCAL_MEM_FENCE);
        }
        if (local_id == 0){
        result[get_group_id(0)] = scratch[0];
        }
        }
        
        __kernel void
        reduce2(__global double* buffer,
        __global double* result,
        __const int n_arrays,
        __const int length,
        __local double* scratch
        ) {
        int array_id = get_global_id(0);
        int global_index = get_global_id(1);
        int array_size = length;
        double accumulator = 0; //INFINITY;
        // Loop sequentially over chunks of input vector
        while (global_index < length) {
        double element = buffer[array_id*array_size + global_index];
        accumulator +=element; //  (accumulator < element) ?
        //accumulator : element;
        global_index += array_size;
        }
        // Perform parallel reduction
        int local_id = get_local_id(1);
        scratch[local_id]= accumulator;
        barrier(CLK_LOCAL_MEM_FENCE);
        
        for(int offset = get_local_size(1)/2;
        offset > 0;
        offset = offset / 2) {
        if (local_id<offset){
        //double other = scratch[local_id+offset];
        scratch[local_id]= scratch[local_id+offset]+scratch[local_id];;//(mine<other) ? mine : other;
        }
        barrier(CLK_LOCAL_MEM_FENCE);
        }
        if (local_id == 0){
        result[get_group_id(0)*get_num_groups(1) + get_group_id(1)] = scratch[0];
        }
        }
        """

        kernel_dict={
            'kernel': kernel_str,
            'name': 'test_process',
            'functions': [{
                'name': 'reduce',
                'dtypes' : [np.double,np.double,np.int32,np.double],
                'shapes' : [(600,),(32,),None,(600,)],
                'arg_roles' : ['input','output','const_input','local'],
                'const_inputs' : [None,None,np.int32(600),None],
                'global_range' : 1024,
                'local_range' : 32
            }]
        }
        gpu_process = Multiprocessing.openCL_plugin.ClProcess(kernel_dict)
        return gpu_process
    
    def send_string(self):
        log.info('Worker {} is working ;)'.format(Multiprocessing.get_process_id()))
        gpu_process = self.generate_GPU_function()
        time.sleep(1)
        comm = Multiprocessing.comm_module
        gpu_function = comm.add_gpu_process(gpu_process)
        log.info('Request gpu evaluation')
        result = gpu_function(np.ones(600,dtype = float))
        log.info('GPU function was processed by Controller, with result = {}'.format(result))        
