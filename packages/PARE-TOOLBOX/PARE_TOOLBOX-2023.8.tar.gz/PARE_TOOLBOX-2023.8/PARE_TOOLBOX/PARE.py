import time
from datetime import datetime
import numpy as np
import pandas as pd
import multiprocessing
from multiprocessing import Pool

import PARE_TOOLBOX.PARE_LIBRARY as PARE_LIB

def SAMPLING_ALGORITHM(SETUP):
    """
    This function creates the samples and evaluates the limit state functions.
    
    See documentation in wmpjrufg.github.io/PAREPY/
    """ 
    
    # Initial setup
    INIT = time.time()
    OF_FUNCTION = SETUP['OF']
    N_POP = SETUP['N_POP']
    D = SETUP['D']
    MODEL = SETUP['MODEL']
    VARS = SETUP['VARS']
    N_G = SETUP['N_G']
    NULL_DIC = SETUP['NULL_DIC']
    MODEL_NAME = 'MCS_LHS'
    RESULTS_R = np.zeros((N_POP, N_G))
    RESULTS_S = np.zeros((N_POP, N_G))
    RESULTS_G = np.zeros((N_POP, N_G))
    RESULTS_I = np.zeros((N_POP, N_G))  

    # Creating samples   
    DATASET_X, RANDOM_STATE = PARE_LIB.SAMPLING(N_POP = N_POP, D = D, MODEL = MODEL, VARS = VARS)   

    # Selecting algorithm architecture
    TYPE_PROCESS, FO_TIME = PARE_LIB.GET_TYPE_PROCESS(SETUP, OF_FUNCTION, PARE_LIB.SAMPLING, PARE_LIB.EVALUATION_MODEL)

    # Multiprocess Objective Function evaluation
    if TYPE_PROCESS == 'PARALLEL':
        POOLS = multiprocessing.cpu_count() - 1   
        INFO = [[list(I), OF_FUNCTION, NULL_DIC] for I in DATASET_X]
        with Pool(processes = POOLS) as pool:
            RESULT = pool.map_async(PARE_LIB.EVALUATION_MODEL, INFO)
            RESULT = RESULT.get()
        for K in range(N_POP):
            RESULTS_R[K, :] = RESULT[K][0]
            RESULTS_S[K, :] = RESULT[K][1]
            RESULTS_G[K, :] = RESULT[K][2]
            RESULTS_I[K, :] = [0 if value <= 0 else 1 for value in RESULT[K][2]]
    # Singleprocess Objective Function evaluation
    elif TYPE_PROCESS == 'SERIAL':
        RESULT = []
        for I in DATASET_X:
            INFO = [I, OF_FUNCTION, NULL_DIC]
            RES = PARE_LIB.EVALUATION_MODEL(INFO)
            RESULT.append(RES)
        for K in range(N_POP):
            RESULTS_R[K, :] = RESULT[K][0]
            RESULTS_S[K, :] = RESULT[K][1]
            RESULTS_G[K, :] = RESULT[K][2]
            RESULTS_I[K, :] = [0 if value <= 0 else 1 for value in RESULT[K][2]] 
            
    # Storage all results
    AUX = np.hstack((DATASET_X, RESULTS_R, RESULTS_S, RESULTS_G, RESULTS_I))
    RESULTS_ABOUT_DATA = pd.DataFrame(AUX)          
    # Rename columns in dataframe 
    COLUMNS_NAMES = []
    for L in range(D):
        COLUMNS_NAMES.append('X_' + str(L))
    for L in range(N_G):
        COLUMNS_NAMES.append('R_' + str(L))  
    for L in range(N_G):
        COLUMNS_NAMES.append('S_' + str(L))
    for L in range(N_G):
        COLUMNS_NAMES.append('G_' + str(L))
    for L in range(N_G):
        COLUMNS_NAMES.append('I_' + str(L))
    RESULTS_ABOUT_DATA.columns = COLUMNS_NAMES
    
    # Resume data in dataframe format
    RESUME_DATA = PARE_LIB.DATA_RESUME(RANDOM_STATE, N_G, RESULTS_ABOUT_DATA)

    # Resume process (Time and outputs)
    END = time.time()
    print('PAREpy report: \n') 
    NAME = MODEL_NAME + '_' + str(datetime.now().strftime('%Y%m%d-%H%M%S'))
    print(f' \U0001F202 ID report: {NAME} \n') 
    print(' \U0001F680' + f' Process Time ({TYPE_PROCESS} version) ' + '\U000023F0' + ' %.2f' % (END - INIT), 'seconds \n') 
    print(' \U0001F550' + ' Objective function time evaluation per sample: ' + ' %.4f' % FO_TIME + ' seconds') 
    PARE_LIB.JSON_FILE(NAME, RESUME_DATA)
    PARE_LIB.TXT_FILE(NAME, RESULTS_ABOUT_DATA)
    PARE_LIB.ZIP_FILE(NAME)

    return RESULTS_ABOUT_DATA

def SAMPLING_ALGORITHM_PARALLEL_CONCAT(PATH = './'):
    
    # Unzip all files
    TAM = PARE_LIB.UNZIP_ALL_FILES(PATH)
        
    # Concatenating datasets
    RESULTS_ABOUT_DATA = PARE_LIB.CONCAT_RESULTS(PATH)
       
    # Counting number of limit state functions
    HEADER = []
    for COLUMN in RESULTS_ABOUT_DATA.columns:
        HEADER.append(COLUMN)
    N_G = 0
    for ELEMENT in HEADER:
        if ELEMENT[0] == 'I':
            N_G += 1

    # Delete all folders (unzip procedure)
    FOLDERS = PARE_LIB.READ_RESULTS_IN_CURRENT_FOLDER(PATH)
    for FOLDER in FOLDERS:
        PARE_LIB.FOLDER_REMOVER(FOLDER, PATH)
 
    # Resume data in dataframe format
    RESUME_DATA = PARE_LIB.DATA_RESUME(None, N_G, RESULTS_ABOUT_DATA)

    # Command window report
    print('PAREpy report: \n') 
    MODEL_NAME = 'MCS_LHS'
    NAME = MODEL_NAME + '_' + str(datetime.now().strftime('%Y%m%d-%H%M%S'))
    print(f' \U0001F202 ID report: {NAME} \n') 
    print(f' \U00002705 jointing {TAM} .txt files totalizing {len(RESULTS_ABOUT_DATA)} samples') 
    PARE_LIB.JSON_FILE(NAME, RESUME_DATA)
    PARE_LIB.TXT_FILE(NAME, RESULTS_ABOUT_DATA)
    PARE_LIB.ZIP_FILE(NAME)

    return RESULTS_ABOUT_DATA
