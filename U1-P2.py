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
llama3 = {'Develpore' : 'Meta',
           'open Source ': 'Yes (open-weight with community license)',
           'multimodel Support' : 'Text (Llama 3), Text + Images (Llama 3.2 Vision)'
           'Typical use case :  Research, fine-tuning, local AI applications, chatbots, coding'} 
mistral = {'Develpore' : 'Mistral AI',
          'open Source' : 'Partially',
          'multimodel Support' : 'Text, Images, Audio',
          'Typical use case' : 'Chatbots, enterprise AI, coding assistants, document analysis, on-premise AI deployments'}

print('gpt4')
print('claude3')
print('gamini')
print('llama3')
print('mistral')

choice_Models= input("Enter Topic Name :")
choiceModels = choice_Models.upper()


if  choiceModels == 'gpt4' or  choiceModels == 'GPT 4': 
    print(gpt4)
    
elif choice_Models == 'claude3' or choiceModels == 'Claude 3':
        print(claude3)
        
elif choice_Models == 'gamini' or choiceModels == 'Gamini':
        print(gamini)
        
elif choice_Models == 'llama3' or choiceModels == 'Llama 3':
        print(llama3)
        
elif choice_Models == 'mistral' or choiceModels == 'Mistral':
        print(mistral)
        
else:
       print("Invalid model choice!")

    









