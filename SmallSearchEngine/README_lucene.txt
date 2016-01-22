######################################################################################################################################
##########################################Lucene Implementation #########################################################
######################################################################################################################################
Introduction to Lucene: Setup, indexing, search
Zipf’s law
Language used: Java 1.8_0_65, Python 2.7
Environment: Linux

######################################################################################################################################
###########################################Description and Deliverables:###############################################################################
######################################################################################################################################
This program uses Lucene to index given CACM corpus. Each file in the CACM corpus is indexed using Lucene Simple Analyzer. The Top ranked
documents for each of the query in queryfile.txt along with the best highlight for each of the document that is found as match is
returned as output in a file "Results.txt". Besides for rendering the Zipf’s plot, details of word-frequency in the stored Index
is returned in another file "IndexStats.txt".
Logic for DocSnippet Match:
In each document match, the regular expression matching each word in query till end of file is taken. Among these, the largest match is taken and from
that the first 200 chars are taken as the highlight
Ex: If the document has 
"Glossary of Computer Engineering and Programming Terminology

CACM June, 1958

CA580603 JB March 22, 1978  9:07 PM

19	5	19
19	5	19
19	5	19"

and query is "Engineering Programming".

The two matches would be str1-"string starting from Engineering till end of file"" and str2 - "the string starting from Programming till end of file".
Since str1 is larger, the output produced would be 200 chars starting from word Engineering in the file.

Deliverables:
Results.txt -> Containts details of the Top ranked documents for each query along with their atmost 200 character document highlight snippet. Max is limited to 100 hits.
queryfile.txt -> The given queries for which the above details are generated.
IndexStats.txt -> The word-frequency pair for the index built by Lucene which is the basis for rendering the Zipf’s Curve.
ZipfPlot.xlsx -> The Zipf curve plot for the above index statistics.
results.eval -> The output file from running bm25 script for the given queries based on which the comparison with Lucene output is done.
ResultComparisonwithBM25.xlsx -> The comparison of hits of the given query in Lucene and the BM25 script.
Information_Retrieval_HW4 -> The project folder for the Lucene Indexer. Import this into Eclipse as project. This contains HW4.java.
HW4.jar -> Jar built with the above project folder. Keep folder CACM with all the CACM files in the same directory as the jar and run it.

Inaddition the below script can be run if the plot has to be rendered dynamically:
render_zipf_plot.py -> Renders the zipf curve using matplotlib library. Expects "IndexStats.txt" to be present in folder where the script is run.
zipf_curve_plot.png -> Generated zipf curve plot from above python script run.

#######################################################################################################################################
############################################Pre Run Instructions:######################################################################
#######################################################################################################################################
Python version 2.x expected
Java 1.8 version

Install matplotlib directions:
yum-builddep python-matplotlib
yum install tkinter.x86_64
yum install python3-tkinter.x86_64
yum install ScientificPython-tk.x86_64
pip install matplotlib

#######################################################################################################################################
##############################################Program run instructions:################################################################
#######################################################################################################################################
To run the Lucene Indexer, use either of the below two ways:
1. Import the given Project into Eclipse. Add the 3 lucene jars: 1) lucene-core-VERSION.jar, 2) lucene-queryparser-VERSION.jar, and 3) lucene-analyzers-common-VERSION.jar
as external library jars to the project and run src/HW4.java.

Or

2. Run HW4.jar using java - jar HW4.jar .
Ensure that CACM folder with all the CACM files are in the same directory as the jar.
This generates files IndexStats.txt Results.txt.

To run the zipf plot script dynamically use:

python zipf_curve_plot.py
Ensure that IndexStats.txt generated from the jar run is present in the same directory.
 
#######################################################################################################################################
################################################Note:##################################################################################
#######################################################################################################################################
matplotlib graph generation in python is tested in Fedora. In case it doesnt workout in MAC OSX, xlsx file where in the plots are
rendered are also given as deliverable.
