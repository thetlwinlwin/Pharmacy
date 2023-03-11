from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_pass, hashed_pass) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)


def get_password_pash(password):
    return pwd_context.hash(password)
