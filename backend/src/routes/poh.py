"""
POH API Routes
Handles POH document information and Q&A functionality
"""

from flask import Blueprint, request, jsonify
from src.services.poh_qa import poh_qa_service

poh_bp = Blueprint('poh', __name__)

@poh_bp.route('/info', methods=['GET'])
def get_document_info():
    """Get current document information"""
    try:
        info = poh_qa_service.get_document_info()
        return jsonify({
            "success": True,
            "document": info
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@poh_bp.route('/ask', methods=['POST'])
def ask_question():
    """Ask a question about the POH"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "Question is required"
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty"
            }), 400
        
        # Generate answer
        result = poh_qa_service.generate_answer(question)
        
        return jsonify({
            "success": True,
            "question": question,
            "answer": result["answer"],
            "source": result["source"],
            "confidence": result["confidence"]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@poh_bp.route('/samples', methods=['GET'])
def get_sample_questions():
    """Get sample questions for testing"""
    try:
        samples = poh_qa_service.get_sample_questions()
        return jsonify({
            "success": True,
            "questions": samples
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@poh_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for POH service"""
    try:
        info = poh_qa_service.get_document_info()
        return jsonify({
            "success": True,
            "status": "healthy",
            "document_loaded": info["pages"] > 0
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "status": "error",
            "error": str(e)
        }), 500

