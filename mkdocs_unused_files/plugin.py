import os
import logging
import urllib.parse
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from bs4 import BeautifulSoup

log = logging.getLogger('mkdocs')

class UnusedFilesPlugin(BasePlugin):

    file_list = []

    config_scheme = (
        ('dir', config_options.Type(str, default='')),
        ('file_types',config_options.Type((str, list), default=[])),
    )

    def matches_type(self, str):
        types = self.config["file_types"]
        return not types or (str and str.endswith(tuple(types)))

    def on_files(self, files, config):
        dir = os.path.join(config.docs_dir, self.config["dir"])
        # Get all files in directory
        for path, _, files in os.walk(dir):
            for file in files:
                # Add all files with the given types to file_list
                # If no types were given, add all files except Markdown files
                if not file.endswith("md") and self.matches_type(file):
                    rel_dir = os.path.relpath(path, config.docs_dir)
                    rel_file = file if (rel_dir == ".") else os.path.join(rel_dir, file)
                    self.file_list.append(rel_file)

    def on_page_content(self, html, page, config, files):
        soup = BeautifulSoup(html, 'html.parser')
        ref_list = []
        # Get all file references in <a href="...">
        for a in soup.find_all('a', href=self.matches_type):
            href = urllib.parse.unquote(a['href'])
            if config.use_directory_urls:
                href = href.replace('..' + os.path.sep, '', 1)
            href = os.path.join(os.path.dirname(page.file.src_uri), href)
            ref_list.append(href)

        # Get all file references in <img src="...">
        for img in soup.find_all('img', src=self.matches_type):
            src = urllib.parse.unquote(img['src'])
            if config.use_directory_urls:
                src = src.replace('..' + os.path.sep, '', 1)
            src = os.path.join(os.path.dirname(page.file.src_uri), src)
            ref_list.append(src)

        # Remove all referenced files from file list
        self.file_list = [i for i in self.file_list if i not in ref_list]

    def on_post_build(self, config):
        if self.file_list:
            log.info('The following files exist in the docs directory, but may be unused:\n  - {}'.format('\n  - '.join(self.file_list)))

