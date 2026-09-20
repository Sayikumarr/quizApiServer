# quizapp/serializers.py

from rest_framework import serializers
from .models import Quiz, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_id', 'option_text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'options', 'answer_id', 'related_md']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'date_created', 'questions']


from .models import Update

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = '__all__'

from rest_framework import serializers
from .models import Result, UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question_id', 'user_answer_id']

class ResultSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True)

    class Meta:
        model = Result
        fields = ['quiz', 'user', 'score', 'user_answers']
