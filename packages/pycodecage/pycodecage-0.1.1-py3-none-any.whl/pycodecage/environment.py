from typing import List, Tuple

from RestrictedPython import compile_restricted

from pycodecage.factories import BuiltinsFactory, InputFactory, PrintFactory


class TrustedEnvironment:
    def __init__(self, code: str, builtins: BuiltinsFactory = None) -> None:
        self.code = code
        self._builtins = builtins
        if self._builtins is None:
            self._builtins = BuiltinsFactory()
        self.print_collector = None
        self.input_factory = None
        self.byte_code = None

    def compile(self) -> None:
        self.byte_code = compile_restricted(
            self.code,
            filename="<string>",
            mode="exec",
        )

    def run(self, inputs: Tuple[str]) -> None:
        if self.byte_code is None:
            self.compile()
        self.print_collector = PrintFactory()
        self.input_factory = InputFactory(inputs)
        self._builtins.update("_print_", self.print_collector)
        self._builtins.update("input", self.input_factory)
        exec(self.byte_code, {"__builtins__": self._builtins.asdict()}, None)

    def get_output(self) -> Tuple[List[str], int]:
        return self.print_collector.output, len(self.input_factory)
