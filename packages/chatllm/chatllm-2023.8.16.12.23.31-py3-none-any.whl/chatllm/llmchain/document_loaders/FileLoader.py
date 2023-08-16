#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : file
# @Time         : 2023/7/15 17:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 文件流
import os

from meutils.pipe import *
from langchain.text_splitter import *
from langchain.document_loaders import *
from langchain.document_loaders.base import Document, BaseLoader
from chatllm.llmchain.document_loaders import TextLoader, Docx2txtLoader, PyMuPDFLoader, UnstructuredFileLoader


class FileLoader(BaseLoader):
    """
        loader = FilesLoader('data/古今医统大全.txt')
        docs = loader.load_and_split()
    """

    def __init__(
        self,
        file_path: Any,
        filename: Optional[str] = None,
        max_workers: int = 3
    ):
        self.file_path = str(file_path).lower()
        self.filename = filename or self.file_path
        self._max_workers = max_workers

    def load(self) -> List[Document]:
        if self.filename.endswith((".txt",)):
            docs = TextLoader(self.file_path, autodetect_encoding=True).load()

        elif self.filename.endswith((".docx",)):
            docs = Docx2txtLoader(self.file_path).load()

        elif self.filename.endswith((".pdf",)):
            docs = PyMuPDFLoader(self.file_path).load()

        elif self.filename.endswith((".csv",)):
            docs = CSVLoader(self.file_path).load()

        else:
            docs = UnstructuredFileLoader(self.file_path, mode='single', strategy="fast").load()

        # schema: file_type todo: 增加字段
        # 静态schema怎么设计存储，支持多文档：metadata存文件名字段（可以放多层级）
        # docs[0].metadata['total_length'] = len(docs[0].page_content)
        # docs[0].metadata['file_name'] = Path(docs[0].metadata['source']).name
        # docs[0].metadata['ext'] = {}  # 拓展字段

        return docs


if __name__ == '__main__':
    p = 'text.py'
    # p = '/Users/betterme/PycharmProjects/AI/ChatLLM/data/医/古今医统大全.txt'
    loader = FileLoader(p)
    docs = loader.load_and_split()
    print(docs)
