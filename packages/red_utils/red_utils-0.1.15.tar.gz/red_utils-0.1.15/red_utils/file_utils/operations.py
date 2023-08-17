from __future__ import annotations

from datetime import datetime
import json

from pathlib import Path
import time
from typing import Any, Union

from .constants import default_json_dir, ts

def export_json(
    input: Union[str, list[list, dict], dict[str, Any]] = None,
    output_dir: str = default_json_dir,
    output_filename: str = f"{ts()}_unnamed_json.json",
):
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    if isinstance(input, dict):
        input = json.dumps(input)

    if Path(f"{output_dir}/{output_filename}").exists():
        raise FileExistsError(
            f"JSON file already exists: {output_dir}/{output_filename}"
        )

    if output_dir.endswith("/"):
        output_dir = output_dir[:-1]

    if not output_filename.endswith(".json"):
        output_filename = f"{output_filename}.json"

    output_path: str = f"{output_dir}/{output_filename}"

    print(f"Output path: {output_path}")

    if not Path(output_path).exists():
        try:
            with open(output_path, "w+") as f:
                f.write(input)
        except FileExistsError as file_exists_exc:
            raise FileExistsError(file_exists_exc)
        except FileNotFoundError as file_not_found_exc:
            raise FileNotFoundError(file_not_found_exc)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception writing JSON to file: {output_path}. Details: {exc}"
            )


def crawl_dir(
    return_type: str = "all",
    in_dir: Union[str, Path] = None,
    files: list[Path] = None,
    dirs: list[Path] = None,
) -> dict[str, list[Path]]:
    """Crawl a directory for sub-directories/files. Continue crawl on new subdirectory.

    Parameters
    ----------
        return_type (str): Return "files", "dirs", or "all"
        in_dir (str | Path): An input directory to start the crawl at.
        files (list[Path]): A list of Path objects to append found files to.
        dirs (list[Path]): A list of Path objects to append found dirs to.

    Returns
    -------
        A dict object of file and dir lists. return_obj['files'] will be a list of files
        found in path, including in subdirectories. return_obj['dirs'] will be a list of
        dirs and subdirs found during crawl.
    """
    valid_return_types: list[str] = ["all", "files", "dirs"]
    if not return_type:
        return_type = "all"

    if not isinstance(return_type, str):
        raise TypeError(f"return_type must be a string")

    return_type = return_type.lower()

    if return_type not in valid_return_types:
        raise ValueError(
            f"Invalid return type: {return_type}. Must be one of {valid_return_types}"
        )

    if not in_dir:
        raise ValueError(f"Missing input directory to crawl")

    if not isinstance(in_dir, Path):
        if not isinstance(in_dir, str):
            raise TypeError(
                f"Invalid type for input directory: {type(in_dir)}. Must be a str or Path object."
            )
        elif isinstance(in_dir, str):
            in_dir: Path = Path(in_dir)
        else:
            raise Exception(
                f"Unhandled exception parsing input directory. Could not detect type of in_dir."
            )

    ## Create files/dirs lists if they do not exist at function call.
    if not files:
        files = []
    if not dirs:
        dirs = []

    try:
        ## Loop over in_dir
        for _f in in_dir.iterdir():
            if _f.is_file():
                ## Append file to files list, if it does not already exist in the list
                if _f not in files:
                    files.append(_f)
            elif _f.is_dir():
                ## Append dir to dirs list, if it does not already exist in the list
                if _f not in dirs:
                    dirs.append(_f)

                ## Re-crawl on new directory
                crawl_dir(in_dir=_f, files=files, dirs=dirs)

    except FileNotFoundError as fnf_exc:
        raise FileNotFoundError(f"Path does not exist: {in_dir}. Details: {fnf_exc}")
    except PermissionError as perm_exc:
        raise PermissionError(
            f"Encountered permission error while scanning {in_dir}. Details: {perm_exc}"
        )
    except Exception as exc:
        raise Exception(f"Unhandled exception crawling path: {in_dir}. Details: {exc}")

    return_obj: dict[str, list[Path]] = {"files": files, "dirs": dirs}

    return return_obj
