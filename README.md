# Spam-filter-with-Naive-Bayes-Classifier
### Problem Description and Data Set
The aim of this project is to build a Naïve Bayes Spam filter. You will be able to download a labeled training set file and a labeled test set file from Canvas. Both files will have the same format. Each line will start with either a 1 (Spam) or a 0 (Ham), then a space, followed by an email subject line. A third file will contain a list of Stop Words—common words that you should remove from your vocabulary list. Format of the Stop Word list will be one word per line.
### Assignment
Your program should prompt the user for the name of a training set file in the format described above and the name of the file of Stop Words. Your program should create a vocabulary of words found in the subject lines of the training set associated with an estimated probability of each word appearing in a Spam and the estimated probability of each word appearing in a Ham email. Your program should then prompt the user for a labeled test set and predict the class (1 = Spam, 0 = Ham) of each subject line using a Naïve Bayes approach as discussed in class. Note: We may or may not test your program on the same files that you used to create it!

### Output to the screen of your program should include:
• How many Spam and Ham emails were in the Test set file that was read in. <br />
• Number of False Positives, True Positives, False Negatives and True Negatives that your spam filter predicted.<br />
• Accuracy, precision, recall and F1 values for your Spam filter on the Test Set file.<br />
