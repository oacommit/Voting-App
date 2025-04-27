from flask import Flask, request, redirect, render_template_string
import redis
import os

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_conn = redis.StrictRedis(host=redis_host, port=6379, db=0)

TEMPLATE = '''
<h1>Vote for your favorite!</h1>
<form method="POST">
    <button type="submit" name="vote" value="Cats">Cats</button>
    <button type="submit" name="vote" value="Dogs">Dogs</button>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form['vote']
        redis_conn.rpush('votes', vote)
        return redirect('/')
    return render_template_string(TEMPLATE)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
