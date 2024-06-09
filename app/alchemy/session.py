import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from contextlib import contextmanager


def create_session(db_path: Path = './app/database/worldbank.sqlite3') -> scoped_session[Session]:
    SQLITE = f'sqlite:///{db_path}'

    engine = create_engine(SQLITE)
    SessionMaker = sessionmaker(bind=engine)
    Session = scoped_session(SessionMaker)
    return Session


@contextmanager
def session_context(session: scoped_session[Session]):
    local_session = session()
    try:
        yield local_session
        local_session.commit()

    except Exception:
        local_session.rollback()
        raise

    finally:
        local_session.close()


if __name__ == "__main__":
    print(os.getcwd())
    print(os.path.relpath(__file__))
    print(Path(os.path.relpath(__file__)).parents[1:-1])
