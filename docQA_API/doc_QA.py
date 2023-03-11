
from langchain.document_loaders import PagedPDFSplitter
import os

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains import VectorDBQA
from langchain.llms import OpenAI



# need to export your API key or os.environ["OPENAI_API_KEY"] = "sk-"


class text_embed_for_QA():
    def __init__(self, embeddings='openAI'): #, textsplitter=None, vectorstore="FAISS"):
        if embeddings=='openAI':
            self.embeddings = OpenAIEmbeddings()
        else:
            raise Exception("Other Embeddings not supported")
        # self.textsplitter = textsplitter # not implemented yet, just using pages for now
        # if vectorstore=="FAISS":
        #     self.vectorstore = FAISS
        # else:
        #     raise Exception("Other Vector Stores not supported")


    def load_pdf(self, input_pdf_file):
        loader = PagedPDFSplitter(input_pdf_file)
        pages = loader.load_and_split()
        assert len(pages) > 0, "No pages found in PDF!"
        return pages

    def embed_index(self, texts):
        faiss_index = FAISS.from_documents(texts, self.embeddings)
        return faiss_index
    
    def similarity_search(self, query):
        docs = self.faiss_index.similarity_search(query, k=2)
        return docs
    
    def load_dbqa_chain(self, pages):
        faiss_index = self.embed_index(pages)
        qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=faiss_index)
        return qa    

    def query_pdf_with_sources(self, qa, query):
        return qa.run(query)



if __name__=="__main__":
    QA_embed = text_embed_for_QA(embeddings='openAI') # textsplitter=None, vectorstore=None)
    pages = QA_embed.load_pdf("pdfs/Tsoumas.pdf")
    qa = QA_embed.load_dbqa_chain(pages)
    result = QA_embed.query_pdf_with_sources(qa, "What is the backdoor problem?")
    print(result)




# To Do:
# 0. use GPT-3.5-turbo
# 1. Implement textsplitter options
# 2. save, load embeddings?
# working with multiple pdfs..


# from langchain.text_splitter import CharacterTextSplitter
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)

# from langchain.vectorstores import Chroma
# db = Chroma.from_documents(texts, embeddings)



# store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
# faiss.write_index(store.index, "docs.index")
# store.index = None
# with open("faiss_store.pkl", "wb") as f:
#     pickle.dump(store, f)


