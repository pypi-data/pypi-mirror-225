from abc import ABC, abstractmethod
from typing import Any, Optional, Annotated


class Script(ABC):
    """
    The abstract Script class serves as an interaction contract such that by extending it with its methods implemented,
        a script can be created that can be used in a generalized yet controlled setting.
    """

    dataset_id: Annotated[int, "The dataset ID"]
    settings: dict[str, Any]
    config: dict[str, dict[str, Any]]

    def __init__(self, dataset_id: int, settings: dict[str, Any], config: dict[str, dict[str, Any]]):
        self.dataset_id = dataset_id
        self.settings = settings
        self.config = config

    @abstractmethod
    def get_config_dependencies(self) -> dict[str, list[str]]:
        """
        Fetch the configuration sections and keys in the sections that the script will use that are not yet provided.

        NB: It is not needed to return all required sections and keys, only at least one that has not been provided yet.
        If all required config is provided, an empty dictionary is to be returned.

        :return: dictionary mapping from section key (string) to a (potentially empty) list of keys of that section
            that the script requires additionally.
        """
        raise NotImplementedError

    @abstractmethod
    def get_scope_dependencies(self) -> list[dict[str, Any]]:
        """
        Fetch the scopes that the script will use and requires to be present in the dataset.

        NB: All required config is assumed to be present.

        :return: List of required scopes, where each is a dictionary containing either
            a 'representation' or a 'scope_id'.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, business_cell_id: Optional[int], bearer_token: str, user_input: dict[Any: Any]) -> Any:
        """
        Execute the script

        NB: All required config and scopes are assumed to be present.

        :param business_cell_id: Business cell to execute the script for, or None if running the script for all.
        :param bearer_token: Bearer token to use for additional requests.
        :param user_input: Dictionary of additional json-serializable input provided by the caller of the script.
        :return: Any json-serializable results the script outputs.
        """
        raise NotImplementedError
