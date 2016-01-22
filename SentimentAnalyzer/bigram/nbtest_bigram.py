import sys
import re
import math
import os
import string
from decimal import Decimal
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

'''Function to calculate probability of bigrams'''

def read_model_probs(prob_other,class_doc_stats,class_prob,word_dict,model_file):
	f=open(model_file,"r")
	model_content=f.read().split('$@%')
	class_stats=[x for x in model_content[0].replace('\n',' ').split(' ') if x!='']
	tot_docs=0
	word_count=0
	for stats in class_stats:
		classname_stat=stats.split(':')
		doccount_word_count=classname_stat[1].split(',')
		class_doc_stats[classname_stat[0]]=(int(doccount_word_count[0]),int(doccount_word_count[1]))
		tot_docs+=int(doccount_word_count[0])
	prob_content=str(model_content[1]).replace('\n#','#').replace('\n',' ').split('@#!')
	prob_content=[x for x in prob_content if x!=' ']
	for model_details in prob_content:
		model_probs=[x for x in model_details.split(' ') if x!='']
		words=model_probs[0].rsplit('||',1)
		word=(words[0],words[1])
		for class_prob_details in model_probs[1:]:
			class_probval=class_prob_details.split(':')
			class_name=class_probval[0]
			if word in word_dict:
				word_dict[word][class_name]=class_probval[1]
			else:
				word_dict[word]={}
				word_dict[word][class_name]=class_probval[1]
	for class_name in class_doc_stats:
		class_prob[class_name]=class_doc_stats[class_name][0]/tot_docs
		word_count+=class_doc_stats[class_name][1]
		prob_other[class_name]=1/(class_doc_stats[class_name][1]+len(word_dict))

''' Function to predict the class of the dev and test documents'''
def predict_class(prediction,prob_other,class_doc_stats,class_prob,fdist_bigram,word_dict):
	prob_values=[]
	new_prob_values=[]
	for class_name in class_prob:
		prob_values.append((class_name,class_prob[class_name]))
	for val in prob_values:
		prob=math.log(val[1],2)
		class_name=val[0]
		for word,freq in fdist_bigram.items():
			if word in word_dict: 
				prob=prob+freq*math.log(Decimal(word_dict[word][class_name]),2)
			else:
				prob=prob+math.log(Decimal(prob_other[class_name]),2)
		new_prob_values.append((class_name,prob))
	prob_values=new_prob_values
	prob_values.sort(key=lambda tup: tup[1],reverse=True) 
	return prob_values,prob_values[0][0]

''' Function to predict the class of the dev and test documents'''
def dir_prediction(prediction,dir_name,prob_other,class_doc_stats,class_prob,word_dict):
	test_pred={}
	for filename in os.listdir(dir_name):
		f=open(os.path.join(dir_name,filename),"r")
		file_content=f.read()
		tokens=nltk.word_tokenize(file_content)
		bigrams=ngrams(tokens,2)
		fdist_bigram = nltk.FreqDist(bigrams)
		pred_prob,predicted_class=predict_class(prediction,prob_other,class_doc_stats,class_prob,fdist_bigram,word_dict)
		if predicted_class in prediction:
			prediction[predicted_class].append(filename)
		else:
			prediction[predicted_class]=[]
			prediction[predicted_class].append(filename)
		test_pred[filename]=[]
		test_pred[filename]=pred_prob
	return prediction,test_pred

''' Function to calculate statistics for analyze prediction '''
def analyze_prediction(file_handler,pred,dev_path,class_name):
	file_handler.writelines("##########################################################################################\n")
	if class_name in pred:
		class_filelist=os.listdir(dev_path)
		compare_set=set(pred[class_name])
		matches=len([x for x in class_filelist if x in compare_set])
		per_match=(matches/len(class_filelist))*100
		file_handler.writelines('Percentage classified correctly:'+str(per_match)+"%\n")
	else:
		file_handler.writelines("Percentage classified correctly : 0% ")
	file_handler.writelines("##########################################################################################\n")

''' The starting point of program '''
def main(argv):
	test_prediction={}
	prediction={}
	test_pred_values={}
	pred_values={}
	prob_other={}
	word_dict={}
	class_doc_stats={}
	class_prob={}
	vocab_stats={}
	predicted_class=''
	pred_prob=[]
	print("######################################################")
	if argv:
		model_file=argv[0]
		test_dir=argv[1]
		pred_file=argv[2]
	read_model_probs(prob_other,class_doc_stats,class_prob,word_dict,model_file)
	f=open(pred_file,"w")
	f.writelines("##########################################################################################\n")
	f.writelines("Prediction for given Directory:"+str(test_dir)+"\n")
	f.writelines("##########################################################################################\n")
	prediction,pred_values=dir_prediction(prediction,test_dir,prob_other,class_doc_stats,class_prob,word_dict)
	for pred_file in pred_values:
		f.writelines("File :"+str(pred_file)+"\n")
		f.writelines("Score :"+str(pred_values[pred_file])+"\n")
	if re.match(r'.*test.*',test_dir):
	    pos_cnt=0
	    neg_cnt=0
	    for docno in pred_values:
	        if pred_values[docno][0][0] == "pos":
	            pos_cnt+=1
	        else:
	            neg_cnt+=1
	        f.writelines('Document No:'+str(docno)+"\n")
	        f.writelines('Predicted Values:'+str(pred_values[docno])+"\n")
	    f.writelines('Positive Predictions :'+str(pos_cnt)+ '\nNegative Predictions :'+str(neg_cnt)+"\n")
	elif re.match(r'.*dev.*',test_dir):
		class_name_search=re.search(".*dev/(.*)",test_dir)
		if class_name_search:
			class_name=class_name_search.group(1)
		else:
			class_name_search=re.search(".*dev\(.*)",test_dir)
			if class_name_search:
				class_name=class_name_search.group(1)
		analyze_prediction(f,prediction,test_dir,class_name)

main(sys.argv[1:])
