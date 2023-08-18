import argparse
import enum
import os
import sys

import pytest
from loguru import logger

from domore import __description__, __version__, exceptions
from domore.compat import ensure_cli_args
from domore.ext.har2case import init_har2case_parser, init_har2pytest_parser, main_har2case, main_har2case_return_case_file
from domore.make import init_make_parser, main_make
from domore.scaffold import init_parser_scaffold, main_scaffold
from domore.utils import init_sentry_sdk, ga_client
init_sentry_sdk()


def init_parser_run(subparsers):
    sub_parser_run = subparsers.add_parser(
        "run", help="Make testcases and run with pytest."
    )
    return sub_parser_run


def main_run(extra_args) -> enum.IntEnum:
    ga_client.track_event("RunAPITests", "hrun")
    # keep compatibility with v2
    extra_args = ensure_cli_args(extra_args)

    tests_path_list = []
    extra_args_new = []
    for item in extra_args:
        if not os.path.exists(item):
            # item is not file/folder path
            extra_args_new.append(item)
        else:
            # item is file/folder path
            tests_path_list.append(item)

    if len(tests_path_list) == 0:
        # has not specified any testcase path
        logger.error(f"No valid testcase path in cli arguments: {extra_args}")
        sys.exit(1)

    testcase_path_list = main_make(tests_path_list)
    if not testcase_path_list:
        logger.error("No valid testcases found, exit 1.")
        sys.exit(1)

    if "--tb=long" not in extra_args_new:
        extra_args_new.append("--tb=long")

    extra_args_new.extend(testcase_path_list)
    logger.info(f"start to run tests with pytest. DoMore version: {__version__}")
    return pytest.main(extra_args_new)


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version"
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_run = init_parser_run(subparsers)
    sub_parser_scaffold = init_parser_scaffold(subparsers)
    sub_parser_har2case = init_har2case_parser(subparsers)
    sub_parser_har2pytest = init_har2pytest_parser(subparsers)
    sub_parser_make = init_make_parser(subparsers)

    if len(sys.argv) == 1:
        # domore
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-V", "--version"]:
            # domore -V
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # domore -h
            parser.print_help()
        elif sys.argv[1] == "startproject":
            # domore startproject
            sub_parser_scaffold.print_help()
        elif sys.argv[1] == "har2case":
            # domore har2case
            sub_parser_har2case.print_help()
            # har file convert to pytest directly
        elif sys.argv[1] == "har2pytest":
            sub_parser_har2pytest.print_help()
        elif sys.argv[1] == "run":
            # domore run
            pytest.main(["-h"])
        elif sys.argv[1] == "make":
            # domore make
            sub_parser_make.print_help()
        sys.exit(0)
    elif (
        len(sys.argv) == 3 and sys.argv[1] == "run" and sys.argv[2] in ["-h", "--help"]
    ):
        # domore run -h
        pytest.main(["-h"])
        sys.exit(0)

    extra_args = []
    if len(sys.argv) >= 2 and sys.argv[1] in ["run", "locusts"]:
        args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[1] == "run":
        sys.exit(main_run(extra_args))
    elif sys.argv[1] == "startproject":
        main_scaffold(args)
    elif sys.argv[1] == "har2case":
        main_har2case(args)
    elif sys.argv[1] == "har2pytest":
        return main_har2case_return_case_file(args)
    elif sys.argv[1] == "make":
        main_make(args.testcase_path)


def main_hrun_alias():
    """ command alias
        hrun = domore run
    """
    if len(sys.argv) == 2:
        if sys.argv[1] in ["-V", "--version"]:
            # hrun -V
            sys.argv = ["domore", "-V"]
        elif sys.argv[1] in ["-h", "--help"]:
            pytest.main(["-h"])
            sys.exit(0)
        else:
            # hrun /path/to/testcase
            sys.argv.insert(1, "run")
    else:
        sys.argv.insert(1, "run")

    main()


def main_dorun_alias():
    """
    command alias: dorun = domore har2pytest & run ; \n
    it will execute the pytest command with HAR file directly.
    @return:
    """

    if len(sys.argv) == 2:
        if sys.argv[1] in ["-V", "--version"]:
            # hrun -V
            sys.argv = ["domore", "-V"]
        elif sys.argv[1] in ["-h", "--help"]:
            pytest.main(["-h"])
            sys.exit(0)
        else:
            for arg in sys.argv[1:]:
                if arg.endswith(".har"):
                    pytest_case_file = main_har2pytest_alias()
                    if not pytest_case_file.endswith("_test.py"):
                        raise exceptions.FileFormatError(
                            f"testcase file should be pytest format, invalid format file: {pytest_case_file}; "
                            f"please use 'har2case' command if you need JSON/YAML format."
                        )
                    # remove all args except 'dorun' command and then append new pytest format script
                    sys.argv[1:] = [pytest_case_file]
                elif os.path.splitext(arg)[-1] != '' and not (arg.lower().endswith((".json", ".yml", ".yaml", "_test.py"))):
                    raise exceptions.FileFormatError(
                        f"testcase file should be JSON/YAML/PYTHON format, invalid format file: {arg}; "
                        f"please use 'har2case' command if you need JSON/YAML/PYTHON format."
                    )

            # dorun /path/to/testcase
            sys.argv.insert(1, "run")
            sys.argv.insert(2, "-s")
            sys.argv.insert(3, "-v")
            sys.argv.append("--capture=sys")
            sys.argv.append("--html=report.html")
            sys.argv.append("--self-contained-html")

            # relate allure report
            # sys.argv.append("--alluredir=./allure_results")

            # # relate pytest-html report
            # sys.argv.append("--html=report.html")
            # sys.argv.append("--self-contained-html")
    else:
        for arg in sys.argv[1:]:
            if arg.endswith(".har"):
                pytest_case_file = main_har2pytest_alias()
                if not pytest_case_file.endswith("_test.py"):
                    raise exceptions.FileFormatError(
                        f"testcase file should be pytest format, invalid format file: {pytest_case_file}; "
                        f"please use 'har2case' command if you need JSON/YAML format."
                    )
                # remove all args except 'dorun' command and then append new pytest format script
                del (sys.argv[1:])
                sys.argv.insert(1, pytest_case_file)

        sys.argv.insert(1, "run")
        sys.argv.insert(2, "-s")
        sys.argv.insert(3, "-v")
        sys.argv.append("--capture=sys")
        sys.argv.append("--html=report.html")
        sys.argv.append("--self-contained-html")

        # ingrate allure report
        # sys.argv.append("--alluredir=./allure_results")

    main()


def main_make_alias():
    """ command alias
        hmake = domore make
    """
    sys.argv.insert(1, "make")
    main()


def main_har2case_alias():
    """ command alias
        har2case = domore har2case
    """
    sys.argv.insert(1, "har2case")

    # exclude the 'Request URL' which contains following keywords
    sys.argv.insert(2, "--exclude")
    sys.argv.insert(3, ".js|.css|.png|.jpg|.jpeg|.ico|skynet-gateway")
    main()


def main_har2pytest_alias() -> str:
    """ command alias about converting HAR file to pytest file.
    """
    # convert HAR file to pytest
    sys.argv.insert(1, "har2pytest")
    # exclude the 'Request URL' which contains following keywords
    sys.argv.insert(2, "--exclude")
    sys.argv.insert(3, ".js|.css|.png|.jpg|.jpeg|.ico|skynet-gateway")

    # return testcase file with '.py' extension
    return main()


if __name__ == "__main__":
    main()
