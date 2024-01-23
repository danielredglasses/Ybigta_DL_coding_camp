import argparse
import logging
from utils.command_handler import CommandHandler
from utils.command_parser import CommandParser

# TODO 1-1: Use argparse to parse the command line arguments (verbose and log_file).
# TODO 1-2: Set up logging and initialize the logger object.

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action = "store_true")
parser.add_argument("--log_path", help = "path to store log file")

args = parser.parse_args()

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=args.log_path, filemode="w",
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

command_parser = CommandParser(args.verbose)
handler = CommandHandler(command_parser)

while True:
    command = input(">> ")
    logger.info(f"Input command: {command}")
    handler.execute(command)