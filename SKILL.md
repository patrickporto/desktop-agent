---
name: Desktop Control
description: Control mouse, keyboard, and screen for desktop automation tasks
---

# Desktop Control Skill

This skill provides comprehensive desktop automation capabilities through PyAutoGUI, allowing AI agents to control the mouse, keyboard, take screenshots, and interact with the desktop environment.

## How to Use This Skill

As an AI agent, you can invoke desktop automation commands using the `uvx desktop-agent` CLI.

### Command Structure

All commands follow this pattern:

```bash
uvx desktop-agent <category> <command> [arguments] [options]
```

**Categories:**
- `mouse` - Mouse control
- `keyboard` - Keyboard input
- `screen` - Screenshots and screen analysis
- `message` - User dialogs
- `app` - Application control (open, focus, list windows)

## Available Commands

### 🖱️ Mouse Control (`mouse`)

Control cursor movement and clicks.

```bash
# Move cursor to coordinates
uvx desktop-agent mouse move <x> <y> [--duration SECONDS]

# Click at current position or specific coordinates
uvx desktop-agent mouse click [x] [y] [--button left|right|middle] [--clicks N]

# Specialized clicks
uvx desktop-agent mouse double-click [x] [y]
uvx desktop-agent mouse right-click [x] [y]
uvx desktop-agent mouse middle-click [x] [y]

# Drag to coordinates
uvx desktop-agent mouse drag <x> <y> [--duration SECONDS] [--button BUTTON]

# Scroll (positive=up, negative=down)
uvx desktop-agent mouse scroll <clicks> [x] [y]

# Get current mouse position
uvx desktop-agent mouse position
```

**Examples:**
```bash
# Move to center of 1920x1080 screen
uvx desktop-agent mouse move 960 540 --duration 0.5

# Right-click at specific location
uvx desktop-agent mouse right-click 500 300

# Scroll down 5 clicks
uvx desktop-agent mouse scroll -5
```

### ⌨️ Keyboard Control (`keyboard`)

Type text and execute keyboard shortcuts.

```bash
# Type text
uvx desktop-agent keyboard write "<text>" [--interval SECONDS]

# Press keys
uvx desktop-agent keyboard press <key> [--presses N] [--interval SECONDS]

# Execute hotkey combination (comma-separated)
uvx desktop-agent keyboard hotkey "<key1>,<key2>,..."

# Hold/release keys
uvx desktop-agent keyboard keydown <key>
uvx desktop-agent keyboard keyup <key>
```

**Examples:**
```bash
# Type text with natural delay
uvx desktop-agent keyboard write "Hello World" --interval 0.05

# Copy selected text
uvx desktop-agent keyboard hotkey "ctrl,c"

# Open Task Manager
uvx desktop-agent keyboard hotkey "ctrl,shift,esc"

# Press Enter 3 times
uvx desktop-agent keyboard press enter --presses 3
```

**Common Key Names:**
- Modifiers: `ctrl`, `shift`, `alt`, `win`
- Special: `enter`, `tab`, `esc`, `space`, `backspace`, `delete`
- Function: `f1` through `f12`
- Arrows: `up`, `down`, `left`, `right`

### 🖼️ Screen & Screenshots (`screen`)

Capture screenshots and analyze screen content. Supports targeting specific windows.

```bash
# Take screenshot
uvx desktop-agent screen screenshot <filename> [--region "x,y,width,height"] [--window <title>] [--active]

# Locate image on screen or within window
uvx desktop-agent screen locate <image_path> [--confidence 0.0-1.0] [--window <title>] [--active]
uvx desktop-agent screen locate-center <image_path> [--confidence 0.0-1.0] [--window <title>] [--active]

# Locate text using OCR within window
uvx desktop-agent screen locate-text-coordinates <text> [--window <title>] [--active]
uvx desktop-agent screen read-all-text [--window <title>] [--active]

# Utility commands
uvx desktop-agent screen pixel <x> <y>
uvx desktop-agent screen size
uvx desktop-agent screen on-screen <x> <y>
```

