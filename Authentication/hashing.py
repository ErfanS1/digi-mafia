from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwdContext.hash(password)

    @staticmethod
    def verify(plainPassword: str, hashedPass: str):
        return pwdContext.verify(plainPassword, hashedPass)
