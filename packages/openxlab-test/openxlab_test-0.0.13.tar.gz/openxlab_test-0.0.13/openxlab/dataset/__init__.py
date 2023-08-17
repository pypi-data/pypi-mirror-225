from openxlab.config import version as config_version
from openxlab.dataset.commands.commit import Commit
from openxlab.dataset.commands.create import Create
from openxlab.dataset.commands.delete import Delete
from openxlab.dataset.commands.download import Download

# from openxlab.dataset.commands.download import Download
from openxlab.dataset.commands.get import Get
from openxlab.dataset.commands.info import Info
from openxlab.dataset.commands.ls import Ls
from openxlab.dataset.commands.upload_file import UploadFile
from openxlab.dataset.commands.upload_folder import UploadFolder
from openxlab.types.command_type import *


def help():
    print("help")


class Dataset(BaseCommand):
    """Dataset Demo"""

    sub_command_list = [
        Get,
        Create,
        UploadFile,
        UploadFolder,
        Info,
        Ls,
        Commit,
        Download,
        Delete,
    ]

    def get_name(self) -> str:
        return "dataset"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--test",
            help=(" This argument is a test argument"),
        )
