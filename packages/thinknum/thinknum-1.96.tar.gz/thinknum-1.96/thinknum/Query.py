import requests
import json
import time
import platform
import itertools


class Query(object):

    OK = 200
    CREATED = 201
    ACCEPTED = 202

    _BASE_URL = 'https://data.thinknum.com'

    def __init__(self, client_id, client_secret, proxies={}, verify=True, timeout=180):
        if not client_id or not isinstance(client_id, str):
            raise Exception('Invalid parameter: client_id')
        if not client_secret or not isinstance(client_secret, str):
            raise Exception('Invalid parameter: client_secret')
        if not isinstance(proxies, dict):
            raise Exception('Invalid parameter: proxies')
        if not isinstance(verify, bool):
            raise Exception('Invalid parameter: verify')
        if not isinstance(timeout, (int, type(None))):
            raise Exception('Invalid parameter: timeout')

        self._client_id = client_id
        self._client_secret = client_secret
        self._proxies = proxies
        self._verify = verify
        self._token = None
        self._authenticate()
        self._headers = {
            "Accept": "application/json",
            "Authorization": "token {token}".format(token=self._token),
            "X-API-Version": "20151130",
            "User-Agent": "Python API 1.96 / {local_version}".format(local_version=platform.python_version())
        }
        self._dataset_id = None
        self._tickers = []
        self._filters = []
        self._functions = []
        self._aggregations = []
        self._groups = []
        self._sorts = []
        self._start = 1
        self._limit = 100000
        self._timeout = timeout
        self._valid_dataset_ids = [dataset.get('id') for dataset in self.get_dataset_list()]

    def _raise_exception_from_response(self, response):
        try:
            message = json.loads(response.text).get("message")
        except Exception as e:
            message = response.text if response.text else 'INTERNAL SERVER ERROR'
        finally:
            raise Exception(message)

    def _requests(self, method, url, headers={}, data={}, json={}, params={}):
        if method not in ['post', 'get', 'head']:
            raise Exception('Not allowed method')
        return getattr(requests, method)(
            url,
            headers=headers,
            data=data,
            json=json,
            params=params,
            proxies=self._proxies,
            verify=self._verify
        )

    def _authenticate(self):
        response = self._requests(
            method='post',
            url='{base_url}/api/authorize'.format(base_url=self._BASE_URL),
            data={
                "version": "20151130",
                "client_id": self._client_id,
                "client_secret": self._client_secret
            }
        )
        if response.status_code != self.OK:
            message = response.text
            raise Exception(message)
        self._token = json.loads(response.text)['auth_token']

    @property
    def _query(self):
        query = {}
        if self._tickers:
            query['tickers'] = self._tickers
        if self._filters:
            query['filters'] = self._filters
        if self._functions:
            query['functions'] = self._functions
        if self._groups:
            query['groups'] = self._groups
        if self._aggregations:
            query['aggregations'] = self._aggregations
        if self._sorts:
            query['sorts'] = self._sorts
        return query

    def reset_query(self):
        del self._tickers[:]
        del self._filters[:]
        del self._functions[:]
        del self._groups[:]
        del self._aggregations[:]
        del self._sorts[:]

    def add_ticker(self, ticker):
        self._tickers.append(ticker)

    def reset_tickers(self):
        del self._tickers[:]

    def _get_condition_depth(self, condition):
        for filter in self._filters:
            for sub_filter in filter.get('conditions', []):
                if sub_filter == condition:
                    return 2
            if filter == condition:
                return 1
        return None

    def add_condition(self, match, condition=None):
        if not condition:
            self._filters.append({
                'match': match,
                'conditions': []
            })
            return self._filters[-1]
        else:
            if self._get_condition_depth(condition) == 2:
                raise Exception('Maximum depth of the condition is two')
            condition['conditions'].append({
                'match': match,
                'conditions': []
            })
            return condition['conditions'][-1]

    def add_filter(self, column, type, value, condition=None):
        if not condition:
            self._filters.append({
                "column": column,
                "type": type,
                "value": value,
            })
        else:
            condition['conditions'].append({
                "column": column,
                "type": type,
                "value": value,
            })

    def reset_filters(self):
        del self._filters[:]

    def add_function(self, function, parameters):
        self._functions.append({
            "function": function,
            "parameters": parameters
        })

    def reset_functions(self):
        del self._functions[:]

    def add_group(self, column):
        self._groups.append({
            "column": column
        })

    def reset_groups(self):
        del self._groups[:]

    def add_aggregation(self, column, type):
        self._aggregations.append({
            "column": column,
            "type": type
        })

    def reset_aggregations(self):
        del self._aggregations[:]

    def add_sort(self, column, order):
        self._sorts.append({
            "column": column,
            "order": order
        })

    def reset_sorts(self, column, order):
        del self._sorts[:]

    # Return all dataset list
    def get_dataset_list(self):
        response = self._requests(
            method='get',
            url='{base_url}/datasets/'.format(base_url=self._BASE_URL),
            headers=self._headers
        )
        if response.status_code != self.OK:
            self._raise_exception_from_response(response)
        return json.loads(response.text).get('datasets', [])

    # Return dataset metadata
    def get_dataset_metadata(self, dataset_id):
        if not dataset_id or dataset_id not in self._valid_dataset_ids:
            raise Exception('Invalid dataset_id')

        response = self._requests(
            method='get',
            url='{base_url}/datasets/{dataset_id}'.format(
                base_url=self._BASE_URL,
                dataset_id=dataset_id
            ),
            headers=self._headers
        )
        if response.status_code != self.OK:
            self._raise_exception_from_response(response)

        result = json.loads(response.text)
        return {
            "id": result.get("id"),
            "display_name": result.get("display_name"),
            "dataset_fields": result.get("dataset_fields", []),
            "unique_fields": result.get("unique_fields", []),
            "functions": result.get("functions", {}),
            "truncate_limit": result.get("truncate_limit"),
            "summary": result.get("summary"),
        }

    # Return dataset list of the ticker
    def get_ticker_dataset_list(self, query):
        if not query:
            return []
        response = self._requests(
            method='get',
            url='{base_url}/datasets/'.format(
                base_url=self._BASE_URL,
                query=query
            ),
            headers=self._headers,
            params={
                "ticker": query
            }
        )
        if response.status_code != self.OK:
            self._raise_exception_from_response(response)
        return json.loads(response.text).get('datasets', [])

    # Return ticker list from search term
    def get_ticker_list(self, query, dataset_id=None):
        if not query:
            return []

        if dataset_id:
            url = '{base_url}/datasets/{dataset_id}/tickers/'.format(
                base_url=self._BASE_URL,
                dataset_id=dataset_id,
            )
        else:
            url = '{base_url}/tickers/'.format(
                base_url=self._BASE_URL,
            )

        response = self._requests(
            method='get',
            url=url,
            headers=self._headers, 
            params={"query": query}
        )
        if response.status_code != self.OK:
            self._raise_exception_from_response(response)

        return json.loads(response.text).get('queries', {}).get(query, [])

    # Return data
    def get_data(self, dataset_id, start=None, limit=None, except_on_truncate=False):
        if not dataset_id or dataset_id not in self._valid_dataset_ids:
            raise Exception('Invalid dataset_id')
        if self._start < 1:
            raise Exception('Start offset is less than 1')
        if self._limit < 1:
            raise Exception('Limit offset is less than 1')
        if start:
            self._start = start
        if limit:
            self._limit = limit

        # 1. POST
        response = self._requests(
            method='post',
            url='{base_url}/datasets/{dataset_id}/query/'.format(
                base_url=self._BASE_URL,
                dataset_id=dataset_id
            ),
            headers=self._headers,
            json=self._query,
        )
        if response.status_code != self.CREATED:
            self._raise_exception_from_response(response)
        result = json.loads(response.text)
        query_id = result.get('id')

        # 2. HEAD
        is_created = False
        for index in range(self._timeout) if self._timeout else itertools.count():
            response = self._requests(
                method='head',
                url='{base_url}/datasets/{dataset_id}/query/{query_id}'.format(
                    base_url=self._BASE_URL,
                    dataset_id=dataset_id,
                    query_id=query_id
                ),
                headers=dict(
                    self._headers,
                    **{"Accept": "application/vnd.thinknum.table+json"}
                ),
                params={
                    "start": self._start,
                    "limit": self._limit
                }
            )
            if except_on_truncate is True and response.headers['X-Truncated'] == 'true':
                raise Exception('Data truncated')
            if response.status_code == self.OK:
                is_created = True
                break
            elif response.status_code == self.ACCEPTED:
                time.sleep(1)
                continue
            else:
                self._raise_exception_from_response(response)

        if not is_created:
            raise Exception("Data still being fetched. Please retry it")

        # 3. GET
        response = self._requests(
            method='get',
            url='{base_url}/datasets/{dataset_id}/query/{query_id}'.format(
                base_url=self._BASE_URL,
                dataset_id=dataset_id,
                query_id=query_id,
            ),
            headers=dict(
                self._headers,
                **{"Accept": "application/vnd.thinknum.table+json"}
            ),
            params={
                "start": self._start,
                "limit": self._limit
            }
        )
        if response.status_code != self.OK:
            self._raise_exception_from_response(response)
        return json.loads(response.text)
