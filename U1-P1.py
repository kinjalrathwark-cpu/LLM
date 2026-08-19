nlp  = {
'Domain_name': "Natural language processing",
'Description': " NLP helps computer understand human language.",
'Applications': "Chatbots"  ,
'Python libraries': "NLTK,spaCy" }

computer_vision = {
'Domain_name' : "Computer Vision",
'Description ': "Computer vision helps computer understand images.",
'Real_Word' : "Face Recognition Medical Images Analysis" ,
'Pythom libraries' : "OpenCV" }

speech_processing = {
'Domain_name' : "Speech Processing",
'Description ': "Speech Processing helps computer understand and generate humna speech. ",
'Real-Word' : "Speech-to-Text" ,
'Pthon libraries' : "SpeechRecognition,pyAudio" }

robotics = {
'Domain_name' : "Robotics",
'Description ': "Robotics user AI to make robots perform intelligent tasks.",
'Real_Word' : "Industrial Robots, Self-driving Robots" ,
'libraries' : "openCV,ROS" }
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
