from types import ModuleType
from typing import Any, Callable, Dict, Tuple, Union

from RestrictedPython import safe_builtins

from pycodecage.exceptions import ExtraInputError
from pycodecage.utils import FileMock, _import


class InputFactory:
    def __init__(self, params: Tuple[str] = None) -> None:
        if params is None:
            params = []
        self.params = params
        self.len = len(params)
        self.curr = 0

    def __call__(self, *args, **kwargs) -> str:
        if self.curr >= self.len:
            raise ExtraInputError("Extra input")
        self.curr += 1
        return self.params[self.curr - 1]

    def __len__(self) -> int:
        return self.len - self.curr


class PrintFactory:
    def __new__(cls, *args, **kwargs) -> object:
        class PrintCollector:
            output = []

            def __init__(self, _getattr_: Callable = None) -> None:
                self._getattr_ = _getattr_

            def write(self, text: str) -> None:
                if text == "\n":
                    return
                PrintCollector.output.append(text)

            def __call__(self) -> str:
                return "".join(PrintCollector.output)

            def _call_print(self, *objects, **kwargs) -> None:
                if kwargs.get("file", None) is None:
                    kwargs["file"] = self
                else:
                    self._getattr_(kwargs["file"], "write")

                print(*objects, **kwargs)

        return PrintCollector


class BuiltinsFactory:
    def __init__(self, modules: list = None) -> None:
        self._builtins = dict(safe_builtins)
        if modules is not None:
            self._builtins.update({module.__name__: module for module in modules})
        self._builtins["__import__"] = _import

    def asdict(self) -> Dict[str, Any]:
        return self._builtins

    def update(self, module_name: str, module: Union[ModuleType, object]) -> None:
        self._builtins[module_name] = module


class FileFactory:
    def __new__(cls, files: Dict[str, str] = None) -> object:
        class FileMockItem(FileMock):
            _files = files

        return FileMockItem
