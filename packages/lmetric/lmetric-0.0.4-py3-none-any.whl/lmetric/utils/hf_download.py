from huggingface_hub import snapshot_download, hf_hub_download
import argparse

# https://huggingface.co/docs/huggingface_hub/guides/download

def download_hf_repo(repo_id, repo_type=None, filename=None, white_patterns=None, black_patterns=None,
                     save_dir=None, save_with_symlinks=False, revision=None):
    """
    Download a repository from Hugging Face Hub or create a snapshot.

    Args:
        repo_id (str): Identifier of the repository in the Hugging Face Hub.
        repo_type (str, optional): Type of the repository. Defaults to None.
        filename (str, optional): File name to download. Defaults to None.
        white_patterns (List[str], optional): List of patterns for including files. Defaults to None.
        black_patterns (List[str], optional): List of patterns for excluding files. Defaults to None.
        save_dir (str, optional): Directory to save the downloaded repository. Defaults to None.
        save_with_symlinks (bool, optional): Whether to use symlinks when saving locally. Defaults to False.
        revision (str, optional): Revision of the repository. Defaults to None.

    Returns:
        None

    Raises:
        SomeException: Description of the exception raised.

    Examples:
        
        download_hf_repo('NousResearch/llama2-7b-hf', save_dir='llama2-7b)

    """

    if filename is not None:
        hf_hub_download(repo_id=repo_id, repo_type=repo_type, filename=filename,
                        local_dir=save_dir, local_dir_use_symlinks=save_with_symlinks,
                        revision=revision)
    else:
        snapshot_download(repo_id=repo_id, repo_type=repo_type,
                          allow_patterns=white_patterns, ignore_patterns=black_patterns,
                          local_dir=save_dir, local_dir_use_symlinks=save_with_symlinks,
                          revision=revision)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--repo_id', required=True, type=str, help='repo id in hf')
    parser.add_argument('--filename', type=str, help='file name you want to download')
    parser.add_argument('--white_patterns', type=str, nargs='+', help='white file patterns')
    parser.add_argument('--black_patterns', type=str, nargs='+', help='black file patterns')
    parser.add_argument('--save_dir', type=str, help='save location if you do not want cache')
    parser.add_argument('--save_with_symlinks', type=str, help='whether use symlinks when saving locally')
    parser.add_argument('--revision', type=str, help='revision')

    args = parser.parse_args()
    kwargs = vars(args)

    download_hf_repo(**kwargs)