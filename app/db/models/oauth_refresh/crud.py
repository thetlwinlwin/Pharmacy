from fastapi import Depends
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.db.models.oauth_refresh.model import RefreshToken
from app.schema.token_schema import RefreshTokenCreate, RefreshTokenUpdate


class RefreshTokenCrud(CrudBase[RefreshToken, RefreshTokenCreate, RefreshTokenUpdate]):
    def __init__(self, model, db_session: Session) -> None:
        super().__init__(model, db_session)

    def add_with_user_id(self, incoming_token: RefreshTokenUpdate) -> None:
        query = self._db_session.query(self.model).filter(
            self.model.user_id == incoming_token.user_id
        )
        try:
            result = query.first()
            if result is None:
                self.create(incoming_token)
            else:
                query.update(
                    incoming_token.dict(exclude_unset=True),
                    synchronize_session=False,
                )
                self._db_session.commit()
        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def search_by_user_id(self, user_id: int) -> RefreshToken:
        try:
            return (
                self._db_session.query(self.model)
                .filter(self.model.user_id == user_id)
                .one()
            )

        except (SQLAlchemyError, NoResultFound) as e:
            raise exc.BadRequest()


# fastapi style depends
def get_oauth_crud(db_session: Session = Depends(get_db)):
    return RefreshTokenCrud(model=RefreshToken, db_session=db_session)
