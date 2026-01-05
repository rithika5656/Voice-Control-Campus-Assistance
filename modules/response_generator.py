"""
Response Generator Module
Generates appropriate responses based on intent and data
"""

from modules.data_handler import DataHandler


class ResponseGenerator:
    """Generates responses for the campus assistant"""
    
    def __init__(self):
        self.data_handler = DataHandler()
        
        # Greeting responses
        self.greetings = [
            "Hello! I'm your Campus Voice Assistant. How can I help you today?",
            "Hi there! Welcome to Campus Assistant. What would you like to know?",
            "Good day! I'm here to help you with campus information. What do you need?"
        ]
        
        # Exit responses
        self.farewells = [
            "Goodbye! Have a great day!",
            "Thank you for using Campus Assistant. Bye!",
            "Take care! Feel free to ask me anytime."
        ]
        
        # Unknown intent responses
        self.unknown_responses = [
            "I'm sorry, I didn't quite understand that. Could you please rephrase?",
            "I'm not sure what you're asking. Try asking about classes, exams, departments, or facilities.",
            "Could you please be more specific? I can help with timetables, exams, department info, and campus facilities."
        ]
        
        self.response_count = 0
    
    def _get_cyclic_response(self, responses):
        """Get a response cycling through the list"""
        response = responses[self.response_count % len(responses)]
        self.response_count += 1
        return response
    
    def generate_response(self, query_result):
        """
        Generate a response based on the processed query
        
        Args:
            query_result: Dictionary from NLP processor containing intent and entities
            
        Returns:
            Response string
        """
        intent = query_result.get('intent', 'unknown')
        entities = query_result.get('entities', {})
        original_text = query_result.get('original_text', '')
        
        # Handle different intents
        if intent == 'greeting':
            return self._handle_greeting()
        
        elif intent == 'exit':
            return self._handle_exit()
        
        elif intent == 'timetable':
            return self._handle_timetable(entities, original_text)
        
        elif intent == 'exam':
            return self._handle_exam(entities, original_text)
        
        elif intent == 'department':
            return self._handle_department(entities)
        
        elif intent == 'facility':
            return self._handle_facility(entities)
        
        elif intent == 'event':
            return self._handle_event()
        
        elif intent == 'faq':
            return self._handle_faq(original_text)
        
        else:
            return self._handle_unknown(original_text)
    
    def _handle_greeting(self):
        """Handle greeting intent"""
        return self._get_cyclic_response(self.greetings)
    
    def _handle_exit(self):
        """Handle exit intent"""
        return self._get_cyclic_response(self.farewells)
    
    def _handle_timetable(self, entities, original_text):
        """Handle timetable-related queries"""
        day = entities.get('day')
        department = entities.get('department')
        
        # Check for tomorrow in the query
        if 'tomorrow' in original_text.lower():
            from datetime import datetime, timedelta
            tomorrow = datetime.now() + timedelta(days=1)
            day = tomorrow.strftime('%A').lower()
        
        return self.data_handler.get_timetable(day=day, department=department)
    
    def _handle_exam(self, entities, original_text):
        """Handle exam-related queries"""
        department = entities.get('department')
        
        # Check for tomorrow's exams
        if 'tomorrow' in original_text.lower():
            return self.data_handler.get_tomorrow_exams(department=department)
        
        return self.data_handler.get_exam_schedule(department=department)
    
    def _handle_department(self, entities):
        """Handle department-related queries"""
        department = entities.get('department')
        return self.data_handler.get_department_info(department=department)
    
    def _handle_facility(self, entities):
        """Handle facility-related queries"""
        facility = entities.get('facility')
        return self.data_handler.get_facility_info(facility=facility)
    
    def _handle_event(self):
        """Handle event-related queries"""
        return self.data_handler.get_events()
    
    def _handle_faq(self, original_text):
        """Handle FAQ queries"""
        answer = self.data_handler.get_faq_answer(original_text)
        if answer:
            return answer
        return "I couldn't find specific information about that. Please contact the respective office for more details."
    
    def _handle_unknown(self, original_text):
        """Handle unknown queries"""
        # Try to find something in FAQ first
        faq_answer = self.data_handler.get_faq_answer(original_text)
        if faq_answer:
            return faq_answer
        
        return self._get_cyclic_response(self.unknown_responses)
    
    def get_help_message(self):
        """Get help message listing available commands"""
        return """
🎓 Campus Voice Assistant - Help

You can ask me about:

📅 **Timetable/Classes**
   - "What are today's classes?"
   - "CSE schedule for Monday"
   - "Tomorrow's timetable for ECE"

📝 **Exams**
   - "What is the exam schedule?"
   - "Tomorrow's exams"
   - "CSE exam dates"

🏛️ **Departments**
   - "Tell me about CSE department"
   - "Who is the HOD of ECE?"
   - "Department contacts"

🏫 **Facilities**
   - "Library timings"
   - "Canteen location"
   - "Hostel information"
   - "Sports facilities"
   - "Medical center"

🎉 **Events**
   - "Upcoming events"
   - "College fest details"

❓ **General Info**
   - "How to apply for leave?"
   - "Attendance requirements"
   - "Fee structure"

Say 'quit' or 'exit' to stop.
"""


# Test the module
if __name__ == "__main__":
    print("=" * 50)
    print("  Response Generator Module Test")
    print("=" * 50)
    
    from modules.nlp_processor import IntentProcessor
    
    generator = ResponseGenerator()
    processor = IntentProcessor()
    
    # Test queries
    test_queries = [
        "Hello",
        "What are tomorrow's classes for CSE?",
        "Tell me about ECE department",
        "Where is the library?",
        "What is the exam schedule?",
        "Upcoming events",
        "How to apply for leave?",
        "Bye"
    ]
    
    print("\n🧪 Testing Response Generation:")
    print("-" * 50)
    
    for query in test_queries:
        query_result = processor.process_query(query)
        response = generator.generate_response(query_result)
        print(f"\n📝 Query: \"{query}\"")
        print(f"💬 Response:\n{response[:200]}..." if len(response) > 200 else f"💬 Response:\n{response}")
    
    print("\n" + "=" * 50)
    print("✅ Response Generator module test complete!")
