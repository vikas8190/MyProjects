import sys
import re
import math

## Translates the content of given queries.txt to map query to the ID in file
def get_query_to_id_map(queries,query_to_id):
	for query in queries:
		querymap=[x[:-1] for x in query.split('(') if x!='']
		if querymap:
			query_to_id[querymap[0]]=querymap[1]

# Reads the Result filename of HW4. Iterates through it and populates hash containing map from query to List of tuples
## which has details of DocID and its corresponding score
def get_retrieved_docset(query_to_id,retrieved_docset,result_filename):
	f=open(result_filename,"r")
	all_result=[x for x in f.read().split('\n') if x!='']
	docno=[]
	for result in all_result:
		match=re.match(r'Found.*?for\s(.*)',result)
		if match:
			query=match.group(1)
		else:
			docno_regex=re.match(r'\d+[.]\sCACM-0*(.*)[.]html\sscore=(.*)',result)
			if docno_regex:
				docno.append((docno_regex.group(1),docno_regex.group(2)))
			if len(docno) == 100:
				retrieved_docset[query]=docno
				docno=[]

## Details from cacm.rel is read into hashmap which maps the query to list of its relevant docs
def get_relevant_docset(query_to_id,relevant_docset,relevant_filename):
	f=open(relevant_filename,"r")
	all_result=[x for x in f.read().split('\n') if x!='']
	for query in query_to_id:
		docset=[]
		for result in all_result:
			result_items=result.split(' ')
			if int(result_items[0])== int(query_to_id[query]):
				docid=result_items[2].split('-')[1]	
				docset.append(docid)
		relevant_docset[query]=docset

# Computes the recall and precision values for the given Retrieved docset and the Relevant doc set
def get_recall_precision(ret_docset,rel_docset):
	precision=[]
	recall=[]
	match_count=0
	tot_count=0
	avg_precision=0
	sum_match_precision=0
	for docno in ret_docset:
		tot_count+=1
		if docno[0] in rel_docset:
			match_count=match_count+1
			sum_match_precision+=match_count/tot_count
		recall_value=match_count/len(rel_docset)
		precision_value=match_count/tot_count
		precision.append((docno[0],precision_value))
		recall.append((docno[0],recall_value))
	avg_precision=sum_match_precision/len(rel_docset)
	return precision,recall,avg_precision

#Computes NDCG given the relevant set and the total number of relevant docs as per relevance judgement file
def get_ndcg(rel_set,tot_rel_docs):
	ndcg=[]
	ideal_rel_set=[1]*tot_rel_docs
	ideal_rel_set=ideal_rel_set+[0]*(len(rel_set)-tot_rel_docs)
	ndcg=get_ndcg_values(rel_set,ideal_rel_set)
	return ndcg

def get_ndcg_values(rel_set,ideal_rel_set):
	dcg_values=[]
	ideal_dcg_values=[]
	ndcg_values=[]
	get_dcg_values(rel_set,dcg_values)
	get_dcg_values(ideal_rel_set,ideal_dcg_values)
	for i in range(0,len(dcg_values)):
		ndcg_values.append(dcg_values[i]/ideal_dcg_values[i]) if ideal_dcg_values[i]!=0 else  ndcg_values.append(0)
	return ndcg_values


def get_dcg_values(rel_set,dcg_values):
	cur_val=0
	p=1
	for rel in rel_set:
		if p > 2:	
			gain=rel/math.log(p,2)
		else:
			gain=rel
		dcg_values.append(cur_val+gain)
		cur_val=cur_val+gain
		p=p+1

def main(argv):
	if argv:
		result_filename=argv[0]
		query_filename=argv[1]
		relevant_filename=argv[2]
	query_to_id={}
	precision=[]
	recall=[]
	ndcg=[]
	f=open(query_filename,"r")
	queries=f.read().split('\n')
	get_query_to_id_map(queries,query_to_id)
	retrieved_docset={}
	relevant_docset={}
	q_id=1
	get_retrieved_docset(query_to_id,retrieved_docset,result_filename)
	get_relevant_docset(query_to_id,relevant_docset,relevant_filename)
	sum_avg_precision=0
	for query in ('portable operating systems','code optimization for space efficiency','parallel algorithms'):
		rel_level=[]
		print("#######################################################################################################################################################")
		print("query : "+str(query))
		print("#######################################################################################################################################################")
		for doc in retrieved_docset[query]:
			rel_level.append(1) if doc[0] in relevant_docset[query] else rel_level.append(0)
		precision,recall,avg_precision=get_recall_precision(retrieved_docset[query],relevant_docset[query])
		sum_avg_precision+=avg_precision
		p_at_k20,r_at_k20,avg_precision=get_recall_precision(retrieved_docset[query][0:20],relevant_docset[query])
		p_at_k20=p_at_k20[len(p_at_k20)-1]
		ndcg=get_ndcg(rel_level,len(relevant_docset[query]))
		print('Rank'.ljust(25)+'Document ID'.ljust(25)+'Document Score'.ljust(25)+'Relevance Level'.ljust(25)+'Precision'.ljust(25)+'Recall'.ljust(25)+'NDCG'.ljust(25))
		for i in range(0,len(precision)):
			score=0
			docno=precision[i][0]
			relevance_level=0
			if docno in relevant_docset[query]:
				relevance_level=1
			for doc in retrieved_docset[query]:
				if docno==doc[0]:
					score=doc[1]
			print(str(i+1).ljust(25)+str(docno).ljust(25)+str(score).ljust(25)+str(relevance_level).ljust(25)+str(precision[i][1]).ljust(25)+str(recall[i][1]).ljust(25)+str(ndcg[i]).ljust(25))
		print('P@K where k=20  : '+str(p_at_k20[1]))
	print('MAP '+str(sum_avg_precision/3))

main(sys.argv[1:])
