from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ResourceReader:
    
    def __init__(self, resource_folder_path):
        self.resource_path = Path(resource_folder_path).resolve()
        if not self.resource_path.is_dir():
            raise ValueError(f"The path {self.resource_path} is not a valid directory.")

    def read_files(self, file_extension=".txt") -> List[Document]:
        documents = []
        for file_path in self.resource_path.glob(f"*{file_extension}"):
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": str(file_path)}
                    ))
        return documents
    
    def read_file_contents(self, documents) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts
    
    def read_file_lines(self, file_extension=".txt") -> List[str]:
        lines = []
        for file_path in self.resource_path.glob(f"*{file_extension}"):
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Read each line from the file and strip newline characters
                    file_lines = [line.strip() for line in file.readlines()]
                    lines.extend(file_lines)  # Add the lines to the list
        return lines