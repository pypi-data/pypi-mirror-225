import numpy as np
import random
import pandas as pd
import json
import time
from datetime import datetime
from scipy.stats.distributions import norm
from scipy.stats.distributions import gumbel_r
from scipy.stats.distributions import gumbel_l
from scipy.stats.distributions import lognorm
from scipy.stats.distributions import uniform
from scipy.stats.distributions import triang
import multiprocessing
from multiprocessing import Pool
import shutil
import os
import os.path
import pandas as pd

def FOLDER_CREATOR(NAME, PATH = './'):
    """
    You can insert the file name with extension or without extension, don't need the path (The path is the current directory).
    """

    # Search extension in filename
    if '.json' in NAME or '.txt' in NAME:
        NAME = NAME.split('.')[0]  
    
    # Create folder
    FOLDER_NAME = NAME
    os.mkdir(FOLDER_NAME)

    return PATH + NAME

def FOLDER_MOVER(NAME, PATH = './'):
    """
    You can insert the file name with extension or without extension, don't need the path (The path is the current directory).
    """
    
    # Search extension in filename
    if '.json' in NAME or '.txt' in NAME:
        NAME = NAME.split('.')[0]
    FOLDER_NAME = NAME
    TXT_FILE = NAME + '.txt'
    JSON_FILE = NAME + '.json'
    
    # Move files to folder created
    shutil.move(TXT_FILE, PATH + FOLDER_NAME)
    shutil.move(JSON_FILE, PATH + FOLDER_NAME)

def FOLDER_REMOVER(NAME, PATH = './'):
    """
    """

    # Search extension in filename
    if '.json' in NAME or '.txt' in NAME:
        NAME = NAME.split('.')[0]
    
    # Remove folder
    shutil.rmtree(NAME)

def FOLDER_ZIP(NAME, PATH = './'):
    """
    """

    # Search extension in filename
    if '.json' in NAME or '.txt' in NAME:
        NAME = NAME.split('.')[0]
    
    # Creating zip file
    NAME = PATH + NAME
    shutil.make_archive(NAME, 'zip', root_dir = PATH, base_dir = NAME, verbose = 0, dry_run = False, owner = None, group = None, logger = None)

def TXT_FILE(NAME, DATA):
    """
    """
    
    # Creating txt file
    DATA.to_csv(NAME + '.txt', sep = ',', index = False, header = True)

    # Print message in command window
    print('\n \U0001F197' + ' txt file created!')

def JSON_FILE(NAME, DATA):
    """
    """
    
    # Creating json file
    with open(NAME + '.json', 'w') as FILE:
        json.dump(DATA, FILE)  

    # Print message in command window
    print('\n \U0001F197' + ' json file created!')

def ZIP_FILE(NAME, PATH = './'):
    """
    """
    
    # Creating the folder
    NAME = FOLDER_CREATOR(NAME)

    # Moving files to folder created
    FOLDER_MOVER(NAME)

    # Creating zip file
    FOLDER_ZIP(NAME)
    
    # Removing folder
    FOLDER_REMOVER(NAME)

    # Print message in command window
    print('\n \U0001F197' + ' zip file created: ', NAME)

def READ_ZIP_FILES(PATH = './'):
    """
    """
    
    # Files in the folder
    FILES = os.listdir(PATH)

    # Searching zip files
    ZIPS = []
    for FILE in FILES:
        if 'MCS_LHS' in FILE and '.zip' in FILE:
            ZIPS.append(FILE)
    
    return ZIPS

def READ_RESULTS_IN_CURRENT_FOLDER(PATH = './'):
    
    # Files in the folder
    FILES = os.listdir(PATH)
    
    # Searching results folders
    FOLDERS = []
    for FILE in FILES:
        if 'MCS_LHS' in FILE and not '.zip' in FILE:
            FOLDERS.append(FILE)
    
    return FOLDERS

