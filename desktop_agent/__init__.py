"""Desktop Agent - CLI for controlling mouse, keyboard, and screen using PyAutoGUI."""
import typer
from desktop_agent.commands import mouse, keyboard, screen, message

app = typer.Typer(
    name="desktop-agent",
    help="Control your desktop with mouse, keyboard, and screen automation",
    no_args_is_help=True,
)

# Register sub-applications
app.add_typer(mouse.app, name="mouse")
app.add_typer(keyboard.app, name="keyboard")
app.add_typer(screen.app, name="screen")
app.add_typer(message.app, name="message")


@app.command()
def version():
    """Show version information."""
    typer.echo("desktop-agent v0.1.0")
