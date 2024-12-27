import logging
from typing import List, Dict, Any
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class PriceRag:

    def __init__(self, llm, retriever):
        self._logger = logging.getLogger(__name__)
        self.llm = llm
        self.retriever = retriever
        self.qa_chain = self._initialize_qa_chain()

    def _initialize_qa_chain(self) -> RetrievalQA:
        prompt_template = self._initialize_prompt_template()
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt_template}
        )
    
    def _initialize_prompt_template(self) -> PromptTemplate:
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Answer:"""
        return PromptTemplate(template=prompt_template, input_variables=["context", "question"])



    def ask_question(self, question: str,  chat_history: []) -> Dict[str, Any]:
        try:

            logging.info(f"Processing question/query: {question}")
            result = self.qa_chain({"query": question, "chat_history": chat_history} )
            chat_history.append((question, result['result']))
            return {
                "answer": result["result"],
                "sources": [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
            }
        except Exception as e:
            logging.error(f"Error during question processing: {e}")
            return {
                "answer": "An error occurred while processing the question.",
                "sources": []
            }