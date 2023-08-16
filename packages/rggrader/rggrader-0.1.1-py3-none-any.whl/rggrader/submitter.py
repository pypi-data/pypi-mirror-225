# submitter.py

import requests

def submit(id_student, name, assignment_name, result, question_name='', code=''):
    data = {
        "id": id_student,
        "name": name,
        "assignment_name": assignment_name,
        "question_name": question_name,
        "code": code,
        "result": result
    }

    r = requests.post('https://rea-submitter.fly.dev/submission/submit/bquery', json=data)
    if r.status_code == 200:
        return 'Assignment successfully submitted'
    else:
        return 'Failed to submit assignment'