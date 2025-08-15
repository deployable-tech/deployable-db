import shutil
import uuid
from pathlib import Path

def store_local_file(src_path: str | Path, storage_dir: str | Path) -> tuple[str, str]:
    """
    Move the file to storage_dir, renaming it to a UUID + original extension.
    Returns (stored_filename, final_path).
    """
    storage_dir = Path(storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)

    src_path = Path(src_path)
    stored_filename = f"{uuid.uuid4()}{src_path.suffix}"
    final_path = storage_dir / stored_filename
    shutil.move(str(src_path), final_path)

    return stored_filename, str(final_path)
