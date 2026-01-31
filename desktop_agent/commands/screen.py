"""Screen and screenshot commands."""
import typer
import pyautogui
from pathlib import Path
from typing import Optional
import json

app = typer.Typer(help="Screen and screenshot commands")


@app.command()
def screenshot(
    filename: str = typer.Argument("screenshot.png", help="Output filename"),
    region: str = typer.Option(None, "--region", "-r", help="Region as 'x,y,width,height'"),
):
    """Take a screenshot of the entire screen or a region."""
    if region:
        try:
            x, y, width, height = map(int, region.split(","))
            img = pyautogui.screenshot(region=(x, y, width, height))
            img.save(filename)
            typer.echo(f"Screenshot saved to {filename} (region: {region})")
        except ValueError:
            typer.echo("Error: Region must be in format 'x,y,width,height'", err=True)
            raise typer.Exit(1)
    else:
        img = pyautogui.screenshot()
        img.save(filename)
        typer.echo(f"Screenshot saved to {filename}")


@app.command()
def locate(
    image: str = typer.Argument(..., help="Path to image to locate"),
    confidence: float = typer.Option(0.9, "--confidence", "-c", help="Match confidence (0.0-1.0)"),
):
    """Locate an image on the screen."""
    try:
        location = pyautogui.locateOnScreen(image, confidence=confidence)
        if location:
            typer.echo(f"Found at: x={location.left}, y={location.top}, width={location.width}, height={location.height}")
        else:
            typer.echo("Image not found on screen")
    except pyautogui.ImageNotFoundException:
        typer.echo("Image not found on screen")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def locate_center(
    image: str = typer.Argument(..., help="Path to image to locate"),
    confidence: float = typer.Option(0.9, "--confidence", "-c", help="Match confidence (0.0-1.0)"),
):
    """Get the center coordinates of an image on the screen."""
    try:
        location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        if location:
            typer.echo(f"Center at: ({location.x}, {location.y})")
        else:
            typer.echo("Image not found on screen")
    except pyautogui.ImageNotFoundException:
        typer.echo("Image not found on screen")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def pixel(
    x: int = typer.Argument(..., help="X coordinate"),
    y: int = typer.Argument(..., help="Y coordinate"),
):
    """Get the RGB color of a pixel at specified coordinates."""
    color = pyautogui.pixel(x, y)
    typer.echo(f"Pixel at ({x}, {y}): RGB{color}")


@app.command()
def size():
    """Get the screen size."""
    screen_size = pyautogui.size()
    typer.echo(f"Screen size: {screen_size.width}x{screen_size.height}")


@app.command()
def on_screen(
    x: int = typer.Argument(..., help="X coordinate"),
    y: int = typer.Argument(..., help="Y coordinate"),
):
    """Check if coordinates are on the screen."""
    is_on_screen = pyautogui.onScreen(x, y)
    if is_on_screen:
        typer.echo(f"({x}, {y}) is on screen")
    else:
        typer.echo(f"({x}, {y}) is NOT on screen")


# OCR functionality
_reader = None


def get_reader(lang: list[str] = None):
    """Get or create EasyOCR reader instance."""
    global _reader
    if _reader is None:
        import easyocr
        langs = lang or ['pt', 'en']
        typer.echo(f"Initializing EasyOCR (languages: {', '.join(langs)})...")
        _reader = easyocr.Reader(langs)
    return _reader


@app.command(name="locate-text-coordinates")
def locate_text_coordinates(
    search: str = typer.Argument(..., help="Text to search for (partial match)"),
    image: Optional[str] = typer.Option(None, "--image", "-i", help="Path to image (if not provided, takes screenshot)"),
    lang: str = typer.Option("pt,en", "--lang", "-l", help="Languages to use (comma-separated)"),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", "-c", help="Case sensitive search"),
):
    """Locate text coordinates on screen or in image using OCR. Searches for partial text matches."""
    # Get or take screenshot
    if image:
        if not Path(image).exists():
            typer.echo(f"Error: Image file '{image}' not found", err=True)
            raise typer.Exit(1)
        image_path = image
    else:
        # Take screenshot
        screenshot_path = "temp_screenshot.png"
        img = pyautogui.screenshot()
        img.save(screenshot_path)
        image_path = screenshot_path
        typer.echo(f"Screenshot taken: {screenshot_path}")

    # Initialize reader
    languages = lang.split(',')
    reader = get_reader(languages)

    # Perform OCR
    typer.echo("Performing OCR...")
    results = reader.readtext(image_path)

    # Search for text
    search_text = search if case_sensitive else search.lower()
    matches = []

    for (bbox, text, confidence) in results:
        compare_text = text if case_sensitive else text.lower()
        if search_text in compare_text:
            # bbox is [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            top_left = bbox[0]
            bottom_right = bbox[2]
            
            x1, y1 = int(top_left[0]), int(top_left[1])
            x2, y2 = int(bottom_right[0]), int(bottom_right[1])
            width = x2 - x1
            height = y2 - y1
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            
            match = {
                "text": text,
                "confidence": float(confidence),
                "bbox": {
                    "x": x1,
                    "y": y1,
                    "width": width,
                    "height": height
                },
                "center": {
                    "x": center_x,
                    "y": center_y
                }
            }
            matches.append(match)

    # Output results
    typer.echo(json.dumps(matches, indent=2))
    # Cleanup temp screenshot
    if not image and Path(screenshot_path).exists():
        Path(screenshot_path).unlink()


@app.command(name="read-all-text")
def read_all_text(
    image: Optional[str] = typer.Option(None, "--image", "-i", help="Path to image (if not provided, takes screenshot)"),
    lang: str = typer.Option("pt,en", "--lang", "-l", help="Languages to use (comma-separated)"),
):
    """Read all text from screen or image using OCR. Returns all detected text with their coordinates."""
    # Get or take screenshot
    if image:
        if not Path(image).exists():
            typer.echo(f"Error: Image file '{image}' not found", err=True)
            raise typer.Exit(1)
        image_path = image
    else:
        # Take screenshot
        screenshot_path = "temp_screenshot.png"
        img = pyautogui.screenshot()
        img.save(screenshot_path)
        image_path = screenshot_path
        typer.echo(f"Screenshot taken: {screenshot_path}")

    # Initialize reader
    languages = lang.split(',')
    reader = get_reader(languages)

    # Perform OCR
    typer.echo("Performing OCR...")
    results = reader.readtext(image_path)

    # Format results
    all_text = []
    for (bbox, text, confidence) in results:
        top_left = bbox[0]
        bottom_right = bbox[2]
        
        x1, y1 = int(top_left[0]), int(top_left[1])
        x2, y2 = int(bottom_right[0]), int(bottom_right[1])
        width = x2 - x1
        height = y2 - y1
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        
        item = {
            "text": text,
            "confidence": float(confidence),
            "bbox": {
                "x": x1,
                "y": y1,
                "width": width,
                "height": height
            },
            "center": {
                "x": center_x,
                "y": center_y
            }
        }
        all_text.append(item)

    # Output results
    typer.echo(json.dumps(all_text, indent=2))

    # Cleanup temp screenshot
    if not image and Path(screenshot_path).exists():
        Path(screenshot_path).unlink()

