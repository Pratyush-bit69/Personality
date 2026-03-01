from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load personality questions at startup
PERSONALITY_QUESTIONS = [
    {"id": 1, "text": "I am the life of the party", "category": "Extraversion"},
    {"id": 2, "text": "I feel comfortable around people", "category": "Extraversion"},
    {"id": 3, "text": "I believe that winning is everything", "category": "Agreeableness"},
    {"id": 4, "text": "I make friends easily", "category": "Extraversion"},
    {"id": 5, "text": "I take time out for others", "category": "Agreeableness"},
    {"id": 6, "text": "I am interested in people", "category": "Extraversion"},
    {"id": 7, "text": "I insult people", "category": "Agreeableness"},
    {"id": 8, "text": "I am often quiet around strangers", "category": "Extraversion"},
    {"id": 9, "text": "I like to make up my own mind", "category": "Openness"},
    {"id": 10, "text": "I am easily disturbed", "category": "Neuroticism"},
]

PERSONALITY_TYPES = {
    'ISTJ': {'name': 'The Logistician', 'color': '#4A90E2', 'strengths': ['Responsible', 'Dependable', 'Loyal']},
    'ISFJ': {'name': 'The Defender', 'color': '#7B68EE', 'strengths': ['Supportive', 'Loyal', 'Hardworking']},
    'INFJ': {'name': 'The Advocate', 'color': '#50C878', 'strengths': ['Insightful', 'Inspiring', 'Principled']},
    'INTJ': {'name': 'The Architect', 'color': '#FF6B6B', 'strengths': ['Strategic', 'Independent', 'Principled']},
    'ISTP': {'name': 'The Virtuoso', 'color': '#FFB84D', 'strengths': ['Strategic', 'Pragmatic', 'Creative']},
    'ISFP': {'name': 'The Adventurer', 'color': '#A78BFA', 'strengths': ['Sensitive', 'Aesthetic', 'Flexible']},
    'INFP': {'name': 'The Mediator', 'color': '#06B6D4', 'strengths': ['Idealistic', 'Loyal', 'Values-driven']},
    'INTP': {'name': 'The Logician', 'color': '#EC4899', 'strengths': ['Analytical', 'Original', 'Independent']},
    'ESTP': {'name': 'The Entrepreneur', 'color': '#F59E0B', 'strengths': ['Bold', 'Pragmatic', 'Natural leader']},
    'ESFP': {'name': 'The Entertainer', 'color': '#8B5CF6', 'strengths': ['Outgoing', 'Spontaneous', 'Friendly']},
    'ENFP': {'name': 'The Campaigner', 'color': '#10B981', 'strengths': ['Enthusiastic', 'Creative', 'Social']},
    'ENTP': {'name': 'The Debater', 'color': '#EF4444', 'strengths': ['Quick-witted', 'Knowledgeable', 'Good listener']},
    'ESTJ': {'name': 'The Executive', 'color': '#3B82F6', 'strengths': ['Efficient', 'Responsible', 'Strong leader']},
    'ESFJ': {'name': 'The Consul', 'color': '#F87171', 'strengths': ['Supportive', 'Responsible', 'Natural leader']},
    'ENFJ': {'name': 'The Protagonist', 'color': '#34D399', 'strengths': ['Inspiring', 'Responsible', 'Caring']},
    'ENTJ': {'name': 'The Commander', 'color': '#FBBF24', 'strengths': ['Strategic', 'Focused', 'Leader']},
}

@app.route('/')
def index():
    return render_template('index.html', questions=PERSONALITY_QUESTIONS)

@app.route('/api/questions')
def get_questions():
    return jsonify({'questions': PERSONALITY_QUESTIONS})

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    responses = data.get('responses', [])
    
    if len(responses) == 0:
        return jsonify({'error': 'No responses provided'}), 400
    
    avg_response = sum(responses) / len(responses)
    
    mbti_types_list = list(PERSONALITY_TYPES.keys())
    type_index = min(int(avg_response * 1.6), len(mbti_types_list) - 1)
    mbti_type = mbti_types_list[type_index]
    
    personality_info = PERSONALITY_TYPES.get(mbti_type, {})
    
    return jsonify({
        'mbti_type': mbti_type,
        'personality': {
            'type': mbti_type,
            'name': personality_info.get('name', 'Unknown'),
            'color': personality_info.get('color', '#000000'),
            'strengths': personality_info.get('strengths', []),
        }
    })

@app.route('/api/personality/<mbti_type>')
def get_personality_details(mbti_type):
    if mbti_type not in PERSONALITY_TYPES:
        return jsonify({'error': 'Unknown personality type'}), 404
    
    personality = PERSONALITY_TYPES[mbti_type]
    return jsonify({
        'type': mbti_type,
        'name': personality['name'],
        'color': personality['color'],
        'strengths': personality.get('strengths', []),
        'description': f"MBTI Type {mbti_type}: {personality['name']}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)