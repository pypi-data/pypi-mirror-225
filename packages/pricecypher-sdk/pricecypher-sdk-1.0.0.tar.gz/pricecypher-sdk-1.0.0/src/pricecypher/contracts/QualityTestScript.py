from abc import ABC, abstractmethod
from typing import Optional, Any

from pricecypher.contracts import Script, TestSuite


class QualityTestScript(Script, ABC):
    """
    The abstract QualityTestScript class serves as an interaction contract such that by extending it with its
        methods implemented, a script can be created that performs data quality tests on a dataset, which can then be
        used in a generalized yet controlled setting.
    """

    def execute(self, business_cell_id: Optional[int], bearer_token: str, user_input: dict[Any: Any]) -> Any:
        return self.execute_tests(business_cell_id, bearer_token)

    @abstractmethod
    def execute_tests(self, business_cell_id: Optional[int], bearer_token: str) -> TestSuite:
        """
        Execute the script to calculate the values of some scope for the given transactions.

        :param business_cell_id: Business cell to execute the script for, or None if running the script for all.
        :param bearer_token: Bearer token to use for additional requests.
        :return: List of all test results that were performed by the test script.
        """
        raise NotImplementedError
