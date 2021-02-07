import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')


def getConfig():
    config = {
        'token': parser.get('data', 'token'),
        'StudentRole': parser.getint('roles', 'StudentRole'),
        'AdvisorRole': parser.getint('roles', 'AdvisorRole'),
        'AssignmentsPath': parser.get('folders', 'assignmentsPath'),
        'SubmissionsPath': parser.get('folders', 'submissionsPath'),
        'QuestionBank': parser.get('files', 'questionBank')
    }
    return config


def load_assignments():
    with open(parser.get('files', 'assignments'), 'r') as f:
        assignments = json.load(f)

    return assignments


def save_assignments(assignment):
    with open(parser.get('files', 'assignments'), 'w') as f:
        json.dump(assignment, f)


def getHelpFile(role):
    config = getConfig()
    if role == config['StudentRole']:
        with open(parser.get('files', 'StudentCommandstxt'), 'r') as f:
            return f.read()
    elif role == config['AdvisorRole']:
        with open(parser.get('files', 'AdvisorCommandstxt'), 'r') as f:
            return f.read()
    else:
        return None


def add_question(question):
    with open(parser.get('files', 'questionBank'), 'r') as f:
        bank = json.load(f)
    bank[question] = []

    with open(parser.get('files', 'questionBank'), 'w') as f:
        json.dump(bank, f)


def get_question(user_id):
    with open(parser.get('files', 'questionBank'), 'r') as f:
        bank = json.load(f)

    for i in bank.keys():
        if user_id not in bank[i]:
            bank[i].append(user_id)

            with open(parser.get('files', 'questionBank'), 'w') as f:
                json.dump(bank, f)

            return i

    return "You don't have any questions left... tryhard..."