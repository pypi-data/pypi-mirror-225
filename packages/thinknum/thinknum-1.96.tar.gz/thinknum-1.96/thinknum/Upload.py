import requests
import json
import os
import gzip
import shutil
import platform


class Upload(object):

    OK = 200
    _BASE_URL = 'https://data.thinknum.com'

    def __init__(self, client_id, client_secret, proxies={}, verify=True):
        self._client_id = client_id
        self._client_secret = client_secret
        self._proxies = proxies
        self._verify = verify

        self._token = None
        self._authenticate()
        self._headers = {
            "Authorization": "token {token}".format(token=self._token),
            "X-API-Version": "20151130",
            "Accept": "application/json",
            "User-Agent": "Python API 1.96 / {local_version}".format(local_version=platform.python_version())
        }

        self._dataset_id = None
    
    def _requests(self, method, url, headers={}, data={}, json={}, params={}, files={}, stream=False, allow_redirects=True):
        if method not in ['post', 'get']:
            raise Exception('Not allowed method')
        return getattr(requests, method)(
            url,
            headers=headers,
            data=data,
            json=json,
            params=params,
            files=files,
            stream=stream,
            proxies=self._proxies,
            verify=self._verify,
            allow_redirects=allow_redirects
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
            raise Exception('Invalid autentication')
        self._token = json.loads(response.text)['auth_token']

    def upload_csv(self, filepath):
        response = self._requests(
            method='post',
            url='{base_url}/uploads/'.format(
                base_url=self._BASE_URL
            ),
            headers=self._headers,
            files={'file': open(filepath, 'rb')}
        )
        upload_id = json.loads(response.text)['id']

        response = self._requests(
            method='get',
            url='{base_url}/uploads/{upload_id}/setup/'.format(
                base_url=self._BASE_URL,
                upload_id=upload_id
            ),
            headers=self._headers
        )
        result = json.loads(response.text)

        response = self._requests(
            method='post',
            url='{base_url}/uploads/{upload_id}/setup/'.format(
                base_url=self._BASE_URL,
                upload_id=upload_id
            ),
            headers=self._headers,
            data={
                'request': json.dumps({
                    "columns": [{
                        "display_name": column["display_name"],
                        "type": column["type"],
                        "id": column["id"],
                        "format": column["format"],
                    } for column in result['columns']],
                    "display_name": result["display_name"],
                    "header": result["header"],
                    "encoding": "utf8",
                    "visibility": result["visibility"],
                    "id": upload_id
                })
            }
        )
        result = json.loads(response.text)
        return {"id": result["id"], "state": result["state"]}

    def check_upload_status(self, upload_id):
        response = self._requests(
            method='get',
            url='{base_url}/uploads/'.format(base_url=self._BASE_URL),
            headers=self._headers
        )
        result = json.loads(response.text)
        for upload in result['uploads']:
            if upload['id'] == upload_id:
                return {
                    "id": upload["id"],
                    "state": upload["state"]
                }
        raise Exception('upload_id not found')
