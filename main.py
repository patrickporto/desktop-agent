import typer

app = typer.Typer()

@app.command()
def main():
    print("Hello from desktop-skill!")


if __name__ == "__main__":
    app()
