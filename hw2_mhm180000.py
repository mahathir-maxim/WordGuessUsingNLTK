'''
Name: Mahathir Maxim
Net Id: MHM180000
Course: CS 4395
Date:2/6/2022
Homework 2

Instruction for running:
created on python3
insert the relative path of the text file in main function
example: sys.argv.append('anat19.txt')
run the .py file
'''

import pathlib
import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from random import seed
from random import randint

seed(1234)

def readfile(filepath):
    '''
    opens the input file and reads from it
    Args:
        filepath: the relative path of the file
    Returns:
        the read text splitted into line separated list
    '''

    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        text_in = f.read()
    return text_in

def findLexicalDiversity(raw_text):
    '''
    gets the raw text, creates the tokens, does some processing and finds the lexical diversity
    Args:
        raw_text: the input text from the file
    Returns:
         lexical diversity and tokens
    '''

    tokens = word_tokenize(raw_text)
    tokens_p=[t for t in tokens]
    tokens_p=[t.lower() for t in tokens_p] #lower cases the tokens
    tokens_p=[t for t in tokens_p if t.isalpha()] #keeps only tokens that contains letters
    token_set = set(tokens_p) #unique set of tokens
    lexical_diversity = len(token_set) / len(tokens_p)
    tokens_p= [t for t in tokens_p if t not in stopwords.words('english')] #gets rid of stop words

    return lexical_diversity, tokens_p

def preprocess(tokens):
    '''
    preprocesses the tokens, creates list of nouns from that
    Args:
        tokens: list of tokens
    Returns:
        processed tokens and noun list
    '''
    tokensnow= [t for t in tokens if len(t)>5] #keeps only tokens with length>5
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokensnow] #gets lemmas for the tokens
    unique_lemmas=set(lemmatized) #unique lemmas
    pos_tags= nltk.pos_tag(unique_lemmas) #parts of speech tagging of the lemmas
    print('\n', pos_tags[:20]) #prints first 20 lemmas with pos
    nouns=[t for t, tag in pos_tags if ('NN' in tag)] #creates noun list
    print('\nNumber of tokens:', len(tokensnow))
    print('Number of nouns:', len(nouns))

    return nouns, tokensnow

def createDict(nouns, tokens):
    '''
    creates dictionary from noun list from tokens by number of times they appear and returns 50 most common words list
    Args:
        nouns: list of nouns
        tokens: processed tokens
    Returns:
         50 most common words list from the tokens that are nouns
    '''
    dict= {noun:tokens.count(noun) for noun in nouns} #creates the dict by number of time each noun appears in tokens
    sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True) #sorts the dict by number of time the keys appear
    common_word_list=[]
    i=0
    print(sorted_dict[:50])

    for t in sorted_dict:
        if i<50:
            common_word_list.append(t[0]) #stores the 50 common words in a list
            i+=1

    return common_word_list

def playAgain(wordList):
    '''
    restarts the word guess game once it finishes according to user input
    Args:
        wordList: list of 50 common words
    Returns:
        nothing
    '''
    userInput=input("Press Y if you want to play again. Else press N\n")
    if userInput=='Y' or userInput=='y':
        wordGuess(wordList)
    else:
        print('Thanks for playing!')

def wordGuess(wordList):
    '''
    driver function for word guess game where random words are selected and each player starts with 5 points and keeps guessing until
    the word is guessed or points go elow zero, whichever comes first
    Args:
        list of 50 words
    Returns:
        nothing
    '''
    score=5
    curr_word=wordList[randint(0, 49)] #a random word selected
    prompt='_'*len(curr_word) #empty prompt with _ created for word length
    attempts=len(curr_word)
    correctGuess=0 #used to see if word guessed correctly when it equals word length
    print('\nLets play a word guessing game')
    print(prompt)

    while 1:

        # when user score goes under zero, so the game terminates
        if score<0:
            print('\nYour score is below 0!')
            print('Game Ends!')
            print('The word is:', curr_word)
            break

        #reads user guess for letter
        guess=input('\nGuess a Letter:\n')

        #user presses ! for quitting the game
        if guess=='!':
            print('Quitting the game')
            break

        #checks if user inserted multiple letters or characters that are not letters
        while (not guess.isalpha()) or len(guess)>1:
            guess=input('Enter 1 letter from a to z in english alphabet!\n')
        charInd= curr_word.find(guess) #checks if the guessed letter is in the word

        #when the user guessed wrong
        if charInd==-1:
            score-=1
            attempts-=1
            print('Sorry, guess again!')
            print('Score is', score)
            print(prompt)

        #when user guessed right
        else:
            score+=1
            print('Right!')
            print('Score is', score)

            while charInd>-1:
                #update the prompt to show the guessed letters in the word in their respective positions and update the word to remove that letter
                prompt=prompt[0:charInd]+curr_word[charInd]+prompt[charInd+1:]
                curr_word=curr_word[0:charInd]+'_'+curr_word[charInd+1:]
                charInd = curr_word.find(guess)
                correctGuess += 1
            print(prompt)

        # when the user guessed all the letters in the word correct and wins the round
        if correctGuess==len(curr_word):
            print('You solved it!')
            break

    playAgain(wordList) # restarts the game


def main():
    '''
    The driver function for processing the text into tokens, getting common words and starting the word guess game
    Args:
        none
    Returns:
        none
    '''
    sys.argv.append('anat19.txt')  # relative path
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        raw_text = readfile(fp)  # call readfile with relative path to get the text

        lexical_diversity, tokens =findLexicalDiversity(raw_text) #gets the lexical diversity
        print("\nLexical diversity: %.2f" % lexical_diversity)
        nouns, processed_tokens=preprocess(tokens) #gets the noun list and processed tokens
        common_word_list=createDict(nouns, processed_tokens) #gets the 50 common words
        wordGuess(common_word_list) #Initiates the game


if __name__=="__main__":
    main()
