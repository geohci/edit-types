[![Build status](https://github.com/geohci/edit-types/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/geohci/edit-types/actions/workflows/test.yml)

# mwedittypes
Edit diffs and type detection for Wikipedia.
The goal is to transform unstructured edits to Wikipedia articles into a structured summary of what actions were taken in the edit.
The library has two major formats (and associated algorithms):
* Simple summary: fast computation of changes that results in a basic summary of counts of changes
* Structured summary: slow but more context-aware computation that provides details of each specific change

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

This repository would return this in the following structure:
* Simple: `{'Template':{'change':1}, 'Wikilink':{'insert':1}`
* Structured: `{'Template':[('parameter', {'1': 'Austrian painter'}, {'1': 'Austrian landscape painter'})], 'Wikilink':[('title', None, 'Olomouc')]}`

### Basic Usage
Simple:
```
>>> from mwedittypes import SimpleEditTypes
>>> prev_wikitext = '{{Short description|Austrian painter}}'
>>> curr_wikitext = '{{Short description|Austrian [[landscape painter]]}}'
>>> et = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en')
>>> et.get_diff()
{'Wikilink': {'insert': 1}, 'Template': {'change': 1}, 'Section': {'change': 1}}
```

Structured:
```
>>> from mwedittypes import StructuredEditTypes
>>> prev_wikitext = '{{Short description|Austrian painter}}'
>>> curr_wikitext = '{{Short description|Austrian [[landscape painter]]}}'
>>> et = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
>>> et.get_diff()
{'context': [Context(type='Section', edittype='change', count=1)],
 'node-edits': [NodeEdit(type='Wikilink', edittype='insert', section='0: Lede', name='landscape painter',
                         changes=[('title', None, 'landscape painter')]),
                NodeEdit(type='Template', edittype='change', section='0: Lede', name='Short description',
                         changes=[('parameter', ('1', 'Austrian painter'), ('1', 'Austrian [[landscape painter]]'))])],
 'text-edits': []}
```

In most cases (~90%), the two approaches agree in their overall results. They differ in the following situations:
* Very large diffs -- when `timeout` is set to `True`, the StructuredEditTypes class is more likely to fall-back to a simple diff and miss some details as a result
* Content moves -- the simplified library cannot detect moves
* Changes vs. Inserts+Removes -- the simplified library does not distinguish between e.g., a template being changed vs. a template being removed and separate template being inserted 

A good example of a diff where they vary in outputs is revision 1107840666 on English Wikipedia ([diff](https://en.wikipedia.org/w/index.php?diff=1107840666&oldid=1094519551&title=Blumenthal,_Saskatchewan&diffmode=source); [model output](https://wiki-topic.toolforge.org/diff-tagging?lang=en&revid=1107840666)).

## Language Coverage
Almost everything in this library is language-agnostic and so works consistently for any language of Wikipedia.
For links, the namespace identification varies but we use a list of prefixes that covers all languages (at the time of generation).
Sentences are semi-challenging in that we must build a list of sentence-ending punctuation that covers all languages. We believe we have done a good job of this but have not explicitly tested this. The list can be found in `mwedittypes/constants.py` under `SENTENCE_BREAKS_REGEX`.
Words are the most challenging aspect and the one place where you will see varying behavior. For them we take two strategies:
* For most languages, we split text based on whitespace. This is the default behavior.
* There are many languages that either don't separate words with whitespace or use whitespace to instead delineate syllables. These can be found in `mwedittypes/constants.py` under `NON_WHITESPACE_LANGUAGES`. For these languages, we instead report the number of characters affected.

## Known Issues
Wikitext/language is verrrrrrry complicated and so there are certain things we can't feasibly extract consistently. The ones we know about:
* Sentences: full stop punctuation is used for [many things](https://en.wikipedia.org/wiki/Full_stop#Usage). Abbreviations are particularly challenging and will falsely split up sentences. On the other hand, Thai has no sentence punctuation so each paragraph is (incorrectly) considered the equivalent of a single sentence. 
* Words: we have done our best to extract words for whitespace-delimited languages but some languages use special spacing characters that may falsely split up words -- e.g., Bengali. We have done our best to detect account for these languages but may have missed some.
* Media: images/audio/video can be included in articles via bracketed links, templates, and galleries. Each have their own syntax, and, in particular templates separate the image name from its formatting options. For galleries/bracket-links, we associate the formatting/caption options with the media and changes to them will trigger as media changes. For templates, we cannot do this.
* Text Formatting: parsing text formatting is quite complicated and context-dependent. We parse the wikitext section-by-section so text formatting split up between sections might parse unexpectedly.

For links, we assume that if the prefix is not for media or a category, the link is a wikilink to namespace 0. This is generally reasonable for current versions of Wikipedia articles
but would overload the `Wikilink` class with e.g., user page links on talk pages or interwiki links for older versions of articles.

## Development
We are happy to receive contributions though will default to keeping the code here relatively general (not overly customized to individual use-cases).
Please reach out or open an issue for the changes you would like to merge so that we can discuss beforehand.

### Code Summary -- StructuredEditTypes
The code for computing diffs and running edit-type detection can be found in two files:
* `mwedittypes/tree_differ.py`: this is the first stage of the diffing pipeline that detects high-level changes.
* `mwedittypes/node_differ.py`: this is the second stage of the diffing pipeline that takes the tree_differ output and gathers the specific details of each change.

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

The bulk of the library parses a wikitext document into a bag of nodes (Templates, Wikilinks, etc.). This uses largely the same parsing approach as `StructuredEditTypes`

The diffing component simply takes the symmetric difference of the nodes associated with each wikitext document to identify what has changed and then summarizes the counts.

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

