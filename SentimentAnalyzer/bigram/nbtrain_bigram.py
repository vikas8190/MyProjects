import sys
import re
import math
import os
from decimal import Decimal
import string
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

''' Function to calculate frequency distribution of train data'''
def calculate_frequency_dist_for_class(word_dict, train_class_dir, class_name):
    total_word_count = 0
    word_list=[]
    for filename in os.listdir(train_class_dir):
        f = open(os.path.join(train_class_dir, filename), "r")
        file_content = f.read()
        #for sentence in sentence_list:
        tokens=nltk.word_tokenize(file_content)
        bigrams=ngrams(tokens,2)
        fdist_bigram = nltk.FreqDist(bigrams)
        for word_bigram,freq in fdist_bigram.items():
            total_word_count+=freq
            if word_bigram in word_dict:
                if class_name in word_dict[word_bigram]:
                    count=word_dict[word_bigram][class_name]
                    word_dict[word_bigram][class_name]+freq
                else:
                    word_dict[word_bigram][class_name]=freq
            else:
                word_dict[word_bigram]={}
                word_dict[word_bigram][class_name]=freq

    return len(os.listdir(train_class_dir))

''' Function to calculate probability of words in classes P(w|C)
where w is the word and C refers to the class(pos/neg)'''
def calculate_probability(word_dict, train_class_dir, word_count_dict, probability_dict,class_name):
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


'''Function to remove words whose combined frequency is less than 5'''
def remove_unwanted_words(word_list):
    new_word_dict = {}
    for word in word_list.keys():
        if (word_list[word].get("pos",0) + word_list[word].get("neg",0)) >= 5:
            new_word_dict[word] = word_list[word]

    return new_word_dict

''' Function to calculate the number of words of class '''
def class_sum(word_list, class_name):
    total = 0
    for word in word_list:
        total += word_list[word].get(class_name,0)
    return total

'''Starting point of module'''
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

    new_word_dict=word_dict
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
        file_handle.writelines("@#!" + str(k[0])+'||'+str(k[1]) + "\n")
        for j in probability_dict[k]:
            file_handle.writelines(j + ":" + str(probability_dict[k][j]) + "\n")


main(sys.argv[1:])
