from asyncio import Task
from typing import List, Tuple, Optional, Set
from fastapi import APIRouter, UploadFile, HTTPException
from .fileSystem import get_printitem_path, save_file, get_item_index_by_name, SCANPATH
from datetime import datetime as dt
from util.filetypes import FileType
import util.processRunner as procesRunner
import subprocess
import asyncio

router = APIRouter(prefix="/print")

@router.post("/{index}")
async def print_by_index(index: int):
    status, stdout, stdin = await procesRunner.run(['lp', get_printitem_path(index)])
    return {"returnStatus": status, "stdout": stdout, "stderr": stdin}

@router.post("/files")
async def print_files(files: List[UploadFile]):
    background_tasks = set()

    async with asyncio.TaskGroup() as tg:
        for file in files:
            path = await save_file(file)
            cmd = ['lp', path]
            task = tg.create_task(procesRunner.run(cmd))
            background_tasks.add(task)
    stati = map(lambda x: x.result(),  background_tasks)
    print(stati)
    return {"returnStatus": stati}

async def get_scanner() -> str:

    status, results, _ = await procesRunner.run(['scanimage', '-L'])

    if not results or status != 0:
        raise IOError
    return results.split(' ')[1].replace("`", "").replace("'", "")

@router.get("/scan")
async def scan_file(filename="", filetype=FileType.PNG):
    """
    scans file to fs
    :param filename: optional filename, if not set `dt.now() is used to set the filename to `%Y%m%d%_%H%M({count}).{filetype}`
    where `{count}` is an optional counter if filename collision. 
    :param filetype: if omitted, default to PNG, is ignored if `{filetype}` was already included in `{filename}
    :return: void
    """
    scanner = await get_scanner()

    # set default filetype
    warnings = []
    if not filename:
        filename = dt.now().strftime("%Y%m%d%_%H%M")
        # TODO check for duplicate
        warnings.append(f'filename omitted, setting filename to {filename}')
    # check for filetype in filename
    if "." in filename:
        filetype = filename.split('.')[1]
        filename = filename.split('.')[0]
        warnings.append(f'filetype in filename, using {filetype}')
    # set default filetype if filetype unsuported
    if not filetype in FileType.getAll():
        warnings.append(f'unsupported filetype, defaulting to {FileType.PNG}')
        filetype = FileType.PNG
    fullname = f'{filename}.{filetype}'
    status, stdout, stderr = await procesRunner.run(['scanimage', ' --format png', f'-d {scanner}', f'> "{SCANPATH}/{fullname}"'])
    scan_index = get_item_index_by_name(fullname)
    if scan_index == -1:
        raise HTTPException(status_code=500, detail=f"file was not saved; internal error; blame Luca{status, stdout, stderr}")
    return {
        "status": status,
        "stdout": stdout,
        "stderr": stderr,
        "warnings": warnings,
        "filename": filename,
        "filetype": filetype,
        "fullname": fullname,
        "scanIndex": scan_index

    }
