from flask import Blueprint, request, jsonify
from services.ai_service import AIService

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from text and mood"""
    data = request.json
    
    if not data.get('text') or not data.get('mood'):
        return jsonify({'error': 'Text and mood are required'}), 400
    
    analysis = AIService.analyze_emotion(data['text'], data['mood'])
    
    return jsonify(analysis)