**Examples:**
```bash
# Screenshot of active window
uvx desktop-agent screen screenshot active.png --active

# Screenshot of a specific application
uvx desktop-agent screen screenshot chrome.png --window "Google Chrome"

# Locate image within Notepad
uvx desktop-agent screen locate-center button.png --window "Notepad"
```

### 💬 Message Dialogs (`message`)

Display user interaction dialogs.

```bash
# Show alert
uvx desktop-agent message alert "<text>" [--title TITLE] [--button BUTTON]

# Show confirmation dialog
uvx desktop-agent message confirm "<text>" [--title TITLE] [--buttons "OK,Cancel"]

# Prompt for input
uvx desktop-agent message prompt "<text>" [--title TITLE] [--default TEXT]

# Password input
uvx desktop-agent message password "<text>" [--title TITLE] [--mask CHAR]
```

**Examples:**
```bash
# Simple alert
uvx desktop-agent message alert "Task completed!"

# Get user confirmation
uvx desktop-agent message confirm "Continue with operation?"

# Ask for user input
uvx desktop-agent message prompt "Enter your name:"
```

### 📱 Application Control (`app`)

Control applications across Windows, macOS, and Linux.

```bash
# Open an application by name
uvx desktop-agent app open <name> [--arg ARGS...]

# Focus on a window by title/name
uvx desktop-agent app focus <name>

# List all visible windows
uvx desktop-agent app list
```

**Examples:**
```bash
# Windows: Open Notepad
uvx desktop-agent app open notepad

# Windows: Open Chrome with a URL
uvx desktop-agent app open "chrome" --arg "https://google.com"

# macOS: Open Safari
uvx desktop-agent app open "Safari"

# Focus on a specific window
uvx desktop-agent app focus "Untitled - Notepad"

# List all open windows
uvx desktop-agent app list
```

## Common Automation Workflows

### Workflow 1: Open Application and Type

```bash
# Open notepad directly (cross-platform)
uvx desktop-agent app open notepad

# Wait for app to open, then focus it
uvx desktop-agent app focus notepad

# Type some text
uvx desktop-agent keyboard write "Hello from Desktop Skill!"
```

### Workflow 2: Screenshot + Analysis

```bash
# Get screen size first
uvx desktop-agent screen size

# Take full screenshot
uvx desktop-agent screen screenshot current_screen.png

# Check if specific UI element is visible
uvx desktop-agent screen locate save_button.png
```

### Workflow 3: Form Filling

```bash
# Click first field
uvx desktop-agent mouse click 300 200

# Fill field
uvx desktop-agent keyboard write "John Doe"

# Tab to next field
uvx desktop-agent keyboard press tab

# Fill second field
uvx desktop-agent keyboard write "john@example.com"

# Submit form (Enter)
uvx desktop-agent keyboard press enter
```

### Workflow 4: Copy/Paste Operations

```bash
# Select all text
uvx desktop-agent keyboard hotkey "ctrl,a"

# Copy
uvx desktop-agent keyboard hotkey "ctrl,c"

# Click destination
uvx desktop-agent mouse click 500 600

# Paste
uvx desktop-agent keyboard hotkey "ctrl,v"
```

## Safety Considerations

When using this skill, AI agents should:

1. **Verify coordinates**: Use `screen size` and `on-screen` before clicking
2. **Add delays**: Insert appropriate delays between commands for UI responsiveness
3. **Validate images**: Ensure image files exist before using `locate` commands
4. **Handle failures**: Commands may fail if windows change or elements move
5. **User safety**: Always confirm destructive actions with user via `message confirm`

## Troubleshooting

### PyAutoGUI Fail-Safe
PyAutoGUI has a fail-safe: moving mouse to screen corner aborts operations. This is a safety feature.

### Image not found
When using `screen locate`, ensure:
- Image file exists and path is correct
- Adjust `--confidence` (try 0.7-0.9)
- Image matches exact screen appearance (resolution, colors)

## Getting Help

```bash
# Show all available commands
uvx desktop-agent --help

# Show commands for specific category
uvx desktop-agent mouse --help
uvx desktop-agent keyboard --help
uvx desktop-agent screen --help
uvx desktop-agent message --help

# Show help for specific command
uvx desktop-agent mouse move --help
```

