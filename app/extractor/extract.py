import requests
from typing import Generator
from app.extractor.tools import flatten_dict, CountryData
from app.alchemy.models import Country, Gdp, create_db
from app.alchemy.session import create_session, session_context
from app.extractor.logger import Logger

URL = 'https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json&page={n}&per_page=1000'
SESSION = create_session()
logger = Logger(__name__)


def count_all():
    with session_context(session=SESSION) as session:
        count = session.query(Gdp.surrogate_id).count()
    return count


def check_pages() -> int:
    """
    Requests the WorldBank api URL json content and return the total pages depending on the number of register per pages inputed (1000 as default).

    Returns:
        int: Total pages.
    """
    response = requests.get(URL.format(n=1))

    if response.status_code == 200:
        page_info = response.json()[0]
        return int(page_info['pages']), int(page_info['total'])


def request_pages(total: int) -> Generator[dict, None, None]:
    """
    Iterate the pages from 1 to total at the WorldBank api URL and yields its json content.

    Args:
        total (int): Total pages to iterate.
    """
    for i in range(1, total+1):
        response = requests.get(URL.format(n=i))

        if response.status_code != 200:
            return

        yield response.json()[1]


def insert_row(data: CountryData):
    """
    Queries the Gdp data based on year and Country.\n
    if the Gdp data does exists:\n
        Skip
    If the Gdp data doesnt exists:\n
        Checks if the Country is missing:\n
            if yes, creates and inserts the Country and Gdp data.\n
            if not, insert the Gdp data\n

    Args:
        data (CountryData).
    """
    with session_context(SESSION) as session:
        gdp = session.query(Gdp).filter_by(
            country_id=data.country_id, year=data.date).first()

        if not gdp:
            country = session.query(Country).filter_by(
                id=data.country_id).first()

            if not country:
                country = Country(
                    id=data.country_id, name=data.country_value, iso3_code=data.countryiso3code)
                session.add(country)
                logger.info(msg=f"Country row inserted: {country}")

            gdp = Gdp(country_relation=country,
                      year=data.date, value=data.value)
            session.add(gdp)
            logger.info(msg=f"GDP row inserted: {country} - {gdp}")


def main():

    create_db()

    npages, nrecords = check_pages()
    ncurrent = count_all()

    if ncurrent == nrecords:
        return 
    
    for response_json in request_pages(total=npages):

        for record in response_json:
            flat_record = flatten_dict(record, sep='_')
            data = CountryData(**flat_record)
            insert_row(data=data)


if __name__ == '__main__':
    main()
