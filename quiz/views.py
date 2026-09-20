from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Quiz, Result
from .serializers import QuizSerializer

class QuizViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def latest_quiz(self, request):
        user = request.query_params.get('user_token')  # Or use request.headers.get('User') as needed
        
        if not user:
            return Response({"message": "User not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the latest quiz based on ID
        latest_quiz = Quiz.objects.order_by('-id').first()
        
        if not latest_quiz:
            return Response({"message": "No quizzes found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already completed the latest quiz
        if Result.objects.filter(quiz=latest_quiz, user=user).exists():
            # Check if the user has completed all previous quizzes
            all_quizzes = Quiz.objects.filter(id__lte=latest_quiz.id).order_by('-id')  # Fetch all quizzes up to the latest
            for quiz in all_quizzes:
                if not Result.objects.filter(quiz=quiz, user=user).exists():
                    quiz_serializer = QuizSerializer(quiz)
                    quiz_data = quiz_serializer.data

                    # Formatting questions as a separate list
                    questions = quiz_data.pop('questions')
                    formatted_data = {"quiz": quiz_data, "questions": questions}

                    return Response(formatted_data)

            # If all quizzes are completed
            return Response({"message": "All quizzes completed"}, status=status.HTTP_200_OK)

        # If the latest quiz is not completed, return the latest quiz
        quiz_serializer = QuizSerializer(latest_quiz)
        quiz_data = quiz_serializer.data

        # Formatting questions as a separate list
        questions = quiz_data.pop('questions')
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
