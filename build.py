packages_include = [
    "os",
    "logging.config",
    "pylibdmtx"
]

modules_exclude = [
    "Tkinter"
]

files_include = [
    os.path.join(os.getcwd(), 'assets'),
    os.path.join(os.getcwd(), 'configs')
]

if sys.platform == "win32":

    app_icon = app_icon.replace('\\', '\\\\')
    app_main = app_main.replace('\\', '\\\\')
    app_platform = "Win32GUI"

modules_include: list = []

for folder in os.listdir(os.path.join(os.getcwd(), 'src')):
    if folder != '__pycache__' and os.path.isdir(os.path.join(os.path.join(os.getcwd(), 'src'), folder)):
        modules_include.append(f'src.{folder}')
        for module in os.listdir(os.path.join(os.path.join(os.getcwd(), 'src'), folder)):
            if module != '__pycache__' and '.py' in module:
                modules_include.append(f'src.{folder}.{module[:-3]}')

cx_Freeze.setup(
    name=app_name,
    author=app_author,
    author_email=app_email,
    version=app_version,
    description=app_description,
    options={"build_exe": {
        "packages": packages_include,
        "excludes": modules_exclude,
        "includes": modules_include,
        "include_files": files_include
    }},
    executables=[cx_Freeze.Executable(
        script=app_main,
        base=app_platform,
        initScript=None,
        target_name=app_name_target,
        shortcut_name=app_name_shortcut,
        shortcut_dir="DesktopFolder",
        icon=app_icon
    )]
)
