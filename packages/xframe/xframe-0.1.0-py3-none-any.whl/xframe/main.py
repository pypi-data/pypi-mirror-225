import argparse
import importlib
import time,timeit
import profile
import time
import traceback
import os
import sys
from os.path import join as pjoin
os.environ["MKL_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1" 
os.environ["OMP_NUM_THREADS"] = "1" 
os.environ['OPENBLAS_NUM_THREADS'] = "1"

def parse_arguments(defaults):
   a_name = defaults['ana_name']
   a_opt = defaults['ana_opt']
   e_name = defaults['exp_name']
   e_opt = defaults['exp_opt']
   parser = argparse.ArgumentParser(description='xFrame main parser')
   parser.add_argument('ana_name', help='analysisWorker name', nargs = '?',default = a_name  , type=str)
   parser.add_argument('ana_opt', help='analysis settings file name', nargs = '?',default = a_opt , type=str)
   parser.add_argument('exp_name', help='experimentWorker name', nargs = '?',default = e_name , type=str)
   parser.add_argument('exp_opt', help='experiment settings file name', nargs = '?',default = e_opt , type=str)
   parser.add_argument('-r', '--run', nargs='?', default = False, help='Run to execute analysis on. Overwrites runs in a_opt if given.', type=int)
   args=parser.parse_args()
   return args
      
def start_routine_cmd():
   import xframe
   defaults = {'ana_name':'MTIP.reconstruct','ana_opt':'3d_model_0','exp_name':False,'exp_opt':False}
   args = parse_arguments(defaults)
   results = xframe.run(ana_name = args.ana_name,ana_settings=args.ana_opt,exp_name=args.exp_name,exp_settings=args.exp_opt,oneshot = True)
   xframe.Multiprocessing.update_free_cpus()
   #print('available cpus = {}'.format(xframe.Multiprocessing.free_cpus))
   #os._exit(0)
   sys.exit()
   
if __name__ == '__main__':
   variables = start_routine_cmd()
