# Frame Range Manager (Blender Extension & Addon)

A lightweight Blender extension (and dual-compatible add-on) to store, edit, update, and restore named frame range presets directly from the Timeline / Dope Sheet editor header.

![Blender 4.2+ / 5.x](https://img.shields.io/badge/Blender-4.2%2B%20%7C%205.x-orange.svg)

---

## Features

- ⏱ **Header Integration**: Popover dropdown right on the Timeline and Dope Sheet headers.
- 💾 **One-Click Store**: Instantly save current start and end frame ranges with custom names.
- 🔄 **Quick Restore**: Toggle between saved frame ranges instantly.
- 🌐 **Cross-Scene Sync**: Automatically syncs saved presets across all scenes within the blendfile.
- ✏️ **Inline Editing**: Rename entries and adjust start/end frames directly within the popup.
- 🛡 **Non-Destructive & File-Safe**: Uses standard scene RNA properties that stay 100% intact across all Blender versions.

---

## Installation

### Method A: Via Personal Extension Repository (Recommended)
Add the extension repository in Blender:
* **URL**: `https://m-dr.github.io/blender-extensions/index.json`  
Then search for **Frame Range Manager** in **Preferences > Get Extensions** and click **Install**.

### Method B: Install from Disk (.zip)
1. Download `frame_range_manager-0.1.0.zip` from the [Releases](https://github.com/m-dr/blender-frame-range-manager/releases) page.
2. In Blender: **Preferences > Get Extensions > Install from Disk...**

---

## Version Compatibility & Legacy Support

* **Blender 4.2+ & 5.x (Modern Extension)**: Uses `blender_manifest.toml`.
* **Legacy Add-on Fallback**: Tagged in Git as `v0.1.0-legacy-addon`. All blendfile presets created with older versions load seamlessly without any data loss.

---

## License

GNU General Public License v3.0 or later (or MIT).
