from app.api.schemas import NoteSchema
from app.db import database, notes
from typing import List



async def get_notes():
    query = notes.select()
    return await database.fetch_all(query=query)

async def create_note(note: NoteSchema):
    query = notes.insert().values(title=note.title, description=note.description)
    return await database.execute(query=query)

async def get_note(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)

async def put_note(id: int, payload: NoteSchema):
    query = (
        notes
        .update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)
    