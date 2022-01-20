[![Python application](https://github.com/Amamgbu/edit-types/actions/workflows/test-app.yml/badge.svg?branch=main)](https://github.com/Amamgbu/edit-types/actions/workflows/test-app.yml)

# edit-types
Edit diffs and type detection for Wikipedia.

## Code
The code for computing diffs and running edit-type detection can be found in two files:
* `edit-types/tree_differ.py`: this is the first stage of the diffing pipeline that detects high-level changes.
* `edit-types/node_differ.py`: this is the second stage of the diffing pipeline that takes the tree_differ output, further processes it, and counts up the edit types.

## Tests
The tests for node/tree differs are contained within the `tests` directory.
They can be run via [pytest](https://docs.pytest.org/en/6.2.x/#).
We are not even close to full coverage which would be at least 12 node types (template/text/etc.) * 4 edit types (insert/remove/change/move) plus probably some non-English and more complex diff tests.
Run them before submitting changes but also please contribute more.

## Documentation
* For more background, see: https://meta.wikimedia.org/wiki/Research:Wikipedia_Edit_Types
* To test out the code, see: https://wiki-topic.toolforge.org/diff-tagging?lang=en
* To see how the code is used in an API, see: https://github.com/wikimedia/research-api-endpoint-template/tree/edit-types