## Integration Tips for AI Agents

1. **Always check screen size first** when working with absolute coordinates
2. **Use relative positioning** when possible (e.g., get current position, calculate offset)
3. **Combine commands** for complex workflows
4. **Validate before executing** (e.g., check if image exists on screen)
5. **Provide user feedback** using message dialogs for important operations
6. **Handle errors gracefully** - commands may fail if UI state changes

## Performance Notes

- Mouse movements with `--duration` are animated and take time
- Image location (`locate`) can be slow on large screens - use regions when possible
- Keyboard commands are generally fast (< 100ms)
- Screenshots depend on screen resolution and region size

## JSON Output Mode

All commands support a `--json` flag for structured output, ideal for programmatic use by AI agents:

```bash
# Text output (default, human-readable)
uvx desktop-agent mouse position
# Output: Position: (960, 540)

# JSON output (structured, machine-readable)
uvx desktop-agent mouse position --json
# Output: {"success": true, "command": "mouse.position", "timestamp": "2026-01-31T10:00:00Z", "duration_ms": 5, "data": {"position": {"x": 960, "y": 540}}}
```

### Response Schema

All JSON responses follow this schema:

```json
{
  "success": true,
  "command": "category.command",
  "timestamp": "2026-01-31T10:00:00Z",
  "duration_ms": 150,
  "data": { ... },
  "error": null
}
```

### Error Response Schema

```json
{
  "success": false,
  "command": "category.command",
  "timestamp": "2026-01-31T10:00:00Z",
  "duration_ms": 50,
  "data": null,
  "error": {
    "code": "image_not_found",
    "message": "Image file 'button.png' not found",
    "details": {},
    "recoverable": true
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `success` | Command succeeded |
| `invalid_argument` | Invalid command arguments |
| `coordinates_out_of_bounds` | Coordinates outside screen |
| `image_not_found` | Image file not found or not on screen |
| `window_not_found` | Target window not found |
| `ocr_failed` | OCR operation failed |
| `application_not_found` | Application not found |
| `permission_denied` | Permission denied |
| `platform_not_supported` | Platform not supported |
| `timeout` | Operation timed out |
| `unknown_error` | Unknown error |

### JSON Output Examples

**Mouse move:**
```bash
uvx desktop-agent mouse move 960 540 --json
```
```json
{"success": true, "command": "mouse.move", "timestamp": "...", "duration_ms": 150, "data": {"x": 960, "y": 540, "duration": 0}, "error": null}
```

**Screen size:**
```bash
uvx desktop-agent screen size --json
```
```json
{"success": true, "command": "screen.size", "timestamp": "...", "duration_ms": 5, "data": {"size": {"width": 1920, "height": 1080}}, "error": null}
```

**Locate image:**
```bash
uvx desktop-agent screen locate button.png --json
```
```json
{"success": true, "command": "screen.locate", "timestamp": "...", "duration_ms": 250, "data": {"image_found": true, "bounding_box": {"left": 100, "top": 200, "width": 50, "height": 30, "center_x": 125, "center_y": 215}}, "error": null}
```

**List windows:**
```bash
uvx desktop-agent app list --json
```
```json
{"success": true, "command": "app.list", "timestamp": "...", "duration_ms": 100, "data": {"windows": ["Untitled - Notepad", "Google Chrome", "Visual Studio Code"]}, "error": null}
```

**Error example:**
```bash
uvx desktop-agent screen locate missing.png --json
```
```json
{"success": false, "command": "screen.locate", "timestamp": "...", "duration_ms": 50, "data": null, "error": {"code": "image_not_found", "message": "Image file 'missing.png' not found", "details": {}, "recoverable": true}}
```

## Integration Tips for AI Agents

1. **Always check screen size first** when working with absolute coordinates
2. **Use relative positioning** when possible (e.g., get current position, calculate offset)
3. **Combine commands** for complex workflows
4. **Validate before executing** (e.g., check if image exists on screen)
5. **Provide user feedback** using message dialogs for important operations
6. **Handle errors gracefully** - commands may fail if UI state changes
7. **Use `--json` flag** for reliable parsing by AI agents
