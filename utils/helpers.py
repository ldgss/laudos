from flask import session

def session_on():
    if 'usuario' in session:
        return True
    return False