"""Generate a help text and command structure graph."""
from click import Command, Group


def print_manual_graph(ctx, version):
    """Output the complete manual graph.

    Returns: None
    """
    comment = "This dataset represents the complete inline documentation " \
              "of cmemc as a graph"
    print(f"""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix void: <http://rdfs.org/ns/void#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#>.
@prefix cli: <https://vocabs.eccenca.com/cli/>.
@prefix s: <http://schema.org/>.
@prefix : <https://cmemc.eccenca.dev/>.
@prefix i: <https://eccenca.com/go/cmemc>.

: a void:Dataset ;
    owl:versionInfo "{version}" ;
    rdfs:label "cmemc: Documentation Graph" ;
    rdfs:comment "{comment}" .

i: a s:SoftwareApplication ;
    rdfs:label "cmemc" ;
    s:softwareVersion "{version}" .
""")
    print_group_manual_graph_recursive(ctx.command, ctx=ctx)


def print_group_manual_graph_recursive(command_group, ctx=None, prefix=""):
    """Output documentation graph (recursive)."""
    commands = command_group.commands
    for key in commands:
        item = commands[key]
        iri = f":{prefix}{key}"
        print(f"{iri} skos:notation '{key}' .")
        if isinstance(item, Group):
            comment = item.get_short_help_str(limit=200)
            sub_group_iri = f":{prefix[:-1]}"
            if sub_group_iri == ":":
                sub_group_iri = "<https://eccenca.com/go/cmemc>"
            print(f"{iri} a cli:CommandGroup .")
            print(f"{iri} rdfs:label '{prefix}{key} Command Group' .")
            print(f"{iri} cli:subGroupOf {sub_group_iri} .")
            print(f"{iri} rdfs:comment '{comment}' .")
            print_group_manual_graph_recursive(
                item,
                ctx=ctx,
                prefix=f"{prefix}{key}-"
            )
        elif isinstance(item, Command):
            comment = item.get_short_help_str(limit=200)
            group_iri = f":{prefix[:-1]}"
            print(f"{iri} a cli:Command .")
            print(f"{iri} rdfs:label '{prefix}{key} Command' .")
            print(f"{iri} cli:group {group_iri} .")
            print(f"{iri} rdfs:comment '{comment}' .")
            for parameter in item.params:
                print_parameter_manual_graph(
                    parameter,
                    prefix=f"{prefix}{key}-"
                )
        else:
            pass


def print_parameter_manual_graph(item, prefix=""):
    """Output documentation graph for parameter."""
    iri = f":{prefix}{item.name}"
    print(f"{iri} a cli:Parameter .")
    print(f"{iri} cli:command :{prefix[:-1]}.")
    if len(item.opts) == 1:
        print(f"{iri} rdfs:label '{item.opts[0]}'.")
    else:
        print(f'{iri} rdfs:label """{max(item.opts, key=len)}""".')
        print(f'{iri} cli:shortenedOption """{min(item.opts, key=len)}""".')
    if item.default not in (None, False, [None, None]):
        print(f"{iri} cli:defaultValue '{item.default}'.")
    try:
        print(f'{iri} rdfs:comment """{item.help}""".')
    except AttributeError:
        pass
