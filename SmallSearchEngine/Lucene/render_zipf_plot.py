import matplotlib.pyplot as plt
import sys
import math

def read_word_freq(index_filename):
	freq=[]
	f=open(index_filename)
	word_freq_contents=f.read().replace('\n',' ').split(' ')
	word_freq_contents=[x for x in word_freq_contents if x!='']
	freq_sum=0
	for word_freq in word_freq_contents:
		word_freq_pair=word_freq.split(':')
		freq_sum+=float(word_freq_pair[1])
		freq.append(float(word_freq_pair[1]))
	freq.sort(reverse=True)
	freq_prob=[x/freq_sum for x in freq]
	rank=list(xrange(len(freq_prob)+1))
	log_freq_prob=[math.log(x) for x in freq_prob]
	log_rank=[math.log(x) for x in rank[1:]]
	#print freq_prob
	print freq_sum
	rank=rank[1:]
	return freq_prob,rank,log_freq_prob,log_rank
	#print freq	

def render_plot(freq_prob,rank,log_freq_prob,log_rank):
	#plt.rcParams['backend'] = 'TkAgg' 
	plt.figure("Zipf Curve plot")
	plt.subplot(211)
	plt.plot(rank,freq_prob)
	plt.ylabel('Probability of Occurence')
	plt.xlabel('Rank(by decreasing frequency)')
	plt.subplot(212)
	plt.plot(log_rank,log_freq_prob)
	plt.ylabel('Log of Probability of Occurence')
	plt.xlabel('Log of Rank(by decreasing frequency)')
	#plt.locator_params(nbins=4)
	plt.show()

def main(argv):
	if argv:
		index_filename=argv[0]
	else:
		index_filename="IndexStats.txt"
	freq_prob,rank,log_freq_prob,log_rank=read_word_freq(index_filename)
	render_plot(freq_prob,rank,log_freq_prob,log_rank)

main(sys.argv[1:])
