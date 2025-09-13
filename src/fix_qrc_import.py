from pathlib import Path

def fix_qrc_import():
    """
    Fix the import error that appears after every ui file changed in Qt Designer.
    
    This opens the ui file and replaces the line with 'from resources.interface.qrc import LogSearcher_resource_rc' 
    """
    cwd = Path(__file__).parent
    print(cwd)
    
    ui_file_path = cwd / "resources"/ "interface" /"LogSearcherUI_ui.py"
    print(f"UI File Path: {ui_file_path}")
    
    path = ui_file_path
    
    with open(path, "r") as file:
        lines = file.readlines()
    
    modified = False
    for i, line in enumerate(lines):
        if "import LogSearcher_resource_rc" in line and "from resources.interface.qrc" not in line:
            lines[i] = line.replace(
                "import LogSearcher_resource_rc",
                "from resources.interface.qrc import LogSearcher_resource_rc"
            )
            print("Replaced import!")
            modified = True
            break
        
    if modified:
        with open(path, "w") as file:
            file.writelines(lines)
            