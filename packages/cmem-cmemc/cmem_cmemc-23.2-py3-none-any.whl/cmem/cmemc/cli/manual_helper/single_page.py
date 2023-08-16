"""Generate a single page documentation Markdown."""
from click import Command, Group


def print_manual(ctx):
    """Output the complete manual.

    Returns: None
    """
    print("""# Command Reference

This section lists the help texts of all commands as a reference
and to search for it.
""")
    print_group_manual_recursive(ctx.command, ctx=ctx)


def print_group_manual_recursive(command_group, ctx=None, prefix=""):
    """Output the help text of a command group (recursive)."""
    commands = command_group.commands
    for key in commands:
        command = commands[key]
        formatter = ctx.make_formatter()
        if isinstance(command, Group):
            print(f"## Command group: {prefix}{key}\n")
            print("```")
            command.format_help(ctx, formatter)
            print(formatter.getvalue().rstrip("\n"))
            print("```\n")

            print_group_manual_recursive(
                command,
                ctx=ctx,
                prefix=f"{prefix}{key} "
            )
        elif isinstance(command, Command):
            print(f"### Command: {prefix}{key}\n")
            print("```text")
            command.format_help(ctx, formatter)
            print(formatter.getvalue().rstrip("\n"))
            print("```\n")
        else:
            pass
