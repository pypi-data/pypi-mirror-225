from typing import Optional

from pricecypher.endpoints.base_endpoint import BaseEndpoint
from pricecypher.exceptions import PriceCypherError
from pricecypher.models import ConfigSection, ConfigSectionWithKeys


class ConfigEndpoint(BaseEndpoint):
    """PriceCypher config service endpoints.

    :param RestClient client: HTTP client for making API requests.
    :param int dataset_id: Dataset ID.
    :param str config_base: (optional) Base URL for PriceCypher config service API.
        (defaults to https://config.pricecypher.com)
    """

    def __init__(self, client, dataset_id, config_base='https://config.pricecypher.com'):
        self.base_url = config_base
        self.client = client
        self.dataset_id = dataset_id

    def sections(self):
        """
        Sections endpoints in config service API.
        :rtype: SectionsEndpoint
        """
        return SectionsEndpoint(self.client, self._url(['api/datasets', self.dataset_id, '/config/sections']))


class SectionsEndpoint(BaseEndpoint):
    """
    PriceCypher sections endpoints in config service API.
    """
    def __init__(self, client, base):
        self.client = client
        self.base_url = base

    def index(self) -> list[ConfigSection]:
        """List all available config sections for the dataset.

        :return: list of config sections.
        :rtype list[ConfigSection]
        """
        return self.client.get(self._url(), schema=ConfigSection.Schema(many=True))

    def get(self, section_key) -> Optional[ConfigSectionWithKeys]:
        """ Retrieve the config section, with its contained key-value pairs, using the given section key.

        :param str section_key: Key of the section to retrieve.
        :return: The requested config section with its contained key-value pairs, or `None` if no such section exists.
        :rtype Optional[ConfigSectionWithKeys]
        """
        try:
            return self.client.get(self._url(section_key), schema=ConfigSectionWithKeys.Schema(many=False))
        except PriceCypherError as e:
            if e.status_code == 404:
                return None
            else:
                raise e
