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

    def update_ref(self, ref, page_uri, use_directory_urls):
        # If use_directory_urls is enabled, references may point 
        # to the parent directory, for which we have to compensate
        if use_directory_urls and ref.startswith("../"):
            ref = urllib.parse.unquote(ref)[3:]
        else:
            ref = urllib.parse.unquote(ref)
        # Add the path of the page containing the reference
        # and normalize for Windows compatibility
        ref = os.path.normpath(os.path.join(os.path.dirname(page_uri), ref))
        return ref

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
            ref_list.append(self.update_ref(a['href'], page.file.src_uri, config.use_directory_urls))

        # Get all file references in <img src="...">
        for img in soup.find_all('img', src=self.matches_type):
            ref_list.append(self.update_ref(img['src'], page.file.src_uri, config.use_directory_urls))

        # Remove all referenced files from file list
        self.file_list = [i for i in self.file_list if i not in ref_list]

    def on_post_build(self, config):
        if self.file_list:
            log.info('The following files exist in the docs directory, but may be unused:\n  - {}'.format('\n  - '.join(self.file_list)))

