# mwsimpleedittypes
Edit diffs and type detection for Wikipedia (simple).
The goal is to transform unstructured edits to Wikipedia articles into a structured summary of what actions were taken in the edit.
This is a simplified version of [mwedittypes](https://pypi.org/project/mwedittypes/), which is a structure-aware version of this library that can also detect content moves and more directly identify edit types.

## Installation
You can install `mwsimpleedittypes` with `pip`:
```
$ pip install mwsimpleedittypes
```

## Example
If one revision of wikitext is as follows:
```
{{Short description|Austrian painter}}
'''Karl Josef Aigen''' (8 October 1684 – 22 October 1762) was a landscape painter, born at Olomouc.
```
and a second revision of wikitext is as follows:
```
{{Short description|Austrian landscape painter}}
'''Karl Josef Aigen''' (8 October 1684 – 22 October 1762) was a landscape painter, born at [[Olomouc]].
```
The changes that happened would be:
* The addition of `landscape` to the short description template -- this would be registered as a Template change.
* The changing of `Olomouc` to a Wikilink.
* Notably, despite this change to the template and addition of a link, the "Text" of the article has not changed.

This repository would return this in the following structure: `{'Template':{'change':1}, 'Wikilink':{'insert':1}`.

### Basic Usage
```
>>> from mwsimpleedittypes import EditTypes
>>> prev_wikitext = '{{Short description|Austrian painter}}'
>>> curr_wikitext = '{{Short description|Austrian [[landscape painter]]}}'
>>> et = EditTypes(prev_wikitext, curr_wikitext, lang='en', timeout=5)
>>> et.get_diff()
{'Wikilink': {'insert': 1}, 'Template': {'change': 1}}
```

## Development
We are happy to receive contributions though will default to keeping the code here relatively general (not overly customized to individual use-cases).
Please reach out or open an issue for the changes you would like to merge so that we can discuss beforehand.

### Code Summary
The code for computing diffs and running edit-type detection can be found in one file `mwsimpleedittypes/differ.py`.

The bulk of the library parses a wikitext document into a bag of nodes (Templates, Wikilinks, etc.).
This is almost all done via the amazing [mwparserfromhell](https://github.com/earwig/mwparserfromhell) library with a few tweaks:
* We use link namespace prefixes -- e.g., Category:, Image: -- to separate out categories and media from other wikilinks.
* We identify some additional media files that are transcluded via templates -- e.g., infoboxes -- or gallery tags.
* We also add some custom logic for parsing `<gallery>` tags to identify nested links, etc., which otherwise are treated as text by `mwparserfromhell`.
* We use custom logic for converting wikitext into text to best match what words show up in the text of the article.

The diffing component simply takes the symmetric difference of the nodes associated with each wikitext document to identify what has changed.

To accurately, but efficiently, describe the scale of textual changes in edits, we also use some regexes and heuristics to describe how much text was changed in an edit in the node differ.
This is generally the toughest part of diffing text but because we do not need to visually describe the diff, just estimate the scale of how much changed, we can use relatively simple methods.
To do this, we break down text changes into five categories and identify how much of each changed: paragraphs, sentences, words, punctuation, and whitespace.

### Testing
The tests for node/tree differs are contained within the `tests` directory.
They can be run via [pytest](https://docs.pytest.org).
We are not even close to full coverage yet given the numerous node types (template, text, etc.) and four actions (insert/remove/change/move) and varying languages for e.g., Text or Category/Media nodes, but we are working on expanding coverage.

## Documentation
* For more background, see: https://meta.wikimedia.org/wiki/Research:Wikipedia_Edit_Types
