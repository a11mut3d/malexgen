

from ..legends import LEGENDS, get_legend, list_legends
from ..legends.base import BaseLegend, Legend
from ..utils.logger import logger


class LegendEngine:

    def __init__(self):
        self._legends = LEGENDS

    def get(self, legend_id: str) -> BaseLegend:

        legend = get_legend(legend_id)
        logger.debug(f"Legend loaded: {legend_id}")
        return legend

    def get_data(self, legend_id: str) -> Legend:

        return self.get(legend_id).get_legend()

    def list_ids(self) -> list[str]:

        return list_legends()

    def list_all(self) -> list[Legend]:

        return [self.get_data(lid) for lid in self.list_ids()]

    def exists(self, legend_id: str) -> bool:

        return legend_id in self._legends

    def count(self) -> int:

        return len(self._legends)


__all__ = ["LegendEngine"]
