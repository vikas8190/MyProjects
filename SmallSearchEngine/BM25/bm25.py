import sys
import math
import operator
import re

# Returns the count of occurence of the word in the document
def frequency_of_term_in_doc(word_index,docno):
	for posting in word_index:
		if docno == posting[0]:
			fi=posting[1]
			break
		else:
			fi=0
	return fi

# Returns the score for the current term which is being evaluated whose details and the document number for which we are calculating score are given to function
def get_term_score(ni,fi,N,qfi,doc_stats,docno):
	k1=1.2
	b=0.75
	k2=100
	score=0
	if fi==0:
		score=0
	else:
		dl=doc_stats[docno]
		total_len=0
		for doc in doc_stats:
			total_len+=doc_stats[doc]
		avdl=total_len/N
		K=k1*((1-b)+b*(dl/avdl))
		comp1=(N-ni+0.5)/(ni+0.5)
		comp2=((k1+1)*fi)/(K+fi)
		comp3=((k2+1)*qfi)/(k2+qfi)
		score=math.log(comp1)*comp2*comp3
	return score

# Returns the bm25 score for the given query
def calculate_bm25(index,doc_stats,query):
	N=len(doc_stats)
	doc_score={}
	query_stats={}
	for term in query.split(' '):
		if term in query_stats:
			query_stats[term]+=1
		else:
			query_stats[term]=1
	for docno in doc_stats:
		score=0
		for term in query_stats:
			qfi=query_stats[term]
			if term in index:
				ni=len(index[term])
				fi=frequency_of_term_in_doc(index[term],docno)
			else:
				ni=0
				fi=0
			score+=get_term_score(ni,fi,N,qfi,doc_stats,docno)
		doc_score[docno]=score
	return doc_score


# Reads the index file and populates the info to index dictionary.
# The info in index.out is split with '#' and ' ' and then ':' to fetch information to populate the index dictionary. The posting for a word is stored as list of tuples
def get_index_info(index_filename):
	index={}
	doc_stats={}
	f=open(index_filename)
	index_content=f.read().replace('\n',' ').split('#')
	for index_info in index_content:
		posting_list=[]
		if len(index_info) == 0:
			continue
		else:
			index_info_list=index_info.split(' ')
			index_info_list=[x for x in index_info_list if x!='']
			word=index_info_list[0]
			for posting in index_info_list[1:]:
				posting_info=posting.split(':')
				docno=int(posting_info[0])
				doc_count=int(posting_info[1])
				if docno in doc_stats:
					doc_stats[docno]+=doc_count
				else:
					doc_stats[docno]=doc_count
				posting_val=(docno,doc_count)
				posting_list.append(posting_val)
			index[word]=posting_list
	f.close()
	return index,doc_stats


def main(argv):
	if argv:
		index_filename=argv[0]
		query_filename=argv[1]
		maxdocs=argv[2]
	index,doc_stats=get_index_info(index_filename)
	query_id=1
	with open(query_filename) as query_content:
		queries=[query.rstrip() for query in query_content]
		# iterates query by query calculates the score for all documents for the query and prints the top results
		for query in queries:
			doc_score=calculate_bm25(index,doc_stats,query)
			sorted_docscore=sorted(doc_score.items(),key=operator.itemgetter(1),reverse=True)[:int(maxdocs)]
			doc_rank=1
			for doc in sorted_docscore:
				print(str(query_id)+" "+"Q0 "+str(doc[0])+" "+str(doc_rank)+" "+str(doc[1])+" system_name")
				doc_rank+=1
			query_id+=1

main(sys.argv[1:])
