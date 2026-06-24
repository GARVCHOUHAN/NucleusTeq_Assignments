from typing import Dict

def create_user_document(
    name: str,
    email: str,
    password: str,
    role: str
) -> Dict:
    return {
        "name": name,
        "email": email,
        "password": password,
        "role": role
    }