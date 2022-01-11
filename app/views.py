from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json, random

from services.session import init_session_data, save_session_data
from business.psychic import Psychic


def index(request):
    return HttpResponse(render(request, 'start.html'))


def sessionData(request):
    psychics = init_session_data (request)
    
    headers =  [
        { 'id': "id", 'header': "", 'width': 40 },
        { 'id': "value", 'header': "Загадано", 'width': 120 },
    ]

    for i in range(0, len(psychics)):
        headers.append (
            { 'id': "psych%s" % i,  'header': psychics[i].getName(),
                'width': 160,
            }
        )
        headers.append (
            { 'id': "score%s" % i,  'header': "Точность-%s" % (i+1), 'template': "<b>#score%s# %%</b>" % (i)}
        )

    return HttpResponse(json.dumps({'histHeaders': headers}), content_type = "application/json")

def history(request):
    psychics = init_session_data (request)
    if psychics:
        history = []
        i = 0
        while psychics[0].getGuess(i):
            hg = {'id': i+1}
            for j in range(0, len(psychics)):
                g = psychics[j].getGuess(i)
                hg['value'] = g.getPlayerValue()
                hg["score%s" % j] = "{:.2f}".format(g.getScore())
                hg["psych%s" % j] = g.getValue()
            history.append(hg)
            i += 1
        return HttpResponse(json.dumps(history), content_type = "application/json")
    else:
        return HttpResponse(json.dumps([]), content_type = "application/json")

def guesses(request):
    psychics = init_session_data (request)
    data = {'error': False}
    value = request.GET.get ('value')

    if not value is None and value and len(value) == 2 and int(value) < 100 and int(value) >= 0:
        for i in range(0, len(psychics)):
             psychics[i].setPlayerValue(value)
        save_session_data(request, psychics)
    elif request.GET.get ('cmd') == 'guess':
        for i in range(0, len(psychics)):
            psychics[i].addGuess()
        save_session_data(request, psychics)
    else:
        data['error'] = True
        data['message'] = "Значение должно содержать две цифры 00 - 99!"

    return HttpResponse(json.dumps(data), content_type = "application/json")
    
