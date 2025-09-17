# Neurolytix\backend\utils\file_handler.py

import aiofiles

async def save_upload(upload_file, destination: str):
    """
    Save an uploaded file asynchronously.
    """
    async with aiofiles.open(destination, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)
