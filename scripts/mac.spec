from PyInstaller.utils.hooks import collect_data_files, collect_submodules

gradio_datas = collect_data_files('gradio')
gradio_hidden = collect_submodules('gradio')

a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    # Bundle our specific models folder into the MEIPASS 'models' directory
    datas=[('../models/best.onnx', 'models'), ('../models/class_labels.json', 'models')] + gradio_datas,
    hiddenimports=['onnxruntime', 'cv2'] + gradio_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'ultralytics'], # Strictly ban PyTorch from the build
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TrashDetector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Hides the terminal window from "Setup-Averse Sam"
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch='arm64', # For your Apple M4 chip
    codesign_identity=None,
    entitlements_file=None,
)

# This creates the actual .app bundle for macOS
app = BUNDLE(
    exe,
    name='TrashDetector.app',
    bundle_identifier='com.thesis.trashdetector',
)