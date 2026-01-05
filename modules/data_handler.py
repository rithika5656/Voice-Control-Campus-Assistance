"""
Data Handler Module
Handles loading and querying data from JSON files
"""

import json
import os
from datetime import datetime, timedelta


class DataHandler:
    """Handles data operations for the campus assistant"""
    
    def __init__(self, data_dir="data"):
        """
        Initialize the data handler
        
        Args:
            data_dir: Directory containing JSON data files
        """
        # Get the absolute path to the data directory
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, data_dir)
        
        # Load all data files
        self.timetable = self._load_json("timetable.json")
        self.exams = self._load_json("exams.json")
        self.departments = self._load_json("departments.json")
        self.campus_info = self._load_json("campus_info.json")
        self.faqs = self._load_json("faqs.json")
        
        print("📚 Data files loaded successfully!")
    
    def _load_json(self, filename):
        """
        Load a JSON file
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Dictionary with JSON data or empty dict if failed
        """
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Warning: {filename} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing {filename}: {e}")
            return {}
    
    def get_timetable(self, day=None, department=None):
        """
        Get timetable information
        
        Args:
            day: Day of the week (e.g., 'monday')
            department: Department code (e.g., 'CSE')
            
        Returns:
            Formatted timetable string
        """
        if not self.timetable:
            return "Sorry, timetable data is not available."
        
        # Default to today if no day specified
        if not day:
            day = datetime.now().strftime('%A').lower()
        
        day = day.lower()
        
        if day not in self.timetable:
            if day == 'sunday':
                return "Sunday is a holiday. No classes scheduled."
            return f"No timetable available for {day.capitalize()}."
        
        day_schedule = self.timetable[day]
        
        # If department specified, return only that department's schedule
        if department:
            department = department.upper()
            if department in day_schedule:
                schedule = day_schedule[department]
                response = f"📅 {department} Schedule for {day.capitalize()}:\n\n"
                for class_info in schedule:
                    response += f"⏰ {class_info['time']}\n"
                    response += f"   📖 {class_info['subject']}\n"
                    response += f"   🚪 Room: {class_info['room']}\n"
                    response += f"   👨‍🏫 Faculty: {class_info['faculty']}\n\n"
                return response
            else:
                return f"No schedule found for {department} department on {day.capitalize()}."
        
        # Return all departments' schedules
        response = f"📅 Timetable for {day.capitalize()}:\n\n"
        for dept, schedule in day_schedule.items():
            response += f"📌 {dept} Department:\n"
            for class_info in schedule:
                response += f"  ⏰ {class_info['time']} - {class_info['subject']} ({class_info['room']})\n"
            response += "\n"
        
        return response
    
    def get_exam_schedule(self, department=None):
        """
        Get exam schedule information
        
        Args:
            department: Department code (e.g., 'CSE')
            
        Returns:
            Formatted exam schedule string
        """
        if not self.exams or 'upcoming_exams' not in self.exams:
            return "Sorry, exam schedule is not available."
        
        upcoming = self.exams['upcoming_exams']
        
        if department:
            department = department.upper()
            if department in upcoming:
                exams = upcoming[department]
                response = f"📝 Upcoming Exams for {department}:\n\n"
                for exam in exams:
                    response += f"📚 {exam['subject']}\n"
                    response += f"   📅 Date: {exam['date']} ({exam['day']})\n"
                    response += f"   ⏰ Time: {exam['time']}\n"
                    response += f"   🚪 Room: {exam['room']}\n"
                    response += f"   📋 Type: {exam['type']}\n\n"
                return response
            else:
                return f"No exam schedule found for {department} department."
        
        # Return all departments' exam schedules
        response = "📝 Upcoming Examination Schedule:\n\n"
        for dept, exams in upcoming.items():
            response += f"📌 {dept} Department:\n"
            for exam in exams[:3]:  # Show only first 3 exams per dept
                response += f"  • {exam['subject']} - {exam['date']} ({exam['time']})\n"
            response += "\n"
        
        # Add exam rules
        if 'exam_rules' in self.exams:
            response += "📋 Important Rules:\n"
            for rule in self.exams['exam_rules'][:3]:
                response += f"  • {rule}\n"
        
        return response
    
    def get_tomorrow_exams(self, department=None):
        """Get exams scheduled for tomorrow"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        if not self.exams or 'upcoming_exams' not in self.exams:
            return "Sorry, exam schedule is not available."
        
        response = "📝 Tomorrow's Exams:\n\n"
        found = False
        
        for dept, exams in self.exams['upcoming_exams'].items():
            if department and dept.upper() != department.upper():
                continue
            for exam in exams:
                if exam['date'] == tomorrow:
                    found = True
                    response += f"📚 {dept} - {exam['subject']}\n"
                    response += f"   ⏰ Time: {exam['time']}\n"
                    response += f"   🚪 Room: {exam['room']}\n\n"
        
        if not found:
            return "No exams scheduled for tomorrow."
        
        return response
    
    def get_department_info(self, department=None):
        """
        Get department information
        
        Args:
            department: Department code (e.g., 'CSE')
            
        Returns:
            Formatted department info string
        """
        if not self.departments or 'departments' not in self.departments:
            return "Sorry, department information is not available."
        
        depts = self.departments['departments']
        
        if department:
            department = department.upper()
            if department in depts:
                info = depts[department]
                response = f"🏛️ {info['full_name']} ({department})\n\n"
                response += f"👤 HOD: {info['hod']}\n"
                response += f"📧 Email: {info['hod_contact']}\n"
                response += f"📍 Office: {info['office']}\n"
                response += f"📞 Phone: {info['phone']}\n"
                response += f"📅 Established: {info['established']}\n"
                response += f"👨‍🏫 Total Faculty: {info['total_faculty']}\n"
                response += f"👨‍🎓 Total Students: {info['total_students']}\n\n"
                response += f"🔬 Labs: {', '.join(info['labs'])}\n\n"
                response += f"💼 Placements:\n"
                response += f"   Average Package: {info['placements']['average_package']}\n"
                response += f"   Highest Package: {info['placements']['highest_package']}\n"
                response += f"   Placement Rate: {info['placements']['placement_rate']}\n"
                return response
            else:
                return f"Department '{department}' not found. Available: CSE, ECE, MECH, CIVIL, EEE"
        
        # Return brief info about all departments
        response = "🏛️ Available Departments:\n\n"
        for dept_code, info in depts.items():
            response += f"📌 {dept_code} - {info['full_name']}\n"
            response += f"   HOD: {info['hod']}\n"
            response += f"   Office: {info['office']}\n\n"
        
        return response
    
    def get_facility_info(self, facility=None):
        """
        Get facility information
        
        Args:
            facility: Facility name (e.g., 'library', 'canteen')
            
        Returns:
            Formatted facility info string
        """
        if not self.campus_info or 'facilities' not in self.campus_info:
            return "Sorry, facility information is not available."
        
        facilities = self.campus_info['facilities']
        
        if facility:
            facility = facility.lower()
            
            if facility == 'library' and 'library' in facilities:
                lib = facilities['library']
                return (f"📚 {lib['name']}\n\n"
                       f"📍 Location: {lib['location']}\n"
                       f"⏰ Timings: {lib['timings']}\n"
                       f"📖 Total Books: {lib['total_books']}\n"
                       f"💻 Digital Resources: {lib['digital_resources']}\n"
                       f"📞 Contact: {lib['contact']}\n"
                       f"🔧 Services: {', '.join(lib['services'])}")
            
            elif facility in ['canteen', 'food'] and 'canteen' in facilities:
                canteens = facilities['canteen']
                response = "🍽️ Campus Canteens:\n\n"
                for name, info in canteens.items():
                    response += f"📌 {name.replace('_', ' ').title()}\n"
                    response += f"   📍 Location: {info['location']}\n"
                    response += f"   ⏰ Timings: {info['timings']}\n\n"
                return response
            
            elif facility in ['hostel', 'accommodation'] and 'hostel' in facilities:
                hostel = facilities['hostel']
                response = "🏠 Hostel Information:\n\n"
                response += f"👦 Boys Hostel:\n"
                response += f"   Blocks: {', '.join(hostel['boys_hostel']['blocks'])}\n"
                response += f"   Warden: {hostel['boys_hostel']['warden']}\n"
                response += f"   Contact: {hostel['boys_hostel']['contact']}\n\n"
                response += f"👧 Girls Hostel:\n"
                response += f"   Blocks: {', '.join(hostel['girls_hostel']['blocks'])}\n"
                response += f"   Warden: {hostel['girls_hostel']['warden']}\n"
                response += f"   Contact: {hostel['girls_hostel']['contact']}\n\n"
                response += f"🍽️ Mess Timings:\n"
                for meal, time in hostel['mess_timing'].items():
                    response += f"   {meal.capitalize()}: {time}\n"
                return response
            
            elif facility in ['sports', 'gym'] and 'sports' in facilities:
                sports = facilities['sports']
                response = "🏆 Sports Facilities:\n\n"
                response += f"🏠 Indoor: {', '.join(sports['indoor'])}\n"
                response += f"🌳 Outdoor: {', '.join(sports['outdoor'])}\n"
                response += f"⏰ Sports Complex: {sports['sports_complex_timing']}\n"
                response += f"⏰ Gym: {sports['gym_timing']}\n"
                response += f"👤 Sports Officer: {sports['sports_officer']}\n"
                response += f"📞 Contact: {sports['contact']}"
                return response
            
            elif facility in ['medical', 'hospital', 'health'] and 'medical' in facilities:
                medical = facilities['medical']
                return (f"🏥 Health Center\n\n"
                       f"📍 Location: {medical['health_center']}\n"
                       f"⏰ Timings: {medical['timings']}\n"
                       f"👨‍⚕️ Doctor: {medical['doctor']}\n"
                       f"📞 Contact: {medical['contact']}\n"
                       f"🚑 Ambulance: {medical['ambulance']}\n"
                       f"🔧 Services: {', '.join(medical['services'])}")
            
            elif facility in ['bus', 'transport'] and 'transport' in facilities:
                transport = facilities['transport']
                return (f"🚌 Transport Facility\n\n"
                       f"🛤️ Bus Routes: {transport['bus_routes']}\n"
                       f"🚌 Total Buses: {transport['total_buses']}\n"
                       f"⏰ Timing: {transport['timing']}\n"
                       f"👤 Transport Officer: {transport['transport_officer']}\n"
                       f"📞 Contact: {transport['contact']}")
            
            else:
                return f"Information about '{facility}' is not available."
        
        # Return general facility overview
        response = "🏫 Campus Facilities:\n\n"
        response += "📚 Library - Central Library\n"
        response += "🍽️ Canteen - Multiple food options\n"
        response += "🏠 Hostel - Boys and Girls hostels\n"
        response += "🏆 Sports - Indoor and outdoor facilities\n"
        response += "🏥 Medical - 24/7 health center\n"
        response += "🚌 Transport - Bus service available\n\n"
        response += "Say 'Tell me about [facility name]' for details."
        
        return response
    
    def get_events(self):
        """Get upcoming events"""
        if not self.campus_info or 'events' not in self.campus_info:
            return "Sorry, events information is not available."
        
        events = self.campus_info['events'].get('upcoming', [])
        
        if not events:
            return "No upcoming events scheduled."
        
        response = "🎉 Upcoming Events:\n\n"
        for event in events:
            response += f"📌 {event['name']}\n"
            response += f"   📅 Date: {event['date']}\n"
            response += f"   📍 Venue: {event['venue']}\n"
            response += f"   📝 {event['description']}\n\n"
        
        return response
    
    def get_faq_answer(self, query):
        """
        Search FAQs for relevant answer
        
        Args:
            query: User's question
            
        Returns:
            FAQ answer if found, None otherwise
        """
        if not self.faqs or 'faqs' not in self.faqs:
            return None
        
        query_lower = query.lower()
        best_match = None
        best_score = 0
        
        for faq in self.faqs['faqs']:
            score = 0
            for keyword in faq['keywords']:
                if keyword in query_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = faq
        
        if best_match and best_score > 0:
            return f"❓ {best_match['question']}\n\n💡 {best_match['answer']}"
        
        return None
    
    def get_important_contacts(self):
        """Get important emergency contacts"""
        if not self.campus_info or 'important_contacts' not in self.campus_info:
            return "Sorry, contact information is not available."
        
        contacts = self.campus_info['important_contacts']
        
        response = "📞 Important Contacts:\n\n"
        for name, number in contacts.items():
            response += f"📌 {name.replace('_', ' ').title()}: {number}\n"
        
        return response


# Test the module
if __name__ == "__main__":
    print("=" * 50)
    print("  Data Handler Module Test")
    print("=" * 50)
    
    handler = DataHandler()
    
    print("\n📋 Testing Data Retrieval:")
    print("-" * 50)
    
    # Test timetable
    print("\n🗓️ Today's CSE Timetable:")
    print(handler.get_timetable(department='CSE'))
    
    # Test exam schedule
    print("\n📝 CSE Exam Schedule:")
    print(handler.get_exam_schedule(department='CSE'))
    
    # Test department info
    print("\n🏛️ CSE Department Info:")
    print(handler.get_department_info(department='CSE'))
    
    # Test facility info
    print("\n📚 Library Info:")
    print(handler.get_facility_info(facility='library'))
    
    # Test FAQ
    print("\n❓ FAQ Test (query: 'how to apply for leave'):")
    print(handler.get_faq_answer("how to apply for leave"))
    
    print("\n" + "=" * 50)
    print("✅ Data Handler module test complete!")
