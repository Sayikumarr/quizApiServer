import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from quiz.models import Quiz, Question, Option

class Command(BaseCommand):
    help = 'Populates the database with quiz data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Assuming the first element is the quiz data and the second element is the list of questions
        quiz_data = data[0]
        questions_data = data[1]

        # Create or update the Quiz object, excluding id and dateTime
        quiz, created = Quiz.objects.update_or_create(
            title=quiz_data['title'],
            defaults={
                'description': quiz_data['description'],
                'date_created': timezone.now()
            }
        )

        for question_data in questions_data:
            # Create or update the Question object, excluding id
            question, created = Question.objects.update_or_create(
                quiz=quiz,
                question=question_data['question'],
                defaults={
                    'answer_id': question_data['answer'],
                    'related_md': question_data['related_md']
                }
            )

            for option_data in question_data['options']:
                # Create Option objects
                for option_id, option_text in option_data.items():
                    Option.objects.update_or_create(
                        question=question,
                        option_id=option_id,
                        defaults={'option_text': option_text}
                    )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with quiz data'))
