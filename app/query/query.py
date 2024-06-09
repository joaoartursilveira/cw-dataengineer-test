import csv
from collections import defaultdict
from sqlalchemy.engine.row import Row
from app.alchemy.models import Country, Gdp
from app.alchemy.session import create_session, session_context
from app.query.logger import Logger


OUTPUT_PATH = './app/database/output.csv'
SESSION = create_session(db_path='./app/database/worldbank.sqlite3')
logger = Logger(__name__)


def query_database(lower_year: int, upper_year: int) -> list[Row[tuple[str, str, str, int, float]]]:
    """
    Queries the local database joining the Country and Gdp tables based on given year interval ordered by country, year asc.\n

    Args:
        lower_year (int): gdp year >= lower_year.
        upper_year (int): gdp year <= upper_year.

    Returns:
        list: Row[Country.id, Country.name, Country.iso3_code, Gdp.year, Gdp.value].

    """
    with session_context(session=SESSION) as session:
        query_data = (session
                      .query(Country.id, Country.name, Country.iso3_code, Gdp.year, Gdp.value)
                      .join(Gdp)
                      .filter(Gdp.year >= lower_year)
                      .filter(Gdp.year <= upper_year)
                      .order_by(Country.name, Gdp.year)
                      .all())
    return query_data


def pivot_query(data: list) -> list[dict]:
    """
    Pivots the query data based on country.id, country.name and country.iso3_code as index and the value for each year as columns.
    """
    data_handler = defaultdict(dict)

    for id, name, iso3_code, year, value in data:
        index = (id, name, iso3_code)
        data_handler[index][year] = value

    buffer = []
    for index, subvalues in data_handler.items():
        pivot_row = {'id': index[0], 'name': index[1], 'iso3_code': index[2]}
        pivot_row.update(subvalues)
        buffer.append(pivot_row)

    return buffer


def write_data(data: list[dict]):
    """
    Writes list of dict data on a csv file.
    """
    fieldnames = [key for key in data[0]]
    with open(OUTPUT_PATH, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,
                                delimiter=',', quoting=csv.QUOTE_MINIMAL)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    logger.info(msg=f'Data output at: {OUTPUT_PATH}')


def main():

    query_data = query_database(lower_year=2019, upper_year=2023)
    pivot_data = pivot_query(data=query_data)
    write_data(data=pivot_data)
    logger.close_log()


if __name__ == '__main__':
    main()
