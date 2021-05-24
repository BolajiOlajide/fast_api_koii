from collections import namedtuple
from typing import List, Set

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute


KOIIRoutes = List[BaseRoute]
Path = namedtuple("Path", ["path", "method"])


class Koii(object):
    _VALID_METHODS: List[str] = ["GET", "POST", "DELETE", "PUT", "PATCH"]
    _TAB_SIZE: int = 12

    def __init__(self, app: FastAPI) -> None:
        if self._is_app_valid(app):
            paths = self._get_paths(app.routes)
            self._format(paths)
        else:
            raise Exception("FastAPI app isn't valid as it has no predefined routes.")

    def _is_app_valid(self, app: FastAPI) -> bool:
        return (
            app is not None
            and app.routes
            and type(app.routes) == list
            and len(app.routes) > 0
        ) == True

    def _get_paths(self, routes: KOIIRoutes) -> List[Path]:
        paths = []

        for route in routes:
            path = route.path
            for valid_method in self._get_valid_methods(route.methods):
                paths.append(Path(path, valid_method))

        return paths

    def _get_valid_methods(self, methods: Set[str]) -> List[str]:
        return [method for method in methods if method in self._VALID_METHODS]

    def _format(self, paths: List[Path]) -> None:
        method_header_fill = " " * (self._TAB_SIZE - len("METHOD"))
        path_header_fill = " " * (self._TAB_SIZE - len("PATH"))

        print(" ")
        method_header = f"\033[1;35;40mMETHOD {method_header_fill}"
        path_header = f"\033[1;35;40mPATH {path_header_fill}"

        print(f"{method_header} {path_header}")
        print(("-" * self._TAB_SIZE) + " " + ("-" * self._TAB_SIZE))

        for path in paths:
            method_fill_str = " " * (self._TAB_SIZE - len(path.method))

            method_to_print = f"\033[1;32;40m{path.method} {method_fill_str}"
            path_to_print = f"\033[0;37;40m{path.path}"

            print(method_to_print + " " + path_to_print)
        print(" ")

