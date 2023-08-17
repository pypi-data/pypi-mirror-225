from openxlab.dataset.commands.utility import ContextInfo
from openxlab.types.command_type import *


class Commit(BaseCommand):
    """Commit local changes"""
    
    def get_name(self) -> str:
        return "commit"
    
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "dataset_repo_name",
            type = str,
        )
        parser.add_argument(
            "--commit_message",
            "-m",
            type = str,
            required = True
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_name = parsed_args.dataset_repo_name
        commit_message = parsed_args.commit_message
        
        ctx = ContextInfo()
        client = ctx.get_client()
                
        req_data_list = [f"{dataset_name}", {"msg" : f"{commit_message}"}]
        client.get_api().commit_dataset(req = req_data_list)
        
        return 0