"""
Logic-Based Student Access and Data Management System
Bohol Island State University - Midterm Project
Flask Web Application - Python Backend
"""

from flask import Flask, render_template, jsonify, request
import math
import json

app = Flask(__name__)

class AccessManagementSystem:
    """Core system implementing all required features - PURE PYTHON"""
    
    def __init__(self):
        # FEATURE 2: SETS (User Classification) - Python sets
        self.students = {"S001", "S002", "S003", "S004", "S005"}
        self.faculty = {"F001", "F002", "F003", "F004", "F005"}
        self.staff = {"ST001", "ST002", "ST003", "ST004", "ST005"}
        self.visitors = {"V001", "V002"}

        self.all_users = self.students | self.faculty | self.staff | self.visitors
        self.authorized_users = {"S001", "S002", "F001", "F002", "ST001", "ST002"}
        self.restricted_users = {"S003", "V001", "V002"}

        self.rooms = {"R101", "R102", "R103", "R201", "R202"}
        self.lab_rooms = {"R101", "R102"}
        self.lecture_rooms = {"R103", "R201", "R202"}

        # FEATURE 3: RELATIONS - Python dictionary
        self.access_permissions = {
            "S001": {"R101", "R102", "R103"},
            "S002": {"R101", "R102"},
            "S003": {"R201"},
            "S004": set(),
            "S005": {"R103"},
            "F001": {"R101", "R102", "R103", "R201", "R202"},
            "F002": {"R101", "R102", "R201"},
            "ST001": {"R101", "R102", "R103", "R201", "R202"},
            "ST002": {"R103", "R202"},
            "V001": {"R201"},
            "V002": set()
        }

        # FEATURE 5: MATRICES - Python 2D list
        self.user_list = sorted(self.all_users)
        self.room_list = sorted(self.rooms)
        self.access_matrix = self._build_access_matrix()

        # FEATURE 6: NUMBER THEORY - Python math.gcd()
        self.user_access_levels = self._calculate_access_levels()

    # FEATURE 1: PROPOSITIONAL LOGIC - Python method
    def evaluate_predicate_logic(self, user, room):
        """Pure Python logic evaluation"""
        is_registered = user in self.all_users
        is_authorized = user in self.authorized_users
        is_restricted = user in self.restricted_users
        has_permission = room in self.access_permissions.get(user, set())

        can_access = is_registered and is_authorized and (not is_restricted) and has_permission
        return can_access

    # FEATURE 4: BOOLEAN FUNCTIONS - Python method
    def evaluate_boolean_function(self, A, B, C, D):
        """Pure Python boolean evaluation"""
        return bool(A and B and C and (not D))

    def _build_access_matrix(self):
        """Pure Python matrix building"""
        matrix = []
        for user in self.user_list:
            row = []
            for room in self.room_list:
                if room in self.access_permissions.get(user, set()):
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix

    def _calculate_access_levels(self):
        """Pure Python number theory using math.gcd()"""
        levels = {}
        for user in self.user_list:
            permission_bits = 0
            for i, room in enumerate(self.room_list):
                if room in self.access_permissions.get(user, set()):
                    permission_bits |= (1 << i)
            if permission_bits > 0:
                levels[user] = math.gcd(permission_bits, 31)
            else:
                levels[user] = 0
        return levels

    # FEATURE 7: PROOF OF CONSISTENCY - Python method
    def verify_rule_consistency(self, user):
        if user in self.restricted_users:
            for room in self.rooms:
                if self.evaluate_predicate_logic(user, room):
                    return False, f"Inconsistency found! Restricted user {user} gained access to {room}."
            return True, f"Proof verified: Restricted user {user} is strictly denied access across all rooms."
        return True, f"User {user} is not restricted."

    def get_matrix_for_html(self):
        """Returns Python dictionary for HTML rendering"""
        formatted_rows = []
        for i, user in enumerate(self.user_list):
            formatted_rows.append({
                'user': user,
                'permissions': self.access_matrix[i],
                'level': self.user_access_levels.get(user, 0)
            })
        return {
            'headers': self.room_list,
            'rows': formatted_rows
        }

    def get_detailed_access_check(self, user, room):
        """Pure Python - returns detailed results"""
        is_registered = user in self.all_users
        is_authorized = user in self.authorized_users
        is_restricted = user in self.restricted_users
        has_permission = room in self.access_permissions.get(user, set())
        
        can_access = self.evaluate_predicate_logic(user, room)
        bool_result = self.evaluate_boolean_function(is_registered, is_authorized, has_permission, is_restricted)
        
        # GCD check
        level = self.user_access_levels.get(user, 0)
        room_num = int(room[1:]) if room[1:].isdigit() else 0
        gcd_value = math.gcd(level, room_num % 31 + 1) if level > 0 and room_num > 0 else 0
        gcd_passed = gcd_value > 1
        
        return {
            'user': user,
            'room': room,
            'granted': can_access,
            'details': {
                'registered': is_registered,
                'authorized': is_authorized,
                'restricted': is_restricted,
                'has_permission': has_permission,
                'bool_result': bool_result,
                'access_level': level,
                'gcd_value': gcd_value,
                'gcd_passed': gcd_passed
            },
            'consistency': self.verify_rule_consistency(user)
        }


# ============================================================
# FLASK ROUTES - Python endpoints
# ============================================================

# Initialize the system (Python object)
system = AccessManagementSystem()

@app.route('/')
def index():
    """Python route that serves the HTML page"""
    matrix_data = system.get_matrix_for_html()
    return render_template('index.html', data=json.dumps(matrix_data))

@app.route('/api/check/<user>/<room>')
def check_api(user, room):
    """Python API endpoint - returns JSON"""
    result = system.evaluate_predicate_logic(user, room)
    return jsonify({
        'granted': result,
        'user': user,
        'room': room
    })

@app.route('/api/detailed_check/<user>/<room>')
def detailed_check_api(user, room):
    """Python API endpoint - returns detailed JSON"""
    result = system.get_detailed_access_check(user, room)
    return jsonify(result)

@app.route('/api/users')
def get_users():
    """Python API - returns user lists"""
    return jsonify({
        'users': system.user_list,
        'authorized': list(system.authorized_users),
        'restricted': list(system.restricted_users)
    })

@app.route('/api/rooms')
def get_rooms():
    """Python API - returns room lists"""
    return jsonify({
        'rooms': system.room_list,
        'lab_rooms': list(system.lab_rooms),
        'lecture_rooms': list(system.lecture_rooms)
    })

@app.route('/api/matrix')
def get_matrix():
    """Python API - returns matrix data"""
    return jsonify(system.get_matrix_for_html())

@app.route('/api/verify/<user>')
def verify_user(user):
    """Python API - consistency check"""
    consistent, message = system.verify_rule_consistency(user)
    return jsonify({
        'user': user,
        'consistent': consistent,
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)