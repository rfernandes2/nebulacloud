from flask_jwt_extended import get_jwt_identity

class VerifyTokenSerializer:
    def __init__(self, token):
        self.token = token

    def validate(self):
        identity = get_jwt_identity()
        if identity:
            return {"valid": True, "user": identity}, 200
        else:
            return {"valid": False, "msg": "Invalid token"}, 498