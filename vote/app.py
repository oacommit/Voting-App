from flask import Flask, request, redirect, render_template_string
import redis
import os

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_conn = redis.StrictRedis(host=redis_host, port=6379, db=0)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Favorite Pet Vote</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .vote-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .vote-btn {
            padding: 15px 30px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        .vote-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        #cats-btn {
            background-color: #3498db;
            color: white;
        }
        #dogs-btn {
            background-color: #e74c3c;
            color: white;
        }
        .results {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 30px;
        }
        .result-box {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 150px;
        }
        .result-count {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        .total-votes {
            margin-top: 30px;
            font-size: 18px;
            color: #7f8c8d;
        }
        .progress-container {
            height: 20px;
            background: #ecf0f1;
            border-radius: 10px;
            margin: 20px 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            transition: width 0.5s;
        }
        #cats-progress {
            background-color: #3498db;
        }
        #dogs-progress {
            background-color: #e74c3c;
        }
    </style>
</head>
<body>
    <h1>Vote for your favorite pet!</h1>
    
    <form method="POST">
        <div class="vote-container">
            <button class="vote-btn" id="cats-btn" type="submit" name="vote" value="Cats">🐱 Cats</button>
            <button class="vote-btn" id="dogs-btn" type="submit" name="vote" value="Dogs">🐶 Dogs</button>
        </div>
    </form>
    
    <div class="results">
        <div class="result-box">
            <div>Cats</div>
            <div class="result-count">{{ cats_count }}</div>
            <div>{{ cats_percent }}%</div>
        </div>
        <div class="result-box">
            <div>Dogs</div>
            <div class="result-count">{{ dogs_count }}</div>
            <div>{{ dogs_percent }}%</div>
        </div>
    </div>
    
    <div class="progress-container">
        <div id="cats-progress" class="progress-bar" style="width: {{ cats_percent }}%"></div>
        <div id="dogs-progress" class="progress-bar" style="width: {{ dogs_percent }}%"></div>
    </div>
    
    <div class="total-votes">
        Total votes: {{ total_votes }}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form['vote']
        redis_conn.rpush('votes', vote)
        return redirect('/')

    # Fetch votes from Redis
    votes = redis_conn.lrange('votes', 0, -1)  # Get all votes

    # Redis returns bytes, so decode them
    decoded_votes = [v.decode('utf-8') for v in votes]
    cats_count = decoded_votes.count('Cats')
    dogs_count = decoded_votes.count('Dogs')
    total_votes = cats_count + dogs_count
    
    # Calculate percentages (handle division by zero)
    if total_votes > 0:
        cats_percent = round((cats_count / total_votes) * 100)
        dogs_percent = round((dogs_count / total_votes) * 100)
    else:
        cats_percent = 0
        dogs_percent = 0

    return render_template_string(
        TEMPLATE, 
        cats_count=cats_count,
        dogs_count=dogs_count,
        cats_percent=cats_percent,
        dogs_percent=dogs_percent,
        total_votes=total_votes
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
