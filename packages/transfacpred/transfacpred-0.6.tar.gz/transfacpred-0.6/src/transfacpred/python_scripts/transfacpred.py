import argparse
import os
import pickle
import pandas as pd
import re
import warnings
import sys
import zipfile
import platform
import requests
import subprocess
from sklearn.ensemble import ExtraTreesClassifier

warnings.filterwarnings('ignore')

BLAST_BINARIES = {
    "Linux": "/../blast_binaries/linux/blastp",
    "Darwin": "/../blast_binaries/mac/blastp",
    "Windows": "/../blast_binaries/windows/blastp.exe",
}

def get_blastp_path(def_file_path):
    operating_system = platform.system()
    blastp_path = def_file_path + BLAST_BINARIES.get(operating_system)
    if not blastp_path:
        print(f"Unsupported operating system: {operating_system}")
        return None

    if not os.path.exists(blastp_path):
        print(f"BLASTP binary not found: {blastp_path}")
        return None

    return blastp_path

def readseq(file):
    with open(file) as f:
        records = f.read()
    records = records.split('>')[1:]
    seqid = []
    seq = []
    for fasta in records:
        array = fasta.split('\n')
        name, sequence = array[0].split()[0], re.sub('[^ACDEFGHIKLMNPQRSTVWY-]', '', ''.join(array[1:]).upper())
        seqid.append('>'+name)
        seq.append(sequence)
    if len(seqid) == 0:
        f=open(file,"r")
        data1 = f.readlines()
        for each in data1:
            seq.append(each.replace('\n',''))
        for i in range (1,len(seq)+1):
            seqid.append(">Seq_"+str(i))
    df1 = pd.DataFrame(seqid)
    df2 = pd.DataFrame(seq)
    return df1,df2


def aac_comp(file):
    std = list('ACDEFGHIKLMNPQRSTVWY')
    df1 = file
    df1.columns = ['Seq']
    dd = []
    for j in df1['Seq']:
        cc = []
        for i in std:
            count = 0
            for k in j:
                temp1 = k
                if temp1 == i:
                    count += 1
                composition = (count/len(j))*100
            cc.append(composition)
        dd.append(cc)
    df2 = pd.DataFrame(dd)
    head = []
    for mm in std:
        head.append('AAC_'+mm)
    df2.columns = head
    return df2




