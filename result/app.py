from flask import Flask, render_template_string
import psycopg2
import os

app = Flask(__name__)
db_host = os.getenv('DB_HOST', 'db')

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pet Preference Results</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --cat-color: #3498db;
            --dog-color: #e74c3c;
            --bg-color: #f8f9fa;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        h1 {
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 2rem;
        }
        
        .results-container {
            display: flex;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .result-card {
            flex: 1;
            background: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: var(--card-shadow);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
        }
        
        .cat-card {
            border-top: 5px solid var(--cat-color);
        }
        
        .dog-card {
            border-top: 5px solid var(--dog-color);
        }
        
        .pet-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .pet-name {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .vote-count {
            font-size: 3rem;
            font-weight: 600;
            margin: 1rem 0;
        }
        
        .cat-count {
            color: var(--cat-color);
        }
        
        .dog-count {
            color: var(--dog-color);
        }
        
        .progress-container {
            width: 100%;
            background: #ecf0f1;
            border-radius: 10px;
            height: 30px;
            margin: 2rem 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            display: flex;
        }
        
        .cat-progress {
            background-color: var(--cat-color);
        }
        
        .dog-progress {
            background-color: var(--dog-color);
        }
        
        .stats {
            background: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: var(--card-shadow);
            margin-top: 2rem;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }
        
        .stat-label {
            font-weight: 600;
        }
        
        .total-votes {
            font-size: 1.5rem;
            text-align: center;
            margin-top: 1rem;
            font-weight: 600;
            color: #2c3e50;
        }
        
        @media (max-width: 768px) {
            .results-container {
                flex-direction: column;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Pet Preference Results</h1>
            <div class="subtitle">See what people love more - Cats or Dogs!</div>
        </header>
        
        <div class="results-container">
            <div class="result-card cat-card">
                <div class="pet-icon">🐱</div>
                <div class="pet-name">Cats</div>
                <div class="vote-count cat-count">{{ cats }}</div>
                <div>votes</div>
            </div>
            
            <div class="result-card dog-card">
                <div class="pet-icon">🐶</div>
                <div class="pet-name">Dogs</div>
                <div class="vote-count dog-count">{{ dogs }}</div>
                <div>votes</div>
            </div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar">
                <div class="cat-progress" style="width: {{ cat_percent }}%"></div>
                <div class="dog-progress" style="width: {{ dog_percent }}%"></div>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-row">
                <span class="stat-label">Total Votes:</span>
                <span>{{ total_votes }}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Cats Percentage:</span>
                <span>{{ cat_percent }}%</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Dogs Percentage:</span>
                <span>{{ dog_percent }}%</span>
            </div>
        </div>
        
        <div class="total-votes">
            Thanks for participating in our survey!
        </div>
    </div>
</body>
</html>
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
    total_votes = cats + dogs
    
    # Calculate percentages
    cat_percent = round((cats / total_votes) * 100, 1) if total_votes > 0 else 0
    dog_percent = round((dogs / total_votes) * 100, 1) if total_votes > 0 else 0
    
    return render_template_string(
        TEMPLATE, 
        cats=cats, 
        dogs=dogs,
        total_votes=total_votes,
        cat_percent=cat_percent,
        dog_percent=dog_percent
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
