import json
from configparser import ConfigParser


def getConfig():
    config = ConfigParser()
    config.read('config.ini')
    config = {
        'token': config.get('data', 'token'),
        'StudentRole': config.getint('roles', 'StudentRole'),
        'AdvisorRole': config.getint('roles', 'AdvisorRole'),
        'AssignmentsPath': config.get('folders', 'assignmentsPath'),
        'SubmissionsPath': config.get('folders', 'submissionsPath')
    }
    return config


def load_assignments():
    with open('Database/assignments.json', 'r') as f:
        assignments = json.load(f)

    return assignments


def save_assignments(assignment):
    with open('Database/assignments.json', 'w') as f:
        json.dump(assignment, f)


def getHelpFile(role):
    config = getConfig()

    if role == config['StudentRole']:
        with open('Database/HelpTexts/StudentCommands.txt', 'r') as f:
            return f.read()
    elif role == config['AdvisorRole']:
        with open('Database/HelpTexts/AdvisorCommands.txt', 'r') as f:
            return f.read()
    else:
        return None