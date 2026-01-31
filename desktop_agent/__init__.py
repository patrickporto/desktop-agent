"""Desktop Agent - CLI for controlling mouse, keyboard, and screen using PyAutoGUI."""
import typer
from desktop_agent.commands import mouse, keyboard, screen, message, app

app_cli = typer.Typer(
    name="desktop-agent",
    help="Control your desktop with mouse, keyboard, and screen automation",
    no_args_is_help=True,
)

# Register sub-applications
app_cli.add_typer(mouse.app, name="mouse")
app_cli.add_typer(keyboard.app, name="keyboard")
app_cli.add_typer(screen.app, name="screen")
app_cli.add_typer(message.app, name="message")
app_cli.add_typer(app.app, name="app")


@app_cli.command()
def version():
    """Show version information."""
    typer.echo("desktop-agent v1.1.0")

