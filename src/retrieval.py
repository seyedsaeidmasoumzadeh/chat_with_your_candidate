"""Retrieval"""


from langchain.chains import RetrievalQA
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain.vectorstores import Chroma
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
from prompts import get_prompt_template
from utils import cv_loader, generator
from langchain.embeddings import HuggingFaceEmbeddings
import settings


class DBQ:
    @staticmethod
    def build_vectordb(llm, cv_path):
        context = cv_loader(cv_path=cv_path)
        prompt_template = get_prompt_template(type="cv_to_markdown")
        markdown = generator(llm=llm, prompt_template=prompt_template, context=context)

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        md_header_splits = markdown_splitter.split_text(text=markdown)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
        )
        texts = text_splitter.split_documents(md_header_splits)
        for i in range(len(texts)):
            texts[i].metadata.update({"source": f"{i}-pl", "page": i})

        vectordb = Chroma.from_documents(
            documents=texts,
            embedding=HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME),
        )
        return vectordb

    @staticmethod
    def build_db(vectordb, llm):
        compressor = LLMChainExtractor.from_llm(llm=llm)

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=vectordb.as_retriever(
                serach_type="similarity", search_kwargs={"k": settings.VECTOR_COUNT}
            ),
        )

        prompt_template = get_prompt_template(type="question_answering")
        db = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=compression_retriever,
            return_source_documents=settings.RETURN_SOURCE_DOCUMENTS,
            chain_type_kwargs={"prompt": prompt_template},
        )
        return db

    def __init__(self, cv_path, llm):
        vector_db = self.build_vectordb(llm=llm, cv_path=cv_path)
        self.db = self.build_db(vector_db, llm=llm)

    def retrive(self, query):
        return self.db({"query": query})
