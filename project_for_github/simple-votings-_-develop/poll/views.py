from django.http import HttpResponse
from datetime import date, datetime

from poll.models import *
from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from poll.forms import SignUpForm

'''
Получить почту и имя пользователя 
'''


def get_user_info(request):
    try:
        name = request.user.username
        mail = request.user.email
    except:
        name = "AnonimusUser"
        mail = "anon@mail.com"

    return (name, mail)


def index(request):
    return HttpResponse("Привет, это первый маленький шажок в вашем приложении! (зайдите на votings)")


# Выбор типа создаваемого голосования
def voting_type_choose(request):
    user_data = get_user_info(request)
    ctx = {
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, 'voting_type_choose.html', ctx)


# Конструктор голосований
def voting_ctor(request):
    type = request.GET.get("vt")
    user_data = get_user_info(request)
    ctx = {
        "type": type,
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, "voting_ctor.html", ctx)


# Отображает голосования, в которых пользователь может принять участие
def vote(request):
    v_object_public = votings.objects.all()[::-1]
    # Выбираем из всех доступных голосований те, в которых пользователь еще не принимал учатсие
    records = voted_user_record.objects.filter(voted_person_id=request.user)
    # Голосования, в которых пользователь уже прининял участие(id)
    passed_votings_id = []
    for el in records:
        passed_votings_id.append(el.voting_id.id)
    good_votings = []
    for el in v_object_public:
        if el.id not in passed_votings_id:
            good_votings.append(el)

    v_object_private = votings.objects.filter(type="private")

    user_data = get_user_info(request)

    ctx = {
        'type': 'voting',
        'public_votings': good_votings,
        'private_votings': v_object_private,
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, 'votings_shower.html', ctx)


# Личный кабинет
def cabinet(request):
    user_data = get_user_info(request)

    ctx = {
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, "user_cabinet.html", ctx)


'''
Страница, показывающая данные конкретного голосование.
'''


def show_concrete_voting(request):
    voting_id = request.GET.get("voting_id", 1)

    # Проверка на то, что пользователь не проходит голосование 2ой раз
    records = voted_user_record.objects.filter(voting_id=voting_id)

    user_data = get_user_info(request)

    for el in records:
        if el.voted_person_id == request.user:
            ctx = {
                'can_vote': False,
                'voting_id': voting_id,
                'user_name': user_data[0],
                'user_mail': user_data[1]
            }
            return render(request, "concrete_voting_shower.html", ctx)

    # Отображаемое голосование и его тип
    voting = (votings.objects.filter(id=voting_id))[0]
    voting_type = voting.type

    # Переменная для корректного определения падежа в надписи "Проголосовало x человек"
    special_letter = voting.times_voted % 10

    # Ответы на голосование
    answers = voting_answers.objects.filter(voting_id=voting_id)
    data = []
    for el in answers:
        data.append(el.text)

    ctx = {
        'can_vote': True,
        'answers': data,
        'name': voting.name,
        'description': voting.description,
        'question': voting.question,
        'visitors': voting.times_voted,
        "author": "ТвойГолос team",
        'date': "30/2/0001",
        'letter': special_letter,
        'voting_id': voting_id,
        'type': voting_type,
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, "concrete_voting_shower.html", ctx)


'''
Страница, показывающая результаты конкретного голосования.
'''


def show_voting_result(request):
    # Отображаемое голосование
    voting_id = request.GET.get("voting_id", 1)
    voting = (votings.objects.filter(id=voting_id))[0]

    # Показываем, что кол-во пользователей, прошедших голосований, увеличилось(переменная av("after-voting") показывает,
    # что пользователь проголосовал, а не просто просматривает результаты)
    # Также заносим в бд запись, что пользователь проголосовал
    av = request.GET.get("av", False)
    if av:
        voting.times_voted += 1
        voting.save()

        record = voted_user_record(voting_id=voting, voted_person_id=request.user)
        record.save()

    # Переменная для корректного определения падежа в надписи "Проголосовало x человек"
    special_letter = voting.times_voted % 10

    # Ответы на голосование из базы данных
    answers = voting_answers.objects.filter(voting_id=voting_id)

    # Ответы, выбранные пользователями
    if voting.type != "many_from_many":
        chosen_answers = [request.GET.get("chosen", "error")]
    else:
        chosen_answers = request.POST.get("answers", "error")
        chosen_answers = chosen_answers.split(',')

    # Увеличиваем значение times_selected у выбранного(ых) ответов
    for answer in chosen_answers:
        for el in answers:
            if el.text == answer:
                el.times_selected += 1
                el.save()

    # Ответы на голосование из базы данных(обновленные)
    answers = voting_answers.objects.filter(voting_id=voting_id)

    data = []
    for el in answers:
        data.append([el.text, el.times_selected])

    # Последний ответ пользователя(дя корректной постановки запятых в блоке с ответами, которые выбрал пользователь)
    if voting.type != "many_from_many":
        last = chosen_answers[-1][0]
    else:
        last = chosen_answers[0]

    user_data = get_user_info(request)
    url = 'http://127.0.0.1:8000/complaint?voting_id=' + voting_id
    ctx = {
        'answers': data,
        'name': voting.name,
        'description': voting.description,
        'question': voting.question,
        'visitors': voting.times_voted,
        "author": "ТвойГолос team",
        'date': "30/2/0001",
        'letter': special_letter,
        'voting_id': voting_id,
        'complaint_href': url,
        'chosen': chosen_answers,
        'last': last,
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, "voting_result.html", ctx)


