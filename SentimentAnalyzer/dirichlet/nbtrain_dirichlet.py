import sys
import re
import math
import os
from decimal import Decimal
import string

'''Function to calculate frequency distribution for words . The output of this function
is a dictionary that contains frequencies of each word for positive and negative class'''
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


'''Function to calculate probaility for each word in the corpus'''
def calculate_probability(word_dict, train_class_dir, word_count_dict, probability_dict,
                          class_name,tunable_parameter):
    tot_words_in_tr_docs=0
    for classname in word_count_dict:
        tot_words_in_tr_docs+=word_count_dict[classname]
    for word in word_dict:
        word_occ_in_tr_doc=0
        for classname in word_dict[word]:
        	word_occ_in_tr_doc+=word_dict[word][classname]
        smooth_factor=tunable_parameter*float(word_occ_in_tr_doc/tot_words_in_tr_docs)
        if word in probability_dict:
            if class_name in word_dict[word]:
                probability_dict[word][class_name] = \
                    (word_dict[word][class_name] + smooth_factor) / (
                        word_count_dict[class_name] + tunable_parameter)
            else:
                probability_dict[word][class_name] = \
                    smooth_factor / (
                        word_count_dict[class_name] + tunable_parameter)
    
        else:
            probability_dict[word] = {}
            probability_dict[word]["pos"] = smooth_factor / (
            word_count_dict["pos"] + tunable_parameter)
            probability_dict[word]["neg"] = smooth_factor / (
            word_count_dict["neg"] + tunable_parameter)
            if class_name in word_dict[word]:
                 probability_dict[word][class_name] = (
                     word_dict[word][class_name] + smooth_factor) \
                                                  / (
                     word_count_dict[class_name] +
                     tunable_parameter)
            else:
                 probability_dict[word][class_name] = smooth_factor / (
                 word_count_dict[class_name] + tunable_parameter)


''' Function to remove words that have combined frequency less than 5'''
def remove_unwanted_words(word_list):
    new_word_dict = {}
    for word in word_list.keys():
        if (word_list[word].get("pos",0) + word_list[word].get("neg",0)) >= 5:
            new_word_dict[word] = word_list[word]

    return new_word_dict


''' Function to calculate the number of words occuring in class'''
def class_sum(word_list, class_name):
    total = 0
    for word in word_list:
        total += word_list[word].get(class_name,0)
    return total

''' Starting point of program'''
def main(argv):
    word_dict = {}
    word_count_dict = {}
    probability_dict = {}
    doc_count_dict = {}
    if argv:
        training_dir = argv[0]
        model_file = argv[1]
        tunable_parameter=float(argv[2])
    for class_name in os.listdir(training_dir):
        class_dir = os.path.join(training_dir, class_name)
        doc_count_dict[class_name] = calculate_frequency_dist_for_class(word_dict, class_dir, class_name)

    new_word_dict = remove_unwanted_words(word_dict)

    for class_name in os.listdir(training_dir):
        word_count_dict[class_name] = class_sum(new_word_dict, class_name)


    for class_name in os.listdir(training_dir):
        class_dir = os.path.join(training_dir, class_name)
        calculate_probability(new_word_dict, class_dir, word_count_dict, probability_dict,
                              class_name,tunable_parameter)

    file_handle = open(model_file, "w")
    for m in word_count_dict:
        file_handle.writelines(
            m + ":" + str(doc_count_dict[m]) + "," + str(word_count_dict[m]) + "\n")
    file_handle.write("$@%" + "\n")
    for k in probability_dict:
        file_handle.writelines("@#!" + k + "\n")
        for j in probability_dict[k]:
            file_handle.writelines(j + ":" + str(probability_dict[k][j]) + "\n")


main(sys.argv[1:])
