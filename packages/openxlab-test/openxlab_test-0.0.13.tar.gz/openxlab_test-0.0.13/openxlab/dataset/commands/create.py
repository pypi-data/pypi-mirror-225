from rich import print as rprint

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.types.command_type import *


class Create(BaseCommand):
    """Create a dataset repo"""
    
    def get_name(self) -> str:
        return "create"
    
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "dataset_repo_name",
            # "-n",
            # required=True,
            help = (
                'Desired dataset name'
            ),
        )

    def take_action(self,  parsed_args: Namespace) -> int:
        dataset_name = parsed_args.dataset_repo_name

        ctx = ContextInfo()
        client = ctx.get_client()
        req_data_dict = {
            "name": f"{dataset_name}",
            "displayname": f"{dataset_name}"
            }
        resp_data_dict = client.get_api().create_dataset(req = req_data_dict)       
        rprint(f"Dataset named: [blue]{resp_data_dict['name']}[/blue] create success!")
        
        return 0
