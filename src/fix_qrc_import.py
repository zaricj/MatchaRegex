from pathlib import Path


def fix_qrc_import():
    """
    Fix generated UI imports after recompiling `.ui` files.
    """
    cwd = Path(__file__).parent
    ui_files = [
        cwd / "gui" / "ui" / "main" / "LogSearcherUI_ui.py",
        cwd / "gui" / "ui" / "dialogs" / "PreBuiltRegexManagerWidget_ui.py",
    ]

    for ui_file in ui_files:
        with open(ui_file, "r") as file:
            lines = file.readlines()

        modified = False
        for i, line in enumerate(lines):
            if "import LogSearcher_resource_rc" in line:
                lines[i] = line.replace(
                    "import LogSearcher_resource_rc",
                    "from gui.assets.qrc import LogSearcher_resource_rc"
                )
                modified = True
                break

        if modified:
            with open(ui_file, "w") as file:
                file.writelines(lines)


if __name__ == "__main__":
    fix_qrc_import()
