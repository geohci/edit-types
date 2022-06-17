[![Build status](https://github.com/geohci/edit-types/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/geohci/edit-types/actions/workflows/test.yml)

# mwedittypes
Edit diffs and type detection for Wikipedia.
The goal is to transform unstructured edits to Wikipedia articles into a structured summary of what actions were taken in the edit.

## Installation
You can install `mwedittypes` with `pip`:
```
$ pip install mwedittypes
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
There is a more full-fledged but slower approach that takes into account article structure when determining changes:
```
>>> from mwedittypes import EditTypes
>>> prev_wikitext = '{{Short description|Austrian painter}}'
>>> curr_wikitext = '{{Short description|Austrian [[landscape painter]]}}'
>>> et = EditTypes(prev_wikitext, curr_wikitext, lang='en', timeout=5)
>>> et.get_diff()
{'Wikilink': {'insert': 1}, 'Template': {'change': 1}}
```

There is also a simplified but faster approach that ignores article structure when determining changes:
```
>>> from mwedittypes import SimpleEditTypes
>>> prev_wikitext = '{{Short description|Austrian painter}}'
>>> curr_wikitext = '{{Short description|Austrian [[landscape painter]]}}'
>>> et = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en', timeout=5)
>>> et.get_diff()
{'Wikilink': {'insert': 1}, 'Template': {'change': 1}}
```

In most cases (~90%), the two approaches agree in their results. They differ in the following situations:
* Very large diffs -- the EditTypes class is more likely to fall-back to a simple diff and miss some details as a result
* Content moves -- the simplified library cannot detect moves
* Changes vs. Inserts+Removes -- the simplified library does not distinguish between e.g., a template being changed vs. a template being removed and separate template being inserted

## Development
We are happy to receive contributions though will default to keeping the code here relatively general (not overly customized to individual use-cases).
Please reach out or open an issue for the changes you would like to merge so that we can discuss beforehand.

### Code Summary -- EditTypes
The code for computing diffs and running edit-type detection can be found in two files:
* `mwedittypes/tree_differ.py`: this is the first stage of the diffing pipeline that detects high-level changes.
* `mwedittypes/node_differ.py`: this is the second stage of the diffing pipeline that takes the tree_differ output, further processes it, and counts up the edit types.

While the diffing/counting is not trivial, the trickiest part of the process is correctly parsing the wikitext into nodes (Templates, Wikilinks, etc.).
This is almost all done via the amazing [mwparserfromhell](https://github.com/earwig/mwparserfromhell) library with a few tweaks in the tree differ:
* We use link namespace prefixes -- e.g., Category:, Image: -- to separate out categories and media from other wikilinks.
* We identify some additional media files that are transcluded via templates -- e.g., infoboxes -- or gallery tags.
* We also add some custom logic for parsing `<gallery>` tags to identify nested links, etc., which otherwise are treated as text by `mwparserfromhell`.
* We use custom logic for converting wikitext into text to best match what words show up in the text of the article.

To accurately, but efficiently, describe the scale of textual changes in edits, we also use some regexes and heuristics to describe how much text was changed in an edit in the node differ.
This is generally the toughest part of diffing text but because we do not need to visually describe the diff, just estimate the scale of how much changed, we can use relatively simple methods.
To do this, we break down text changes into five categories and identify how much of each changed: paragraphs, sentences, words, punctuation, and whitespace.

### Code Summary -- SimpleEditTypes
The code for computing diffs and running edit-type detection can be found in one file `mwedittypes/simple_differ.py`.

The bulk of the library parses a wikitext document into a bag of nodes (Templates, Wikilinks, etc.). This uses largely the same parsing approach as `EditTypes`

The diffing component simply takes the symmetric difference of the nodes associated with each wikitext document to identify what has changed and then summarizes similarly to `EditTypes`.

### Testing
The tests for components are contained within the `tests` directory.
They can be run via [pytest](https://docs.pytest.org).
We are not even close to full coverage yet given the numerous node types (template, text, etc.) and four actions (insert/remove/change/move) and varying languages for e.g., Text or Category/Media nodes, but we are working on expanding coverage.

### Releases
When a release is ready, there are a few simple steps to take:
* Update the version number in `setup.py` and `mwedittypes/__init__.py` per [semantic versioning](https://semver.org/) and push to Github.
* Create a tag with the same version number (easiest to do this as part of the next step on Github).
* Make a Github release with the new version and summary of changes. This will trigger the publish to PyPi action.

Troubleshooting:
* If something fails, you can always rollback the release (Github UI) and delete the associated tag (on your local repository: `git tag -d [tag]; git push origin :[tag]`) and retry.
* This relies on a PyPi secret so you must have correct privileges on the Github repo.

## Documentation
* For more background, see: https://meta.wikimedia.org/wiki/Research:Wikipedia_Edit_Types
* To test out the code, see: https://wiki-topic.toolforge.org/diff-tagging?lang=en
* To see how the code is used in an API, see: https://github.com/wikimedia/research-api-endpoint-template/tree/edit-types

