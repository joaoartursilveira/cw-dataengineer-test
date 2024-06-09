from pathlib import Path
from sqlalchemy import ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


DB_NAME = Path('./app/database/worldbank.sqlite3')
SQLITE = f'sqlite:///{DB_NAME}'


def todict(obj):
    """ 
    Return the object's dict excluding private attributes,
    sqlalchemy state and relationship attributes.
    """
    excl = ('_sa_adapter', '_sa_instance_state')
    return {k: v for k, v in vars(obj).items() if not k.startswith('_') and not any(hasattr(v, a) for a in excl)}


class Base(DeclarativeBase):

    def __repr__(self) -> str:
        params = ', '.join(f'{k}={v}' for k, v in todict(self).items())
        return f"{self.__class__.__name__}({params})"


class Country(Base):
    __tablename__ = 'country'

    surrogate_id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    iso3_code: Mapped[str] = mapped_column(nullable=False)

    gdp_relation = relationship('Gdp', back_populates='country_relation')

    def __init__(self, id: str, name: str, iso3_code: str):
        self.id = id
        self.name = name
        self.iso3_code = iso3_code


class Gdp(Base):
    __tablename__ = 'gdp'

    surrogate_id: Mapped[int] = mapped_column(primary_key=True)
    country_id = mapped_column(ForeignKey('country.id'))
    year: Mapped[int]
    value: Mapped[float] = mapped_column(nullable=True)

    country_relation = relationship('Country', back_populates='gdp_relation')

    __table_args__ = (UniqueConstraint(
        'country_id', 'year', name='unique_country_year'),)

    def __init__(self, country_relation: Country, year: int, value: float):
        self.country_relation = country_relation
        self.year = year
        self.value = value


engine = create_engine(SQLITE, echo=True)


def create_db():
    if not DB_NAME.exists():
        DB_NAME.touch()
        Base.metadata.create_all(bind=engine)
    else:
        Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    create_db()
