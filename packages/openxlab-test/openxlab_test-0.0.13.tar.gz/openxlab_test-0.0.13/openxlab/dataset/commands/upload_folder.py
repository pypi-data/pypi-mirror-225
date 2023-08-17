from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.io.upload import Uploader
from openxlab.types.command_type import *


class UploadFolder(BaseCommand):
    """Upload resources from local to remote"""

    def get_name(self) -> str:
        return "upload_folder"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "dataset_repo_name",
            # "-n",
            # type=str,
            # required=True,
            help=(
                "The dataset repo you want upload files."
            ),
        )
        parser.add_argument(
            "--source_path",
            "-s",
            type=str,
            required=True,
            help=(
                "The path of the file you want to upload."
            ),
        )
        parser.add_argument(
            "--destination_path",
            "-d",
            type=str,
            # required=True,
            help=(
                "The target path you want upload files."
            ),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_repo_name = parsed_args.dataset_repo_name
        source_path = parsed_args.source_path
        destination_path = parsed_args.destination_path
        
        ctx = ContextInfo()
        client = ctx.get_client().get_api()
        uploader = Uploader(client, dataset_repo_name)
        uploader.upload_folder(source_path, destination_path)
        return 0
