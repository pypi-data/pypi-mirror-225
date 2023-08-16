import re

from autologbook.elog_post_splitter import elog_url_pattern


def test_url_guessing():
    test_strings = ['https://localhost:8080/logbook/123',
                    'http://localhost:8080/logbook/123',
                    'https://10.166.62.14:8080/logbook/1234',
                    'https://10.166.62.14/logbook/1234',
                    'http://10.166.16.65:443/Vega-Cold-Analysis/12']
    results = [{'url': 'https://localhost', 'port': '8080', 'logbook': 'logbook', 'msg_id': '123'},
               {'url': 'http://localhost', 'port': '8080', 'logbook': 'logbook', 'msg_id': '123'},
               {'url': 'https://10.166.62.14', 'port': '8080', 'logbook': 'logbook', 'msg_id': '1234'},
               {'url': 'https://10.166.62.14', 'port': None, 'logbook': 'logbook', 'msg_id': '1234'},
               {'url': 'http://10.166.16.65', 'port': '443', 'logbook': 'Vega-Cold-Analysis', 'msg_id': '12'}
               ]
    for test_string, result in zip(test_strings, results):
        match = re.match(elog_url_pattern, test_string)
        if match:
            for key in result.keys():
                assert match.group(key) == result[key]
        else:
            assert False
