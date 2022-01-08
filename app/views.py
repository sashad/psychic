from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json, random

startPage = """
<!DOCTYPE html>
<html>
  <head>
    <title>Тестирование экстрасенсов</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="https://cdn.webix.com/edge/webix.css" type="text/css" />
    <script src="https://cdn.webix.com/edge/webix.js" type="text/javascript"></script>
</head>
  <body>
    <script src="static/layouts.js" type="text/javascript">
    </script>
  </body>
</html>
"""

def index(request):
    return HttpResponse(startPage)


def sessionData(request):
    cols = request.session.get('psychCount')
    if not cols:
        cols = random.randrange(3,6)
        request.session['psychCount'] = cols
        request.session['history'] = []

    headers =  [
        { 'id': "id", 'header': "", 'width': 40 },
        { 'id': "value", 'header': "Загадано", 'width': 120 },
    ]

    for i in range (1, cols):
        headers.append (
            { 'id': "psych%s" % i,  'header': "Экстрасенс-%s" % i,
                'width': 160,
            }
        )
        headers.append (
            { 'id': "score%s" % i,  'header': "Рэйтинг-%s" % i, 'template': "<b>#score%s#</b>" % (i)}
        )

    return HttpResponse(json.dumps({'histHeaders': headers}), content_type = "application/json")

def history(request):
    return HttpResponse(json.dumps(request.session.get('history', [])), content_type = "application/json")

def guesses(request):
    history = request.session.get('history', [])
    data = {'error': False}
    value = request.GET.get ('value')

    if not value is None and value and len(value) == 2 and int(value) < 100:
        history[0]['value'] = value
        for i in range(1, request.session.get('psychCount')):
            if int(value) == int(history[0]["psych%s" % i]):
                history[0]["score%s" % i] = history[0]["score%s" % i] + 1
            else:
                history[0]["score%s" % i] = history[0]["score%s" % i] - 1
        request.session['history'] = history
    elif request.GET.get ('cmd') == 'guess':
        g = {'id': len(history) + 1, 'value':'Предсказано:'}
        for i in range(1, request.session.get('psychCount')):
            g["psych%s" % i] = "{:02d}".format(random.randrange(0, 99))
            if len(history):
                g["score%s" % i] = history[0]["score%s" % i]
            else:
                g["score%s" % i] = 0
        data['guess'] = g
        history.insert(0, g)
        request.session['history'] = history
    else:
        data['error'] = True

    return HttpResponse(json.dumps(data), content_type = "application/json")
    
