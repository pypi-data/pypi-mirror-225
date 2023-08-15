import requests
import json


class GraphDB(object):

    def __init__(self, base_url, credentials=None):
        """

        """
        self.base_url = base_url
        self.credentials = credentials

    def is_running(self):
        """
        Check if GraphDB server is running
        """
        if requests.get(self.base_url + "rest/repositories", auth=self.credentials):
            # returns True for all Status Codes 200-400
            return True
        else:
            print("Graph_DB is not running or access is not granted")
            return False

    def clear_repository(self, repository):
        """
        Clear contents of currently selected repository
        """
        url = self.base_url + 'repositories/' + repository + '/' + 'statements'
        response = requests.request(method='DELETE', url=url, auth=self.credentials)
        return response

    def upload_rdf_file(self, repository, graph, rdf_file, rdf_as_file=False):
        """
        Upload rdf from turtle file or variable into selected graph from repository
        """
        url = self.base_url + 'repositories/' + repository + '/' + 'statements'
        headers = {
            'Content-type': 'application/x-turtle'
        }
        params = {'graph': graph}
        if rdf_as_file:
            data = open(rdf_file, 'r', encoding='utf-8').read()
        else:
            data = rdf_file
        response = requests.request(method='PUT', url=url, headers=headers, params=params,
                                    data=data, auth=self.credentials)
        return response

    def download_graph(self, repository, graph, download_format='application/rdf+json',
                       save_as_file=False, export_filename='data.json'):

        url = self.base_url + 'rest/explore/graph'
        params = {
            'uri': graph,
            'role': 'context',
            'inference': 'all',
            'bnodes': True,
            'sameAs': True
        }
        # params = json.dumps(params, separators=('&', '='))
        headers = {
            'Accept': download_format,
            'X-GraphDB-Repository': repository,
        }
        response = requests.request(method='GET', url=url, params=params, headers=headers,
                                    auth=self.credentials)
        download = json.loads(response.text)
        if save_as_file:
            with open(export_filename, 'w') as f:
                json.dump(download, f)
        return download
