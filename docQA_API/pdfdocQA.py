from fastapi import FastAPI, File, UploadFile


from typing import Union
import os
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain.llms import OpenAIChat
from langchain import PromptTemplate, LLMChain

import aiofiles
from typing import List


from doc_QA import text_embed_for_QA


class Query(BaseModel):
    username: str
    password: str
#    openai_key: str
    querytext: str

class QueryRequest(BaseModel):
    query: Query


def query_api(question: str, pdf_filepath: str) -> Union[str, dict]:
    #openaichat = OpenAIChat(model_name="gpt-3.5-turbo")
    QA_embed = text_embed_for_QA(embeddings='openAI') # textsplitter=None, vectorstore=None)
    pages = QA_embed.load_pdf(pdf_filepath)
    qa = QA_embed.load_dbqa_chain(pages)
    result = QA_embed.query_pdf_with_sources(qa, question)

    return {"answer": result.strip() }

def read_pdf_files():
    pdfs = []
    # read pdfs in the current directory
    for file in os.listdir("."):
        if file.endswith(".pdf"):
            pdfs.append(os.path.join("pdfs", file))
    return pdfs

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

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}  



@app.post("/query/")
async def run_query(request: Request):
    print("starting...")
    query_request = QueryRequest.parse_raw(await request.body())
    username = query_request.query.username
    password = query_request.query.password
    if password == 'abc123':
        print('User %s authenticated' % username)
        pdffiles = read_pdf_files()
        response = query_api(query_request.query.querytext, pdffiles[0] ) # only use first pdf for now
        return JSONResponse(content=jsonable_encoder(response))
    else:
        print('User not authenticated')
        raise HTTPException(status_code=401, detail="User not authenticated")



