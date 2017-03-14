
import json

from keen.api import KeenApi, HTTPMethods
from keen import exceptions, utilities

class SavedQueriesInterface:

    def __init__(self, api):
        self.api = api
        self.saved_query_url = "{0}/{1}/projects/{2}/queries/saved".format(
            self.api.base_url, self.api.api_version, self.api.project_id
        )

    def all(self):
        """
        Gets all saved queries for a project from the Keen IO API.
        Master key must be set.
        """
        self._check_for_master_key()

        response = self._get_json(HTTPMethods.GET, self.saved_query_url, self.api.master_key)

        return response

    def get(self, query_name):
        """
        Gets a single saved query for a project from the Keen IO API given a
        query name.
        Master key must be set.
        """
        self._check_for_master_key()

        url = "{0}/{1}".format(self.saved_query_url, query_name)
        response = self._get_json(HTTPMethods.GET, url, self.api.master_key)

        return response

    def results(self, query_name):
        """
        Gets a single saved query with a 'result' object for a project from the
        Keen IO API given a query name.
        Read or Master key must be set.
        """
        self._check_for_master_or_read_key()

        url = "{0}/{1}/result".format(self.saved_query_url, query_name)
        key = self.api.master_key if self.api.master_key else self.api.read_key
        response = self._get_json(HTTPMethods.GET, url, key)

        return response

    def create(self, query_name, saved_query):
        """
        Creates the saved query via a PUT request to Keen IO Saved Query endpoint.
        Master key must be set.
        """
        self._check_for_master_key()

        url = "{0}/{1}".format(self.saved_query_url, query_name)
        payload = json.dumps(saved_query)
        response = self._get_json(HTTPMethods.PUT, url, self.api.master_key, data=payload)

        return response

    def update(self, query_name, saved_query):
        """
        Updates the saved query via a PUT request to Keen IO Saved Query
        endpoint.
        Master key must be set.
        """
        return self.create(query_name, saved_query)

    def delete(self, query_name):
        """
        Deletes a saved query from a project with a query name.
        Master key must be set.
        """
        self._check_for_master_key()

        url = "{0}/{1}".format(self.saved_query_url, query_name)
        response = self._get_json(HTTPMethods.DELETE, url, self.api.master_key)

        return True

    def _get_json(self, http_method, url, key, *args, **kwargs):
        response = self.api.fulfill(http_method, url, headers=utilities.headers(key), *args, **kwargs)
        self.api._error_handling(response)

        return response.json()

    def _check_for_master_key(self):
        if not self.api.master_key:
            raise exceptions.InvalidEnvironmentError(
                "The Keen IO API requires a master key to perform this operation on saved queries. "
                "Please set a 'master_key' when initializing the "
                "KeenApi object."
            )

    def _check_for_master_or_read_key(self):
        if not (self.api.read_key or self.api.master_key):
            raise exceptions.InvalidEnvironmentError(
                "The Keen IO API requires a read key or master key to perform this operation on saved queries. "
                "Please set a 'read_key' or 'master_key' when initializing the "
                "KeenApi object."
            )
