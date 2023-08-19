"""Implements the web scraper logic of the library.

Advisories (really Advisor summaries) are listed on the home page of the Intel Security Center
inside of an HTML table. The code in this module is responsible for retrieving the contents of
that table then parsing the data to allow iteration over Advisory objects.

"""
import datetime
import logging
import re
import unicodedata
from typing import Final, Iterator

import bs4
import requests
from bs4 import Tag

from iscwatch.advisory import Advisory

INTEL_HOME_PAGE: Final = "https://www.intel.com"
INTEL_PAGE_NOT_FOUND: Final = "https://www.intel.com/content/www/us/en/404.html"
ISC_HOME_PAGE: Final = "https://www.intel.com/content/www/us/en/security-center/default.html"

logger = logging.getLogger(__name__)

def iter_advisories() -> Iterator[Advisory]:
    """Iterate over all Intel Security Center product advisories"""
    if result := requests.get(ISC_HOME_PAGE):
        for row_data in iter_advisory_table_row_data(result.text):
            yield Advisory(
                title=text_from_tag(row_data[0]),
                link=link_from_tag(row_data[0]),
                id=text_from_tag(row_data[1]),
                updated=date_from_tag(row_data[2]),
                released=date_from_tag(row_data[3]),
            )


def text_from_tag(tag: Tag):
    """Extract text from tag and remove unicode special characters and whitespace."""
    return strip_unicode(tag.text).strip()


def link_from_tag(tag: Tag) -> str:
    """Convert relative path HREF from anchor tag into absolute path page link."""
    if (anchor := tag.find("a")) and isinstance(anchor, Tag):
        return f"{INTEL_HOME_PAGE}{anchor['href']}"
    return INTEL_PAGE_NOT_FOUND


def date_from_tag(tag: Tag) -> datetime.date:
    """Convert advisory table date format to datetime.datetime.
    
    The regular expression pattern in this function was arrived through trial and error.
    Unfortunately, the way that dates are entered in the HTML table cells is not completely
    consistent (e.g, "Jan" in some cases, "January" in others).  The &nbsp versus a "real"
    space was particularly challenging.
    
    """
    date_pattern = (
        r"(?P<month>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\w*"
        r"(\s|&nbsp;)(?P<day>0?[1-9]|[12][0-9]|3[01]), (?P<year>[0-9]{4})"
    )
    if m := re.search(date_pattern, tag.text):
        return datetime.datetime.strptime(
            f"{m['month']} {m['day']}, {m['year']}", "%b %d, %Y"
        ).date()
    logger.warning(f"Unable to parse date: {tag.text}")
    return datetime.datetime.min.date()


def strip_unicode(text: str):
    """Magic internet code that removes special characters from unicode strings."""
    return "".join(
        char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char)
    )


def iter_advisory_table_row_data(page: str) -> Iterator[tuple[Tag, Tag, Tag, Tag]]:
    """Iterate over ISC Advisory HTML table and yield all data (TD) for each row

    An ISC Advisory HTML rows consist of 4 TD elements (cells):
        <td><a href="/content/.../intel-sa-00886.html">Advisory Title</a></td>
        <td>INTEL-SA-00886</td>
        <td>May 9, 2023</td>
        <td>May 9, 2023</td>

    """
    soup = bs4.BeautifulSoup(page, features="html.parser")
    if (advisory_table := soup.find("table")) and isinstance(advisory_table, Tag):
        advisory_table_rows = advisory_table.find_all("tr", class_="data")
        for one_advisory_table_row in advisory_table_rows:
            yield tuple(one_advisory_table_row.find_all("td"))
