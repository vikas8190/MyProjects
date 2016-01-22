######################################################################################################################################
##########################################Page Rank Calculator #########################################################
######################################################################################################################################
Page Rank Calculator
Language used: Python
Compiler version: 3.4
Environment: Linux

######################################################################################################################################
###########################################Description:###############################################################################
######################################################################################################################################
This compute PageRank on a collection of 183,811 web documents. The page rank calculator takes in the file name containing the inlink 
graph details. The Algorithm for page rank is as per the details given in the problem set as:
while PageRank has not converged do
  sinkPR = 0
  foreach page p in S                  /* calculate total sink PR */
    sinkPR += PR(p)
  foreach page p in P
    newPR(p) = (1-d)/N                 /* teleportation */
    newPR(p) += d*sinkPR/N             /* spread remaining sink PR evenly */
    foreach page q in M(p)             /* pages pointing to p */
      newPR(p) += d*PR(q)/L(q)         /* add share of PageRank from in-links */
  foreach page p
    PR(p) = newPR(p)
 
#######################################################################################################################################
############################################Pre Run Instructions:######################################################################
#######################################################################################################################################
Python version 3.x expected

#######################################################################################################################################
##############################################Program run instructions:################################################################
#######################################################################################################################################
For run with convergence:
python3.4 PageRank.py 
Do you want to run pagerank computation with convergence. Type Yes if so : Yes
For run without convergence for sample graph: 
python3.4 IR_webcrawler.py concordance >output_file.txt
Do you want to run pagerank computation with convergence. Type Yes if so : No 

The output of the program gets written to PageRank_output.txt in the same directory where PageRank.py is placed. 
#######################################################################################################################################
################################################Note:##################################################################################
#######################################################################################################################################
In case softlink is created in the linux machine to point python to python3.4, then run the commands mentioned above like python PageRank.py etc.

