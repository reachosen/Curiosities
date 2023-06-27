api_sources = {
    'pmc': {
        'base_url': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
        'namespaces': None,
        'result_key': 'IdList/Id',
        'id_key': 'Id',
        'title_key': None,
        'summary_key': None,
        'documentation_url': 'https://www.ncbi.nlm.nih.gov/books/NBK25501/'
    },
    'europe_pmc': {
        'base_url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/search',
        'namespaces': None,
        'result_key': 'resultList/result',
        'id_key': 'id',
        'title_key': 'title',
        'summary_key': 'abstractText',
        'documentation_url': 'https://europepmc.org/RestfulWebService'
    },
    'plos': {
        'base_url': 'https://api.crossref.org/works',
        'namespaces': None,
        'result_key': 'message/items',
        'id_key': 'DOI',
        'title_key': 'title',
        'summary_key': 'abstract',
        'documentation_url': 'https://api.crossref.org/'
    },
    'arxiv': {
        'base_url': 'http://export.arxiv.org/api/query',
        'namespaces': {
            'default': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        },
        'result_key': 'entry',
        'id_key': 'id',
        'title_key': 'title',
        'summary_key': 'summary',
        'documentation_url': 'https://arxiv.org/help/api/index'
    }
}
