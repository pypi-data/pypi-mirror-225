from . import ClassImportDefinition
import logging  # functionality managed by Hydra

from datetime import datetime
import importlib
from mdutils.mdutils import MdUtils
from mdutils.fileutils import MarkDownFile
import os

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def chat(
    vectordb_location: str,
    embedding_import: ClassImportDefinition,
    vectordb_import: ClassImportDefinition,
    llm_import: ClassImportDefinition,
    llm_parameters,
    prompt_parameters,
    output_file,
) -> object:
    module = importlib.import_module(embedding_import.module_name)
    class_ = getattr(module, embedding_import.class_name)
    embedding = class_()

    logging.warn(
        "CAUTION: This function uses external compute services "
        "(like OpenAI or HuggingFace). This is likely to cost money."
    )
    module = importlib.import_module(vectordb_import.module_name)
    class_ = getattr(module, vectordb_import.class_name)
    vectordb = class_(embedding_function=embedding, persist_directory=vectordb_location)

    module = importlib.import_module(llm_import.module_name)
    class_ = getattr(module, llm_import.class_name)
    llm = class_(**llm_parameters)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        # output_key = 'answer',
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectordb.as_retriever(),
        memory=memory,
        # return_source_documentsTrue,
    )

    # NOTE: trial API keys may have very restrictive rules. It is plausible that you run into
    # constraints after the 2nd question.
    for question in prompt_parameters:
        result = qa({"question": question})
        chat_output(question, result)
        chat_output_to_file(result, output_file)

    logging.info("=======================")

    return qa


def chat_output(question: str, result: dict) -> None:
    logging.info("=======================")
    logging.info(f"Q: {question}")
    logging.info(f"A: {result['answer']}")


# TODO: Either I do not understand mdutils or it is an unfriendly package when trying to append.
def chat_output_to_file(result: dict, output_file) -> None:
    first_write = not os.path.isfile(output_file["path"])

    mdFile = MdUtils(file_name="tmp.md")

    if first_write:
        mdFile.new_header(1, "LLM Chat Session with quke")
        mdFile.write(
            datetime.now().astimezone().strftime("%a %d-%b-%Y %H:%M %Z"), align="center"
        )
        mdFile.new_paragraph("")
        mdFile.new_header(2, "Experiment settings", header_id="settings")
        mdFile.insert_code(output_file["conf_yaml"], language="yaml")
        mdFile.new_header(2, "Chat", header_id="chat")
    else:
        existing_text = MarkDownFile().read_file(file_name=output_file["path"])
        mdFile.new_paragraph(existing_text)

    mdFile.new_paragraph(f"Q: {result['question']}")
    mdFile.new_paragraph(f"A: {result['answer']}")

    new = MarkDownFile(name=output_file["path"])

    new.append_end((mdFile.get_md_text()).strip())
