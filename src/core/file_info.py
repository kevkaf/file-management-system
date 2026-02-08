import os
import stat
import logging
import mimetypes
import platform
import ctypes
from datetime import datetime
from pathlib import Path
from  typing import Union, Optional, Dict, Any  

logger = logging.getLogger(__name__)
mimetypes.init()


class FileInfos:

    @staticmethod
    def get_file_info(filepath: Union[str, Path]) -> Optional[Dict]:
        
        path = Path(filepath)

        if not path.exists():
            logger.error("Path doesn't exist: %s", path)
            return None

        try:
            path_stat = path.stat()

            info = {
                "name": path.name,
                "path": str(path.absolute()),
                "parent": str(path.parent),
                "type": "Directory" if path.is_dir() else "File",
                "size_bytes": path_stat.st_size,
                "size_human": FileInfos._human_readable_size(path_stat.st_size),
                "created": datetime.fromtimestamp(path_stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(path_stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(path_stat.st_atime).isoformat(),
                "permissions": FileInfos._get_permissions(path_stat.st_mode),
                "owner": path_stat.st_uid,
                "group": path_stat.st_gid,
                "inode": path_stat.st_ino,
                "device": path_stat.st_dev,
            }
            
            if path.is_file():
                info.update({
                    "lines": FileInfos._count_lines(path),
                    "extension": path.suffix,
                    "mime_type": FileInfos._get_file_type(path),
                    "is_hidden": FileInfos.is_hidden(path)
                })
            elif path.is_dir():
                items = list(path.iterdir())
                info.update({
                    "item_count": len(items),
                    "is_empty": len(items) == 0,
                    "is_hidden": FileInfos.is_hidden(path)
                })

            # Symlink Information
            if path.is_symlink():
                info.update({
                    "type": "Symbolic Link",
                    "target": str(path.resolve()),
                    "is_broken": not path.exists(),
                })

            logger.debug("File info retrieved: %s", path)
            return info
        
        except OSError as e:
                logger.error("Error getting infos: %s", path)
                return None
        
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def _get_permissions(mode: int) -> str:
        perm_map = [
            (stat.S_IRUSR, 'r'), (stat.S_IWUSR, 'w'), (stat.S_IXUSR, 'x'),
            (stat.S_IRGRP, 'r'), (stat.S_IWGRP, 'w'), (stat.S_IXGRP, 'x'),
            (stat.S_IROTH, 'r'), (stat.S_IWOTH, 'w'), (stat.S_IXOTH, 'x')
        ]

        if stat.S_ISDIR(mode): type_char = "d"
        elif stat.S_ISLNK(mode): type_char = "l"
        else: type_char = "-"

        perms = [char if mode & bit else "-" for bit, char in perm_map]
        return type_char + "".join(perms)
    
    @staticmethod
    def _count_lines(p: Path) -> int:

        try:
            with p.open("r", encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception as e:
            try:
                # Fallback for binary files
                with p.open("rb") as f:
                    return sum(1 for _ in f)
            except Exception as e2:
                logger.error("Error counting lines in %s: %s", p, e2)
                return None
            
    @staticmethod
    def _get_file_type(filepath: Union[str, Path]) -> Optional[str]:
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return None
            
            if filepath.is_dir():
                return "Directory"
            elif filepath.is_symlink():
                return "Symbolic Link"
            
            mime_type, _ = mimetypes.guess_type(str(filepath))
            return mime_type or "application/octet-stream"
        except Exception as e:
            logger.error(f"Error getting MIME type for {filepath}: {e}")
            return None

    @staticmethod
    def is_hidden(filepath: Union[str, Path]) -> bool:

        path = Path(filepath)
        # Unix file
        if path.name.startswith("."):
            return True

        # Windows file
        try:
            if platform.system() == "Windows":
                attrs = ctypes.windll.kernel32.GetFileAttributeW(str(path))
                return attrs != -1 and attrs & 2
        except:
            pass
        return False

    @staticmethod
    def compare_files(file1: str | Path, file2: str | Path) -> Dict[str, Any]:
        """Deep comparison of two files using buffered reading"""
        p1, p2 = Path(file1), Path(file2)
        
        if not (p1.is_file() and p2.is_file()):
            return {"error": "Both paths must be files"}

        # Quick size check first
        size1, size2 = p1.stat().st_size, p2.stat().st_size
        if size1 != size2:
            return {"content_equal": False, "reason": "Size mismatch"}

        # Buffered content check
        try:
            with p1.open('rb') as f1, p2.open('rb') as f2:
                while True:
                    chunk1, chunk2 = f1.read(8192), f2.read(8192)
                    if chunk1 != chunk2:
                        return {"content_equal": False, "reason": "Content mismatch"}
                    if not chunk1:
                        return {"content_equal": True}
        except Exception as e:
            return {"error": str(e)}
        

    @staticmethod
    def get_directory_tree(directory: Union[str, Path], max_depth: int = 3) -> Optional[Dict]:
        """Get directory tree structure"""
        try:
            directory = Path(directory)
            if not directory.is_dir():
                return None
            
            def build_tree(path: Path, depth: int = 0):
                if depth > max_depth:
                    return None
                
                tree = {
                    "name": path.name,
                    "path": str(path),
                    "type": "directory" if path.is_dir() else "file",
                    "size": path.stat().st_size if path.is_file() else 0,
                }
                
                if path.is_dir():
                    tree["children"] = []
                    try:
                        for child in path.iterdir():
                            child_tree = build_tree(child, depth + 1)
                            if child_tree:
                                tree["children"].append(child_tree)
                    except PermissionError:
                        tree["permission_error"] = True
                
                return tree
            
            return build_tree(directory)
            
        except Exception as e:
            logger.error(f"Error building directory tree for {directory}: {e}")
            return None