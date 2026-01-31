"""Application control commands - cross-platform app launching and focusing."""
import platform
import subprocess
import typer

app = typer.Typer(help="Application control commands")


def _get_platform() -> str:
    """Get the current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"


@app.command()
def open(
    name: str = typer.Argument(..., help="Application name or path to open"),
    args: list[str] = typer.Option(None, "--arg", "-a", help="Arguments to pass to the application"),
):
    """
    Open an application by name or path.
    
    Cross-platform support:
    - Windows: Uses 'start' command
    - macOS: Uses 'open -a' command  
    - Linux: Uses the application name directly or common launchers
    
    Examples:
        desktop-agent app open notepad
        desktop-agent app open "Google Chrome"
        desktop-agent app open /path/to/app
    """
    current_platform = _get_platform()
    args = args or []
    
    try:
        if current_platform == "windows":
            # On Windows, use 'start' command
            # shell=True is needed for 'start' to work
            if args:
                subprocess.Popen(
                    f'start "" "{name}" {" ".join(args)}',
                    shell=True,
                )
            else:
                subprocess.Popen(f'start "" "{name}"', shell=True)
                
        elif current_platform == "macos":
            # On macOS, use 'open -a' for applications
            cmd = ["open", "-a", name]
            if args:
                cmd.extend(["--args"] + args)
            subprocess.Popen(cmd)
            
        else:  # Linux
            # Try common methods to open applications
            cmd = [name] + args
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            
        typer.echo(f"Opened application: {name}")
        
    except FileNotFoundError:
        typer.echo(f"Error: Application '{name}' not found", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error opening application: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def focus(
    name: str = typer.Argument(..., help="Window title or application name to focus"),
):
    """
    Focus on a window by title or application name.
    
    Cross-platform support:
    - Windows: Uses pyautogui to find and focus windows
    - macOS: Uses AppleScript via osascript
    - Linux: Uses wmctrl or xdotool
    
    Examples:
        desktop-agent app focus "Untitled - Notepad"
        desktop-agent app focus "Google Chrome"
        desktop-agent app focus "Visual Studio Code"
    """
    current_platform = _get_platform()
    
    try:
        if current_platform == "windows":
            import pyautogui
            import ctypes
            from ctypes import wintypes
            
            # Find window by title
            user32 = ctypes.windll.user32
            
            # Callback function to enumerate windows
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool,
                wintypes.HWND,
                wintypes.LPARAM
            )
            
            found_hwnd = None
            
            def enum_callback(hwnd, lparam):
                nonlocal found_hwnd
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buffer = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buffer, length + 1)
                        title = buffer.value
                        if name.lower() in title.lower():
                            found_hwnd = hwnd
                            return False  # Stop enumeration
                return True  # Continue enumeration
            
            user32.EnumWindows(EnumWindowsProc(enum_callback), 0)
            
            if found_hwnd:
                # Restore if minimized
                SW_RESTORE = 9
                user32.ShowWindow(found_hwnd, SW_RESTORE)
                # Bring to foreground
                user32.SetForegroundWindow(found_hwnd)
                typer.echo(f"Focused window: {name}")
            else:
                typer.echo(f"Error: Window '{name}' not found", err=True)
                raise typer.Exit(1)
                
        elif current_platform == "macos":
            # Use AppleScript to activate application
            script = f'''
            tell application "{name}"
                activate
            end tell
            '''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                typer.echo(f"Focused application: {name}")
            else:
                typer.echo(f"Error: Could not focus '{name}': {result.stderr}", err=True)
                raise typer.Exit(1)
                
        else:  # Linux
            # Try wmctrl first, then xdotool
            try:
                result = subprocess.run(
                    ["wmctrl", "-a", name],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    typer.echo(f"Focused window: {name}")
                else:
                    raise FileNotFoundError("wmctrl failed")
            except FileNotFoundError:
                # Try xdotool
                result = subprocess.run(
                    ["xdotool", "search", "--name", name, "windowactivate"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    typer.echo(f"Focused window: {name}")
                else:
                    typer.echo(
                        f"Error: Could not focus '{name}'. Install wmctrl or xdotool.",
                        err=True
                    )
                    raise typer.Exit(1)
                    
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error focusing window: {e}", err=True)
            raise typer.Exit(1)
        raise


@app.command()
def list():
    """
    List all visible windows.
    
    Cross-platform support:
    - Windows: Uses Windows API
    - macOS: Uses AppleScript
    - Linux: Uses wmctrl
    """
    current_platform = _get_platform()
    windows = []
    
    try:
        if current_platform == "windows":
            import ctypes
            from ctypes import wintypes
            
            user32 = ctypes.windll.user32
            
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool,
                wintypes.HWND,
                wintypes.LPARAM
            )
            
            def enum_callback(hwnd, lparam):
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buffer = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buffer, length + 1)
                        title = buffer.value
                        if title.strip():
                            windows.append(title)
                return True
            
            user32.EnumWindows(EnumWindowsProc(enum_callback), 0)
            
        elif current_platform == "macos":
            script = '''
            tell application "System Events"
                set windowList to {}
                repeat with proc in (every process whose background only is false)
                    repeat with win in (every window of proc)
                        set end of windowList to (name of proc) & " - " & (name of win)
                    end repeat
                end repeat
                return windowList
            end tell
            '''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                # Parse AppleScript list output
                output = result.stdout.strip()
                if output:
                    windows = [w.strip() for w in output.split(",")]
                    
        else:  # Linux
            result = subprocess.run(
                ["wmctrl", "-l"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        # wmctrl format: <hwnd> <desktop> <hostname> <title>
                        parts = line.split(None, 3)
                        if len(parts) >= 4:
                            windows.append(parts[3])
            else:
                typer.echo("Error: wmctrl not found. Install it with: sudo apt install wmctrl", err=True)
                raise typer.Exit(1)
                
        if windows:
            typer.echo("Visible windows:")
            for i, title in enumerate(windows, 1):
                typer.echo(f"  {i}. {title}")
        else:
            typer.echo("No visible windows found")
            
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error listing windows: {e}", err=True)
            raise typer.Exit(1)
        raise