# Страница, которая добавляет данные о голосовании в бд
def create_voting(request):
    # Удалось ли создать голосование
    creation_success = True

    type = request.GET.get("vt")
    user_data = get_user_info(request)

    try:
        if type == "discrete":
            name = request.POST.get("v_name")
            question = request.POST.get("v_question")
            # Проверка на случай, если пользователь не ввел название голосования
            if name == "":
                name = question

            description = request.POST.get("v_description")
            answer1 = request.POST.get("v_a1")
            answer2 = request.POST.get("v_a2")

            # Создание голосования
            voting = votings(name=name, question=question, description=description, author=request.user,
                             type="discrete")
            voting.save()

            # Создание ответов к голосованию
            v_answer1 = voting_answers(voting_id=voting, text=answer1)
            v_answer1.save()
            v_answer2 = voting_answers(voting_id=voting, text=answer2)
            v_answer2.save()

        else:
            name = request.POST.get("v_name")
            question = request.POST.get("v_question")
            # Проверка на случай, если пользователь не ввел название голосования
            if name == "":
                name = question

            description = request.POST.get("v_description")
            answers = request.POST.get("v_a")
            answers = answers.split(',')  # Изначально вопросы разделены запятыми

            # Создание голосования
            if type == "one_from_many":
                voting = votings(name=name, question=question, description=description, author=request.user,
                                 type="one_from_many")
            else:
                voting = votings(name=name, question=question, description=description, author=request.user,
                                 type="many_from_many")
            voting.save()

            # Создание ответов к голосованию
            for el in answers:
                v_answer = voting_answers(voting_id=voting, text=el)
                v_answer.save()

    except:
        creation_success = False

    ctx = {
        "creation_success": creation_success,
        "name": name,
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, "create_voting.html", ctx)


'''
Редактировать голосование
'''


def voting_editing(request):
    user_data = get_user_info(request)

    # Отображаемое голосование
    voting_id = request.GET.get("vi", 1)
    voting = (votings.objects.filter(id=voting_id))[0]

    # Проверяем, является ли пользователь автором голосования, которое он хочет отредактировать
    if voting.author != request.user:
        return render(request, 'voting_editing.html', {'can_edit': False})

    # Ответы на голосование
    answers = voting_answers.objects.filter(voting_id=voting_id)
    answers_texts = []
    for i in range(len(answers)):
        answers_texts.append(answers[i].text)

    # Отображаем ответы в зависимости от типа голосования
    if voting.type == "discrete":
        ctx = {
            'can_edit': True,
            "voting": voting,
            "answer1": answers_texts[0],
            "answer2": answers_texts[1],
            'user_name': user_data[0],
            'user_mail': user_data[1]
        }
    else:
        answers_str = ','.join(answers_texts)
        ctx = {
            'can_edit': True,
            "voting": voting,
            "answers": answers_str,
            'user_name': user_data[0],
            'user_mail': user_data[1]
        }

    return render(request, 'voting_editing.html', ctx)


'''
Сохранить изменения от редактирования голосования
'''


