import json
import logging
import random
import string
import sys
import torch
import experiment_utils as utils
from transformers import BertForMaskedLM
from transformers import BertConfig
from happytransformer import HappyBERT
from tqdm import tqdm
import ast
import os
import glob
import natsort
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)

def set_seed(seed=42):
    """
    Sets seed for all random number generators available.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    try:
        torch.cuda.manual_seed_all(seed)
    except:
        print('Cuda manual seed is not set')

def main():
    
    if 'bert-large' in filename:
        bert = HappyBERT('bert-large-uncased')
        config = BertConfig.from_pretrained('bert-large-uncased')
    elif 'bert-base' in filename:
        bert = HappyBERT('bert-base-uncased')
        config = BertConfig.from_pretrained('bert-base-uncased')
    mlm = BertForMaskedLM(config)
    mlm.eval()

    bert.mlm = mlm

    result_list = []
    config_list = []
    config_path = '../data/'+test_dir_name+'/config.txt'

    with open(config_path, "r") as f:
        config = f.readlines()
    
        
    test_path = '../data/'+test_dir_name+'/test_sentences.txt'
    test_m_path = '../data/'+test_dir_name+'/test_sentences_m.txt'


    with open(test_path,'r') as test_file:
        sentence = test_file.readlines()
    with open(test_m_path,'r') as test_m_file:
        mask = test_m_file.readlines()
    
    for k in tqdm(range(len(sentence))):
        mask_word = mask[k].strip("\n")
        sentence_w_mask = sentence[k].replace(mask_word, "[MASK]")
        options = ast.literal_eval(config[k])

        result = bert.predict_mask(sentence_w_mask, options=options, num_results=2)
        result_list.append(str(result))
        

    
    with open('../data/zeroshot_'+test_name+'/'+filename+'.txt', 'w') as result_file:
        result_file.write('\n'.join(result_list))

def evaluation():
    correct_count = 0
    mask_word = []
    result_output = []
    
    result_path = '../data/zeroshot_'+test_name+'/'+filename+'.txt'
    with open(result_path, 'r') as result_file:
        result_list = result_file.readlines()
    print(result_path)
    for index in range(20):
        right_answer_path = '../data/'+test_dir_name+'/test_sentences_m.txt'
        with open(right_answer_path, 'r') as answer_file:
            right_answer = answer_file.readlines()
            for answer in right_answer:

                mask_word.append(answer.strip("\n"))

    for i in range(len(result_list)):
        first_answer = result_list[i].split('},')[0]
        
        if mask_word[i] in first_answer:
            answer_output = "right answer :"+ str(mask_word[i])+ "    result: "+ str(result_list[i])+"    score:"+"correct"
            result_output.append(answer_output)
            correct_count += 1
        else:
            answer_output = "right answer :"+ str(mask_word[i])+ "    result: "+ str(result_list[i])+"    score:"+"wrong"
            result_output.append(answer_output)
    output_file_path = 'result/zeroshot_'+test_name+'/'+filename+'.txt'
    
    
    with open(output_file_path,'w') as f:
        f.write('\n'.join(result_output))
        
    
    accuracy = correct_count/len(result_list) * 100
    print(round(accuracy,2))

if __name__ == "__main__":
    test_dir_name = sys.argv[1] 
    test_name = sys.argv[2] # easy / hard / joint
    filename = sys.argv[3]
    seed = sys.argv[4]

    set_seed(int(seed))
    main()
    evaluation()

