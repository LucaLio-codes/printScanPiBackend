from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from typing import List
from util.filetypes import FileType
import os, aiofiles

router = APIRouter(prefix="/fs")
SCANPATH = "/share/scans"
PRINTPATH = "/share/print"


@router.get("/scans")
def get_scanned_items()-> List[str]:
    return os.listdir(SCANPATH)

def get_item_index_by_name(name: str) -> int:
    for i, item in enumerate(get_scanned_items()):
        if name == item:
            return i
    return  -1

@router.get("/print")
def get_printable_items() -> List[str]:
    return list(filter(lambda x: any(ft in x for ft in FileType.getAll()),os.listdir(PRINTPATH)))

async def save_file(file: UploadFile) -> str:
    """
    :param file: file to be saved
    :return: path to saved file
    """
    path = os.path.join(PRINTPATH, file.filename)
    async with open(path, 'wb') as outFile:
        content = await file.read()
        await outFile.write(content)

    return  path

def get_printitem_path(index: int) -> str:
    items = get_printable_items()
    return os.path.join(PRINTPATH, items[index])

@router.get("/scans/{fileIndex}")
async def get_scanned_item_by_index(fileIndex: int) -> FileResponse:
    filenames = os.listdir(SCANPATH)
    filePath = os.path.join(SCANPATH, filenames[fileIndex])
    return FileResponse(filePath)
