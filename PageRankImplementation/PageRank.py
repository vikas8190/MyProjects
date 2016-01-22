#author : Vikas Janardhanan
import math
import time
import operator
import sys

d=0.85
PR={}
newPR={}
f=open('PageRank_output.txt','w')
def read_from_file(filename):
	page_map={}
	with open(filename) as file_content:
		lines=[line.rstrip() for line in file_content]
		for line in lines:
			page_list=line.split(' ')
			page_map[page_list[0]]=list(set(page_list[1:len(page_list)]))
	return page_map

def get_value_list(page_map):
	val_list=[]
	L={}	
	Source=[]
	for key,value in page_map.items():
		if not value:
			Source.append(key)
		else:
			val_list+=value
			for v in value:
				if v in L:
					L[v]+=1
				else:
					L[v]=1
	return val_list,L,Source

def get_perplexity(PR):
	entropy=0
	for page in PR:
		p=PR[page]
		entropy+=p*math.log(1/p,2)
	return 2**(entropy)

def set_initial_rank(P,N):
	for page in P:
		PR[page]=1.0/N
	return PR

def get_sinkPR(PR,S):
	sinkPR=0
	for sinkpage in S:
		sinkPR+=PR[sinkpage]
	return sinkPR

def get_newPR(PR,P,M,L,N,S):
	d=0.85
	sinkPR=get_sinkPR(PR,S);
	for page in P:
		newPR[page]=(1.0-d)/N
		newPR[page]+=d*(sinkPR/N)
		if page in M:
			for q in M[page]:
				newPR[page]+=d*PR[q]/L[q]
	return newPR

def compute_pagerank(P,M,L,N,S):
	newPR=get_newPR(PR,P,M,L,N,S)
	for page in P:
		PR[page]=newPR[page]

def compute_pagerank_cont(P,M,L,N,S):
	i=1
	f.writelines("############################################################\n")
	while(i<=100):
		compute_pagerank(P,M,L,N,S)
		if(i in (1,10,100)):
			f.writelines("PageRank Value for iteration no "+str(i)+":\n")
			sPR=sorted(PR.items(),key=operator.itemgetter(1),reverse=True)
			for page in sPR:
				f.writelines(page)
			f.writelines("############################################################\n")
		i+=1
	

def compute_pagerank_until_converges(P,M,L,N,S):
	per_count=0
	prev_p=get_perplexity(PR)
	i=1
	f.writelines("#####################################################################\n")
	while per_count < 4:
		f.writelines("Iteration no:"+str(i)+":\n")
		if(i%10==0):
			print("PageRank computation in progress. Please wait..............Currently running in "+str(i)+"th iteration .")
		compute_pagerank(P,M,L,N,S)
		curr_p=get_perplexity(PR)
		f.writelines("Perplexity: "+str(curr_p)+"\n")
		f.writelines("#####################################################################\n")
		if math.fabs(curr_p-prev_p) <  1:
			per_count+=1
		else:
			per_count=0
		prev_p=curr_p
		i=i+1

def print_results(M,Source,S,N):
	inlink_count={}
	sPR=sorted(PR.items(),key=operator.itemgetter(1),reverse=True)[:50]
	f.writelines("##########################################################################\n")
	f.writelines("Top 50 pages in decreasing order of pageRank\n")
	f.writelines("(Page,PageRank)\n")
	for page in sPR:
		f.writelines(str(page)+"\n")	
	f.writelines("##########################################################################\n")
	f.writelines("Top 50 pages in decreasing order of inlink count\n")
	for key,value in M.items():
		inlink_count[key]=len(value)
	inlink_count=sorted(inlink_count.items(),key=operator.itemgetter(1),reverse=True)[:50]
	for page in inlink_count:
		f.writelines(str(page)+"\n")
	f.writelines("##########################################################################\n")
	f.writelines("Proportion of pages with no in-links:"+str(len(Source)/N)+"\n")	
	f.writelines("Proportion of pages with no out-links:"+str(len(S)/N)+"\n")
	cnt=0
	initial_rank=1.0/N
	for page in PR:
		if(PR[page] < initial_rank):
			cnt+=1
	f.writelines("Proportion of pages whose PageRank is less than initial uniform values:"+str(cnt/N)+"\n")
	
	

def main(argv):
	mode=input("Do you want to run pagerank computation with convergence. Type Yes if so : ")
	start_time=time.time()
	P=[]
	M={}
	S=[]
	if argv:
		filename=argv[0]
	else:
		filename="wt2g_inlinks"
	M=read_from_file(filename)
	
	P=list(M.keys())
	V,L,Source=get_value_list(M)
	f.writelines("source count : "+str(len(Source))+"\n")
	S=set(P)-set(V)
	t=list(set(V)-set(P))
	P=P+t
	N=len(P)
	PR=set_initial_rank(P,N)
	if(mode=="Yes" or mode=="yes"):
		compute_pagerank_until_converges(P,M,L,N,S)
		print_results(M,Source,S,N)
	else:
		compute_pagerank_cont(P,M,L,N,S)
	print("Run completed in --- %s seconds ---" % (time.time() - start_time))


main(sys.argv[1:])
