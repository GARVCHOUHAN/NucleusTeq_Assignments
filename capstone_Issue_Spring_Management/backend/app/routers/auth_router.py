from app.schemas.login_schema import LoginRequest
@router.post("/login")
def login_user(
    user: LoginRequest
):

    return AuthService.login_user(user)