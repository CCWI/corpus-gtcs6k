# Corpus on German topic classification and success (GTCS6k)
In this repository we provide the data set for the corpus on German topic classification and success (GTCS6k). Please see the [corpus website](https://ccwi.github.io/corpus-gtcs6k/) for more information about the corpus.

## How to get started?
We provide the corpus to the scientific community. However, for legal reasons, we are not allowed to share the entire data of the posts directly. In order to still publish the corpus while respecting the rights of third parties, we instead provide the annotations along with the IDs of the posts and a script that allows interested readers to retrieve the posts of the corpus on their own.

Requirement: You need a Facebook app that has successfully passed the review and holds the *Public Page Content Access* permission.

Necessary steps for the retrieval of the posts:
 1. Edit the file `data/config.py` and add your Facebook Access Token
 1. Run `data/retreive_posts.py` to retrieve the posts
 1. Open `data/posts.json` to inspect the posts

## Experiments
The usage of the experiments is described in a spearate [README](experiments/README.md) in the experiments folder.

 ## License
The software in this repository is available under the MIT license ([LICENSE](LICENSE)).

The corpus itself however is provided under the terms of the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](http://creativecommons.org/licenses/by-nc-sa/4.0/). By using the corpus you agree to this license.