def UNZIP_FILE(NAME, PATH = './'):
    """
    """

    # Search extension in filename
    if not 'zip' in NAME:
        NAME = NAME + '.zip'

    # Unzip one file
    shutil.unpack_archive(PATH+NAME, PATH, 'zip')

def UNZIP_ALL_FILES(PATH = './'):
    """
    """
    
    # Read name all zip files
    ZIP_FILENAME = READ_ZIP_FILES(PATH)

    # Unzip all files
    for FILE in ZIP_FILENAME:
        UNZIP_FILE(FILE, PATH)
    
    return len(ZIP_FILENAME) 

def CONCAT_RESULTS(PATH = './'):
    '''
    This function concat all results from MCS_LHS folders into the root folder.
    Is possible change the path to a specific folder.
    The result (a file named like 'concat_result.txt') in the specificed folder. By default, the path is the root folder.
    '''

    # Read results in folders
    FOLDERS = READ_RESULTS_IN_CURRENT_FOLDER(PATH)

    # Concatenating datasets
    COMPLETE_DATA = []
    for FOLDER in FOLDERS:
        FILES = os.listdir(PATH + FOLDER)
        # JSON_FILE = [FILE for FILE in FILES if '.json' in FILE][0]
        TXT_FILE = [FILE for FILE in FILES if '.txt' in FILE][0]   
        COMPLETE_PATH = PATH + FOLDER + '/' + TXT_FILE
        DATA = pd.read_csv(COMPLETE_PATH, sep = ",", header = 0)
        COMPLETE_DATA.append(DATA)
    FINAL_DATA = pd.concat(COMPLETE_DATA, ignore_index = True)

    return FINAL_DATA

def SAMPLING(**kwargs):
    """ 
    This algorithm generates a set of random numbers according to a type distribution.

    See documentation in wmpjrufg.github.io/RASDPY/
    """
    if len(kwargs) != 4:
        raise ValueError("this fuction require four inputs!")

    # Creating variables
    N_POP = kwargs['N_POP']
    D = kwargs['D']
    MODEL = kwargs['MODEL']
    VARS = kwargs['VARS']
    RANDOM_STATE = random.sample(range(1, 1000), D)
    RANDOM_SAMPLING = np.zeros((N_POP, D))
    
    # Monte Carlo sampling
    if MODEL.upper() == 'MCS':
        for I in range(D):
            # Type of distribution, mean and standard deviation
            TYPE = VARS[I][0].upper()
            MEAN = VARS[I][1]
            STD = VARS[I][2]
            # Normal or Gaussian
            if TYPE == 'GAUSSIAN' or TYPE == 'NORMAL':
                RANDOM_SAMPLING[:, I] = norm.rvs(loc = MEAN, scale = STD, size = N_POP, random_state = RANDOM_STATE[I])
            # Gumbel right or Gumbel maximum
            elif TYPE == 'GUMBEL MAX':
                RANDOM_SAMPLING[:, I] = gumbel_r.rvs(loc = MEAN, scale = STD, size = N_POP, random_state = RANDOM_STATE[I])
            # Gumbel left or Gumbel minimum
            elif TYPE == 'GUMBEL MIN':
                RANDOM_SAMPLING[:, I] = gumbel_l.rvs(loc = MEAN, scale = STD, size = N_POP, random_state = RANDOM_STATE[I])
            # Lognormal
            elif TYPE == 'LOGNORMAL':
                RANDOM_SAMPLING[:, I] = lognorm.rvs(s = STD, loc = MEAN, scale = np.exp(MEAN), size = N_POP, random_state = RANDOM_STATE[I])
            # Uniform
            elif TYPE == 'UNIFORM':
                RANDOM_SAMPLING[:, I] = uniform.rvs(loc = MEAN, scale=STD, size = N_POP, random_state = RANDOM_STATE[I])
            # Triangular
            elif TYPE == 'TRIANGULAR':
                LOC = VARS[I][1]
                SCALE = VARS[I][2]
                C = VARS[I][3]
                #loc is the start, scale is the base width, c is the mode percentage
                RANDOM_SAMPLING[:, I] = triang.rvs(loc = LOC, scale = SCALE, c = (C - LOC) / (SCALE - LOC), size = N_POP, random_state = RANDOM_STATE[I])

    return RANDOM_SAMPLING, RANDOM_STATE

