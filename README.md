# markdown broken links

Check for broken relative links in markdown documentation

## What can it do?

This python program can be used to check broken **relative links** in your markdown documentation. It will check the following:
* If a particular relative link exists
* If a particular tag exists
* It also checks for relative links specified by href

### What it cannot do?

It cannot do the following:
* Cannot check absolute links (starting with http://)
* Cannot check tags in the same file, yet.

## Download

```
git clone git://github.com/prasantjalan/markdown-broken-links
```

## Run the demo

```
python check-broken-links.py sample_md_doc
```

sample_md_doc: Sample md pages with broken and working links. You can use these sample pages to look for link examples.

## Usage

```
python check-broken-links.py <directory_with_markdown_files>
```

