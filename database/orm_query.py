from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from database.models import Dictionary


async def orm_add_word_translation(session: AsyncSession, data: dict):
    dictionary_entry = Dictionary(
        word = data["word"],
        translation = data["translation"]
    )
    session.add(dictionary_entry)
    await session.commit()

async def orm_get_all_words_translations(session: AsyncSession):
    query = select(Dictionary)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_delete_word_translation(session: AsyncSession, id: int):
    query = delete(Dictionary).where(Dictionary.id == id)
    await session.execute(query)
    await session.commit()