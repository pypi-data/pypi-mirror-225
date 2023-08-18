# Release History

## 0.1.2 (2023-08-18)

**Added**
 - feat: add `har2pytest` command to convert .har file into pytest script file directly.

**Changed**

- change: support execute `domore run` or `dorun` command to run `.json` `.yaml` `.yml` `.py` `.har` file directly.
- change: some other optimizations.
- change: remove command `hrun`.
- change: extract API name within HTTP request into different class and as class name.

## 0.1.2 (2023-07-27)

**Changed**

- change: revise prompt message of command line

## 0.1.1 (2023-07-27)

**Added**

- feat: integrate [locust](https://locust.io/) v1.0
- feat: add `--profile` flag for har2case to support overwrite headers/cookies with specified yaml/json configuration file
- feat: support variable and function in response extract expression
- feat: add optional message for assertion
- feat: implement step setup/teardown hooks
- feat: support alter response in teardown hooks
- feat: add sentry sdk
- feat: extract session variable from referenced testcase step
- feat: make pytest files in chain style
- feat: `hrun` supports run pytest files
- feat: get raw testcase model from pytest file
- feat: make referenced testcase as pytest class

**Fixed**

- fix: pydantic validation error when body is None
- fix: only convert jmespath path for some fields in white list
- fix: parse upload info with session variables
- fix: catch exceptions caused by GA report failure
- fix: catch exceptions when getting socket address failed
- fix: keep negative index in jmespath unchanged when converting pytest files, e.g. body.users[-1]
- fix: variable should not start with digit
- fix: ignore comments and blank lines when parsing .env file
- fix: parameterize failure caused by pydantic version
- fix: ImportError caused by jinja2 version
- fix: failure in getting client and server IP/port when requesting HTTPS
- fix: upgrade dependencies for security
- fix: chinese garbled in response
- fix: incorrect variables and variable type hints
- fix: display error in request body if the list inputted from with_json() contains dict
- fix: validation failed when validation-value is in string format
- fix: decode brotli encoding
- fix: parameters feature with custom functions
- fix: request json field with variable reference
- fix: pickle BufferedReader TypeError in upload feature
- fix: validate with variable or function whose evaluation result is "" or not text
- fix: raise TestCaseFormatError if teststep validate invalid
- fix: raise TestCaseFormatError if ref testcase is invalid
- fix: missing setup/teardown hooks for referenced testcase
- fix: compatibility for `black` on Android termux that does not support multiprocessing well
- fix: mishandling of request header `Content-Length` for GET method
- fix: validate with jmespath containing variable or function, e.g. `body.locations[$index].name`
- fix: ValueError when type_match None
- fix: override referenced testcase export in teststep
- fix: avoid duplicate import
- fix: override locust weight
- fix: path handling error when har2case har file and cwd != ProjectRootDir
- fix: missing list type for request body
- fix: avoid '.csv' been converted to '_csv'
- fix: convert har to JSON format testcase
- fix: missing ${var} handling in overriding config variables
- fix: SyntaxError caused by quote in case of headers."Set-Cookie"
- fix: FileExistsError when specified project name conflicts with existed file
- fix: testcase path handling error when path startswith "./" or ".\\"
- fix: incorrect summary success when testcase failed
- fix: reload to refresh previously loaded debugtalk module
- fix: escape $$ in variable value
- fix: miss formatting referenced testcase
- fix: handle cases when parent directory name includes dot/hyphen/space
- fix: ensure converted python file in utf-8 encoding
- fix: duplicate running referenced testcase
- fix: ensure compatibility issues between testcase format v2 and v3
- fix: ensure compatibility with deprecated cli args in v2, include --failfast/--report-file/--save-tests
- fix: UnicodeDecodeError when request body in protobuf
- fix: convert jmespath.search result to int/float unintentionally
- fix: referenced testcase should not be run duplicately
- fix: requests.cookies.CookieConflictError, multiple cookies with name
- fix: missing exit code from pytest
- fix: skip invalid testcase/testsuite yaml/json file
- fix: missing request json
- fix: override testsuite/testcase config verify
- fix: only strip whitespaces and tabs, \n\r are left because they maybe used in changeset
- fix: log testcase duration before raise ValidationFailure
- fix: compatibility with different path separators of Linux and Windows
- fix: IndexError in ensure_file_path_valid when file_path=os.getcwd()
- fix: ensure step referenced api, convert to v3 testcase
- fix: several other compatibility issues

**Changed**

- change: add `--tb=long` for `hrun` command to use shorter traceback format by default
- change: load yaml file with FullLoader
- change: remove support for dead python 3.6, upgrade supported python version to 3.7/3.8/3.9/3.10/3.11
- change: replace events reporter from sentry to Google Analytics
- change: override variables strategy, step variables > extracted variables from previous steps
- change: import locust at beginning to monkey patch all modules
- change: open file in binary mode
- change: make converted referenced pytest files always relative to ProjectRootDir
- change: log function details when call function failed
- change: do not raise error if failed to get client/server address info
- change: skip reporting sentry for errors occurred in debugtalk.py
- change: make `allure-pytest`, `requests-toolbelt`, `filetype` as optional dependencies
- change: move all unittests to tests folder
- change: save testcase log in PWD/logs/ directory
- change: `har2case` generate pytest file by default
- change: add domore version in generated pytest file
- change: add `export` keyword in TStep to export session variables from referenced testcase
- change: rename TestCaseInOut field, config_vars and export_vars
- change: rename StepData field, export_vars
- change: search debugtalk.py upward recursively until system root dir

## 0.1.0 (2023-07-20)

**Added**

- feat: dump log for each testcase
- feat: add default header `HRUN-Request-ID` for each testcase
- feat: add `make` sub-command to generate python testcases from YAML/JSON
- feat: format generated python testcases with [`black`](https://github.com/psf/black)
- feat: make testsuite and run testsuite
- feat: testcase/testsuite config support getting variables by function
- feat: har2case with request cookies
- feat: log request/response headers and body with indent
- feat: each testcase has an unique id in uuid4 format
- feat: builtin allure report
- feat: dump log for each testcase
- 
**Fixed**

- fix: compatibility with testcase file path includes dots, space and minus sign
- fix: testcase generator, validate content.xxx => body.xxx
- fix: extract response cookies
- fix: handle errors when no valid testcases generated
- fix: ensure referenced testcase share the same session

**Changed**

- remove support for Python 2.7
- replace logging with [loguru](https://github.com/Delgan/loguru)
- replace string format with f-string
- remove dependency colorama and colorlog
- generate reports/logs folder in current working directory
- remove cli `--validate`
- remove cli `--pretty`
- remove sentry sdk
- refactor all
- replace jsonschema validation with pydantic
- remove compatibility with testcase/testsuite format v1
- replace unittest with pytest
- remove builtin html report, allure will be used with pytest later
- remove locust support temporarily
- update command line interface
- remove default added `-s` option for hrun