
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
<p>Cats: {{ cats_count }}</p>
<p>Dogs: {{ dogs_count }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form['vote']
        redis_conn.rpush('votes', vote)
        return redirect('/')

    # Fetch votes from Redis
    votes = redis_conn.lrange('votes', 0, -1)  # Get all votes

    # lrange returns a list of bytes, so decode first
    decoded_votes = [v.decode('utf-8') for v in votes]
    cats_count = decoded_votes.count('Cats')
    dogs_count = decoded_votes.count('Dogs')

    return render_template_string(TEMPLATE, cats_count=cats_count, dogs_count=dogs_count)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
