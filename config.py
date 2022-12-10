"""
Flask app configuration
"""

DEBUG = True
SC = ";"
TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
LESSON_CATALOG = {
    "Accounting": [".accounting", "Accounting"],
    "Engineering documents": [".engineering", "Engineering"],
    "IT Helpdesk": [".it_helpdesk", "Helpdesk"],
    "Time Reporting": [".time_reporting", "Time Reporting"],
}
display = {}

for key in LESSON_CATALOG:
    display[key] = LESSON_CATALOG[key]



