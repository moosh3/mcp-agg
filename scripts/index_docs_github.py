#!/usr/bin/env python3
import argparse
import os
import re
import requests
import logging
import sys
from urllib.parse import urlparse

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='recursively fetch .md & .markdown files from a github repo'
    )
    parser.add_argument('-n', '--name', required=True, help='name of the directory to store files')
    parser.add_argument('-u', '--url', required=True, help='github repo url')
    return parser.parse_args()

def sanitize_filename(path):
    """flat filename from path, in case you want a single-level folder."""
    sanitized = re.sub(r'[\\:*?"<>|]', '-', path)
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    return sanitized

def get_repo_info(repo_url):
    repo_url = repo_url.rstrip('/')
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    parsed = urlparse(repo_url)
    parts = [p for p in parsed.path.split('/') if p]
    if len(parts) < 2:
        raise ValueError(f'invalid github repository url: {repo_url}')
    owner, repo = parts[0], parts[1]
    return owner, repo

def github_get(url, logger):
    """wrapper for GET requests to the github api, handling optional token."""
    headers = {}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['authorization'] = f'token {token}'
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logger.warning(f'github api error: {e} for {url}')
        return None

def download_file(download_url, out_path, logger):
    headers = {}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['authorization'] = f'token {token}'
    try:
        r = requests.get(download_url, headers=headers, timeout=20)
        r.raise_for_status()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'wb') as f:
            f.write(r.content)
        logger.info(f'downloaded {download_url} -> {out_path}')
    except requests.RequestException as e:
        logger.warning(f'failed to download {download_url}: {e}')

def recurse_directory(api_url, base_dir, prefix_path, owner, repo, logger):
    contents = github_get(api_url, logger)
    if not contents or not isinstance(contents, list):
        return
    
    for item in contents:
        item_type = item.get('type')
        name = item.get('name')
        
        if item_type == 'dir':
            # go deeper
            sub_api_url = item.get('url')
            if sub_api_url:
                recurse_directory(
                    sub_api_url,
                    base_dir,
                    os.path.join(prefix_path, name),
                    owner,
                    repo,
                    logger
                )
        elif item_type == 'file':
            # check if .md or .markdown
            if name.lower().endswith('.md') or name.lower().endswith('.markdown'):
                # either flatten paths or preserve directory structure
                # here we preserve directory structure under base_dir
                out_path = os.path.join(base_dir, prefix_path, name)
                download_file(item['download_url'], out_path, logger)

def main():
    logger = setup_logging()
    args = parse_arguments()
    owner, repo = get_repo_info(args.url)
    logger.info(f'owner: {owner}, repo: {repo}')
    
    base_dir = os.path.join('docs', args.name)
    os.makedirs(base_dir, exist_ok=True)
    
    # start from root of the repo
    root_api_url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    
    # The recurse_directory function is already set up to handle subdirectories
    # We just need to ensure it's called properly from the root
    recurse_directory(root_api_url, base_dir, '', owner, repo, logger)

if __name__ == '__main__':
    main()