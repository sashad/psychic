import pickle, random
from business.psychic import Psychic

def init_session_data(request):
    data = request.session.get('data')
    if not data:
        psychics = []
        for i in range(0, random.randrange(3,6)):
            p = Psychic("Экстрасенс-%s" % (i+1))
            psychics.append(p)
            s = pickle.dumps(psychics, 0)
        request.session['data'] = s.decode('utf-8')
    else:
        psychics = pickle.loads(data.encode('utf-8'))
    return psychics


def save_session_data(request, psychics):
    s = pickle.dumps(psychics, 0)
    request.session['data'] = s.decode('utf-8')
