import dataclasses

from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from pytech.sqlalchemy_tools.models import BaseSqlModel

__all__ = ["retrieve_all_data"]


def retrieve_all_data(session: Session, model: type(BaseSqlModel)) -> list:
    """
    Function used to retrieve data from a specific model using a specific Engine.

    :param session: the session to use for the connection
    :param model: the model class from which retrieve the data
    :return:
    """

    if not isinstance(session, Session):
        raise TypeError("'session' must be a valid Session.")

    if not issubclass(model, BaseSqlModel):
        raise TypeError("'model' must inherit from 'BaseSqlModel'.")

    result = session.execute(
        select(model)
    )
    return [dataclasses.asdict(el) for [el] in result]
