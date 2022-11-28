from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import date

from documents import Document


class DocumentDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_document(self, text: str, rubrics: list[str], created_date: date) -> int:
        new_document = Document(text=text, rubrics=rubrics, created_date=created_date)
        self.db_session.add(new_document)
        await self.db_session.flush()
        self.db_session.refresh(new_document)
        return new_document.id

    # async def get_all_books(self) -> List[Document]:
    #     q = await self.db_session.execute(select(Document).order_by(Document.id))
    #     return q.scalars().all()

    # async def update_book(self, book_id: int, name: Optional[str], author: Optional[str], release_year: Optional[int]):
    #     q = update(Document).where(Document.id == book_id)
    #     if name:
    #         q = q.values(name=name)
    #     if author:
    #         q = q.values(author=author)
    #     if release_year:
    #         q = q.values(release_year=release_year)
    #     q.execution_options(synchronize_session="fetch")
    #     await  self.db_session.execute(q)
