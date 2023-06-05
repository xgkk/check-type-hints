### [check-type-hints](https://github.com/xgkk/check-type-hints)
### [pypi](https://pypi.org/project/check-type-hints/)
### What can it do? 
It is a simple pre-commit plug-in that helps you check type hints in committed python files. Currently, only python is supported

### Main function
#### function 1: `--filter`
It can help you filter folders that you don't want to check, like tests, pytests...
#### function 2: `--method`
It helps you filter function and method names that you don't want to check, such as get, post, put, and delete in Django view
#### function 3: `--ignore/--no-ignore`
By default, the plug-in checks type-hints that are not filled in, breaking the commit code and telling you where there is a problem. If you don't want to interrupt the commit, you can enable `--ignore`, which will only prompt warnings

### Example:
#### First:
`pip install pre-commit`
`pip install check-type-hints`
#### then:
Add file **.pre-commit-config.yaml** to the project root directory.
eg:
```yaml
repos:
  - repo: local
    hooks:
      - id: typehint-check
        name: Typehint Check
        entry: check_type_hints check --no-ignore --filter tests  --filter pytests --method get --method post --method put --method patch --method delete
        language: system
        types: [ python ]
        stages: [ commit ]
        pass_filenames: false
        verbose: true
```
#### and then:
`pre-commit install`
#### and finally:
You can enjoy it!