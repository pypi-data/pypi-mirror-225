# from process_bigraph.type_system import types  #ProcessTypes
import pprint

pretty = pprint.PrettyPrinter(indent=2)


def pp(x) -> None:
    """Print ``x`` in a pretty format."""
    pretty.pprint(x)


# types = ProcessTypes()   # TODO -- how will Composite know these types?
# types.type_registry.register_multiple(sed_types)
