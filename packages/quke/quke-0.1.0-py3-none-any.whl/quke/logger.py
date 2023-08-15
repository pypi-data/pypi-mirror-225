import logging


# TODO: All my logged messages have a class/module of xxx.logger. This is not useful.
class FunctionInfoFilter(logging.Filter):
    def filter(self, record):
        record.class_name = (
            record.funcName.split(".")[0] if "." in record.funcName else None
        )
        record.function_name = record.funcName.split(".")[-1]
        return True


# Create the base logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create the formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(module)s - %(class_name)s - %(function_name)s - %(message)s"
)

# Create the handler and attach the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# TODO: Logger messages appear twice, differently formatted.
# Presumably since logger already exists. Replace instead of addHandler()?
# Add the handler to the logger
# logger.addHandler(handler)

# Add the FunctionInfoFilter to include class and function names in log messages
logger.addFilter(FunctionInfoFilter())
