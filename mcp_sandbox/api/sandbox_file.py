from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from mcp_sandbox.core.sandbox_modules.manager import SandboxManager
from mcp_sandbox.core.sandbox_modules.file_ops import SandboxFileOpsMixin
from mcp_sandbox.utils.config import logger
import io
import os
import tarfile
import mimetypes

router = APIRouter()

class APISandboxManager(SandboxManager, SandboxFileOpsMixin):
    pass

sandbox_manager = APISandboxManager()

@router.get("/sandbox/file")
def get_sandbox_file(
    sandbox_id: str = Query(..., description="Sandbox ID"),
    file_path: str = Query(..., description="Absolute path to the file inside the sandbox, e.g. /app/results/foo.txt")
):
    """
    Read-only access to files inside a running sandbox.
    Returns the file content as a download if found.
    """
    try:
        sandbox = sandbox_manager.sandbox_client.containers.get(sandbox_id)
        stream, stat = sandbox.get_archive(file_path)
        tar_bytes = io.BytesIO(b"".join(stream))
        with tarfile.open(fileobj=tar_bytes) as tar:
            members = tar.getmembers()
            if not members:
                raise HTTPException(status_code=404, detail="File not found in sandbox")
            rel_path = file_path.lstrip("/")
            member = next((m for m in members if m.name == rel_path), None)
            if member is None:
                basename = os.path.basename(file_path)
                member = next((m for m in members if m.name.endswith(basename)), members[0])
            fileobj = tar.extractfile(member)
            if not fileobj:
                raise HTTPException(status_code=404, detail="File not found in sandbox")
            mime_type, _ = mimetypes.guess_type(member.name)
            mime_type = mime_type or "application/octet-stream"
            headers = {"Content-Disposition": f"inline; filename={member.name}"}
            return StreamingResponse(fileobj, media_type=mime_type, headers=headers)
    except Exception as e:
        logger.error(f"Failed to fetch file from sandbox {sandbox_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching file from sandbox: {e}")
