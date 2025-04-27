from flask import Flask, render_template_string
import psycopg2
import os

app = Flask(__name__)
db_host = os.getenv('DB_HOST', 'db')

TEMPLATE = '''
<h1>Results:</h1>
<h2>Cats: {{ cats }}</h2>
<h2>Dogs: {{ dogs }}</h2>
'''

def get_votes():
    conn = psycopg2.connect(host=db_host, dbname='postgres', user='postgres', password='postgres')
    cur = conn.cursor()
    cur.execute('SELECT vote, COUNT(*) FROM votes GROUP BY vote')
    votes = dict(cur.fetchall())
    cur.close()
    conn.close()
    return votes

@app.route('/')
def results():
    votes = get_votes()
    cats = votes.get('Cats', 0)
    dogs = votes.get('Dogs', 0)
    return render_template_string(TEMPLATE, cats=cats, dogs=dogs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