def pred(file1):
    a = []

    # Define the directory structure
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'Models')

    # Download and unzip Models.zip if not already done
    models_url = 'https://webs.iiitd.edu.in/raghava/transfacpred/Models.zip'
    models_zip_path = os.path.join(base_dir, 'Models.zip')

    if not os.path.exists(models_dir):
        response = requests.get(models_url)
        with open(models_zip_path, 'wb') as models_zip:
            models_zip.write(response.content)
        
        with zipfile.ZipFile(models_zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
        
        os.remove(models_zip_path)

    # Load the model
    model_path = os.path.join(models_dir, 'ET_model.pkl')
    with open(model_path, 'rb') as model_file:
        clf = pickle.load(model_file)

    data_test = file1
    y_p_score1 = clf.predict_proba(data_test)
    y_p_s1 = y_p_score1.tolist()
    a.extend(y_p_s1)
    df_a = pd.DataFrame(a)
    df_1a = df_a.iloc[:, -1].round(2)
    df_2a = pd.DataFrame(df_1a)
    df_2a.columns = ['ML_score']

    return df_2a



def BLAST_processor(blast_result, name1, ml_results, thresh):
    df3 = ml_results  
    if os.stat(blast_result).st_size != 0:
        df1 = pd.read_csv(blast_result, sep="\t", names=['name', 'hit', 'identity', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9'])
        df2 = name1
        cc = []
        for i in df2[0]:
            kk = i.replace('>', '')
            if len(df1.loc[df1.name == kk]) > 0:
                df4 = df1[['name', 'hit']].loc[df1['name'] == kk].reset_index(drop=True)
                if df4['hit'][0].split('_')[0] == 'P':
                    cc.append(0.5)
                if df4['hit'][0].split('_')[0] == 'N':
                    cc.append(-0.5)
            else:
                cc.append(0)
        df6 = pd.DataFrame()
        df6['Seq_ID'] = [i.replace('>', '') for i in df2[0]]
        df6['ML_Score'] = df3['ML_score']
        df6['BLAST_Score'] = cc
        df6['Total_Score'] = df6['ML_Score'] + df6['BLAST_Score']
        df6['Prediction'] = ['Transcription Factor' if df6['Total_Score'][i] > thresh else 'Non-Transcription Factor' for i in range(0, len(df6))]
    else:
        df2 = name1
        ss = []
        vv = []
        for j in df2[0]:
            ss.append(j.replace('>', ''))
            vv.append(0)
        df6 = pd.DataFrame()
        df6['Seq_ID'] = ss
        df6['ML_Score'] = df3['ML_score']
        df6['BLAST_Score'] = vv
        df6['Total_Score'] = df6['ML_Score'] + df6['BLAST_Score']
        df6['Prediction'] = ['Transcription Factor' if df6['Total_Score'][i] > thresh else 'Non-Transcription Factor' for i in range(0, len(df6))]
    return df6


def main():


##################################   BLAST Path    ############################################
    nf_path = os.path.dirname(__file__)
    blastp = get_blastp_path(nf_path)
    # Define the directory structure
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(base_dir, 'database')

    # Download and unzip database.zip if not already done
    database_url = 'https://webs.iiitd.edu.in/raghava/transfacpred/database.zip'
    database_zip_path = os.path.join(base_dir, 'database.zip')

    if not os.path.exists(database_dir):
        response = requests.get(database_url)
        with open(database_zip_path, 'wb') as database_zip:
             database_zip.write(response.content)
    
        with zipfile.ZipFile(database_zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
    
        os.remove(database_zip_path)

    # Assign the path of the extracted database folder to the blastdb variable
    blastdb = os.path.join(database_dir, 'transfacpred')
 
###########################################################################################
 
    print('\n\n############################################################################################')
    print('# TransFacPred is developed for predicting Transcription Factors using protein sequence    #')
    print('# information, developed by Prof G. P. S. Raghava group.                                   #')
    print('# Please cite: https://webs.iiitd.edu.in/raghava/transfacpred/                             #')
    print('############################################################################################')

    parser = argparse.ArgumentParser(description='Please provide the following arguments')

    parser.add_argument("-i", "--input", type=str, required=True, help="Input: File name containing protein or peptide sequence in FASTA format.")
    parser.add_argument("-o", "--output", type=str, help="Output: File for saving results by default outfile.csv")
    parser.add_argument("-t", "--threshold", type=float, help="Threshold: Value between 0 to 1 by default -0.38")
    parser.add_argument("-d", "--display", type=int, choices=[1, 2], help="Display: 1:Transcription Factors, 2: All Sequences, by default 1")

   

    args = parser.parse_args()

    Sequence = args.input  # Input variable

    if args.output is None:
        result_filename = "outfile.csv"
    else:
        result_filename = args.output

    if args.threshold is None:
        Threshold = -0.38
    else:
        Threshold = float(args.threshold)

    if args.display is None:
        dplay = int(1)
    else:
        dplay = int(args.display)

    print('\n\nSummary of Parameters:')
    print('Input File: ', Sequence, '; Threshold: ', Threshold)
    print('Output File: ', result_filename, '; Display: ', dplay)

    print("\n\n======Initiating Prediction Using Hybrid Model. Please Wait.......================\n")

    df_2b, df_1b = readseq(Sequence)
    df_3b = aac_comp(df_1b)
    df_4b = pred(df_3b)

    blast_cmd = blastp + " -task blastp -db " + blastdb + " -query " + Sequence + " -out RES_1_6_6.out -outfmt 6 -evalue 100 -max_target_seqs 1"
    #print("BLAST Command:", blast_cmd)
    os.system(blast_cmd)



    df44 = BLAST_processor('RES_1_6_6.out', df_2b, df_4b, Threshold)
    if dplay == 1:
        df44 = df44.loc[df44.Prediction == "Transcription Factor"]
    else:
        df44 = df44
    df44 = round(df44, 3)
    df44.to_csv(result_filename, index=None)

    os.remove('RES_1_6_6.out')

    print("\n=========Process Completed. Have an awesome day ahead.=============\n")
    print('\n======= Thanks for using TransFacPred. Your results are stored in file:', result_filename, ' =====\n\n')


if __name__ == "__main__":
    main()
