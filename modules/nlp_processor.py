"""
Natural Language Processing Module
Handles intent identification and keyword extraction
"""

import re
from datetime import datetime, timedelta


class IntentProcessor:
    """Handles NLP tasks including intent identification and entity extraction"""
    
    def __init__(self):
        # Define intents with their associated keywords
        self.intents = {
            'timetable': {
                'keywords': ['timetable', 'class', 'schedule', 'lecture', 'period', 
                            'timing', 'classes', 'today', 'tomorrow', 'when'],
                'patterns': [
                    r'what.*class',
                    r'when.*class',
                    r'today.*schedule',
                    r'tomorrow.*schedule',
                    r'class.*timing',
                    r'schedule.*for'
                ]
            },
            'exam': {
                'keywords': ['exam', 'examination', 'test', 'internal', 'semester',
                            'exam schedule', 'exam date', 'exam time', 'exams'],
                'patterns': [
                    r'when.*exam',
                    r'exam.*schedule',
                    r'exam.*date',
                    r'next.*exam',
                    r'upcoming.*exam'
                ]
            },
            'department': {
                'keywords': ['department', 'hod', 'head', 'faculty', 'professor',
                            'teacher', 'staff', 'office', 'contact', 'phone'],
                'patterns': [
                    r'who.*hod',
                    r'department.*info',
                    r'contact.*department',
                    r'about.*department'
                ]
            },
            'facility': {
                'keywords': ['library', 'canteen', 'hostel', 'sports', 'gym',
                            'medical', 'hospital', 'bus', 'transport', 'wifi'],
                'patterns': [
                    r'where.*library',
                    r'library.*timing',
                    r'canteen.*open',
                    r'hostel.*timing',
                    r'bus.*route'
                ]
            },
            'event': {
                'keywords': ['event', 'fest', 'cultural', 'technical', 'seminar',
                            'workshop', 'placement', 'drive', 'program'],
                'patterns': [
                    r'upcoming.*event',
                    r'next.*fest',
                    r'when.*placement'
                ]
            },
            'faq': {
                'keywords': ['leave', 'fee', 'certificate', 'attendance', 'scholarship',
                            'apply', 'bonafide', 'rules', 'how to', 'procedure'],
                'patterns': [
                    r'how.*apply',
                    r'what.*fee',
                    r'attendance.*requirement'
                ]
            },
            'greeting': {
                'keywords': ['hello', 'hi', 'hey', 'good morning', 'good afternoon',
                            'good evening', 'help', 'assist'],
                'patterns': [
                    r'^hello',
                    r'^hi\b',
                    r'^hey'
                ]
            },
            'exit': {
                'keywords': ['bye', 'goodbye', 'exit', 'quit', 'stop', 'thank you',
                            'thanks', 'done'],
                'patterns': [
                    r'bye',
                    r'exit',
                    r'quit'
                ]
            }
        }
        
        # Department name mappings
        self.department_mappings = {
            'cse': 'CSE', 'computer': 'CSE', 'computer science': 'CSE', 'cs': 'CSE',
            'ece': 'ECE', 'electronics': 'ECE', 'communication': 'ECE', 'ec': 'ECE',
            'mech': 'MECH', 'mechanical': 'MECH', 'me': 'MECH',
            'civil': 'CIVIL', 'ce': 'CIVIL',
            'eee': 'EEE', 'electrical': 'EEE', 'ee': 'EEE'
        }
        
        # Day mappings
        self.day_mappings = {
            'today': self._get_today(),
            'tomorrow': self._get_tomorrow(),
            'monday': 'monday', 'mon': 'monday',
            'tuesday': 'tuesday', 'tue': 'tuesday',
            'wednesday': 'wednesday', 'wed': 'wednesday',
            'thursday': 'thursday', 'thu': 'thursday',
            'friday': 'friday', 'fri': 'friday',
            'saturday': 'saturday', 'sat': 'saturday',
            'sunday': 'sunday', 'sun': 'sunday'
        }
    
    def _get_today(self):
        """Get today's day name"""
        return datetime.now().strftime('%A').lower()
    
    def _get_tomorrow(self):
        """Get tomorrow's day name"""
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.strftime('%A').lower()
    
    def preprocess_text(self, text):
        """
        Preprocess the input text
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned and lowercased text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep apostrophes
        text = re.sub(r"[^\w\s']", '', text)
        
        return text
    
    def identify_intent(self, text):
        """
        Identify the user's intent from the text
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        text = self.preprocess_text(text)
        
        if not text:
            return ('unknown', 0.0)
        
        intent_scores = {}
        
        for intent_name, intent_data in self.intents.items():
            score = 0
            
            # Check keywords
            for keyword in intent_data['keywords']:
                if keyword in text:
                    score += 1
            
            # Check patterns
            for pattern in intent_data['patterns']:
                if re.search(pattern, text):
                    score += 2  # Patterns are weighted higher
            
            intent_scores[intent_name] = score
        
        # Get the intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        best_score = intent_scores[best_intent]
        
        if best_score > 0:
            # Normalize score to confidence (0-1)
            max_possible = len(self.intents[best_intent]['keywords']) + \
                          len(self.intents[best_intent]['patterns']) * 2
            confidence = min(best_score / max_possible, 1.0)
            return (best_intent, confidence)
        
        return ('unknown', 0.0)
    
    def extract_entities(self, text):
        """
        Extract relevant entities from the text
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary of extracted entities
        """
        text = self.preprocess_text(text)
        entities = {
            'department': None,
            'day': None,
            'subject': None,
            'facility': None
        }
        
        # Extract department
        for key, value in self.department_mappings.items():
            if key in text:
                entities['department'] = value
                break
        
        # Extract day
        for key, value in self.day_mappings.items():
            if key in text:
                entities['day'] = value
                break
        
        # Extract facility
        facilities = ['library', 'canteen', 'hostel', 'sports', 'gym', 
                     'medical', 'hospital', 'bus', 'transport']
        for facility in facilities:
            if facility in text:
                entities['facility'] = facility
                break
        
        return entities
    
    def process_query(self, text):
        """
        Main method to process a user query
        
        Args:
            text: Raw input text
            
        Returns:
            Dictionary with intent, confidence, and entities
        """
        intent, confidence = self.identify_intent(text)
        entities = self.extract_entities(text)
        
        return {
            'original_text': text,
            'processed_text': self.preprocess_text(text),
            'intent': intent,
            'confidence': confidence,
            'entities': entities
        }


# Test the module
if __name__ == "__main__":
    print("=" * 50)
    print("  NLP Intent Processor Module Test")
    print("=" * 50)
    
    processor = IntentProcessor()
    
    # Test queries
    test_queries = [
        "What is tomorrow's exam schedule?",
        "Tell me about CSE department",
        "What are today's classes for ECE?",
        "Where is the library?",
        "How to apply for leave?",
        "Hello, can you help me?",
        "What are the upcoming events?",
        "Thank you, bye!"
    ]
    
    print("\n🧪 Testing Intent Recognition:")
    print("-" * 50)
    
    for query in test_queries:
        result = processor.process_query(query)
        print(f"\n📝 Query: \"{query}\"")
        print(f"   Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        print(f"   Entities: {result['entities']}")
    
    print("\n" + "=" * 50)
    print("✅ NLP Module test complete!")
