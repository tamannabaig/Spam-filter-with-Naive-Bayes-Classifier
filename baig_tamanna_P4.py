# -*- coding: utf-8 -*-
"""
Date: Mon Oct 28 2019
@author: Tamanna Baig
Project 4: Spam-Ham Classifier

"""
'''******************************************************************'''

import pandas as pd
import math

def cleantext(line):
#    spl = [","",[,]!.,"-!-@;':#/$%^&*()+/?"""]
    line = line.lower()
    line = line.strip()
    for char in line:
        
        if char in """[]!.,"-!@;_':#$%^&*()–+/?\’|{<>}:0123456789\x92\x97\x94\x93\x96""":
        #"""~!@#$%^&*()_-+|{}[]<>?/\=\"\'':0123456789\x92\x97\x94\x93\x96""":
        #"""[]!.,"-!@;_':#$%^&*()+/?""":
#            print(char)    
            line = line.replace(char, " ")
    return line

def countwords(words, is_spam, counted):
    for each_word in words:
        if each_word in counted:
            if is_spam == 1:
                counted[each_word][1] += 1
            else:
                counted[each_word][0] += 1
        else:
            if is_spam == 1:
                counted[each_word] = [0, 1]
            else:
                counted[each_word] = [1, 0]
    return counted

def make_percent_list(k, count_dict, spams, hams):
    for each_key in count_dict:
        count_dict[each_key][0] = (count_dict[each_key][0] + k)/(2*k + hams)
        count_dict[each_key][1] = (count_dict[each_key][1] + k)/(2*k + spams)
    
    
    return count_dict

def calc_prob(test_words, vocab, test_spam, test_ham):
    # 1 is for spam values
    # 0 is for ham values
#    print(test_spam)
#    print(test_ham)
    
    x = test_spam/(test_spam+test_ham)
    y = test_ham/(test_spam+test_ham)
    
    s_temp = 1
    h_temp = 1
    pred = list()
    for key,val in vocab.items():
        if key in test_words:
            h_temp = h_temp + math.log(val[0])
            s_temp = s_temp + math.log(val[1])
#            s_temp = s_temp * val[0]
#            h_temp = h_temp * val[1]
        else:
            #print('else')
#            s_temp = s_temp * (1-val[0])
#            h_temp = h_temp * (1-val[1])
            h_temp = h_temp + math.log(1-val[0])
            s_temp = s_temp + math.log(1-val[1])
            
    h = math.exp(h_temp)
    s = math.exp(s_temp)
#    s = s_temp
#    h = h_temp

    stu = (s*x)/((s*x)+(h*y))
    
#    print(s, h, x, y)
    if(stu > 0.5):
        pred = 1 #Spam
    else:
        pred = 0 #Ham

    return pred
    
def calc_final_values(actual, predictions, spam, ham):
    
    print('___________________________________________________\n')
    print('RESULTS OF THE SPAM FILTER ARE DISPLAYED BELOW:')
    print('------------------------------------------------')
    print('Number of spam entried in Test: ', spam)
    print('Number of ham entried in Test: ', ham)
    
    tn = 0 #TN = True Negatives: actual = 0, pred = 0
    tp = 0 #TP = True Positives: actual = 1, pred = 1
    fp = 0 #FP = False Positives: actual = 0 pred = 1 [Type 1 Error] 
    fn = 0 #FN = False Negatives: actual = 1 pred = 0 [Type 2 Error]
    
    for i in range(len(predictions)):
        if (actual[i] == 0 and predictions[i] == 0):
            tn += 1
        if (actual[i] == 1 and predictions[i] == 1):
            tp += 1
        if (actual[i] == 0 and predictions[i] == 1):
            fp += 1
        if (actual[i] == 1 and predictions[i] == 0):
            fn += 1    
    #Calculate Accuracy
    
    accuracy = (tn + tp)/len(predictions)
    precision = tp/(tp + fp)
    recall = tp/(tp + fn)
    
    f1 = 2 * precision * recall / (precision + recall)
          
    print('--------------------------------------')
    print('True Positive: ', tp)
    print('True Negative: ', tn)
    print('False Positive: ', fp)
    print('True Negative: ', fn)
    print('--------------------------------------')
    print('Accuracy :', round(accuracy,3))
    print('Precision: ', round(precision,3))
    print('Recall: ', round(recall,3))
    print('F1 Score: ', round(f1,3))

'''******************************************************************'''    
def main():
        
    #Initial Values
    
    spam = 0
    ham = 0
    counted = dict()
    
    train_file = str(input("Enter the name of the training file:  (Ex: GEASTrain.txt)\n"))
    stop_file = str(input("Enter the name of file with StopWords: (Ex: stopWords.txt)\n"))
    
#    train_file = 'GEASTrain.txt'
#    test_file = 'GEASTest.txt'
#    example = 'example.txt'
#    stop_file = 'StopWords.txt'
    
    stopwords = pd.read_csv(stop_file, header = None)
    stoplist = stopwords[0].tolist()
    
    file = open(train_file, "r")
    textLine = file.readline()
    #print(textLine)
    while textLine != "":
       # print(textLine)
        is_spam = int(textLine[:1])
    #    print(is_spam)
        if(is_spam == 1):
            spam += 1   #Counts total number of spam entries in train file
        else:
            ham += 1    #Counts total number of ham entries in train file
        
        
        textLine = cleantext(textLine[1:])

        words = textLine.split()
    #    print('words: ', words)
    
    #To remove the stopwords from the word list'''
        for w in words:
            if w in stoplist:
                words.remove(w)
                #print(w)
        
        words = set(words)
        
        counted = countwords(words, is_spam, counted)
        textLine = file.readline()
    
    vocab = (make_percent_list(0.5, counted, spam, ham))
    
#    print(vocab['your'])
   
    file.close()
    
    
    print('\n------------------------------------------------------------')
    print('The Calculations on training set has completed!!' )
    print('--------------------------------------------------------------')
    test_spam = 0
    test_ham = 0
    predictions = list()
    actual = list()
    
    test_file = str(input("Enter the name of the test file:  (Ex: GEASTest.txt)\n"))
    
#    calculate_test_results(test_file, vocab)
    t = open(test_file, "r")
    test_line = t.readline()

    while test_line != "":
        #print(test_line)
        is_test_spam = int(test_line[:1])
        actual.append(is_test_spam)
        if(is_test_spam == 1):
            test_spam += 1   #Counts total number of spam entries in train file
        else:
            test_ham += 1    #Counts total number of ham entries in train file
            
#    print(test_spam, test_ham)
    
        test_line = cleantext(test_line[1:])
        test_words = test_line.split()
    #    print('words: ', test_words)
    
    #To remove the stopwords from the word list
#        print('before stoplist: ',len(test_words))
        for tw in test_words:
            if tw in stoplist:
                test_words.remove(tw)
#        print('after stoplist: ',len(test_words))        
        test_words = set(test_words)
#        print(test_words)
#        print('set: ',len(test_words))
        pred = calc_prob(test_words, vocab, test_spam, test_ham)
        
        predictions.append(pred)
               
        #Goes to next line
        test_line = t.readline()
         
    t.close()
    
#    print(actual)
#    print(predictions)
    
    calc_final_values(actual, predictions, test_spam, test_ham)
    
main()