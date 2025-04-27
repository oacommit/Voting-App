import redis
import psycopg2
import os
import time

redis_host = os.getenv('REDIS_HOST', 'redis')
db_host = os.getenv('DB_HOST', 'db')

def main():
    r = redis.StrictRedis(host=redis_host, port=6379, db=0)
    conn = psycopg2.connect(host=db_host, dbname='postgres', user='postgres', password='postgres')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        vote TEXT NOT NULL
    )
    ''')
    conn.commit()

    while True:
        vote = r.lpop('votes')
        if vote:
            cur.execute('INSERT INTO votes (vote) VALUES (%s)', (vote.decode('utf-8'),))
            conn.commit()
        time.sleep(1)

if __name__ == '__main__':
    main()