def EVALUATION_MODEL(INFO):
    SAMPLE = INFO[0]
    OF_FUNCTION = INFO[1]
    NULL_DIC = INFO[2]
    R, S, G = OF_FUNCTION(SAMPLE, NULL_DIC)
    RESULTS = [R, S, G]
    return RESULTS

def NEWTON_RAPHSON(f, df, x0, tol):
    if abs(f(x0)) < tol:
        return x0
    else:
        return NEWTON_RAPHSON(f, df, x0 - f(x0)/df(x0), tol)

def GET_TYPE_PROCESS(SETUP, OF_FUNCTION, SAMPLING, EVALUATION_MODEL):
    """ 
    This function gets the type of process.
    It executes the function with a dataset of 10 samples. 
    The return is a string with the type of process. 
    The NPOP always is 10.
    """

    # Initial setup
    N_POP = 5
    D = SETUP['D']
    MODEL = SETUP['MODEL']
    VARS = SETUP['VARS']
    NULL_DIC = SETUP['NULL_DIC']
   
    DATASET_X, _ = SAMPLING(N_POP = N_POP, D = D, MODEL = MODEL, VARS = VARS)   

    INIT_TIME = time.time()
    POOLS = multiprocessing.cpu_count() - 1   
    INFO = [[list(I), OF_FUNCTION, NULL_DIC] for I in DATASET_X]
    with Pool(processes = POOLS) as pool:
        RESULT = pool.map_async(EVALUATION_MODEL, INFO)
        RESULT = RESULT.get()
    FINISH_TIME = time.time() 
    
    INIT_TIME2 = time.time()
    RESULT = []
    for I in DATASET_X:
        INFO = [I, OF_FUNCTION, NULL_DIC]
        INIT_TIME_FO = time.time()
        RES = EVALUATION_MODEL(INFO)
        END_TIME_FO = time.time()
        RESULT.append(RES)
    FINISH_TIME2 = time.time()
    FO_TIME = (END_TIME_FO - INIT_TIME_FO)  

    if (FINISH_TIME - INIT_TIME) < (FINISH_TIME2 - INIT_TIME2):
        TYPE_PROCESS = 'PARALLEL'
    else:
        TYPE_PROCESS = 'SERIAL'

    return TYPE_PROCESS, FO_TIME

