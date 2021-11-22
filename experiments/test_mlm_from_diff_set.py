import numpy
import sys
import os

def evaluation_whole():
    correct_count = 0
    mask_word = []
    result_output = []
    
    result_path = '../data/'+dirname+'/result/'+filename
    with open(result_path, 'r') as result_file:
        result_list = result_file.readlines()
    print(result_path)
    for index in range(20):
        right_answer_path = '../data/'+test_dir+'/test_sentences_m.txt'
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
    output_dir = 'result/'+dirname
    
    output_file_path = 'result/'+dirname+'/'+filename
    
    with open(output_file_path,'w') as f:
        f.write('\n'.join(result_output))
        
    
    accuracy = correct_count/len(result_list) * 100
    print(round(accuracy,2))

if __name__ == "__main__":
    dirname = sys.argv[1]
    test_dir = sys.argv[2]
    filename = sys.argv[3]
    evaluation_whole()


                        

