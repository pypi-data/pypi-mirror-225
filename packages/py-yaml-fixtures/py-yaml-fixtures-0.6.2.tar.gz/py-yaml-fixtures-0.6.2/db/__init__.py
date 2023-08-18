import os
from typing import List
import sqlalchemy as sa

from py_yaml_fixtures import FixturesLoader
from py_yaml_fixtures.factories.sqlalchemy import SQLAlchemyModelFactory
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

PY_YAML_FIXTURES_DIR = 'fixtures'

BaseModel = declarative_base()


class UserRoleAssociation(BaseModel):
    """Join table between Role and User"""

    __tablename__ = "users_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)
    user: Mapped["User"] = relationship(back_populates="user_role_associations")

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True, nullable=False)
    role: Mapped["Role"] = relationship(back_populates="role_user_associations")

    def __init__(self, user=None, role=None):
        self.user = user
        self.role = role

d
class Role(BaseModel):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    role_user_associations: Mapped[List["UserRoleAssociation"]] = relationship(back_populates="role")
    users: AssociationProxy[List["User"]] = association_proxy("role_user_associations", "user", creator=lambda u: UserRoleAssociation(user=u))


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)

    user_role_associations: Mapped[List["UserRoleAssociation"]] = relationship(back_populates="user")
    roles: AssociationProxy[List["Role"]] = association_proxy("user_role_associations", "role", creator=lambda r: UserRoleAssociation(role=r))

if __name__ == '__main__':
    engine = create_engine('sqlite:///')
    BaseModel.metadata.create_all(bind=engine)
    session = sessionmaker(engine)
    model_classes = [User, Role, UserRoleAssociation]
    with session.begin() as sess:
        factory = SQLAlchemyModelFactory(session=sess, models=model_classes)
        loader = FixturesLoader(factory, fixture_dirs=[
            os.path.dirname(os.path.abspath(__file__)),
        ])
        loader.create_all(lambda id_, model, created: print(
            '{action} {identifier}: {model}'.format(
                action='Creating' if created else 'Updating',
                identifier=id_.key,
                model=repr(model)
            )))
