import json
import re

from django.core.management.base import BaseCommand, CommandError
from openai import OpenAI


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("recipe_names", nargs="+", type=str)

    def handle(self, *args, **options):
        for recipe_name in options["recipe_names"]:
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)
            #
            # poll.opened = False
            # poll.save()

            client = OpenAI(
                # defaults to os.environ.get("OPENAI_API_KEY")
                api_key="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",
            )

            response = chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Get me a json list of ingredients for " + recipe_name + " containing only the names separated by comma"
                    }
                ],
                model="gpt-3.5-turbo",
            )

            contentString = response.choices[0].message.content
            print(contentString)

            if "```json" in contentString:
                matches = re.findall(r'```json(.*?)```', contentString, re.DOTALL)
                contentString = matches[0]
            #matches = "".join(matches)
            #matches = matches.replace('\\n', '')

            print("------")

            print(contentString)

            print("------")

            data_list = json.loads(contentString)

            print(data_list['ingredients'])

            self.stdout.write(
                self.style.SUCCESS('Successfully created recipe "%s"' % recipe_name)
            )