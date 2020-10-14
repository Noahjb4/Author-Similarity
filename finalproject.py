#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:25:54 2019

@author: noahjb
"""
import math

class TextModel:
    
    def __init__(self, model_name):
        
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.letters = {}
        self.symbols = {}
        self.dicts1 = ['words', 'word_lengths', 'stems', 'sentence_lengths', 'letters', 'symbols' ]
        self.dicts2 = [self.words, self.word_lengths, self.stems ,self.sentence_lengths, self.letters, self.symbols ]
        
        
        
    def __repr__(self):
        
        """Return a string representation of the TextModel."""
        
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of letters: ' + str(len(self.letters)) + '\n'
        s += '  number of symbols: ' + str(len(self.symbols)) + '\n'
        return s
    

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        
        word_list = clean_text(s) 
        symbol_list = symbols(s)
        
        for w in word_list:
            if w not in self.words: 
                self.words[w] = 1
            else:
                self.words[w] += 1
    
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            
            for l in w:
                if l not in self.letters:
                    self.letters[l] = 1
                else:
                    self.letters[l] += 1
                    
            
            wordstem = stem(w) 
            if wordstem not in self.stems:
                if ((wordstem + 'e') in self.stems):
                    self.stems[wordstem+'e'] += 1
                elif (wordstem[:-1] in self.stems):
                    self.stems[wordstem[:-1]]
                else:
                    self.stems[wordstem] = 1
            else:
                self.stems[wordstem] += 1 
            
                
        period = s.split('. ')

        for w in period:

            m = 1

            for z in w:

                if z == ' ':

                    m += 1

            if m not in self.sentence_lengths:

                self.sentence_lengths[m] = 1

            else:

                self.sentence_lengths[m] +=1
                    
                    
        for s in symbol_list:
            if s not in self.symbols:
                self.symbols[s] = 1
            else:
                self.symbols[s] += 1
            
                    
            
        
    
    def add_file(self, filename):
        """ add text of a file to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        
        self.add_string(text)
        
    def save_model(self):
        """saves the models dictionaries"""
        for i in range(len(self.dicts1)):
            f = open((self.name+'_'+self.dicts1[i]), 'w')      
            f.write(str(self.dicts2[i]))
            f.close
    
    def read_model(self):
        """copies saved dictionaires to a model"""
        for i in range(len(self.dicts1)):
            f = open((self.name+'_'+self.dicts1[i]), 'r')
            dstr = f.read()
            f.close
            
            self.dicts2[i] = dict(eval(dstr))
        
        self.words = self.dicts2[0]
        self.word_lengths = self.dicts2[1]
        self.stems = self.dicts2[2]
        self.sentence_lengths = self.dicts2[3]
        self.letters = self.dicts2[4]
        self.symbols = self.dicts2[5]
        
    def similarity_scores(self, other):
        """creates a score of similarity between text"""
        scores = []
        
        for i in range(len(self.dicts2)):
            dict_score = compare_dictionaries(other.dicts2[i] ,self.dicts2[i])
            scores += [dict_score]
        
        return scores
    
    def classify(self, source1, source2):
        """determines if which source is more similar to the text"""
        
        scores1 = source1.similarity_scores(self)
        scores2 = source2.similarity_scores(self)
        
        print('scores for ' +source1.name+ ':', scores1)
        print('scores for ' +source2.name+ ':', scores2)
        print()
        
        sum1 = 0
        sum2 = 0
        total1 = 0
        total2 = 0
        weights = [10,7,5,7,1,3]
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                sum1 += 1
            else:
                sum2 += 1
            total1 += weights[i]*scores1[i]
            total2 += weights[i]*scores2[i]
        
        if sum1 > sum2:
            print(self.name + ' is more likely to come from ' + source1.name)
            print(sum1,sum2)
            print()
        elif sum2 > sum1:
            print(self.name + ' is more likely to come from ' + source2.name)
            print(sum1,sum2)
            print()
        else:
            if total1 > total2:
                print(self.name + ' is more likely to come from ' + source1.name)
                print(total1,total2)
                print()
            else:
                print(self.name + ' is more likely to come from ' + source2.name)
                print(total1,total2)
                print()
            
        

def stem(s):
    """takes words and returnes their root"""
    if (len(s)>1) and (s[-1] != 's'):
        if (len(s)>5) and (s[-3:] == 'ing'):
            if s[-4] == s[-5] and s[-5] == 'm':
                s = s[:-4]
            else:
                s = s[:-3]
                
        elif (s[-2:] == 'er' or s[-2:] == 'al' or s[-2:] == 'ac' or\
              s[-2:] == 'ar' or s[-2:] == 'or'):
            s = s[:-2]
            
        elif s[-4:] == 'able' or s[-4:] == 'sion' or\
            s[-4:] == 'tion' or s[-4:] == 'ship' or s[-4:] == 'ment':
            if s[-4:] == 'sion':
                s = s[:-3]
            else:
                s = s[:-4]
            
        elif (len(s) > 5) and (s[-3:] == 'ade' or\
             s[-3:] == 'ism' or s[-3:] == 'age' or\
             s[-3:] == 'ate' or s[-3:] == 'ful' or\
             s[-3:] == 'ize' or s[-3:] == 'ive'):
            
            s = s[:-3] 
        
    
    elif len(s)>1:
        
        s = stem(s[:-1])
    
    return s

        
def symbols(txt):
    """returns the symbols of a text"""
    nt = ''
    lct = txt.lower()
    for i in range(len(lct)):
        if lct[i] not in ' abcdefghijklmnopqrstuvwxyz':
            nt += lct[i]
    
    return list(nt)


def clean_text(txt):
    """ removes symbols and spaces from text"""
    nt = ''
    
    for i in range(len(txt)):
        if txt[i] not in '!@#$%^&*()":;?.,}{[]\<>+-_=|`~':
            nt += txt[i]
            
    return nt.lower().split()


def compare_dictionaries(d1, d2):
    """gives a similarity score betweeen 2 dictionairies"""
    
    score = 0
    total = 0
    
    for i in d1:
        total += d1[i]
    
    for i in d2:
        if i in d1:
            score += d2[i]*(math.log(d1[i]/total))
        else:
            score += math.log(0.5/total)
    
    return score


def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    print(mystery.similarity_scores(source1)) 
    print(compare_dictionaries(source1.word_lengths, mystery.word_lengths))
    
def run_tests():
    """ your docstring goes here """
    source1 = TextModel('J.K. rowling')
    source1.add_file('rowling.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('Harry Potter Book 5')
    new1.add_file('book5.txt')
    new1.classify(source1, source2)
   
    new2 = TextModel('bible')
    new2.add_file('bible.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('The Spanish Tragedy')
    new3.add_file('kyd.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel("Grimms' Fairy Tales")
    new4.add_file('tales.txt')
    new4.classify(source1, source2)
    
    new5 = TextModel('Poems By Rupert Brook')
    new5.add_file('poems.txt')
    new5.classify(source1, source2)
    
    

    
    
        