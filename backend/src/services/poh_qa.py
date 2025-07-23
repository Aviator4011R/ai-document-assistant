"""
POH Q&A Service
Provides document-based question answering using the processed POH content
"""

import json
import os
from typing import List, Dict, Optional
import openai
from openai import OpenAI

class POHQAService:
    def __init__(self):
        self.data_dir = "/home/ubuntu/ai-backend/data"
        self.content = None
        self.chunks = None
        self.client = None
        self.load_content()
        self.setup_openai()
    
    def setup_openai(self):
        """Initialize OpenAI client"""
        try:
            self.client = OpenAI()
            print("OpenAI client initialized successfully")
        except Exception as e:
            print(f"Warning: OpenAI initialization failed: {e}")
            self.client = None
    
    def load_content(self):
        """Load processed POH content"""
        try:
            # Load full content
            content_path = os.path.join(self.data_dir, "poh_content.json")
            if os.path.exists(content_path):
                with open(content_path, 'r') as f:
                    self.content = json.load(f)
                print(f"Loaded POH content: {self.content['title']}")
            
            # Load chunks
            chunks_path = os.path.join(self.data_dir, "poh_chunks.json")
            if os.path.exists(chunks_path):
                with open(chunks_path, 'r') as f:
                    self.chunks = json.load(f)
                print(f"Loaded {len(self.chunks)} content chunks")
                
        except Exception as e:
            print(f"Error loading POH content: {e}")
    
    def get_document_info(self) -> Dict:
        """Get document information"""
        if self.content:
            return {
                "title": self.content["title"],
                "subtitle": self.content["subtitle"],
                "pages": len(self.content["pages"]),
                "sections": len(self.content["sections"])
            }
        return {"title": "No document loaded", "subtitle": "", "pages": 0, "sections": 0}
    
    def search_relevant_chunks(self, query: str, max_chunks: int = 5) -> List[Dict]:
        """Simple keyword-based search for relevant chunks"""
        if not self.chunks:
            return []
        
        query_lower = query.lower()
        scored_chunks = []
        
        for chunk in self.chunks:
            chunk_text = chunk["text"].lower()
            score = 0
            
            # Simple keyword matching
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 2:  # Skip very short words
                    score += chunk_text.count(word)
            
            if score > 0:
                scored_chunks.append((score, chunk))
        
        # Sort by score and return top chunks
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:max_chunks]]
    
    def generate_answer(self, question: str) -> Dict:
        """Generate answer based on POH content"""
        if not self.content:
            return {
                "answer": "No document is currently loaded. Please upload a document first.",
                "source": "system",
                "confidence": 0
            }
        
        # Search for relevant content
        relevant_chunks = self.search_relevant_chunks(question)
        
        if not relevant_chunks:
            return {
                "answer": "I couldn't find information about that topic in the 1967 Piper Cherokee PA-32-300 POH. Please try rephrasing your question or ask about aircraft systems, procedures, or specifications covered in this manual.",
                "source": "document_search",
                "confidence": 0
            }
        
        # Combine relevant chunks
        context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])
        
        # Generate answer using OpenAI if available
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": f"""You are an AI assistant specialized in the 1967 Piper Cherokee PA-32-300 POH (Pilot's Operating Handbook). 

IMPORTANT RULES:
1. Only answer questions based on the provided POH content
2. If information is not in the POH, clearly state that
3. Be precise and reference specific procedures or specifications
4. Use aviation terminology appropriately
5. Keep answers concise but complete

POH Content:
{context}"""
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                
                answer = response.choices[0].message.content.strip()
                return {
                    "answer": answer,
                    "source": "1967 Piper Cherokee PA-32-300 POH",
                    "confidence": 0.8
                }
                
            except Exception as e:
                print(f"OpenAI API error: {e}")
        
        # Fallback: Return relevant chunks directly
        answer = f"Based on the 1967 Piper Cherokee PA-32-300 POH:\n\n{context[:800]}..."
        return {
            "answer": answer,
            "source": "1967 Piper Cherokee PA-32-300 POH",
            "confidence": 0.6
        }
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions for testing"""
        return [
            "What is the maximum gross weight?",
            "What are the engine specifications?",
            "What is the fuel capacity?",
            "What are the takeoff procedures?",
            "What are the landing procedures?",
            "What are the emergency procedures?",
            "What is the cruise speed?",
            "What are the electrical system specifications?"
        ]

# Global instance
poh_qa_service = POHQAService()

