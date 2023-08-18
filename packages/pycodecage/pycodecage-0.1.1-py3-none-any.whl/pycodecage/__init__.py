import warnings

from pycodecage.environment import TrustedEnvironment
from pycodecage.factories import BuiltinsFactory, FileFactory
from pycodecage.test_case import TestCase
from pycodecage.utils import run_tests

__version__ = "0.0.1"
warnings.filterwarnings("ignore", category=SyntaxWarning)
