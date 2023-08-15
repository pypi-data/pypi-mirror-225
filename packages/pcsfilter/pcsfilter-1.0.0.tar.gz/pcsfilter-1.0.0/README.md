# pcsFilter
Tool for filtering out **P**ython **C**ode **S**mells by 
formatting the code and checking the code style after.

---

**pcsFilter** is a wrapper around the following tools: 
1. [blue](https://pypi.org/project/blue/)
2. [isort](https://pypi.org/project/isort/)
3. [flake8](https://pypi.org/project/flake8/)
4. [radon](https://pypi.org/project/radon/) ("cc" command)

pcsFilter runs mentioned tools in a given order. The following functionality 
is applied on top:

1. _flake8_ number of issues with details and _radon cc_ score are saved upon 
   the first run to _./.pcsFilter_ folder. The _./.pcsFilter_ folder path is 
   default and can be overriden via the output path option 
   (`-o` or `--output-path`).
2. When _pcsFilter_ is executed again the new results are compared with the 
   previous ones.
3. If new results are worse then: 
   1. a short message will be printed
   2. if "strict" (`-s` or `--strict`) option is used then:
      - _pcsFilter_ will exit with status = 1
4. New scores and their details will be saved to a default or given output path.

## Installation
```shell
pip install pcsFilter
```

## Usage
### Base
```shell
pcsFilter <path to project or file>
```

### Strict
Fail with status = 1, when new scores are worse. Has no effect during the 
first run.
```shell
pcsFilter -s <path to project or file>
pcsFilter --strict <path to project or file>
```

### Override output path
Default output path is `./.pcsFilter`. It can be overriden the following way:
```shell
pcsFilter -o <new output path> <path to project or file>
pcsFilter --output-path <new output path> <path to project or file>
```

### Help message
```shell
pcsFilter --help
```

## Contributing
Any contribution is always welcome!  
Please follow [this code of conduct](./CODE_OF_CONDUCT.md).  
[This doc](./CONTRIBUTING.md) explains contribution details.