def manage_voting(request):
    can_edit = True
    success = True

    try:
        voting_id = request.GET.get('vi', 1)
        voting = votings.objects.filter(id=voting_id)[0]
        # Проверяем, является ли пользователь автором голосования, которое он хочет отредактировать
        if voting.author != request.user:
            return render(request, 'manage_editing.html', {'success': success, 'can_vote': False})

        # Изменяем само голосование
        voting.name = request.POST.get('v_name')
        voting.question = request.POST.get('v_question')
        voting.description = request.POST.get('v_description')
        voting.save()

        # Изменяем вопросы голосования
        if voting.type == 'discrete':
            answers = voting_answers.objects.filter(voting_id=voting)
            answer1 = answers[0]
            answer2 = answers[1]
            answ1_new_text = request.POST.get('v_a1')
            answ2_new_text = request.POST.get('v_a2')

            # Если текст вопроса не изменился, не меняем его
            if answer1.text != answ1_new_text:
                answer1.text = answ1_new_text
                answer1.times_selected = 0
                answer1.save()

            if answer2.text != answ2_new_text:
                answer2.text = answ2_new_text
                answer2.times_selected = 0
                answer2.save()

        else:
            answers = voting_answers.objects.filter(voting_id=voting_id)

            new_answers = request.POST.get("v_a")
            new_answers = new_answers.split(',')  # Изначально вопросы разделены запятыми

            # Сначала убираем из бд те варианты, которые больше не являются ответами
            for i in range(len(answers)):
                if answers[i].text not in new_answers:
                    answers[i].delete()
                else:
                    new_answers.remove(answers[i].text)
            # Затем добавляем новые
            for el in new_answers:
                v_answer = voting_answers(voting_id=voting, text=el)
                v_answer.save()
    except:
        success = False

    user_data = get_user_info(request)
    ctx = {
        'can_edit': can_edit,
        'success': success,
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, 'manage_editing.html', ctx)


'''
Страница со всеми голосованиями, которые создал конкретный пользователь
'''


def user_votings(request):
    user_votings = votings.objects.filter(author=request.user)[::-1]
    user_data = get_user_info(request)

    ctx = {
        'votings': user_votings,
        'votings_count': len(user_votings),
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, 'user_votings.html', ctx)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, email=email)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})


def complaint(request):
    user_data = get_user_info(request)
    voting_id = request.GET.get("voting_id", 1)
    voting = votings.objects.filter(id=voting_id)[0]
    ctx = {'vote': voting,
           'user_name': user_data[0],
           'user_mail': user_data[1]}
    return render(request, 'create_complaint.html', ctx)


def complaint_done(request):
    theme = request.GET.get('choose_theme', '')
    description = request.GET.get('complaintDescription', '')
    voting_id = request.GET.get('vi', 1)
    user_id = request.user
    voting = votings.objects.filter(id=voting_id)[0]
    comp = complaints(voting_id=voting, author=user_id, type=voting.type, description=description, date_added= datetime.now().date())

    comp.save()

    return HttpResponse("Спасибо, мы обязательно учтем вашу жалобу!")


def complaint_list(request):

    user_data = get_user_info(request)
    comp_list = complaints.objects.filter(author=request.user)

    ctx = {'list': comp_list,
           'user_name': user_data[0],
           'user_mail': user_data[1],
           }

    return render(request, 'complaint_list.html', ctx)

def complaint_page (request):
    user_data = get_user_info(request)
    complaint_id = request.GET.get("ui", 1)
    complaint = complaints.objects.filter(id=complaint_id)[0]
    ctx = {'comp': complaint,
           'user_name': user_data[0],
           'user_mail': user_data[1]}
    return render(request, 'complaint_page.html', ctx)
    comp = complaints(voting_id=voting, author=user_id, type=voting.type, description=description)
    comp.save()
    return HttpResponse("Спасибо, мы обязательно учтем вашу жалобу!")


'''
Отобоажение голосований, в которых пользователь уже принял участие
'''


def history(request):
    user_data = get_user_info(request)

    # Голосования, в которых пользователь уже принял участие
    records = voted_user_record.objects.filter(voted_person_id=request.user)
    votings = []
    for el in records:
        votings.append(el.voting_id)
    votings = votings[::-1]

    ctx = {
        'type': 'history',
        'public_votings': votings,
        'private_votings': [],
        'user_name': user_data[0],
        'user_mail': user_data[1]
    }
    return render(request, 'votings_shower.html', ctx)

def acc_settings(request):
    user = request.user
    ctx = {
        'user_name': user.username,
        'user_mail': user.email,
        'user_date': user.date_joined,
        'user_f_name': user.first_name,
        'user_l_name': user.last_name,
    }
    return render(request, "acc_settings.html",ctx)

def settings(request):
        user = request.user
        ctx = {
            'user_name': user.username,
            'user_mail': user.email,
            'user_date': user.date_joined,
            'user_f_name': user.first_name,
            'user_l_name': user.last_name,
            'id': user.id,
        }
        return render(request, "settings.html",ctx)


# изменение данных в бд
def editing(request):
        user=request.user
        ctx = {
            'user_name': user.username,
            'user_mail': user.email,
            'user_date': user.date_joined,
            'user_f_name': user.first_name,
            'user_l_name': user.last_name,
            'id': user.id,
        }
        person = User.objects.filter(id=request.user.id)[0]

        if request.method == "POST":
            person.username = request.POST.get("username")
            person.first_name = request.POST.get("firstname")
            person.last_name = request.POST.get("lastname")
            person.email = request.POST.get("mail")
            person.save()
            return render(request, "acc_settings.html", ctx)
        return HttpResponse("error")
