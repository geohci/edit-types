[![Build status](https://github.com/geohci/edit-types/actions/workflows/test-app.yml/badge.svg?branch=main)](https://github.com/geohci/edit-types/actions/workflows/test-app.yml)

# edit-types
Edit diffs and type detection for Wikipedia. The goal is to transform unstructured edits to Wikipedia articles into a structured summary of what actions were taken in the edit.

Fundamentally, this requires two technologies: 1) the ability to compute diffs between revisions of wikitext, and, 2) the ability to map these diffs to specific actions.

## Example
If one revision of wikitext is as folows:
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

## Code
The code for computing diffs and running edit-type detection can be found in two files:
* `edit-types/tree_differ.py`: this is the first stage of the diffing pipeline that detects high-level changes.
* `edit-types/node_differ.py`: this is the second stage of the diffing pipeline that takes the tree_differ output, further processes it, and counts up the edit types.

## Tests
The tests for node/tree differs are contained within the `tests` directory.
They can be run via [pytest](https://docs.pytest.org/en/6.2.x/#).
We are not even close to full coverage which would be at least 12 node types (template/text/etc.) * 4 edit types (insert/remove/change/move) plus probably some non-English and more complex diff tests.

## Documentation
* For more background, see: https://meta.wikimedia.org/wiki/Research:Wikipedia_Edit_Types
* To test out the code, see: https://wiki-topic.toolforge.org/diff-tagging?lang=en
* To see how the code is used in an API, see: https://github.com/wikimedia/research-api-endpoint-template/tree/edit-types

