# SWAHILI CLEANER
## _Best Swahili Processing Library_



Swahili Cleaner is the swahili version Text Processing library for Natural Language Processing

- ✨Magic ✨

## Features

- It can clean text by removing emojs
- Remove Unicode characters
- Cleaning the urls
- Cleaning the html elements
- remove parentheses
- remove numbers and keep text/alphabet only
- set in lowercase
- Removing stop words both Swahili and English
- Cleaning the whitespaces



## Installation



```sh
!pip install eganetswahilicleaner
```


## How to use

```sh
from eganetswahilicleaner.clean import clean_text
train['text']=train['text'].apply(clean_text)
test['text']=test['text'].apply(clean_text)

```
_Where train['text'] this is a column in a pandas dataframe_
