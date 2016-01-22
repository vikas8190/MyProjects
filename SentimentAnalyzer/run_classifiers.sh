# running unigram
echo "Running unigram classifier model with laplace smoothing"
python3.4 unigram/nbtrain.py "textcat/train" model_unigram.txt
python3.4 unigram/nbtest.py model_unigram.txt "textcat/test" prediction_test.txt
python3.4 unigram/nbtest.py model_unigram.txt "textcat/dev/pos" prediction_dev_pos.txt
python3.4 unigram/nbtest.py model_unigram.txt "textcat/dev/neg" prediction_dev_neg.txt
# running bigrams
echo "Running bigram classifier with laplace smoothing"
python3.4 bigram/nbtrain_bigram.py "textcat/train" model_bigram.txt
python3.4 bigram/nbtest_bigram.py model_bigram.txt "textcat/test" bigram_prediction_test.txt
python3.4 bigram/nbtest_bigram.py model_bigram.txt "textcat/dev/pos" bigram_prediction_dev_pos.txt
python3.4 bigram/nbtest_bigram.py model_bigram.txt "textcat/dev/neg" bigram_prediction_dev_neg.txt
# running dirichlet smoothed
echo "Running unigram classifier with laplace smoothing"
python3.4 dirichlet/nbtrain_dirichlet.py "textcat/train" model_dirichlet.txt 0.35
python3.4 dirichlet/nbtest_dirichlet.py model_dirichlet.txt "textcat/test" dirichlet_prediction_test.txt
python3.4 dirichlet/nbtest_dirichlet.py model_dirichlet.txt "textcat/dev/pos" dirichlet_prediction_dev_pos.txt
python3.4 dirichlet/nbtest_dirichlet.py model_dirichlet.txt "textcat/dev/neg" dirichlet_prediction_dev_neg.txt
