from typing import Any

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, lazyload

from app.core.roles import UserRole
from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.db.models.users.users import User
from app.schema.user_schema import UserCreate, UserUpdate


class UserCrud(CrudBase[User, UserCreate, UserUpdate]):
    def __init__(self, model, db_session: Session) -> None:
        super().__init__(model, db_session)

    def search(
        self,
        filter_params: dict[str, Any],
    ) -> list[User] | None:
        try:
            results = (
                self._db_session.query(self.model).filter_by(**filter_params).all()
            )
            if results is None:
                raise exc.NotFound()
            return results

        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def login_with_phone(self, phone: str) -> User | None:
        try:
            result = (
                self._db_session.query(self.model)
                .filter(self.model.phone == phone)
                .one()
            )
            return result
        except SQLAlchemyError as e:
            raise exc.Unauthorized("Incorrect username or password.", headers=None)

    def change_passcode(self, id: int, new_password: str) -> User | None:
        try:
            query = self._db_session.query(self.model).filter(self.model.id == id)
            query.update(
                {self.model.password: new_password},
                synchronize_session=False,
            )
            self._db_session.commit()
            return query.one()
        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def freeze(self, id: int) -> None:
        try:
            self._db_session.query(self.model).filter(self.model.id == id).update(
                {self.model.is_active: False}, synchronize_session=False
            )
            self._db_session.commit()
        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def is_admin_not_full(self, limit: int) -> bool:
        try:
            results = (
                self._db_session.query(func.count(self.model.role))
                .filter(self.model.role == UserRole.admin)
                .scalar()
            )
            if results >= limit:
                raise exc.Forbidden(details="Maxmium number of admin has reached.")
            return True
        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def get_only_the_id(self, id: int) -> int:
        try:
            stmt = (
                select(self.model)
                .options(lazyload(self.model.purchases), lazyload(self.model.all_sales))
                .where(self.model.id == id)
            )
            obj = self._db_session.scalar(stmt)
            if obj is None:
                raise exc.NotFound()
            return obj
        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def check_empty(self) -> bool:
        try:
            result = self._db_session.query(func.count(self.model.id)).scalar()
            if result:
                raise exc.Forbidden()
            return True
        except SQLAlchemyError as e:
            raise exc.BadRequest()


# fastapi style depends
def get_user_crud(db_session: Session = Depends(get_db)):
    return UserCrud(model=User, db_session=db_session)
