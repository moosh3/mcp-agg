#!/usr/bin/env python3
import argparse
import os
import re
import requests
from urllib.parse import urljoin, urlparse
import logging
import sys

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Index a website\'s llms.txt into folders')
    parser.add_argument('-n', '--name', required=True, help='Name of the project')
    parser.add_argument('-u', '--url', required=True, help='URL to the llms.txt file')
    return parser.parse_args()

def download_file(url, output_path, logger):
    """Download a file from a URL to the specified output path."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the content to the file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Downloaded: {url} -> {output_path}")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        return None

def extract_links(content, base_url):
    """Extract markdown and text links from content."""
    # Pattern to match markdown links and plain URLs ending with .md or .txt
    pattern = r'\[([^\]]+)\]\(([^)]+\.(?:md|txt))\)|(?:^|\s)(https?://\S+\.(?:md|txt))'
    
    # Pattern to match GitHub repository links (but not specific files)
    github_pattern = r'\[([^\]]+)\]\((https?://github\.com/[^/]+/[^/)]+)(?:/?\))|(?:^|\s)(https?://github\.com/[^/\s]+/[^\s/]+)(?!/\S+)'
    
    links = []
    # Process regular markdown and text links
    for match in re.finditer(pattern, content):
        if match.group(2):  # Markdown link
            link = match.group(2)
        else:  # Plain URL
            link = match.group(3)
        
        # Make sure the link is absolute
        absolute_link = urljoin(base_url, link)
        links.append(absolute_link)
    
    # Process GitHub repository links (only for README.md)
    for match in re.finditer(github_pattern, content):
        if match.group(2):  # Markdown link
            repo_url = match.group(2)
        else:  # Plain URL
            repo_url = match.group(3)
        
        # Add README.md URL for GitHub repositories
        if repo_url:
            readme_url = f"{repo_url.rstrip('/')}/raw/main/README.md"
            links.append(readme_url)
            
            # Alternative branch name in case main doesn't exist
            readme_master_url = f"{repo_url.rstrip('/')}/raw/master/README.md"
            links.append(readme_master_url)
    
    return links

def sanitize_filename(url):
    """Create a sanitized, flat filename from a URL."""
    parsed_url = urlparse(url)
    
    # Start with the netloc (domain)
    parts = [parsed_url.netloc]
    
    # Add path without extension
    path = parsed_url.path.strip('/')
    
    # If this is a GitHub README URL, handle it specially
    if 'github.com' in parsed_url.netloc and '/raw/' in parsed_url.path and 'README.md' in parsed_url.path:
        # Extract organization and repository name
        path_segments = parsed_url.path.split('/')
        if len(path_segments) >= 5:
            # Format: /org/repo/raw/branch/README.md
            org = path_segments[1]
            repo = path_segments[2]
            return f"github-{org}-{repo}-README.md"
    
    # For other URLs, create a flattened name
    if path:
        # Remove file extension first
        base_path = os.path.splitext(path)[0]
        # Replace slashes and other invalid chars with dashes
        sanitized_path = re.sub(r'[\\/*?:"<>|]', '-', base_path)
        sanitized_path = sanitized_path.replace('/', '-')
        parts.append(sanitized_path)
    
    # Rejoin with dashes and add original extension
    base = '-'.join(parts)
    
    # Get original extension
    ext = os.path.splitext(parsed_url.path)[1]
    if not ext:
        ext = '.txt'  # Default extension if none is found
    
    # Limit filename length to avoid issues on some filesystems
    if len(base) > 200:
        base = base[:200]
    
    return f"{base}{ext}"

def determine_output_path(url, base_dir):
    """Determine the flat output path for a file based on its URL."""
    filename = sanitize_filename(url)
    return os.path.join(base_dir, filename)

def process_file(url, base_dir, visited, logger, base_url=None, depth=0):
    """Process a file and extract its links."""
    if url in visited:
        logger.debug(f"Already processed: {url}")
        return
    
    # Check if this is a GitHub README.md URL (raw/main or raw/master)
    is_github_readme = '/raw/main/README.md' in url or '/raw/master/README.md' in url
    
    # Only add to visited if not a GitHub README or if it's successful
    if not is_github_readme:
        visited.add(url)
    
    if base_url is None:
        base_url = url
    
    output_path = determine_output_path(url, base_dir)
    content = download_file(url, output_path, logger)
    
    # For GitHub READMEs, we try both main and master branches, so mark as visited only if successful
    if content and is_github_readme:
        visited.add(url)
    
    # Only extract and process links from the initial file (depth 0)
    # For GitHub READMEs and direct links, we don't process further
    if content and depth == 0:
        links = extract_links(content, url)
        for link in links:
            process_file(link, base_dir, visited, logger, base_url, depth + 1)

def main():
    """Main function."""
    logger = setup_logging()
    args = parse_arguments()
    
    # Create base directory
    base_dir = os.path.join("./docs", args.name)
    os.makedirs(base_dir, exist_ok=True)
    
    logger.info(f"Starting indexing of {args.url} into {base_dir}")
    
    # Process the initial file with depth=0
    visited = set()
    process_file(args.url, base_dir, visited, logger, depth=0)
    
    logger.info(f"Indexing complete. Processed {len(visited)} files.")

if __name__ == "__main__":
    main()