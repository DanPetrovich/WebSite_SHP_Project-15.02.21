from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import *

'''
Класс, хранящий данные об одном отдельном голосовании
'''


class votings(models.Model):
    id = models.AutoField(primary_key=True)

    # Имя голосования
    name = models.TextField(default='Voting')

    # id автора голосования
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # дата создания голосования
    date_created = models.TextField(default="30/02/0001")

    # Публичное или приватное голосование
    is_public = models.BooleanField(default=False)

    # Тип голосования(дискретное, 1 из множества, несколько из множества)
    type = models.TextField(default='')

    # Описание голосования
    description = models.TextField(default='No Description')

    # Вопрос голосования
    question = models.TextField(default='Question')

    # Кол-во лайков
    likes_number = models.IntegerField(default=0)

    # Кол-во комментариев
    comments_number = models.IntegerField(default=0)

    # Кол-во проголосовавших пользователей
    times_voted = models.IntegerField(default=0)


'''
Класс, хранящий данные об одном ответе на голосование.
'''


class voting_answers(models.Model):
    id = models.AutoField(primary_key=True)

    # Текст ответа
    text = models.TextField(default='Answer')

    # Сколько раз этот ответ был выбран
    times_selected = models.IntegerField(default=0)

    # Голосование, для которого этот ответ
    voting_id = models.ForeignKey(default=1, to=votings, on_delete=models.CASCADE)


'''
Запись о том, кто уже принял участие в голосовании.
'''


class voted_user_record(models.Model):
    id = models.AutoField(primary_key=True)

    # id человека, уже проголосовавшего в голосовании
    voted_person_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # Голосование, для которого этот ответ
    voting_id = models.ForeignKey(default=1, to=votings, on_delete=models.CASCADE)


'''
класс создания жалоб
'''

class complaints(models.Model):
    id = models.AutoField(primary_key=True)

    voting_id = models.ForeignKey(default=1, to=votings, on_delete=models.CASCADE)

    # id автора голосования
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # Тип голосования
    type = models.TextField(default='')

    # Описание жалобы
    description = models.TextField(default='No Description')

    # дата создания жалобы
    date_added = models.TextField(default="30/02/0001")

    # Ответили ли на жалобу
    is_answered = models.BooleanField(default=False)

    # Ответ
    answer = models.TextField(default='')

    # дата создания жалобы
    date_answer = models.TextField(default="30/02/0001")
