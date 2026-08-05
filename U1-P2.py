gpt4 = {'Develpore' : 'OpenAI',
         'open Source' : 'No ',
         'multimodel Support' : 'Text, Images, Audio (in supported products)', 
         'Typical use case' : 'General AI assistant, coding, content generation, data analysis, customer support'} 
claude3 = {'Develpore' : 'Anthropic',
          'open Source': 'No',
          'multimodel Support' : 'Text, Images',
          'Typical use case' : 'Long-document analysis, enterprise assistants, coding, writing, reasoning'} 
gamini = {'Develpore' : 'Google',
          'open Source' : 'No',
          'multimodel Support': 'Text, Images, Audio, Video, Code',
          'Typical use case ': 'Search, productivity, document understanding, coding, multimodal AI assistants'} 
Llama3 = {'Develpore' : 'Meta',
           'open Source ': 'Yes (open-weight with community license)',
           'multimodel Support' : 'Text (Llama 3), Text + Images (Llama 3.2 Vision)'
           'Typical use case :  Research, fine-tuning, local AI applications, chatbots, coding'} 
Mistral = {'Develpore' : 'Mistral AI',
          'open Source' : 'Partially',
          'multimodel Support' : 'Text, Images, Audio',
          'Typical use case' : 'Chatbots, enterprise AI, coding assistants, document analysis, on-premise AI deployments'}



choiceModels=int(input("1.GPT-4 ,2.Clude 3, 3.Gemini, 4.Llama 3, 5.Mistral "
                       "\nEnter Youre Choice:"))



if  choiceModels == 1: 
    print("\nGPT-4")
    for key, value in gpt4.items():
           print(key, ":" ,value)

elif choiceModels == 2:
        print("\nClude 3")
        for key,value in claude3.items():
               print(key, ":" ,value)

elif choiceModels == 3:
        print("Gamini")
        for key,value in gamini.items():
                print(key, ":" ,value)

elif choiceModels == 4:
        print("Llama 3")
        for key,value in Llama3.items():
                print(key, ":" ,value)

elif choiceModels == 5:
        print("Mistral")
        for key,value in Mistral.items():
                print(key, ":" ,value)

else:
       print("Invalid model choice!")

    





#create a python application to compare major Large language Models.
# include the following model:
#GPR-4
#cluded 3
#gemini
#Llama 3
#Mistral


#Display
#Develpore
#open Source
#multimodel Support
#Typical use case 