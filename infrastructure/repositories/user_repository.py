from sqlalchemy.orm import Session
from infrastructure.db_models.models import UserModel
from domain.models.user import User

class UserReposirity:
    def __init__(self, db_session: Session):
        self.db =db_session
    
    def authenticate(self, username: str, password: str) -> User | None:
        db_user = self.db.query(UserModel).filter(
            UserModel.UserName == username,
            UserModel.Password == password
        ).first()
        if db_user:
            return User(
                user_id=db_user.UserID,
                username=db_user.UserName,
                password=db_user.Password,
                role=db_user.Role,
                customer_id=db_user.CustomerID
            )
        return None
