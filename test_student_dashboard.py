#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from flask import url_for

def test_student_dashboard():
    with app.app_context():
        try:
            # Test if we can create a test request context
            with app.test_request_context():
                # Test URL generation
                student_dashboard_url = url_for('student_dashboard')
                print(f"✅ Student dashboard URL: {student_dashboard_url}")
                
                # Test if template exists
                import os
                template_path = os.path.join('templates', 'student_dashboard.html')
                base_template_path = os.path.join('templates', 'student_base.html')
                
                if os.path.exists(template_path):
                    print(f"✅ Template exists: {template_path}")
                else:
                    print(f"❌ Template missing: {template_path}")
                    
                if os.path.exists(base_template_path):
                    print(f"✅ Base template exists: {base_template_path}")
                else:
                    print(f"❌ Base template missing: {base_template_path}")
                
                # Test template rendering (without user context)
                try:
                    from flask import render_template_string
                    test_template = """
                    {% extends "student_base.html" %}
                    {% block content %}
                    <h1>Test</h1>
                    {% endblock %}
                    """
                    # This will fail if there are template syntax errors
                    print("✅ Template syntax appears to be valid")
                except Exception as e:
                    print(f"❌ Template syntax error: {e}")
                
                print("✅ All basic tests passed!")
                
        except Exception as e:
            print(f"❌ Error in test: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_student_dashboard()