def DATA_RESUME(RANDOM_STATE, N_G, RESULTS_ABOUT_DATA):
    
    # Creates data for .json type output considering the chosen step
    N_POP = len(RESULTS_ABOUT_DATA)
    STEP = 1000
    VALUES = list(np.arange(1, N_POP, STEP, dtype = int))

    if VALUES[-1] != N_POP:
        VALUES.append(N_POP)
    VALUES = [int(X) for X in VALUES]
    RESUME_DATA = {'seeds': RANDOM_STATE, 'number of samples': VALUES, 'results': {}}
    for L in range(N_G):
        KEY = f'I_{L}' 
        N_F = []
        P_F = []
        BETA = []
        for I in VALUES:
            LINES = RESULTS_ABOUT_DATA[:I]            
            # Failure probability
            N_FAILURE = int(LINES[KEY].sum())
            P_FVALUE = N_FAILURE / I
            F = lambda beta: P_FVALUE - 0.50 + (0.033333333333333333*beta*(0.70710678118654757*pow(np.pi, -0.5) + 0.70710678118654757*pow(np.pi, -0.5)*np.exp(-0.5*pow(beta, 2)) + 2.8284271247461903*pow(np.pi, -0.5)*np.exp(-0.40500000000000003*pow(beta, 2)) + 1.4142135623730951*pow(np.pi, -0.5)*np.exp(-0.32000000000000006*pow(beta, 2)) + 2.8284271247461903*pow(np.pi, -0.5)*np.exp(-0.24499999999999997*pow(beta, 2)) + 1.4142135623730951*pow(np.pi, -0.5)*np.exp(-0.17999999999999999*pow(beta, 2)) + 2.8284271247461903*pow(np.pi, -0.5)*np.exp(-0.125*pow(beta, 2)) + 1.4142135623730951*pow(np.pi, -0.5)*np.exp(-0.080000000000000016*pow(beta, 2)) + 2.8284271247461903*pow(np.pi, -0.5)*np.exp(-0.044999999999999998*pow(beta, 2)) + 1.4142135623730951*pow(np.pi, -0.5)*np.exp(-0.020000000000000004*pow(beta, 2)) + 2.8284271247461903*pow(np.pi, -0.5)*np.exp(-0.005000000000000001*pow(beta, 2))))
            F_PRIME = lambda beta: 0.033333333333333333*beta*(-0.70710678118654757*pow(np.pi, -0.5)*beta*np.exp(-0.5*pow(beta, 2)) - 2.2910259710444141*pow(np.pi, -0.5)*beta*np.exp(-0.40500000000000003*pow(beta, 2)) - 0.90509667991878107*pow(np.pi, -0.5)*beta*np.exp(-0.32000000000000006*pow(beta, 2)) - 1.3859292911256331*pow(np.pi, -0.5)*beta*np.exp(-0.24499999999999997*pow(beta, 2)) - 0.50911688245431419*pow(np.pi, -0.5)*beta*np.exp(-0.17999999999999999*pow(beta, 2)) - 0.70710678118654757*pow(np.pi, -0.5)*beta*np.exp(-0.125*pow(beta, 2)) - 0.22627416997969527*pow(np.pi, -0.5)*beta*np.exp(-0.080000000000000016*pow(beta, 2)) - 0.2545584412271571*pow(np.pi, -0.5)*beta*np.exp(-0.044999999999999998*pow(beta, 2)) - 0.056568542494923817*pow(np.pi, -0.5)*beta*np.exp(-0.020000000000000004*pow(beta, 2)) - 0.028284271247461908*pow(np.pi, -0.5)*beta*np.exp(-0.005000000000000001*pow(beta, 2))) + 0.023570226039551584*pow(np.pi, -0.5) + 0.023570226039551584*pow(np.pi, -0.5)*np.exp(-0.5*pow(beta, 2)) + 0.094280904158206336*pow(np.pi, -0.5)*np.exp(-0.40500000000000003*pow(beta, 2)) + 0.047140452079103168*pow(np.pi, -0.5)*np.exp(-0.32000000000000006*pow(beta, 2)) + 0.094280904158206336*pow(np.pi, -0.5)*np.exp(-0.24499999999999997*pow(beta, 2)) + 0.047140452079103168*pow(np.pi, -0.5)*np.exp(-0.17999999999999999*pow(beta, 2)) + 0.094280904158206336*pow(np.pi, -0.5)*np.exp(-0.125*pow(beta, 2)) + 0.047140452079103168*pow(np.pi, -0.5)*np.exp(-0.080000000000000016*pow(beta, 2)) + 0.094280904158206336*pow(np.pi, -0.5)*np.exp(-0.044999999999999998*pow(beta, 2)) + 0.047140452079103168*pow(np.pi, -0.5)*np.exp(-0.020000000000000004*pow(beta, 2)) + 0.094280904158206336*pow(np.pi, -0.5)*np.exp(-0.005000000000000001*pow(beta, 2))
            BETA_VALUE = NEWTON_RAPHSON(F, F_PRIME, 0.0, 1e-6)
            N_F.append(N_FAILURE)
            P_F.append(P_FVALUE)
            BETA.append(BETA_VALUE)
        RESUME_DATA['results'][KEY] = {'Failure rate': N_F, 'Failure probability': P_F, 'Reliability index': BETA}

    return RESUME_DATA  
