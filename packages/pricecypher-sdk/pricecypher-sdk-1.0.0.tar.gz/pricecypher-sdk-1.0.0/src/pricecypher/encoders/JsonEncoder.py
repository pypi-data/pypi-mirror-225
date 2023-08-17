import dataclasses
import numpy as np

from json import JSONEncoder


class PriceCypherJsonEncoder(JSONEncoder):
    """
    JSON encoder that can properly serialize dataclasses and numpy numbers.
    """
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()

        return super().default(obj)
