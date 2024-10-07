from flask import jsonify

def validateKeyArgs(data, key_values):
    for key in key_values:
        if key not in data:
            return jsonify({"error": "falta el argumento "+str(key)}), 400
        
def existKeyArgs(data, key):
    if key not in data:
        return False
    else:
        return True