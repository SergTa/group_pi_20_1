import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'models'))

from predict_model_wrapper import predict_release_risk

# Подключение к базе данных SQLite
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Проверка наличия таблицы 'releases'
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='releases'")
result = cursor.fetchone()

if result is None:
    # Если таблицы нет, создаем её
    cursor.execute('''
        CREATE TABLE releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            importance_of_business_processes INT,
            technical_complexity INT,
            team_experience INT,
            level_of_integration_with_other_systems INT,
            reaction_to_mistakes INT,
            criticality_of_streams INT
        )
    ''')
    print("Таблица 'releases' создана.")
else:
    print("Таблица 'releases' уже существует.")

# Закрываем соединение с базой данных
conn.commit()
conn.close()

app = Flask(__name__)
# Включаем поддержку CORS для всех маршрутов
CORS(app)

# Подключение к базе данных
conn = sqlite3.connect('example.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/get-releases')
def get_releases():
    cursor.execute("SELECT id, importance_of_business_processes, technical_complexity, team_experience, level_of_integration_with_other_systems, reaction_to_mistakes, criticality_of_streams FROM releases")
    rows = cursor.fetchall()
    releases = [
        {'id': row[0], 'importance_of_business_processes': row[1], 'technical_complexity': row[2], 'team_experience': row[3], 'level_of_integration_with_other_systems': row[4], 'reaction_to_mistakes': row[5], 'criticality_of_streams': row[6]}
        for row in rows
    ]
    return jsonify(releases)

@app.route('/add-release', methods=['POST'])
def add_release():
    data = request.get_json()
    cursor.execute(
        """INSERT INTO releases (importance_of_business_processes, technical_complexity, team_experience, level_of_integration_with_other_systems, reaction_to_mistakes, criticality_of_streams)
           VALUES (:importance_of_business_processes, :technical_complexity, :team_experience, :level_of_integration_with_other_systems, :reaction_to_mistakes, :criticality_of_streams)""",
        {
            'importance_of_business_processes': data['importance_of_business_processes'],
            'technical_complexity': data['technical_complexity'],
            'team_experience': data['team_experience'],
            'level_of_integration_with_other_systems': data['level_of_integration_with_other_systems'],
            'reaction_to_mistakes': data['reaction_to_mistakes'],
            'criticality_of_streams': data['criticality_of_streams']
        }
    )
    conn.commit()
    return jsonify({'message': 'Release added successfully'})

@app.route('/update-release/<int:id>', methods=['PUT'])
def update_release(id):
    data = request.get_json()
    cursor.execute(
        """UPDATE releases SET
           importance_of_business_processes = :importance_of_business_processes,
           technical_complexity = :technical_complexity,
           team_experience = :team_experience,
           level_of_integration_with_other_systems = :level_of_integration_with_other_systems,
           reaction_to_mistakes = :reaction_to_mistakes,
           criticality_of_streams = :criticality_of_streams
           WHERE id = :id""",
        {
            'importance_of_business_processes': data['importance_of_business_processes'],
            'technical_complexity': data['technical_complexity'],
            'team_experience': data['team_experience'],
            'level_of_integration_with_other_systems': data['level_of_integration_with_other_systems'],
            'reaction_to_mistakes': data['reaction_to_mistakes'],
            'criticality_of_streams': data['criticality_of_streams'],
            'id': id
        }
    )
    conn.commit()
    return jsonify({'message': 'Release updated successfully'})

@app.route('/delete-release/<int:id>', methods=['DELETE'])
def delete_release(id):
    cursor.execute("DELETE FROM releases WHERE id = ?", (id,))
    conn.commit()
    return jsonify({'message': 'Release deleted successfully'})

@app.route('/predict-risk', methods=['POST'])
def predict_risk():
    data = request.get_json()
    release_properties = [
        [
            data['importance_of_business_processes'], #'Importance of Business Processes'
            data['technical_complexity'], #'Technical Complexity'
            data['team_experience'], #'Team Experience'
            data['level_of_integration_with_other_systems'], #'Level of Integration with Other Systems'
            data['reaction_to_mistakes'], #'Reaction to Mistakes'
            data['criticality_of_streams'] #'Criticality of Streams'
        ]
    ]
    
    result = predict_release_risk(release_properties)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
