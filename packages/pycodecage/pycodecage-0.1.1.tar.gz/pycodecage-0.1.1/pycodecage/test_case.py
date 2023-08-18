from typing import List

from pycodecage.environment import TrustedEnvironment


class TestCase:
    def __init__(
        self,
        name: str,
        inputs: List[any],
        expected_results: List[str],
    ) -> None:
        self.name = name
        self.inputs = tuple(map(str, inputs))
        self.expected_results = expected_results

    def run(self, environment: TrustedEnvironment) -> None:
        environment.run(self.inputs)
        self.check_result(*environment.get_output())

    def check_result(self, output: List[str], inputs_left: int) -> None:
        output_is_correct = output == self.expected_results
        no_inputs_left = inputs_left == 0
        result = "OK" if output_is_correct and no_inputs_left else "FAIL"
        print(f"{self.name}: {result}")
        if not output_is_correct:
            print(f"Expected: {self.expected_results}")
            print(f"Got: {output}")
        if not no_inputs_left:
            print(f"User isn'n used all inputs. Inputs left: {inputs_left}")
        print("=" * 20)
