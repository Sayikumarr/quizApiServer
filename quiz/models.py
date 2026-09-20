from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    answer_id = models.CharField(max_length=10)
    related_md = models.TextField(blank=True, null=True)

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_id = models.CharField(max_length=10)
    option_text = models.CharField(max_length=255)

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='results', on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    score = models.IntegerField()

class UserAnswer(models.Model):
    result = models.ForeignKey(Result, related_name='user_answers', on_delete=models.CASCADE)
    question_id = models.IntegerField()
    user_answer_id = models.CharField(max_length=10)


class Update(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
