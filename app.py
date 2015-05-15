# -*- coding: utf-8 -*- 

from flask import Flask, request, Response
from stackexchange import Site, StackOverflow, Sort, DESC

try:
    import config
except:
    import sys
    print 'No config.py file found. Exiting...'
    sys.exit(0)


MAX_QUESTIONS = 5


app = Flask(__name__)
so = Site(StackOverflow, config.stackexchange['api_key'])


def get_response_string(q):
    q_data = q.json
    check = ' :white_check_mark:' if q.json['is_answered'] else ''
    return "|%d|%s <%s|%s> (%d answers)" % (q_data['score'], check, q.url,
                                            q.title, q_data['answer_count'])


@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow python list comprehension
    '''
    text = request.values.get('text')

    qs = so.search(intitle=text, sort=Sort.Votes, order=DESC)

    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    for q in qs[:MAX_QUESTIONS]:
        resp_qs.append(get_response_string(q))

    return Response('\n'.join(resp_qs), content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
