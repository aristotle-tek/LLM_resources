# A simple example to create an API to which you can upload a pdf and then query it using GPT-3.
# In the background it generates FAISS embeddings using OpenAIEmbeddings
# export your OPENAI_API_KEY to use, then deploy with 
# uvicorn pdfdocQA:app --reload
# To make a request, the user would need to enter a hardcoded password ('123abc' below)

import os

from langchain.document_loaders import PagedPDFSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import VectorDBQA
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain import PromptTemplate, LLMChain

from fastapi import FastAPI, File, UploadFile
from typing import Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


import aiofiles
from typing import List



class Query(BaseModel):
    username: str
    password: str
#    openai_key: str
    querytext: str

class QueryRequest(BaseModel):
    query: Query




app = FastAPI()


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = await file.read()
            async with aiofiles.open(file.filename, 'wb') as f:
                await f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            await file.close()

    loader = PagedPDFSplitter(input_pdf_file)

    pages = loader.load_and_split()
    assert len(pages) > 0, "No pages found in PDF!"
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
    app.state.qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=faiss_index)

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}  



@app.post("/query/")
async def run_query(request: Request):
    query_request = QueryRequest.parse_raw(await request.body())
    username = query_request.query.username
    password = query_request.query.password
    if password == 'abc123':
        print('User %s authenticated' % username)
        result = app.state.qa.query_pdf_with_sources(qa, query_request.query.querytext)
        return JSONResponse(content=jsonable_encoder(response))
    else:
        print('User not authenticated')
        raise HTTPException(status_code=401, detail="User not authenticated")



