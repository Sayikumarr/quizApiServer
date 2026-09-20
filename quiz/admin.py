from django.contrib import admin
from .models import Quiz, Question, Option, Result, UserAnswer, Update

# Register the Quiz model
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_created')
    search_fields = ('title',)

# Register the Question model
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question', 'answer_id')
    search_fields = ('question',)
    list_filter = ('quiz',)

# Register the Option model
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_id', 'option_text')
    search_fields = ('option_text',)
    list_filter = ('question',)

# Register the Result model
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'date_taken', 'user', 'name', 'score')
    search_fields = ('user', 'name')
    list_filter = ('quiz', 'date_taken')

# Register the UserAnswer model
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('result', 'question_id', 'user_answer_id')
    search_fields = ('question_id',)
    list_filter = ('result',)

# Register the Update model
@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')
    search_fields = ('title',)
