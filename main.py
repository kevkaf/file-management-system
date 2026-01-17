from pathlib import Path
import shutil
import os

def organize_file(directory):
    root = Path(directory)

    output_file = root / "report.txt"
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Documents": [".pdf", ".txt", ".md", ".doc", ".docx"],
        "Archives": [".zip", ".rar", ".tar"],
        "Videos": [".mp4"],
        "Others": [] 
    }


    # Creeate the different folders

    for category in categories:
        cat_dir = root / category
        cat_dir.mkdir(exist_ok=True)

    for item in root.iterdir():
        if item.is_file():
            filename = item.name
            
            file_extension = item.suffix.lower()

            moved = False
            for category, extensions in categories.items():
                if file_extension in extensions:
                    dir_dst = root / category / filename
                    shutil.move(str(item), str(dir_dst))
                    with open(output_file, "a") as f:
                        f.write(f"-------{filename} to {category}\n")

                    moved = True
                    break

            
            if not moved:
                dst = root / "Others" / filename
                shutil.move(str(item), str(dst))
                with open(output_file, "a") as f:
                    f.write(f"Moved {filename} to Others")
                


if __name__ == "__main__":
    # Replace working dir with the dir to organize
    dir_to_organize = input("Directory to organize: ").strip()

    root = Path(dir_to_organize)

    if root.exists():
        organize_file(root)
        print("Organization complete!")
    else:
        print("Directory does not exist")