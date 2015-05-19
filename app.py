# -*- coding: utf-8 -*- 

from flask import Flask, request, Response, redirect
from mixpanel import Mixpanel
from stackexchange import Site, StackOverflow, Sort, DESC

import os

try:
    import config
    se_key = config.stackexchange['api_key']
    mixpanel_token = config.mixpanel['token']
except:
    se_key = os.environ.get('SE_KEY')
    mixpanel_token = os.environ.get('MIXPANEL_TOKEN')


if not se_key or not mixpanel_token:
    import sys
    print 'No config.py file found. Exiting...'
    sys.exit(0)


MAX_QUESTIONS = 5


app = Flask(__name__)
so = Site(StackOverflow, se_key)
mp = Mixpanel(mixpanel_token)


def get_response_string(q):
    q_data = q.json
    check = ' :white_check_mark:' if q.json['is_answered'] else ''
    return "|%d|%s <%s|%s> (%d answers)" % (q_data['score'], check, q.url,
                                            q.title, q_data['answer_count'])


@app.route('/support')
def support():
    mp.track(-1, 'Support Page')
    return redirect('https://donorbox.org/karangoel-karan-s-college-fund')


@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow python list comprehension
    '''
    text = request.values.get('text')

    try:
        qs = so.search(intitle=text, sort=Sort.Votes, order=DESC)
    except UnicodeEncodeError:
        return Response(('Only English language is supported. '
                         '%s is not valid input.' % text),
                         content_type='text/plain; charset=utf-8')

    mp.track(request.values.get('team_domain'), 'New Query', {
            'channel_name': request.values.get('channel_name'),
            'user_name': request.values.get('user_name'),
            'text': request.values.get('text'),
            'question_length': len(qs)
        })

    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    for q in qs[:MAX_QUESTIONS]:
        resp_qs.append(get_response_string(q))

    if len(resp_qs) is 1:
        resp_qs.append(('No questions found. Please try a broader search or '
                        'search directly on '
                        '<https://stackoverflow.com|StackOverflow>.'))

    resp_qs.append(('\n<https://slack-overflow.herokuapp.com/support|'
                    ':innocent: Contribute to Karan\'s College '
                    'Fund Piggy Bank :innocent:>'))

    return Response('\n'.join(resp_qs),
                    content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    mp.track(-1, 'Homepage')
    return redirect('https://github.com/karan/slack-overflow')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=port, debug=True)
