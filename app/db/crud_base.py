from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import insert, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import exceptions as exc
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: ModelType,
        db_session: Session,
    ) -> None:
        self.model = model
        self._db_session = db_session

    def create(
        self,
        input_obj: CreateSchemaType,
    ) -> ModelType | None:
        try:
            # this is for returning model after created
            # stmt = insert(self.model).values(**input_obj.dict()).returning(self.model)
            # result = self._db_session.scalar(stmt)
            # self._db_session.commit()
            # return result
            stmt = insert(self.model).values(**input_obj.dict())
            self._db_session.execute(stmt)
            self._db_session.commit()
        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def update_by_id(
        self,
        id_to_update: int,
        new_vals: UpdateSchemaType,
    ) -> ModelType | None:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == id_to_update)
                .values(new_vals.dict(exclude_unset=True))
            )
            self._db_session.execute(stmt)
            self._db_session.commit()

        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def delete_by_id(
        self,
        id: int,
    ) -> None:
        try:
            obj_to_del = self._db_session.get(self.model, id)
            if obj_to_del is None:
                raise exc.NotFound()

            self._db_session.delete(obj_to_del)
            self._db_session.commit()

        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def get_by_id(
        self,
        id: int,
    ) -> ModelType | None:
        try:
            obj = self._db_session.get(self.model, id)
            if obj is None:
                raise exc.NotFound()
            return obj

        except SQLAlchemyError as e:
            raise exc.BadRequest()
