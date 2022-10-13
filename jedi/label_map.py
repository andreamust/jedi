"""

"""
from SPARQLWrapper import SPARQLWrapper, JSON

ENPOINT_URL = "https://query.wikidata.org/sparql"


# get last part of the url
def get_property_id(url: str) -> str:
    """
    Get the property id from an url
    :param url: the url
    :return: the property id
    """
    return url.split('/')[-1]


def get_property_label(property_url: str) -> str:
    """
    Get the label of a property from Wikidata
    :param property_url: the url of the property
    :return: the label of the property
    """
    query = """
    SELECT ?label WHERE {
      wd:%s rdfs:label ?label .
      FILTER (lang(?label) = "en")
    }
    """ % get_property_id(property_url)

    sparql = SPARQLWrapper(ENPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            return result["label"]["value"]
    except Exception as e:
        return ""


def get_url_from_id(id: str) -> str:
    """
    Get a corresponding url from a id
    (e.g. Q42 -> http://www.wikidata.org/prop/P26) in a mapping file
    :param id: the id
    :return: the url of the id
    """
    with open('../data/humans.spol.rowids', 'r') as file:
        for line in file:
            if id in line:
                return line.split('\t')[1].strip()


def get_label_from_id(id: str) -> str | None:
    """
    Get a corresponding label from a id
    (e.g. Q42 -> http://www.wikidata.org/prop/P26) in a mapping file
    :param id: the id
    :return: the label of the id or None if the id is not in the mapping file
    """
    try:
        property_url = get_url_from_id(id)
        return get_property_label(property_url)
    except Exception as e:
        return None


if __name__ == '__main__':
    # for testing purposes only
    print(get_label_from_id('1791939373'))
