# Blender Frame Range Manager Addon

A lightweight Blender 4.x / 5.x addon to store, edit, update, and restore named frame range presets directly from the Timeline / Dope Sheet editor header.

![Popover Button](https://img.shields.io/badge/Blender-4.0%2B%20%7C%205.x-orange.svg)

## Features

- ⏱ **Header Integration**: Popover dropdown right on the Timeline / Dope Sheet header.
- 💾 **One-Click Store**: Instantly save current start and end frame ranges with custom names.
- 🔄 **Quick Restore**: Toggle between saved frame ranges instantly.
- ✏️ **Inline Editing**: Rename entries and adjust start/end frames directly within the popup menu.
- ♻️ **Update Presets**: Overwrite saved ranges with current timeline selection.

## Installation

1. Download or clone this repository as a `.zip` file (or compress `blender-frame-range-manager` folder).
2. Open Blender, go to **Edit > Preferences > Add-ons**.
3. Click **Install...** (or **Install from Disk**) and select the `.zip` file.
4. Enable **Frame Range Manager**.

Alternatively, copy `__init__.py` or the `blender-frame-range-manager` directory into your Blender scripts folder:
`%APPDATA%\Blender Foundation\Blender\<VERSION>\scripts\addons\`

## License

MIT License
