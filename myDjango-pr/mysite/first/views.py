from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


# Create your views here.
def hello_world(request):
    ctx = {'content': 2, 'time': datetime.now()}
    ctx['phrases'] = [
        'Hello - привет',
        'World - мир',
        'Tounge - язык'
    ]
    return render(request, "index.html", ctx)

def test(request):
    return HttpResponse("Toster-tester")


def sum(request):
    a = request.GET.get('a', None)
    b = request.GET.get('b', None)
    ctx = {'a': a, 'b': b, 'sum': '', 'no_data': False, 'error': False}
    result = []
    op_line = "{} {} {} {}".format(datetime.now(), request.META.get('REMOTE_ADDR'), a, b)

    if a is None and b is None:
        ctx['no_data'] = True
    else:
        try:
            result.append({'op': '+', 'res': int(a) + int(b)})
            result.append({'op': '-', 'res': int(a) - int(b)})
            result.append({'op': '*', 'res': int(a) * int(b)})
            result.append({'op': '/', 'res': int(a) / int(b)})
            ctx['sum'] = result
        except Exception as e:
            ctx['error'] = True
            ctx['sum'] = e

    return render(request, 'Calculator.html', ctx)
