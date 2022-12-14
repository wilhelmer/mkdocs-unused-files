# mkdocs-unused-files

An MkDocs plugin to find unused (orphaned) files in your project.

## Installation

Install the package with pip:

```
pip install mkdocs-unused-files
```

Enable the plugin in your mkdocs.yml:

```yaml
plugins:
  - search
  - unused_files:
      dir: 'images'
      file_types:
        - "png"
        - "jpg"
        - "svg"
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

## How It Works

When building your MkDocs project, the plugin searches for unused files of certain types in a specified directory. If unused files are found, the plugin displays an info message, listing the files.

Search is done as follows:

1. Get the list of files in the specified directory.
2. Collect all image and hyperlink references in the HTML output (`<a href="...">` and `<img src="...">`).
3. Compare the list of files with the list of references, and remove all files that have been referenced.
4. Once all pages have been processed, display an MkDocs info message listing all non-referenced files:

```bash
INFO     -  The following files exist in the docs directory, but may be unused:
            - images/image1.svg
            - images/subdir/image2.png 
```

## Options

* `dir`: The directory where to search for unused files. Path is relative to `docs_dir`. The plugin recurses all subdirectories. For example, if you specify `images` and `docs_dir` is set to `docs`, the plugin searches in `docs/images`, including all subdirectories. Defaults to `docs_dir`.
* `file_types`: List of file types the plugin should process. Defaults to `['png']`.
