from app.api import crud
from app.api.schemas import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException
from typing import List
from collections import namedtuple

router = APIRouter()


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_notes()

@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(note: NoteSchema):
    note_id = await crud.create_note(note)
    return {**note.dict(), "id": note_id}

@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int):
    note = await crud.get_note(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{id}/", response_model=NoteDB)
async def update_note(id: int, note: NoteSchema):
    notedb = await crud.get_note(id)
    if not notedb:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id =  await crud.put_note(id, note)

    return {**note.dict(), "id": note_id}


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int):
    note = await crud.get_note(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete_note(id)

    return note