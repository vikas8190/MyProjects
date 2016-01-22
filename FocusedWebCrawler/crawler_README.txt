######################################################################################################################################
##########################################Focused WebCrawler #########################################################
######################################################################################################################################
Web Crawler
Language used: Python
Compiler version: 3.4
Environment: Linux

######################################################################################################################################
###########################################Description:###############################################################################
######################################################################################################################################
The webcrawler starts with the seed link "http://en.wikipedia.org/wiki/Hugh_of_Saint-Cher" and works in below two ways:
1.In case of no keyword, it starts from the seed link and fetches the first 1000 links outwards until particular depth at which  1000 links are found.
2.In case of "concordance" keyword, it starts from seed link and returns whatever links which has the keyword among the first 1000 links which are crawled. 
The links present in a webpage is further crawled only if the keyword is present in the webpage.

#######################################################################################################################################
############################################Pre Run Instructions:######################################################################
#######################################################################################################################################
Python version 3.x expected
Beautifulsoap,requests library to be installed(Installation instructions are below)

#######################################################################################################################################
#############################################Installation instructions:################################################################
#######################################################################################################################################
pip3.4 install requests
pip3.4 install beautifulsoup4

#######################################################################################################################################
##############################################Program run instructions:################################################################
#######################################################################################################################################
For run without any keyword:
python3.4 IR_webcrawler.py > output_file.txt
For run without "concordance" as keyword:
python3.4 IR_webcrawler.py concordance >output_file.txt

The output of the program gets written to output_file.txt
#######################################################################################################################################
################################################Note:##################################################################################
#######################################################################################################################################
In case softlink is created in the linux machine to point python to python3.4, then run the commands mentioned above like python IR_web_crawler.py etc.
To install the libraries for python admin privilege might be required.
