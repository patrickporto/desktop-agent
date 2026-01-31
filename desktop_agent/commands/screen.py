"""Screen and screenshot commands."""
import typer
import pyautogui
from pathlib import Path
from typing import Optional
import json
import pywinctl

app = typer.Typer(help="Screen and screenshot commands")


def _get_window_region(window_name: Optional[str] = None, active: bool = False) -> Optional[tuple[int, int, int, int]]:
    """Get the region of a specific or active window using PyWinCtl."""
    try:
        if active:
            window = pywinctl.getActiveWindow()
            if not window:
                typer.echo("Error: No active window found", err=True)
                return None
        elif window_name:
            windows = pywinctl.getWindowsWithTitle(window_name)
            if not windows:
                typer.echo(f"Error: Window with title '{window_name}' not found", err=True)
                return None
            window = windows[0]
        else:
            return None

        return (int(window.left), int(window.top), int(window.width), int(window.height))
    except Exception as e:
        typer.echo(f"Error getting window region: {e}", err=True)
        return None


@app.command()
def screenshot(
    filename: str = typer.Argument("screenshot.png", help="Output filename"),
    region: str = typer.Option(None, "--region", "-r", help="Region as 'x,y,width,height'"),
    window: Optional[str] = typer.Option(None, "--window", "-w", help="Target window title"),
    active: bool = typer.Option(False, "--active", "-a", help="Target active window"),
):
    """Take a screenshot of the entire screen, a window, or a specific region."""
    target_region = None

    # Determine region from window targeting
    window_region = _get_window_region(window, active)
    if window_region:
        target_region = window_region
        typer.echo(f"Targeting window region: {target_region}")

    # Manual region override
    if region:
        try:
            target_region = tuple(map(int, region.split(",")))
            typer.echo(f"Using manual region override: {target_region}")
        except ValueError:
            typer.echo("Error: Region must be in format 'x,y,width,height'", err=True)
            raise typer.Exit(1)

    try:
        if target_region:
            img = pyautogui.screenshot(region=target_region)
            img.save(filename)
            typer.echo(f"Screenshot saved to {filename} (region: {target_region})")
        else:
            img = pyautogui.screenshot()
            img.save(filename)
            typer.echo(f"Screenshot saved to {filename}")
    except Exception as e:
        typer.echo(f"Error taking screenshot: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def locate(
    image: str = typer.Argument(..., help="Path to image to locate"),
    confidence: float = typer.Option(0.9, "--confidence", "-c", help="Match confidence (0.0-1.0)"),
    window: Optional[str] = typer.Option(None, "--window", "-w", help="Search within a specific window"),
    active: bool = typer.Option(False, "--active", "-a", help="Search within the active window"),
):
    """Locate an image on the screen or within a targeted window."""
    region = _get_window_region(window, active)
    if region:
        typer.echo(f"Searching within window region: {region}")

    try:
        location = pyautogui.locateOnScreen(image, confidence=confidence, region=region)
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
    window: Optional[str] = typer.Option(None, "--window", "-w", help="Search within a specific window"),
    active: bool = typer.Option(False, "--active", "-a", help="Search within the active window"),
):
    """Get the center coordinates of an image on the screen or within a window."""
    region = _get_window_region(window, active)
    if region:
        typer.echo(f"Searching within window region: {region}")

    try:
        location = pyautogui.locateCenterOnScreen(image, confidence=confidence, region=region)
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
_reader_langs = None


def _get_system_language() -> str:
    """Detect the system language in a cross-platform way.
    
    Returns the ISO 639-1 language code (e.g., 'en', 'pt', 'es').
    Falls back to 'en' if detection fails.
    """
    import locale
    try:
        # Get system locale (works on Windows, Linux, macOS)
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            # Extract language code (e.g., 'pt_BR' -> 'pt', 'en_US' -> 'en')
            lang_code = system_locale.split('_')[0].lower()
            return lang_code
    except Exception:
        pass
    return 'en'


def _get_default_languages() -> list[str]:
    """Get default languages for OCR based on system locale.
    
    Returns a list with the system language and English (if different).
    """
    system_lang = _get_system_language()
    if system_lang == 'en':
        return ['en']
    return [system_lang, 'en']


def get_reader(lang: list[str] = None):
    """Get or create EasyOCR reader instance."""
    global _reader, _reader_langs
    langs = lang or _get_default_languages()
    # Reinitialize if languages changed
    if _reader is None or set(langs) != set(_reader_langs or []):
        import easyocr
        typer.echo(f"Initializing EasyOCR (languages: {', '.join(langs)})...")
        _reader = easyocr.Reader(langs)
        _reader_langs = langs
    return _reader


@app.command(name="locate-text-coordinates")
def locate_text_coordinates(
    search: str = typer.Argument(..., help="Text to search for (partial match)"),
    image: Optional[str] = typer.Option(None, "--image", "-i", help="Path to image (if not provided, takes screenshot)"),
    lang: Optional[str] = typer.Option(None, "--lang", "-l", help="Languages to use (comma-separated, default: system language + en)"),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", "-c", help="Case sensitive search"),
    window: Optional[str] = typer.Option(None, "--window", "-w", help="Search within a specific window"),
    active: bool = typer.Option(False, "--active", "-a", help="Search within the active window"),
):
    """Locate text coordinates on screen, within a window, or in an image using OCR."""
    # Get or take screenshot
    if image:
        if not Path(image).exists():
            typer.echo(f"Error: Image file '{image}' not found", err=True)
            raise typer.Exit(1)
        image_path = image
    else:
        # Check for window targeting
        region = _get_window_region(window, active)
        if region:
            typer.echo(f"Taking screenshot of window region: {region}")

        # Take screenshot
        screenshot_path = "temp_screenshot.png"
        img = pyautogui.screenshot(region=region)
        img.save(screenshot_path)
        image_path = screenshot_path
        typer.echo(f"Screenshot taken: {screenshot_path}")

    # Initialize reader
    languages = lang.split(',') if lang else None
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
    lang: Optional[str] = typer.Option(None, "--lang", "-l", help="Languages to use (comma-separated, default: system language + en)"),
    window: Optional[str] = typer.Option(None, "--window", "-w", help="Read from a specific window"),
    active: bool = typer.Option(False, "--active", "-a", help="Read from the active window"),
):
    """Read all text from screen, a targeted window, or an image using OCR."""
    # Get or take screenshot
    if image:
        if not Path(image).exists():
            typer.echo(f"Error: Image file '{image}' not found", err=True)
            raise typer.Exit(1)
        image_path = image
    else:
        # Check for window targeting
        region = _get_window_region(window, active)
        if region:
            typer.echo(f"Taking screenshot of window region: {region}")

        # Take screenshot
        screenshot_path = "temp_screenshot.png"
        img = pyautogui.screenshot(region=region)
        img.save(screenshot_path)
        image_path = screenshot_path
        typer.echo(f"Screenshot taken: {screenshot_path}")

    # Initialize reader
    languages = lang.split(',') if lang else None
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

