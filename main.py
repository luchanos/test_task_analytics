import uvicorn
from fastapi.routing import APIRoute
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Request

from config import async_session
from dals import DocumentDAL
from elasticsearch import AsyncElasticsearch
from datetime import date

from settings import ELASTIC_URL


class InsertDocumentModel(BaseModel):
    created_date: date
    text: str
    rubrics: list[str]


class SearchDocumentsModel(BaseModel):
    search_query: str


async def create_document(request: Request, body: InsertDocumentModel):
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    created_date = date.today()
    async with async_session() as session:
        async with session.begin():
            document_dal = DocumentDAL(session)
            document_id = await document_dal.create_document(text=body.text,
                                                             rubrics=body.rubrics,
                                                             created_date=body.created_date)
            document = {**body.dict(), "id": document_id, "created_date": created_date}
            await elastic_client.index(index="documents", document=document)
            return {"success": True, "document_id": document_id}


async def search_documents(request: Request, search_query: str):
    elastic_query = {
        "match": {
            "text": search_query,
        },
    }
    elastic_client: AsyncElasticsearch = request.app.state.elastic_client
    async with async_session() as session:
        async with session.begin():
            document_dal = DocumentDAL(session)
            res = await elastic_client.search(index="documents", query=elastic_query, fields=["id", ], source=False)
            ids = [document["fields"]["id"][0] for document in res.body["hits"]["hits"]]
            documents = await document_dal.get_documents_by_ids(ids)
            return documents


async def delete_document(request: Request, document_id: int):
    pass


routes = [
    APIRoute(path="/create_document", endpoint=create_document, methods=["POST"]),
    APIRoute(path="/search_documents", endpoint=search_documents, methods=["GET"]),
]

app = FastAPI()
elastic_client = AsyncElasticsearch(ELASTIC_URL)
app.state.elastic_client = elastic_client
app.include_router(APIRouter(routes=routes))

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
