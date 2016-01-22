######################################################################################################################################
##########################################Small Search Engine - BM25 Implementation #########################################################
######################################################################################################################################
Small Search Engine - BM25
Language used: Python
Compiler version: 3.4
Environment: Linux

######################################################################################################################################
###########################################Description:###############################################################################
######################################################################################################################################
This program computes the bm25 score for all documents for all the given queries and prints the top results.
Implementation:
Indexer:
1. Reads the input stemmed document file . Splits the read information based on '#' which will give all related info for a document 
   as an element of the list.
2. Each of the document info is split on ' ' then which gives info of each word in document and the document number will be first
   element in the list lst1
3. Iteratively each element in lst1 which would be a word in the document is taken and the occurence of that word in the current
   document is incremented in index dictionary if the word doesnt contain numbers
4. The whole index built is written into a file by iterating through index. '#' is prefixed before the word and between document 
   number and its count ':'  is added for formatting

bm25:
1. Input index file is read and then below logic in step 2 is used to create a data structure which contains information for index and
   document statistics
2. Read contents of the index.out file. Split by '#' to get all word related info together as element in list. Then split by ' '
   to obtain each document related info for that word in a list. This is split by ':' to get document number and document count. 
   Using these info the index data structure and document statistics dictionary is populated. The postings are in the form of
   list of tuples
3. For each query the bm25 score for all documents is calculated and top documents with higher scores are output
4. Using the info populated into index data structure and document statistics dictionary, the bm25 score is calculated
5. Since relevance information is not available the formula for bm25 is simplified into:
   (N-ni+0.5)/(ni+0.5)*((k1+1)*fi)/(K+fi)*((k2+1)*qfi)/(k2+qfi) after substituting R and r as 0


#######################################################################################################################################
############################################Pre Run Instructions:######################################################################
#######################################################################################################################################
Python version 3.x expected

#######################################################################################################################################
##############################################Program run instructions:################################################################
#######################################################################################################################################
For run the indexer: 
python3.4 indexer.py tccorpus.txt index.out 
For generating ranked list of documents for all queries in input file:
python3.4 bm25.py index.out queries.txt 100 > results.eval 

The output of the program gets written to results.eval 
#######################################################################################################################################
################################################Note:##################################################################################
#######################################################################################################################################
In case softlink is created in the linux machine to point python to python3.4, then run the commands mentioned above like python bm25.py etc.






######################################################################################################################################
##########################################Retrieval Effectiveness Evaluation #########################################################
######################################################################################################################################
To evaluate retrieval effectiveness
Language used: Python
Compiler version: 3.4
Environment: Linux

######################################################################################################################################
###########################################Description:###############################################################################
######################################################################################################################################
This program computes the below efficiency metrics for the results retrieved by Lucene based on the relevance judgement given 
as input to the program for the input queries given to program.
1- Precision
2- Recall
3- P@K, where K = 20
4- Normalized Discounted Cumulative Gain (NDCG)
5- Mean Average Precision (MAP)


#######################################################################################################################################
############################################Pre Run Instructions:######################################################################
#######################################################################################################################################
Python version 3.x expected

#######################################################################################################################################
##############################################Program run instructions:################################################################
#######################################################################################################################################
For run the indexer: 
python3.4 check_effectiveness.py results.txt queries.txt cacm.rel >EffectivenessResult.txt
where:
results.txt is the retrieved document details from Lucene 
cacm.rel is the relevance judgement file
queries.txt is the list of queries which is used to test the effectiveness
The output of the program gets written to EffectivenessResult.txt which has details related to precision,recall etc which is asked in question. 
#######################################################################################################################################
################################################Note:##################################################################################
#######################################################################################################################################
In case softlink is created in the linux machine to point python to python3.4, then run the commands mentioned above like python check_effectiveness etc.
