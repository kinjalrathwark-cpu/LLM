nlp  = {
'Domain_name': "NLP",
'Description': "Natural language processing ",
'Realword': "text summariser"  ,
'libraries': "nltk,spacy" }

computer_vision = {
'Domain_name' : "NLP",
'Description ': "Natural language processing ",
'Real_Word' : "text summariser" ,
'libraries' : "nltk,spacy" }

speech_processing = {
'Domain_name' : "NLP",
'Description ': "Natural language processing ",
'Real-Word' : "text summariser" ,
'libraries' : "nltk,spacy" }

robotics = {
'Domain_name' : "NLP",
'Description ': "Natural language processing ",
'Real_Word' : "text summariser" ,
'libraries' : "nltk,spacy" }


print('Please seclt your option')
print('1.nlp')
print('2.coputer_vision')
print('3.speech_processing')
print('4.robotics')

choic=int(input('Enter your number'))

if choic==1:
    print(nlp)
elif choic==2:
    print(computer_vision)
elif choic==3:
    print(speech_processing)
elif choic==4:
    print(robotics)
else:
    print("Enter Valid Number")
