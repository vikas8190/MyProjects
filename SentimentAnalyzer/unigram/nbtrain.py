import sys
import re
import math
import os
from decimal import Decimal
import string
import operator


'''
Function to calculate frequency distribution for training data . The output is
a dictionary that consists of frequencies of words for positive and negative classes
'''
def calculate_frequency_dist_for_class(word_dict, train_class_dir, class_name):
    total_word_count = 0
    word_list=[]
    for filename in os.listdir(train_class_dir):
        f = open(os.path.join(train_class_dir, filename), "r")
        sentence_list = f.read().split('\n')
        for sentence in sentence_list:
            new_word_list=sentence.split()
            if ' ' in new_word_list:
                new_word_list.remove(' ')
            if '' in new_word_list:
                new_word_list.remove('')
            new_word_list = [x for x in new_word_list if x != '']
            word_list.extend(new_word_list)
        
    total_word_count= len(word_list)
    for word in word_list:
        if word in word_dict:
            if class_name in word_dict[word]:
                count = word_dict[word][class_name]
                word_dict[word][class_name] = count + 1
            else:
                word_dict[word][class_name] = 1
        else:
            word_dict[word] = {}
            word_dict[word][class_name] = 1
    
    return len(os.listdir(train_class_dir))


'''
Function to calculate probabilty for words in a class . i.e P(w|C)
where w is the word and C refers to class
'''
def calculate_probability(word_dict, train_class_dir, word_count_dict, probability_dict,
                          class_name):
    for word in word_dict:
        if word in probability_dict:
            if class_name in word_dict[word]:
                probability_dict[word][class_name] = \
                    Decimal(word_dict[word][class_name] + 1) / Decimal(
                        word_count_dict[class_name] + len(word_dict.keys()))
    
            else:
                probability_dict[word][class_name] = \
                    1 / Decimal(
                        word_count_dict[class_name] + len(word_dict.keys()))
    
        else:
            probability_dict[word] = {}
            probability_dict[word]["pos"] = 1 / Decimal(
            word_count_dict["pos"] + len(word_dict.keys()))
            probability_dict[word]["neg"] = 1 / Decimal(
            word_count_dict["neg"] + len(word_dict.keys()))
            if class_name in word_dict[word]:
                 probability_dict[word][class_name] = Decimal(
                     word_dict[word][class_name] + 1) \
                                                  / Decimal(
                     word_count_dict[class_name] +
                     len(word_dict.keys()))
            else:
                 probability_dict[word][class_name] = 1 / Decimal(
                 word_count_dict[class_name] + len(word_dict.keys()))



''' Function to remove words whose combined frequency is less than 5'''
def remove_unwanted_words(word_list):
    new_word_dict = {}
    for word in word_list.keys():
        if (word_list[word].get("pos",0) + word_list[word].get("neg",0)) >= 5:
            new_word_dict[word] = word_list[word]

    return new_word_dict


''' Calculates the number of words for a class'''
def class_sum(word_list, class_name):
    total = 0
    for word in word_list:
        total += word_list[word].get(class_name,0)
    return total

''' Function to calculate highest weight ratio for words '''
def get_highest_weight_ratio(probability_dict):
    f=open("Highest_ratio_details_with_laplace.txt","w")
    log_top_20_1={}
    log_top_20_2={}
    for k in probability_dict.keys():
        log_top_20_1[k] = math.log(probability_dict[k]["pos"]/probability_dict[k]["neg"],2)
        log_top_20_2[k] = math.log(probability_dict[k]["neg"]/probability_dict[k]["pos"],2)
    log_top_20_posbyneg = sorted(log_top_20_1.items(), key=operator.itemgetter(1), reverse =True)
    log_top_20_negbypos = sorted(log_top_20_2.items(), key=operator.itemgetter(1) , reverse = True)
    f.writelines("Top 20 pos/neg\n")
    for k in range(19):
        f.writelines(str(log_top_20_posbyneg[k])+"\n")

    f.writelines("TOP 20 neg/pos\n")
    for k in range(19):
        f.writelines(str(log_top_20_negbypos[k])+"\n")
    f.close()

''' Main function : The starting point of program'''
def main(argv):
    word_dict = {}
    word_count_dict = {}
    probability_dict = {}
    doc_count_dict = {}
    if argv:
        training_dir = argv[0]
        model_file = argv[1]
    for class_name in os.listdir(training_dir):
        class_dir = os.path.join(training_dir, class_name)
        doc_count_dict[class_name] = calculate_frequency_dist_for_class(word_dict, class_dir, class_name)

    new_word_dict = remove_unwanted_words(word_dict)
    #new_word_dict = word_dict

    for class_name in os.listdir(training_dir):
        word_count_dict[class_name] = class_sum(new_word_dict, class_name)


    for class_name in os.listdir(training_dir):
        class_dir = os.path.join(training_dir, class_name)
        calculate_probability(new_word_dict, class_dir, word_count_dict, probability_dict,
                              class_name)

    file_handle = open(model_file, "w")
    for m in word_count_dict:
        file_handle.writelines(
            m + ":" + str(doc_count_dict[m]) + "," + str(word_count_dict[m]) + "\n")
    file_handle.write("$@%" + "\n")
    for k in probability_dict:
        file_handle.writelines("@#!" + k + "\n")
        for j in probability_dict[k]:
            file_handle.writelines(j + ":" + str(probability_dict[k][j]) + "\n")
    get_highest_weight_ratio(probability_dict)
    file_handle.close()


main(sys.argv[1:])
