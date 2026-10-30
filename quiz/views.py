from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Quiz, Result, Question, Option
from .serializers import QuizSerializer

class QuizViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def latest_quiz(self, request):
        user = request.query_params.get('user_token')  # Or use request.headers.get('User') as needed
        
        if not user:
            return Response({"message": "User not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the latest quiz that contains questions
        latest_quiz = Quiz.objects.filter(questions__isnull=False).distinct().order_by('-id').first()
        
        if not latest_quiz:
            return Response({"message": "No quizzes found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already completed the latest quiz
        if Result.objects.filter(quiz=latest_quiz, user=user).exists():
            # Check previous quizzes that actually have questions
            all_quizzes = Quiz.objects.filter(id__lte=latest_quiz.id, questions__isnull=False).distinct().order_by('-id')
            for quiz in all_quizzes:
                if not Result.objects.filter(quiz=quiz, user=user).exists():
                    quiz_serializer = QuizSerializer(quiz)
                    quiz_data = quiz_serializer.data

                    # Formatting questions as a separate list
                    questions = quiz_data.pop('questions')
                    if not questions:
                        continue
                    formatted_data = {"quiz": quiz_data, "questions": questions}

                    return Response(formatted_data)

            # If all quizzes are completed
            return Response({"message": "All quizzes completed"}, status=status.HTTP_200_OK)

        # If the latest quiz is not completed, return the latest quiz
        quiz_serializer = QuizSerializer(latest_quiz)
        quiz_data = quiz_serializer.data

        # Formatting questions as a separate list
        questions = quiz_data.pop('questions')
        if not questions:
            return Response({"message": "No questions found in latest quiz"}, status=status.HTTP_404_NOT_FOUND)
        formatted_data = {"quiz": quiz_data, "questions": questions}

        return Response(formatted_data)




from .models import Update
from .serializers import UpdateSerializer
from rest_framework import generics

class UpdateList(generics.ListAPIView):
    queryset = Update.objects.all().order_by('-date_created')
    serializer_class = UpdateSerializer


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Quiz, Result, UserAnswer
from .serializers import ResultSerializer

@api_view(['POST'])
def save_results(request):
    data = request.data
    quiz_id = data.get('quizId')
    user = data.get('user_token')
    user_name = data.get('user_name')
    results = data.get('results')

    # Ensure quiz exists
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check for duplicate submission
    if Result.objects.filter(quiz=quiz, user=user).exists():
        return Response({"error": "You have already submitted results for this quiz."}, status=status.HTTP_409_CONFLICT)

    # Create Result object
    result = Result.objects.create(quiz=quiz, user=user, score=0, name=user_name)
    
    # Calculate score and create UserAnswer objects
    score = 0
    for item in results:
        question_id = item.get('question_id')
        user_answer_id = item.get('user_answer')
        
        # Save user answer
        UserAnswer.objects.create(result=result, question_id=question_id, user_answer_id=user_answer_id)
        
        # Check if answer is correct (assuming `answer_id` is the correct answer in Question model)
        if user_answer_id == str(quiz.questions.get(id=question_id).answer_id):
            score += 1
    
    # Update result score
    result.score = score
    result.save()

    # Serialize the response
    response_data = {
        "quizId": quiz_id,
        "user_token": user,
        "user_name": user_name,
        "results": results
    }

    return Response(response_data, status=status.HTTP_201_CREATED)


from django.db import transaction

@api_view(['POST'])
def create_quiz(request):
    """
    Public endpoint to create a new Quiz with Questions and Options from AI JSON.
    Payload:
    [
      {"title": "...", "description": "..."},
      [
        {
          "question": "...",
          "options": [{"1": "..."}, {"2": "..."}, {"3": "..."}, {"4": "..."}],
          "answer": "1",
          "related_md": "..."
        }
      ]
    ]
    """
    data = request.data
    if not isinstance(data, list) or len(data) < 2:
        return Response({"error": "Invalid format. Expected [metadata_dict, questions_list]."}, status=status.HTTP_400_BAD_REQUEST)

    meta = data[0]
    questions_list = data[1]

    title = meta.get('title')
    description = meta.get('description', '')
    if not title:
        return Response({"error": "Quiz title is required."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        quiz = Quiz.objects.create(title=title, description=description)

        created_questions = 0
        for q in questions_list:
            q_text = q.get('question', '')
            answer_id = str(q.get('answer', '1'))
            related_md = q.get('related_md', '')

            question_obj = Question.objects.create(
                quiz=quiz,
                question=q_text,
                answer_id=answer_id,
                related_md=related_md
            )
            created_questions += 1

            options = q.get('options', [])
            for opt_dict in options:
                if isinstance(opt_dict, dict):
                    for opt_id, opt_text in opt_dict.items():
                        Option.objects.create(
                            question=question_obj,
                            option_id=str(opt_id),
                            option_text=str(opt_text)
                        )

    return Response({
        "status": "success",
        "quiz_id": quiz.id,
        "title": quiz.title,
        "questions_count": created_questions
    }, status=status.HTTP_201_CREATED)

