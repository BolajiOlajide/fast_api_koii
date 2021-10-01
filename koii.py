from typing import List, NamedTuple, Set

from colorama import Fore
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute, Route


KOIIRoutes = List[BaseRoute]


class Path(NamedTuple):
    path: str
    method: str


class Koii(object):
    _VALID_METHODS: Set[str] = frozenset(["GET", "POST", "DELETE", "PUT", "PATCH"])
    _TAB_SIZE: int = 12

    def __init__(self, app: FastAPI) -> None:
        if self._is_app_valid(app):
            paths = self._get_paths(app.routes)
            self._format(paths)
        else:
            raise Exception("FastAPI app isn't valid as it has no predefined routes.")

    @staticmethod
    def _is_app_valid(app: FastAPI) -> bool:
        for route in app.routes:
            if isinstance(route, (APIRoute, Route)):
                # valid for defined FastApi and predefined starlette routes (docs routes)
                return True

    def _get_paths(self, routes: KOIIRoutes) -> List[Path]:
        paths = []

        for route in routes:
            for valid_method in self._get_valid_methods(route.methods):
                paths.append(Path(route.path, valid_method))

        return paths

    def _get_valid_methods(self, methods: Set[str]) -> List[str]:
        return [method for method in methods if method in self._VALID_METHODS]

    def _format(self, paths: List[Path]) -> None:
        method_header_fill = " " * (self._TAB_SIZE - len("METHOD"))
        path_header_fill = " " * (self._TAB_SIZE - len("PATH"))

        print(" ")
        method_header = f"{Fore.LIGHTMAGENTA_EX} METHOD {method_header_fill}"
        path_header = f"{Fore.LIGHTMAGENTA_EX}PATH {path_header_fill}"

        print(f"{method_header} {path_header}")
        print(("-" * self._TAB_SIZE) + " " + ("-" * self._TAB_SIZE))

        for path in paths:
            method_fill_str = " " * (self._TAB_SIZE - len(path.method) - 2)

            method_to_print = f"{Fore.GREEN} {path.method} {method_fill_str}"
            path_to_print = f"{Fore.CYAN} {path.path}"

            print(method_to_print + " " + path_to_print)
        print(" ")
