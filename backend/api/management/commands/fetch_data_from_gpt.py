# your_app/management/commands/my_custom_command.py
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from openai import OpenAI
import json 



def chat_with_chatgpt():
    
    
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
    )

    response = chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Generate a json file that includes food. The only parameter should be the name of the dish and the list of ingredients."
            }
        ],
    model="gpt-3.5-turbo",
    )

    contentString = response.choices[0].message.content

    data_list = json.loads(contentString)

    print(data_list)

    recipeNameList = [];
    recipeIngredientList = [];



class Command(BaseCommand):

    help = 'Your custom command description here'

    def handle(self, *args, **options):
        # Your script or actions here

        

        user_prompt = "Write a summary of the benefits of exercise."
        chat_with_chatgpt()
    
        self.stdout.write(self.style.SUCCESS('Successfully executed your custom command'))
        
