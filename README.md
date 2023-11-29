# liquid-tag-parser

## What is it? 

This is an auxiliary Python script that we use for specific problem. The problem it solves is the following. We have a JSON file and we use the objects from this JSON in other files. We want to make sure that there are no objects that we don't use.
So, the script does three things:
1. Parse JSON and save all JSON objects (aka translation keys) on the third level as `category.group.parameter`
2. Parses the directories with files using these objects and save all objects references
3. Cehck the set difference between the set from p.1 and the set from p.2
4. Prints in console the unused JSON objects if any

## Using as Git action

You can run the script as a Github action, for example, when someone creates a new PR.

1. Create a `yaml` file in `.github/workflows` directory.
2. Copy the following snippet into `yaml` file:
```
name: Your script name

on: 
  pull_request:    
    branches: [ "main", "test", "develop" ]

  workflow_dispatch:

jobs:
  links-checker:
    name: json-tags-checker
    runs-on: ubuntu-latest
    steps:
    - name: Normal checkout
      uses: actions/checkout@v3
      
    - name: Check-out checker repository
      uses: actions/checkout@v2
      with:
        repository: paveltovchigrechko/liquid-tag-parser
        path: "liquid-tag-parser"
        
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Run parser
      run: python3 liquid-tag-parser/check_t_tags.py      
``` 

