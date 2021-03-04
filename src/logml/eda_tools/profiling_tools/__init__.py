import glob
import os

ROOT_MODULE = 'logml.eda_tools.profiling_tools'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

for file_ in glob.glob(f'{ROOT_DIR}/*.py', recursive=True):
    module_ = os.path.basename(file_).replace('.py', '')
    __import__(f'{ROOT_MODULE}.{module_}')
