# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 01:10:12 2021

@author: Pushpa
"""
import streamlit as st 
import pickle
import string
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

def app():
    
    unigrams = pickle.load(open("./pickle/unigramslist.pkl", 'rb'))
    #dfbiagramcolle1 = pickle.load(open("./pickle/dfbiagramcolle.pkl", 'rb'))
    #dfbiagramcolle = pd.DataFrame(dfbiagramcolle1) 
    #dftriagramcolle1= pickle.load(open("./pickle/dftriagramcolle.pkl", 'rb'))
    #dftriagramcolle = pd.DataFrame(dftriagramcolle1) 
    dfbiagramcolle = pd.read_pickle("./pickle/dfbiagramcolle.pkl")
    dftriagramcolle = pd.read_pickle("./pickle/dftriagramcolle.pkl")
    
    st.title("Prediction Results")
    number = st.sidebar.slider("Select the number of words to predict :", min_value=1, max_value = 10, value=5)
    word = st.sidebar.text_input(label = "Enter the Word/letters")
       
    if (st.sidebar.button("Predict")): 
        printinput = word
        #print("statement is: " + printinput)
        
        printinput=printinput.lower()
        printinput=printinput.translate(str.maketrans('','','01234567890'))
        #print(string.punctuation)
        #print(printinput)
        
        
        flaglist=string.punctuation
        flag=0
        
        for i in range(len(flaglist)):
            if str.endswith(printinput,flaglist[i]):
                flag=flag+1
                
        #print("Flag is "+ str(flag))
        
        if flag==0 :
            
            if str.endswith(printinput," ") :
                #print("Biagram and Triagram")
                # filter1 = dfbiagramcolle["Search1"]== printinput
                # filter2 = dftriagramcolle["Search1"]== printinput[1]
                frames = [dftriagramcolle, dfbiagramcolle]
                df = pd.concat(frames)
                #print(dftriagramcolle.head())
                #print(dfbiagramcolle.head())
                printinput=printinput.strip()
                printinput=printinput.translate(str.maketrans('','',string.punctuation))
                #print(len(printinput))
                words = printinput.split()
                #print(words)
                if len(words) == 1:
                    #print("Biagram and Triagram if")
                    df = df.loc[df['Search1']==words[0]]
                else:
                    print("Biagram and Triagram else")
                    words= words[-2]+" "+words[-1]
                    print(words)
                    df = df.loc[df['Search1']==words]
                df.reset_index()
                df = df.sort_values(by='Freq',ascending=False)
                #print(df.head(10))
                selection = df[['Word', 'Freq', 'Next']]
                #print("Top 10 next word prediction is ")
                #print(selection.head(10))
                df_1=selection.head(number)
                df_1.reset_index()
                if len(df_1) >0:
                    st.text('Input Text:' + printinput) 
                    st.text('Prediction type: (3) [space] - Previous Word Complete; Predicts Next Word.')
                    st.text('Predicted Words:')
                    st.dataframe(df_1)
                    st.title("Bar Chart")
                    fig = plt.figure(figsize = (10, 5))
                    plt.barh(df_1['Word'], df_1['Freq'])
                    plt.xlabel("Number of Freq")
                    plt.ylabel("Words")    
                    plt.title("Word Freq Count") 
                    st.pyplot(fig)
                    st.title("Word Cloud")
                    # plot word cloud
                    # word cloud options
                    # https://www.datacamp.com/community/tutorials/wordcloud-python
                    #print('\n*** Plot Word Cloud - Top 100 ***')
                    d = {}
                    for a, x in df_1[['Word','Freq']].values:
                        d[a] = x 
                    print(d)
                    wordcloud = WordCloud(background_color="white")
                    wordcloud.generate_from_frequencies(frequencies=d)
                    fig = plt.figure(figsize = (10, 5))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    st.pyplot(fig)
                else:
                    st.text('Input Text:' + printinput) 
                    st.text('No predicted Words found:')
            else :
                #print("Unigram")
                printinput=printinput.strip()
                printinput=printinput.translate(str.maketrans('','',string.punctuation))
                words = printinput.split()
                newlist =[]
                print(words)
                if len(words) == 1:
                    words=words[0]
                else:
                    words=words[-1]
                print(words)
                for i in range(len(unigrams)):       
                    if str.startswith(unigrams[i],words) or (words==unigrams[i]):
                        newlist.append(unigrams[i])
                dfnewlist = Counter(newlist)
                #print(newlist)
                
                if len(dfnewlist) >0:
                    df  = pd.DataFrame.from_dict(dfnewlist, orient='index').reset_index()
                    df.columns = ['Word','Freq']
                    #print(df.head())
                    df = df.sort_values(by='Freq',ascending=False)
                    #print(df.head(10))
                    selection = df[['Word','Freq']]
                    #print("Top 10 next word prediction is ")
                    #print(selection.head(10))
                    df_1=selection.head(number)
                    df_1.reset_index()
                    st.text('Input Text:' + printinput) 
                    st.text('Prediction type: (2) [alphabet] - Word Maybe Incomplete; Predicts Current Word.')
                    st.text('Predicted Words:')
                    st.dataframe(df_1)
                    st.title("Bar Chart")
                    fig = plt.figure(figsize = (10, 5))
                    plt.barh(df_1['Word'], df_1['Freq'])
                    plt.xlabel("Number of Freq")
                    plt.ylabel("Words")    
                    plt.title("Word Freq Count")
                    st.pyplot(fig)
                    st.title("Word Cloud")
                    # plot word cloud
                    # word cloud options
                    # https://www.datacamp.com/community/tutorials/wordcloud-python
                    #print('\n*** Plot Word Cloud - Top 100 ***')
                    d = {}
                    for a, x in df_1[['Word','Freq']].values:
                        d[a] = x 
                    print(d)
                    wordcloud = WordCloud(background_color="white")
                    wordcloud.generate_from_frequencies(frequencies=d)
                    fig = plt.figure(figsize = (10, 5))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    st.pyplot(fig)
                else:
                    st.text('Input Text:' + printinput) 
                    st.text('No predicted Words found:')
    
        else:
            st.text('Input Text:' + word) 
            st.text('No prediction due to punctuation')
            st.text('Prediction type: (1) [punctuation] - No Prediction.')
            #print("No prediction due to punctuation")
        
    st.sidebar.info("INSTRUCTIONS")
    st.sidebar.info('To predict next word, please type a sentence or a phrase.\n At least three chars requried. Use slider control to increase or decrease count of predicted words.\n For best results count should be 5 or more')
    
    
    st.sidebar.info('Word Prediction Is Based On The Last Character: (1) [punctuation] - No Prediction. (2) [alphabet] - Word Maybe Incomplete; Predicts Current Word. (3) [space] - Previous Word Complete; Predicts Next Word')

                 
