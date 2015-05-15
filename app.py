from flask import Flask, request, Response
app = Flask(__name__)


@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow hello world
    '''
    user_id = request.values.get('user_id')
    user_name = request.values.get('user_name')
    channel_name = request.values.get('channel_name')
    text = request.values.get('text')

    return Response(text, content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
