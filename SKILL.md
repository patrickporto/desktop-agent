---
name: Desktop Control
description: Control mouse, keyboard, and screen using PyAutoGUI for desktop automation tasks
---

# Desktop Control Skill

This skill provides comprehensive desktop automation capabilities through PyAutoGUI, allowing AI agents to control the mouse, keyboard, take screenshots, and interact with the desktop environment.

## Installation

To install this skill, run the installation script:

```bash
python scripts/install.py
```

Or install manually with uv:

```bash
cd /path/to/desktop-skill
uv sync
```

## Prerequisites

- Python 3.12+
- PyAutoGUI (installed automatically)
- Typer (installed automatically)

## How to Use This Skill

As an AI agent, you can invoke desktop automation commands using the `desktop-skill` CLI or by running `python main.py` from the skill directory.

### Command Structure

All commands follow this pattern:

```bash
python main.py <category> <command> [arguments] [options]
```

**Categories:**
- `mouse` - Mouse control
- `keyboard` - Keyboard input
- `screen` - Screenshots and screen analysis
- `message` - User dialogs

## Available Commands

### 🖱️ Mouse Control (`mouse`)

Control cursor movement and clicks.

```bash
# Move cursor to coordinates
python main.py mouse move <x> <y> [--duration SECONDS]

# Click at current position or specific coordinates
python main.py mouse click [x] [y] [--button left|right|middle] [--clicks N]

# Specialized clicks
python main.py mouse double-click [x] [y]
python main.py mouse right-click [x] [y]
python main.py mouse middle-click [x] [y]

# Drag to coordinates
python main.py mouse drag <x> <y> [--duration SECONDS] [--button BUTTON]

# Scroll (positive=up, negative=down)
python main.py mouse scroll <clicks> [x] [y]

# Get current mouse position
python main.py mouse position
```

**Examples:**
```bash
# Move to center of 1920x1080 screen
python main.py mouse move 960 540 --duration 0.5

# Right-click at specific location
python main.py mouse right-click 500 300

# Scroll down 5 clicks
python main.py mouse scroll -5
```

### ⌨️ Keyboard Control (`keyboard`)

Type text and execute keyboard shortcuts.

```bash
# Type text
python main.py keyboard write "<text>" [--interval SECONDS]

# Press keys
python main.py keyboard press <key> [--presses N] [--interval SECONDS]

# Execute hotkey combination (comma-separated)
python main.py keyboard hotkey "<key1>,<key2>,..."

# Hold/release keys
python main.py keyboard keydown <key>
python main.py keyboard keyup <key>
```

**Examples:**
```bash
# Type text with natural delay
python main.py keyboard write "Hello World" --interval 0.05

# Copy selected text
python main.py keyboard hotkey "ctrl,c"

# Open Task Manager
python main.py keyboard hotkey "ctrl,shift,esc"

# Press Enter 3 times
python main.py keyboard press enter --presses 3
```

**Common Key Names:**
- Modifiers: `ctrl`, `shift`, `alt`, `win`
- Special: `enter`, `tab`, `esc`, `space`, `backspace`, `delete`
- Function: `f1` through `f12`
- Arrows: `up`, `down`, `left`, `right`

### 🖼️ Screen & Screenshots (`screen`)

Capture screenshots and analyze screen content.

```bash
# Take screenshot
python main.py screen screenshot <filename> [--region "x,y,width,height"]

# Locate image on screen
python main.py screen locate <image_path> [--confidence 0.0-1.0]
python main.py screen locate-center <image_path> [--confidence 0.0-1.0]

# Get pixel color at coordinates
python main.py screen pixel <x> <y>

# Get screen dimensions
python main.py screen size

# Check if coordinates are valid
python main.py screen on-screen <x> <y>
```

**Examples:**
```bash
# Full screenshot
python main.py screen screenshot desktop.png

# Screenshot of specific region
python main.py screen screenshot region.png --region "100,100,800,600"

# Find button on screen
python main.py screen locate-center button.png --confidence 0.9

# Get color at cursor position
python main.py screen pixel 500 500
```

### 💬 Message Dialogs (`message`)

Display user interaction dialogs.

```bash
# Show alert
python main.py message alert "<text>" [--title TITLE] [--button BUTTON]

# Show confirmation dialog
python main.py message confirm "<text>" [--title TITLE] [--buttons "OK,Cancel"]

# Prompt for input
python main.py message prompt "<text>" [--title TITLE] [--default TEXT]

# Password input
python main.py message password "<text>" [--title TITLE] [--mask CHAR]
```

**Examples:**
```bash
# Simple alert
python main.py message alert "Task completed!"

# Get user confirmation
python main.py message confirm "Continue with operation?"

# Ask for user input
python main.py message prompt "Enter your name:"
```

## Common Automation Workflows

### Workflow 1: Open Application and Type

```bash
# Open Run dialog
python main.py keyboard hotkey "win,r"

# Wait for dialog to open (agent should add delay)
# Type application name
python main.py keyboard write "notepad"

# Press Enter
python main.py keyboard press enter
```

### Workflow 2: Screenshot + Analysis

```bash
# Get screen size first
python main.py screen size

# Take full screenshot
python main.py screen screenshot current_screen.png

# Check if specific UI element is visible
python main.py screen locate save_button.png
```

### Workflow 3: Form Filling

```bash
# Click first field
python main.py mouse click 300 200

# Fill field
python main.py keyboard write "John Doe"

# Tab to next field
python main.py keyboard press tab

# Fill second field
python main.py keyboard write "john@example.com"

# Submit form (Enter)
python main.py keyboard press enter
```

### Workflow 4: Copy/Paste Operations

```bash
# Select all text
python main.py keyboard hotkey "ctrl,a"

# Copy
python main.py keyboard hotkey "ctrl,c"

# Click destination
python main.py mouse click 500 600

# Paste
python main.py keyboard hotkey "ctrl,v"
```

## Safety Considerations

When using this skill, AI agents should:

1. **Verify coordinates**: Use `screen size` and `on-screen` before clicking
2. **Add delays**: Insert appropriate delays between commands for UI responsiveness
3. **Validate images**: Ensure image files exist before using `locate` commands
4. **Handle failures**: Commands may fail if windows change or elements move
5. **User safety**: Always confirm destructive actions with user via `message confirm`

## Troubleshooting

### Command not found
```bash
# Use full path to main.py
cd /path/to/desktop-skill
python main.py <command>
```

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
python main.py --help

# Show commands for specific category
python main.py mouse --help
python main.py keyboard --help
python main.py screen --help
python main.py message --help

# Show help for specific command
python main.py mouse move --help
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
