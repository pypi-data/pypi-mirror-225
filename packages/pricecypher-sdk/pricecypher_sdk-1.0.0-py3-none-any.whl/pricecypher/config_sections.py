from pricecypher.endpoints import ConfigEndpoint
from pricecypher.models import ConfigSection
from pricecypher.rest import RestClient


class ConfigSections(object):
    """
    Config API. Exposes all available operations on dataset configs, like fetching the available sections, and
    retrieving the key-value pairs of a section and parsing it to a dictionary.

    :param str bearer_token: Bearer token for PriceCypher (logical) API. Needs 'read:configuration' scope.
    :param int dataset_id: Dataset that is queried by these config operations.
    :param str config_base: (optional) Base URL for PriceCypher config service API.
        (defaults to the static default_config_base, which by default is https://config.pricecypher.com)
    :param RestClientOptions rest_options: (optional) Set any additional options for the REST client, e.g. rate-limit.
        (defaults to None)
    """

    """ Default user-tool base URL """
    default_config_base = 'https://config.pricecypher.com'

    def __init__(self, bearer_token, dataset_id, config_base=None, rest_options=None):
        self._bearer = bearer_token
        self._dataset_id = dataset_id
        self._config_base = config_base if config_base is not None else self.default_config_base
        self._rest_options = rest_options
        self._client = RestClient(jwt=bearer_token, options=rest_options)

    def index(self) -> list[ConfigSection]:
        """
        List all available config sections for the dataset.

        :return: list of config sections.
        :rtype list[ConfigSection]
        """
        return ConfigEndpoint(self._client, self._dataset_id, self._config_base).sections().index()

    def get_parsed_section(self, section_key) -> dict:
        """
        Retrieves the config section by the given key, and parses the contained key-value pairs into a single dict.

        :return: Dictionary of all key-value pairs in the given section, or an empty dict if no such section exists.
        :rtype: dict Mapping config keys (str) to config values (any).
        """
        section = ConfigEndpoint(self._client, self._dataset_id, self._config_base).sections().get(section_key)

        if section is None:
            return {}

        return {
            key_value.key: key_value.value
            for key_value in section.keys
        }
