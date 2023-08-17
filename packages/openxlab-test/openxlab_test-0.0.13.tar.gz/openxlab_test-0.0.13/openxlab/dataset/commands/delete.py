from argparse import ArgumentParser
from argparse import Namespace

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.types.command_type import *


class Delete(BaseCommand):
    """ "Delete repository for user"""

    def get_name(self) -> str:
        return "delete"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("dataset_repo_name", help="The dataset repo you want to delete")

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_repo_name = parsed_args.dataset_repo_name

        ctx = ContextInfo()
        client = ctx.get_client()
        parsed_ds_name = dataset_repo_name.replace("/", ",")
        print(f"Delete {dataset_repo_name}...")
        delete_flag = client.get_api().delete_repo(parsed_ds_name)
        print(f"Dataset {dataset_repo_name} deleted successfully!")

        return 0
