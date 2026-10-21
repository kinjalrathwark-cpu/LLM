from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field 

Email_purpose=input("Enter the Email purpose:")
Recipient_type=input("Enter the Recipient type: ")
Important_details=input("Enter the Important details provided by the user: ")
Desired_tone=input("Enter the Desired tone: ")
to_name=input("Enter the to name: ")
from_name=input("Enter the from name: ")
start_date=input("Enter the start date: ")
end_date=input("Enter the end date: ")
return_date=input("Enter the return date: ")



# 1. Define Prompt Template with System and Human roles
prompt_template = ChatPromptTemplate.from_messages([
    ("system", " Email Generator"),
    ("human", "For this purpose  '{Email purpose/situation}' '{Recipient type}'  '{Important details provided by the user}' '{Desired tone}' '{to name}' '{from name}' '{start date}' '{end date}' '{return date}'  "),
   
])

api_key=os.getenv("GEMINI_API_KEY")

# 2. Initialize Real Google Gemini Chat Model
# Uses key from .env if present, otherwise uses placeholder until key is added
chat_model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key = api_key,
    temperature=0.7
)
output_parser = StrOutputParser()

first_chain = prompt_template | chat_model | output_parser

class EmailCheckerOutput(BaseModel):
    evaluation: str = Field(
        description="Overall evaluation of the generated email."
    )

    identified_issues: list[str] = Field(
        description="List of grammar, clarity, tone, professionalism, completeness, or subject-line problems."
    )

    suggestions: list[str] = Field(
        description="Specific suggestions for improving the email."
    )

    improved_email: str = Field(
        description="The fully improved version of the email, including subject, greeting, body and closing."
    )

email_checker_parser = PydanticOutputParser(
    pydantic_object=EmailCheckerOutput
)

# STAGE 2: EMAIL CHECKER PROMPT
checker_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an Email Quality Checker.

        Evaluate the email generated in Stage 1.

        Check the email for:

        1. Grammar
        2. Clarity
        3. Tone
        4. Professionalism
        5. Completeness
        6. Appropriate subject line
        """
    ),
    ("human", "Generated email: {generated_email}")
])

second_chain = checker_prompt | chat_model | email_checker_parser


# 5. Invoke the pipeline with user parameters
try:
    response = first_chain.invoke({"Email purpose/situation": Email_purpose, "Recipient type": Recipient_type, "Important details provided by the user": Important_details, "Desired tone": Desired_tone,"to name": to_name, "from name": from_name, "start date": start_date, "end date": end_date, "return date": return_date})
    print(response)
    print("Recipient type")
    print("Important details provided by the user")
    print("Desired tone")
except Exception as e:
    print("=" * 60)
    print("ℹ️ GEMINI API EXECUTION STATUS:")
    print("=" * 60)
    print("To execute this live against Google Gemini, please add your GEMINI_API_KEY to the .env file.")
    print(f"Notice: {e}")

#second chain 
try:
    response = first_chain.invoke({"Email purpose/situatuon":Email_purpose, "Recipient type": Recipient_type, "Important details provided by the user": Important_details, "Desired tone": Desired_tone,"to name": to_name, "from name": from_name, "start date": start_date, "end date": end_date, "return date": return_date})
    print(response)
    checker_result = second_chain.invoke({
       "generated_email": response,
       "format_instructions": email_checker_parser.get_format_instructions()
    })


    print("\n" + "=" * 60)
    print(" EMAIL CHECKER")
    print("=" * 60)

    print("\nEvaluation:")
    print(checker_result.evaluation)

    print("\nIdentified Issues:")
    for issue in checker_result.identified_issues:
        print(f"- {issue}")

    print("\nSuggestions:")
    for suggestion in checker_result.suggestions:
         print(f"- {suggestion}")

    print("\nImproved Email:")
    print(checker_result.improved_email)


except Exception as e:

    print("\n" + "=" * 60)
    print("GEMINI API EXECUTION ERROR")
    print("=" * 60)

    print(f"Error: {e}")    