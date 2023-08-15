from . import DatabaseAction, ClassImportDefinition, ClassRateLimit
from . import embed
from . import llm_chat

import hydra
import logging  # functionality managed by Hydra
from omegaconf import DictConfig, OmegaConf
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class ConfigParser:
    """Turns config into a more programming friendly and consistent format.

    For core classes and functions groups configuration by
    class/function arguments for convenience.

    Provides an abstraction layer on top of the structure of the
    Hydra configuration files.
    """
    def __init__(self, cfg: DictConfig) -> None:
        """Creates configuration abstraction."""
        self.cfg = cfg

        # TODO: Read from cfg
        self.src_doc_folder = cfg.source_document_folder

        # TODO: Is this sufficiently robust? What if the user wants a folder not related to wcd/pwd?
        # Consider using os.path.isabs(path) or os.path.abspath(path). Or just pass the string and
        # 'Python will handle it'?
        self.vectordb_location = os.path.join(
            os.getcwd(),
            cfg.internal_data_folder,
            cfg.embedding.vectordb.vectorstore_location,
        )
        self.embedding_import = ClassImportDefinition(
            cfg.embedding.embedding.module_name, cfg.embedding.embedding.class_name
        )
        self.vectordb_import = ClassImportDefinition(
            cfg.embedding.vectordb.module_name, cfg.embedding.vectordb.class_name
        )
        self.llm_import = ClassImportDefinition(
            cfg.llm.module_name_llm, cfg.llm.class_name_llm
        )
        self.embedding_rate_limit = ClassRateLimit(
            cfg.embedding.embedding.rate_limit_chunks,
            cfg.embedding.embedding.rate_limit_delay,
        )
        self.embedding_kwargs = self.get_embedding_kwargs(cfg)

        self.splitter_import = ClassImportDefinition(
            cfg.embedding.splitter.module_name, cfg.embedding.splitter.class_name
        )
        self.splitter_args = self.get_args_dict(cfg.embedding.splitter.args)

        try:
            self.write_mode = DatabaseAction[
                (cfg.embedding.vectordb.vectorstore_write_mode).upper()
            ]
        except Exception:
            logging.warn(
                f"Invalid value configured for cfg.embedding.vectorstore_write_mode: "
                f"{cfg.embedding.vectordb.vectorstore_write_mode}. Using no_overwrite instead."
            )
            self.write_mode = DatabaseAction.NO_OVERWRITE

        self.questions = cfg.question.questions

        try:
            if not cfg.embed_only:
                self.embed_only = False
            else:
                self.embed_only = True
        except Exception:
            self.embed_only = False

        try:  # try statement done for testing suite
            self.output_file = os.path.join(
                hydra.core.hydra_config.HydraConfig.get()["runtime"]["output_dir"],
                cfg.experiment_summary_file,
            )
        except Exception:
            self.output_file = cfg.experiment_summary_file

    def get_embed_params(self):
        embed_parameters = {
            "src_doc_folder": self.src_doc_folder,
            "vectordb_location": self.vectordb_location,
            "embedding_import": self.embedding_import,
            "embedding_kwargs": self.embedding_kwargs,
            "vectordb_import": self.vectordb_import,
            "rate_limit": self.embedding_rate_limit,
            "splitter_params": self.get_splitter_params(),
            "write_mode": self.write_mode,
        }
        return embed_parameters

    def get_chat_params(self):
        chat_parameters = {
            "vectordb_location": self.vectordb_location,
            "embedding_import": self.embedding_import,
            "vectordb_import": self.vectordb_import,
            "llm_import": self.llm_import,
            "llm_parameters": self.get_llm_parameters(),
            "prompt_parameters": self.questions,
            "output_file": self.get_chat_session_file_parameters(self.cfg),
        }
        return chat_parameters

    def get_splitter_params(self):
        return {
            "splitter_import": self.splitter_import,
            "splitter_args": self.splitter_args,
        }

    def get_args_dict(self, cfg_sub):
        return OmegaConf.to_container(cfg_sub, resolve=True)

    def get_llm_parameters(self):
        return OmegaConf.to_container(self.cfg.llm.llm_args, resolve=True)

    def get_chat_session_file_parameters(self, cfg):
        chat_sesion_file_parameters = {
            "path": self.output_file,
            "conf_yaml": OmegaConf.to_yaml(cfg),
        }
        return chat_sesion_file_parameters

    def get_embedding_kwargs(self, cfg):
        try:
            if cfg.embedding.embedding.kwargs:
                embedding_kwargs = cfg.embedding.embedding.kwargs
            else:
                embedding_kwargs = {}
        except Exception:
            embedding_kwargs = {}
        return embedding_kwargs


@hydra.main(version_base=None, config_path="conf", config_name="config")
def slice(cfg: DictConfig) -> None:
    embed_parameters = ConfigParser(cfg).get_embed_params()

    embed.embed(**embed_parameters)
    logging.info("\n" + OmegaConf.to_yaml(cfg))

    if not ConfigParser(cfg).embed_only:
        chat_parameters = ConfigParser(cfg).get_chat_params()
        llm_chat.chat(**chat_parameters)


if __name__ == "__main__":
    slice()
