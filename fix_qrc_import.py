from pathlib import Path

def fix_qrc_import():

    ui_file_path: str = r"C:\Users\ZaricJ\Documents\02_Entwicklung_und_Tools\Arbeit GitLab\RegexFileSearcher\src\resources\interface\LogSearcherUI_ui.py"
    path = Path(ui_file_path)
    
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
            
fix_qrc_import()