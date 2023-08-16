""" 
functions to read and write files in a "smart" way
"""
import pyreadstat
import pandas as pd 
from pathlib import Path
import charset_normalizer
# read pyreadstat files

def read_pyreadstat(file_path,**kwargs):
    ''' 
    reads in a "metadata rich file"
    (dta, sav,b7bdat). Note, xport format not supported
    as it doesnt supply value labels.

    '''
    file_path = Path(file_path)
    ext = file_path.suffix 
    if ext=='.sav':
        read = pyreadstat.read_sav
    elif ext=='.sas7bdat':
        read = pyreadstat.read_sas7bdat
    elif ext=='.dta':
        read = pyreadstat.read_dta
    elif ext=='.por':
        read = pyreadstat.read_por

    return read(file_path,**kwargs)



def detect_file_encoding(file_path):
    """ 
    detects file encoding using charset_normalizer package
    """ 
    with open(file_path,'rb') as f:
        data = f.read()
        encoding_for_input = charset_normalizer.detect(data)

    is_confident = encoding_for_input["confidence"]==1
    if not is_confident:
        print("Be careful, the detected file encoding for:")
        print(f"{file_path}")
        print(r"has less than 100% confidence")
    #chardet_normalizer.detect returns confidence,encoding (as a string), and language (eg English)
    return encoding_for_input["encoding"]


def read_table(file_path,castdtype = "string"):
    """ 
    reads in a tabular file (ie spreadsheet) after detecting
    encoding and file extension without any type casting.

    currently supports csv and tsv

    defaults to not casting values (ie all columns are string dtypes)
    and not parsing strings into NA values (eg "" is kept as "")
    """ 
    ext = Path(file_path).suffix
    if ext==".csv":
        sep = ","
    elif ext==".tsv":
        sep = "\t"
        
    encoding = detect_file_encoding(file_path)
    file_encoding = pd.read_csv(
        file_path,sep=sep,encoding=encoding,dtype=castdtype,
        keep_default_na=False)

    return file_encoding


