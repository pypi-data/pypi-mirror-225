import pytest
from finesse.script.compiler import KatCompiler
from finesse.script.spec import KatSpec
from finesse.script.adapter import ItemAdapter, ElementFactory, ElementSetter
from finesse.components.general import Connector
from finesse.components.node import NodeDirection, NodeType


def _resolve(value):
    if isinstance(value, list):
        for index, item in enumerate(value):
            value[index] = _resolve(item)
    else:
        try:
            value = value.eval()
        except AttributeError:
            pass

    return value


# Fixture for fuzzing tests. Hypothesis requires package scoped fixtures. Registers a
# special component that accepts a single argument of any type, which can be used to
# test parsing KatScript to Python objects.
@pytest.fixture(scope="package")
def fuzz_argument():
    class FuzzElement(Connector):
        """A fake element for fuzzing."""

        def __init__(self, name, value):
            super().__init__(name)
            self.value = value

            # Add some ports (required by the parent class).
            self._add_port("p1", NodeType.OPTICAL)
            self.p1._add_node("i", NodeDirection.INPUT)
            self.p1._add_node("o", NodeDirection.OUTPUT)

            self._add_port("p2", NodeType.OPTICAL)
            self.p2._add_node("i", NodeDirection.INPUT)
            self.p2._add_node("o", NodeDirection.OUTPUT)

    # Note: this breaks the "rule" not to modify the default KatSpec in the
    # /tests/script/katscript tree, but it's the simplest way to test parsing of
    # arbitrary arguments.
    spec = KatSpec()

    # Register fuzz element.
    spec.register_element(
        ItemAdapter(
            full_name="fuzz",
            factory=ElementFactory(item_type=FuzzElement),
            setter=ElementSetter(item_type=FuzzElement),
        )
    )

    compiler = KatCompiler(spec=spec)

    def _(argument_script):
        model = compiler.compile(f"fuzz el1 {argument_script}")
        value = model.el1.value

        return _resolve(value)

    return _
