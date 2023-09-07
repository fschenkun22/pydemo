from flask import Flask,url_for,request,redirect

app = Flask(__name__)

@app.route('/',methods=['GET','POST','PUT','DELETE'])
def index():
    print(request.method)
    return 'index'

@app.route('/login')
def login():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return{
        'code':200,
        'msg':'login success'
    }

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('static', filename='style.css'))

# 一直运行
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)