from django.shortcuts import render
from .serializers import QuestionSerializer
from .models import Question
from rest_framework import generics
from rest_framework import mixins
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#importing libraries
import nltk
import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) 

fin = """
Hamile Kathmandu, Lalitpur, Bhaktapur Area ma Cake Delivery Garchhau. 

Payment garna ko lagi tapaile Esewa, Paypal choose garna saknu hunchha. 

Hamro ringroad vitra ko delivery charge Rs.50 chha ahni ringroad bahira 100 delivery charge lagxa. 

We have all flavor of cakes like White Forest Flavor, Black Forest, Chocolate, Red Velvet Flavors.

The Cake price cost ranges from Rs 600 to Rs 1200.
"""

# Create your views here.
class QuestionAPIView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        print(data)
        if 1==1:
            raw = fin.lower()
            #TOkenisation
            sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
            word_tokens = nltk.word_tokenize(raw)# converts to list of words

            lemmer = WordNetLemmatizer()
            def LemTokens(tokens):
                return [lemmer.lemmatize(token) for token in tokens]
            remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
            def LemNormalize(text):
                return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

            GREETING_INPUTS = ("hello", "hi", "greetings", "what's up","hey",)
            GREETING_RESPONSES = ["Hi, Welcome to Your Koseli - Online Cake Delivery", "hey, Welcome to Your Koseli - Online Cake Delivery"]

            def greeting(sentence):
                """If user's input is a greeting, return a greeting response"""
                for word in sentence.split():
                    if word.lower() in GREETING_INPUTS:
                        return random.choice(GREETING_RESPONSES)

            # Generating response
            def response(user_response):
                robo_response=''
                sent_tokens.append(user_response)
                TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
                tfidf = TfidfVec.fit_transform(sent_tokens)
                vals = cosine_similarity(tfidf[-1], tfidf)
                idx=vals.argsort()[0][-2]
                flat = vals.flatten()
                flat.sort()
                req_tfidf = flat[-2]
                if(req_tfidf==0):
                    robo_response=robo_response+"I am sorry! I don't understand you, You can whatsapp/viber us for any queries!"
                    return robo_response
                else:
                    robo_response = robo_response+sent_tokens[idx]
                    return robo_response   

            flag=True
            while(flag==True):
                user_response = data
                user_response=user_response.lower()
                if(user_response!='bye'):
                    if(user_response=='thanks' or user_response=='thank you' ):
                        flag=False
                        print("YK BOT: You are welcome..")
                    else:
                        if(greeting(user_response)!=None):
                            return HttpResponse(greeting(user_response)) 
                        else:
                            return HttpResponse(response(user_response)) 
                else:
                    flag=False
                    return HttpResponse("Good Bye!") 
        return JsonResponse("wrng", status=status.HTTP_400_BAD_REQUEST)