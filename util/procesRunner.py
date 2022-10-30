import asyncio
from typing import Tuple, List, Optional

async def run(cmd: List[str]) -> Tuple[Optional[int], str, str]:
    proc = await asyncio.create_subprocess_shell(' '.join(cmd), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode(), stderr.decode()