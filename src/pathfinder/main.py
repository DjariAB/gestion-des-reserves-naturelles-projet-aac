import time
from typing import Callable

from .search.dijkstras import DijkstrasSearch
from .search.bellman_ford import BellmanFordSearch
from .models.grid import Grid
from .models.solution import Solution
from .models.search_types import Search
from .models.search_types import Search

SearchFunction = Callable[[Grid], Solution]

SEARCH: dict[Search, SearchFunction] = {
    Search.DIJKSTRAS_SEARCH: DijkstrasSearch.search,
    Search.BELLMAN_FORD: BellmanFordSearch.search,
}


class PathFinder:
    @staticmethod
    def find_path(
        grid: Grid,
        search: Search,
    ) -> Solution:
        start_time = time.perf_counter()
        solution = SEARCH[search](grid)
        time_taken = (time.perf_counter() - start_time) * 1000
        solution.time = time_taken

        return solution
