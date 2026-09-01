# Agent Operating Guide: Frame Range Manager

This repository contains the **Frame Range Manager** Blender extension.

---

## 1. Structure
- `blender_manifest.toml`: Extension manifest for Blender 4.2+ / 5.x.
- `__init__.py`: Addon implementation (retaining `bl_info` for backward compatibility).
- `scripts/build_extension.py`: Builder that generates `dist/frame_range_manager-<version>.zip`.

---

## 2. Release SOP for Agents
1. Verify version numbers in `blender_manifest.toml` and `__init__.py`.
2. Run `python scripts/build_extension.py` to produce distribution zip.
3. Test registration:
   ```bash
   blender --background --factory-startup --python-expr "import sys, importlib.util; spec = importlib.util.spec_from_file_location('frame_range_manager', '__init__.py'); mod = importlib.util.module_from_spec(spec); mod.register(); mod.unregister()"
   ```
4. Commit and push tag:
   ```bash
   git commit -am "Release v<version>"
   git tag v<version>
   git push origin master --tags
   ```
