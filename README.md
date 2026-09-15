# aimis-maya-generator

This repository contains a Maya Python script that programmatically generates a simple low-poly "fan" character (original, non-game asset), creates a basic joint hierarchy, applies a skinCluster, and saves the scene as a Maya ASCII file (.ma).

Files:
- aimis_maya_create_and_save_ma.py — Run inside Maya Script Editor (Python) to create the scene and save `aimis_fan_model_for_maya.ma` on your desktop.
- LICENSE — MIT License.

How to use:
1. Open Maya (recommended 2018+).
2. Open Script Editor -> Python tab.
3. Paste the contents of `aimis_maya_create_and_save_ma.py` (or open the file) and run it.
4. The script creates a new scene, builds simple geometry and joints, binds them, and saves `aimis_fan_model_for_maya.ma` to your desktop.

Notes:
- This is a basic template model intended as a starting point for modeling/rigging work.
- If you want UVs, textures, higher detail, or a specific naming convention (e.g., for your studio pipeline), tell me and I will extend the script.
