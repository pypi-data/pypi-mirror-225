import os

from tqdm import tqdm

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.constants import FILE_THRESHOLD
from openxlab.dataset.io import downloader
from openxlab.types.command_type import *


class Get(BaseCommand):
    """Get a whole dataset"""
    
    def get_name(self) -> str:
        return "get"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "dataset_repo_name",
            type = str,
        )
        parser.add_argument(
            "--destination_path",
            "-d",
            type = str,
            # required = True
        )

    def take_action(self, parsed_args: Namespace) -> int:
        dataset_name = parsed_args.dataset_repo_name
        detination_path = parsed_args.destination_path
        if not detination_path:
            detination_path = os.getcwd()
        
        ctx = ContextInfo()
        client = ctx.get_client()
              
        # parse dataset_name 
        parsed_ds_name = dataset_name.replace("/",",")
        parsed_save_path = dataset_name.replace("/","___")
        
        
        data_dict = client.get_api().get_dataset_files(dataset_name=parsed_ds_name)
        info_dataset_id = data_dict['list'][0]['dataset_id']

        object_info_list = []
        for info in data_dict['list']:
            curr_dict = {}
            curr_dict['size'] = info['size']
            curr_dict['name'] = info['path'][1:]
            object_info_list.append(curr_dict)
        
        with tqdm(total = len(object_info_list)) as pbar:
            for idx in range(len(object_info_list)):
                # exist already
                print(f"Downloading No.{idx+1} of total {len(object_info_list)} files")
                if os.path.exists((os.path.join(detination_path, parsed_save_path, object_info_list[idx]['name']))):
                    print(f"target already exists, jumping to next !")
                    pbar.update(1)
                    continue

                # big file download
                if object_info_list[idx]['size'] > FILE_THRESHOLD:
                    download_url = client.get_api().get_dataset_download_urls(info_dataset_id, object_info_list[idx])
                    downloader.BigFileDownloader(url = download_url,
                                                filename = object_info_list[idx]['name'],
                                                download_dir = os.path.join(detination_path, parsed_save_path),
                                                blocks_num = 4).start()
                    pbar.update(1)
                
                # small file download    
                else:
                    download_url = client.get_api().get_dataset_download_urls(info_dataset_id, object_info_list[idx])
                    downloader.SmallFileDownload(url = download_url,
                                                 filename = object_info_list[idx]['name'],
                                                 download_dir = os.path.join(detination_path, parsed_save_path)
                                                 )._single_thread_download()
                    pbar.update(1)

        print(f"\nDownload Complete!")
        return 0