# edit-types
Edit diffs and type detection for Wikipedia.

## Code
The code for computing diffs and running edit-type detection can be found in two files:
* `edit-types/tree_differ.py`: this is the first stage of the diffing pipeline that detects high-level changes.
* `edit-types/node_differ.py`: this is the second stage of the diffing pipeline that takes the tree_differ output, further processes it, and counts up the edit types.

## Documentation
* For more background, see: https://meta.wikimedia.org/wiki/Research:Wikipedia_Edit_Types
* To test out the code, see: https://wiki-topic.toolforge.org/diff-tagging?lang=en
* To see how the code is used in an API, see: https://github.com/wikimedia/research-api-endpoint-template/tree/edit-types

