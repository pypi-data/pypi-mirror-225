#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : UnstructuredFileLoader
# @Time         : 2023/8/16 08:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from langchain.text_splitter import *
from langchain.document_loaders import UnstructuredFileLoader as _UnstructuredFileLoader
from langchain.document_loaders.base import Document, BaseLoader

from meutils.pipe import *
from meutils.fileparser import stream_parser, stream2tempfile4process


class UnstructuredFileLoader(_UnstructuredFileLoader):

    def __init__(self, file_path, mode: str = "single", **unstructured_kwargs: Any):
        """Initialize with file path."""

        try:
            import unstructured  # noqa:F401
        except ImportError:
            raise ValueError(
                "unstructured package not found, please install it with "
                "`pip install unstructured`"
            )

        self.file_path = file_path
        self.mode = mode
        self.unstructured_kwargs = unstructured_kwargs

    def load(self) -> List[Document]:
        fn = lambda file_path: _UnstructuredFileLoader(file_path, mode=self.mode, **self.unstructured_kwargs).load()

        if isinstance(self.file_path, List) or (
            isinstance(self.file_path, (str, os.PathLike))
            and len(self.file_path) < 256
            and Path(self.file_path).is_file()
        ):
            return fn(self.file_path)  # 按页

        filename, file_stream = stream_parser(self.file_path)
        docs = stream2tempfile4process(file_stream, fn)

        if filename:
            for doc in docs or []:
                doc.metadata['source'] = filename

        return docs
