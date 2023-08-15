import requests
from pathlib import Path
import json
from . import utils


class OntoRefine:
    """
    Class to access the REST API of the Onto Refine Project of a GraphDB Instance.
    The API is not officially released as REST API, so changes might occur without notice.
    """

    def __init__(self, base_url, credentials, onto_refine_path='orefine/command/core/'):
        self.base_url = base_url
        self.onto_refine_path = onto_refine_path
        self.onto_refine_base_url = base_url + onto_refine_path
        self.credentials = credentials

    def get_new_csrf_token(self):
        """ Token to be added to most API Requests """

        url = self.onto_refine_base_url + "get-csrf-token"
        payload = ""
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload, auth=self.credentials)
        j = json.loads(response.text)
        return j["token"]

    def get_current_project_ids(self):
        """ Return list of all project IDs."""
        return list(self.get_all_projects_meta_data()["projects"].keys())

    def get_all_projects_meta_data(self, export_as_json=False):
        """ Get all projects Meta-Data (and ids) """

        url = self.onto_refine_base_url + "get-all-project-metadata?csrf_token=" + self.get_new_csrf_token()

        headers = {
            'Accept': 'application/json',
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, auth=self.credentials)

        data = json.loads(response.text)
        if export_as_json:
            with open('tmp/all_open_refine_projects_meta_data.json', 'w') as f:
                json.dump(data, f, indent=4)

        return data

    def create_ontorefine_project(self, project_name, data_file, format_type="text/json", options=None):
        """format can be of (compare: https://docs.openrefine.org/technical-reference/openrefine-api)"""
        # compare https://github.com/paulmakepeace/refine-client-py/blob/master/google/refine/refine.py for options

        current_project_ids = set(self.get_current_project_ids())

        if options is None:
            options = utils.get_options_from_type(format_type)

        multipart_form_data = {
            'project-file': (project_name, open(data_file, 'rb')),
            'project-name': (None, project_name),
            'format': (None, format_type),
            'options': (None, json.dumps(options))
        }

        url = self.onto_refine_base_url + "create-project-from-upload"
        params = {
            'csrf_token': self.get_new_csrf_token()
        }
        requests.request(method="POST", url=url, params=params, files=multipart_form_data, auth=self.credentials)

        created_projects = list(set(self.get_current_project_ids()) - current_project_ids)
        if len(created_projects) > 0:
            return created_projects[0]
        else:
            print("Project could not be created!")
            return None

    def fill_down(self, project_id, column):
        """ Fill Down column with element"""
        url = self.onto_refine_base_url + 'fill-down'

        params = {
            'columnName': column,
            'project': project_id,
            'csrf_token': self.get_new_csrf_token()
        }

        data = {
            "engine": '{"facets": [], "mode": "record-based"}'
        }

        response = requests.request(method='POST', url=url, params=params, data=data, auth=self.credentials)
        print(json.loads(response.text)["historyEntry"]["description"])
        return response

    def apply_rdf_mapping(self, rdf_map_path, project_id, outputpath=None):
        """ Apply mapping to uploaded OntoRefine Project File and convert it to turtle file"""

        url = self.base_url + "rest/rdf-mapper/rdf/ontorefine:{}".format(project_id)
        
        rdf_map = json.loads(Path(rdf_map_path).read_text())

        headers = {
            'Accept': 'text/turtle;charset=UTF-8',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(rdf_map), auth=self.credentials)
        if outputpath:
            with open(outputpath, 'w') as f:
                f.write(response.text)

        return response.text
