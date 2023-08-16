"""A command line interface to run a Client instance"""

from typing import List, Optional, Tuple

import argparse
import logging
import sys
import os

from . import display
from .psquared import PSquared
from .response_error import ResponseError
from . import utils

_ENVARS_MAPPING = {
    "CLIENT_CA_CERTIFICATE": "CA_CERTIFICATE",
    "CLIENT_CERTIFICATE": "CERTIFICATE",
    "CLIENT_KEY": "KEY",
    "CLIENT_LOG_FILE": "LOG_FILE",
    "CLIENT_LOG_LEVEL": "LOG_LEVEL",
    "CLIENT_INI_FILE": "INI_FILE",
    "CLIENT_INI_SECTION": "INI_SECTION",
    "CLIENT_QUIET": "QUIET",
    "CLIENT_SCHEDULER": "SCHEDULER",
}

_LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

MISSING_ARGUMENT = 1
MISSING_ARGUMENT_MESSAGE = "Missing argument"
MISSING_OPTION = 2
MISSING_OPTION_MESSAGE = "Missing option"
MULTIPLE_TRANSITIONS = 3
MULTIPLE_TRANSITIONS_MESSAGE = "Multiple transitions"


def _create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and populated the argparse.ArgumentParser for this executable.
    """
    parser = argparse.ArgumentParser(
        description="Command Line interface to a PSquared server."
    )
    parser.add_argument("-?", help="Prints out this help", action="help")
    parser.add_argument(
        "--abandon",
        dest="ABANDON",
        help="abandons the processing of items with the specified configuration if they have"
        + " failed, i.e. they will be ignored in responses to a request for info or unprocessed"
        + ' items. (This is a shortcut for "-t abandon.")',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--cacert",
        dest="CA_CERTIFICATE",
        help="path to the file containing one or more CA x509 certificates, if different from the"
        + " default, ${HOME}/.psquared/client/cert/cacert.pem",
        default=None,
    )
    parser.add_argument(
        "--cancel",
        dest="CANCEL",
        help="cancels  processing of the items with the specified configuration if they have not"
        + ' completed, i.e. they can be re-submitted later. (This is a shortcut for "-t cancel.")',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--cert",
        dest="CERTIFICATE",
        help="path to the client's x509 certificate, if different from the default,"
        + " ${HOME}/.psquared/client/cert/psquared_client.pem",
        default=None,
    )
    parser.add_argument(
        "--create",
        dest="CREATION_FILE",
        help="reads the specified file and creates the appropriate configurations and versions. "
        + "Note: the .py extension does not have to be specified, but is required in the files"
        + " actual name.",
        default=None,
    )
    parser.add_argument(
        "-e",
        "--executing",
        dest="EXECUTING",
        help="lists the set of items that have been submitted and are being processed by the"
        + " specified configuration/version",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-F",
        "--failed",
        dest="FAILED",
        help="lists the set of items that have been submitted but failed to be processed"
        + " processed by the specified configuration/version",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="FILE",
        help="the name of a file containing a list of items which will be added to any specified"
        + "on the command line",
        default=None,
    )
    parser.add_argument(
        "-H",
        "--history",
        dest="HISTORY",
        help="the processing history of the items with the specified configuration."
        + '(Overrides "-i".)',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--info",
        dest="INFO",
        help="provide information on either the application when no configuration is specified,"
        + " the configuration when no version is specified, or the current processing state of"
        + " the items with the specified configuration/version.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--length",
        dest="LENGTH",
        help="the length of a page when returning a report. (Ignored if items are specified.)",
        default=None,
    )
    parser.add_argument(
        "--log_file",
        dest="LOG_FILE",
        help="The file, as opposed to stdout, into which to write log messages",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        default="INFO",
        dest="LOG_LEVEL",
        help="The logging level for this execution",
        choices=_LOG_LEVELS.keys(),
    )
    parser.add_argument(
        "--key",
        dest="KEY",
        help="path to the client's private x509 key, if different from the default,"
        + " ${HOME}/.psquared/client/private/psquared_client.key",
        default=None,
    )
    parser.add_argument(
        "-m",
        "--message",
        dest="MESSAGE",
        help="adds the specified text as a option message to a requested change in the"
        + "items/configuration pairings",
        default=None,
    )
    parser.add_argument(
        "--page",
        dest="PAGE",
        help="the page, of specified length, from the total collection, to return in a"
        + " report. (Ignored if items are specified.)",
        default=None,
    )
    parser.add_argument(
        "--prepared",
        dest="PREPARED",
        help="lists the set of items that are know to this program and are ready to be"
        + " submitted for processing by the specified configuration/version",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--processed",
        dest="PROCESSED",
        help="lists the set of items that have been submitted and successfully processed by the"
        + " specified configuration/version",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="QUIET",
        help="stop the results of any transition execution from being displayed. Explicit request"
        + " for info will still produce output",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--recover",
        dest="RECOVER",
        help="returns an abandoned processing of items with the specified configuration so that"
        + " is can be re-submitted later."
        + ' (This is a shortcut for "-t recover.")',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--reset",
        dest="RESET",
        help="resets the processing of items with the specified configuration if they have"
        + ' completed, i.e. they it can be re-submitted later. (This is a shortcut for "-t'
        + ' reset.")',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--resolved",
        dest="RESOLVED",
        help="resets the processing items with the specified configuration if they have failed,"
        + ' i.e. they it can be re-submitted later. (This is a shortcut for "-t resolved.")',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--scheduler",
        dest="SCHEDULER",
        help="uses the named scheduler to submit items for processing with the specified"
        + " configuration rather than the default one.",
        default=None,
    )
    parser.add_argument(
        "-s",
        "--submit",
        dest="SUBMIT",
        help="submits the items for processing with the specified configuration pair,"
        + ' if they are ready. (This is a shortcut for "-t submit.")',
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t",
        "--transition",
        dest="TRANSITION",
        help="the transition for the items with the specified configuration/version that should be"
        + " executed.",
        default=None,
    )
    parser.add_argument(
        "--template",
        dest="TEMPLATE_FILE",
        help="writes out a creation template to the specified file.",
        default=None,
    )
    parser.add_argument(
        "-u",
        "--unprocessed",
        dest="UNPROCESSED",
        help="lists the set of items that have been submitted but not successfully processed by"
        + " the specified configuration/version",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-V",
        dest="VERSION",
        help="the version of the specified configuration to use if not the default one",
        default=None,
    )
    parser.add_argument(
        "--veto",
        dest="VETO",
        help='the name of the veto, is any, to apply to the submission. ("family" is the only'
        + " supported one at the moment)",
        default=None,
    )
    parser.add_argument(
        "-w",
        "--waiting",
        dest="WAITING",
        help="lists the set of items that have been submitted and are waiting to be processed by"
        + " the specified configuration/version",
        action="store_true",
        default=False,
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def _extract_config_and_items(
    args: list[str], filename: str
) -> Tuple[Optional[str], List[str]]:
    """
    Extracts the configuration and items from the command's arguments.
    """
    items: List[str]
    if 0 == len(args):
        config = None
        items = []
    else:
        config = args[0]
        if 1 == len(args):
            items = []
        else:
            items = args[1:]

    if None is not filename:
        with open(filename, "r", encoding="utf-8") as items_file:
            lines = items_file.readlines()
            for line in lines:
                if 0 != len(line) and "\n" == line[-1:]:
                    item = line[:-1].strip()
                else:
                    item = line[0:-1].strip()
                if "" != item and not item.startswith("#"):
                    items.append(item)
    return config, items


def _guard_multiple_transitions(current: str, requested: str) -> str:
    """
    Guards against trying to do two different transitions in the same invocation.
    """
    if None is not current and current != requested:
        logging.error(
            "%s: Only one type of transition is possible per invocation",
            MULTIPLE_TRANSITIONS_MESSAGE,
        )
        sys.exit(MULTIPLE_TRANSITIONS)
    return requested


def _display_report(  # pylint: disable = too-many-arguments
    psquared: PSquared,
    name: str,
    version: str,
    report: str,
    page: Optional[int] = None,
    length: Optional[int] = None,
    items: Optional[List[str]] = None,
) -> None:
    """
    Displays the requested report.

    Args:
        psquared: the instance from which to retrieve the report.
        name: the name of the configuration whose command URL
            should be returned.
        version: the version of the named configuration whose
            command URL should be returned.
        report: the type of report that should be returned.
        page: the page number of the paginated results to return.
        length: the length of a page for the paginated results.
        items: the set of items that should be included in the
            results.

    """
    _verify_args(name, version)
    result, version = psquared.get_report(name, version, report, page, length, items)
    display.info(name, version, result)


def _optional_items(items: Optional[List[str]]) -> Optional[List[str]]:
    """
    Returns None when items is empty, otherwise returns supplied items
    """
    if None is items or 0 == len(items):
        return None
    return items


def _resolve_transition(options: argparse.Namespace) -> Optional[str]:
    transition = options.TRANSITION
    if options.SUBMIT:
        transition = _guard_multiple_transitions(transition, "submit")
    if options.RESOLVED:
        transition = _guard_multiple_transitions(transition, "resolved")
    if options.CANCEL:
        transition = _guard_multiple_transitions(transition, "cancel")
    if options.RESET:
        transition = _guard_multiple_transitions(transition, "reset")
    if options.ABANDON:
        transition = _guard_multiple_transitions(transition, "abandon")
    if options.RECOVER:
        transition = _guard_multiple_transitions(transition, "recover")
    return transition


def _set_transition(current, requested):
    if None != current and current != requested:
        eprint(MULTIPLE_TRANSITIONS_MESSAGE + ': Only one type of transition is possible per invocation')
        sys.exit(MULIPLE_TRANSITIONS)
    return requested


def _verify_args(name: str, version: str) -> None:
    """
    Verifys that the necessary arguments for a report a present.
        Exits if they are not.

    Args:
        name: the name of the configuration whose command URL
            should be returned.
        version: the version of the named configuration whose
            command URL should be returned.

    """
    if None is name:
        logging.debug("%s: Configuration must be supplied", MISSING_ARGUMENT_MESSAGE)
        sys.exit(MISSING_ARGUMENT)
    if None is version:
        logging.debug("%s: Version must be supplied", MISSING_OPTION_MESSAGE)
        sys.exit(MISSING_OPTION)


def main():  # pylint: disable = too-many-branches, too-many-locals, too-many-statements
    """
    Command Line interface to a PSquared server.
    """
    parser = _create_argument_parser()
    envar_values = utils.read_envar_values(_ENVARS_MAPPING)
    options = parser.parse_args(namespace=envar_values)
    args = options.args

    if None is options.LOG_FILE:
        logging.basicConfig(stream=sys.stdout, level=_LOG_LEVELS[options.LOG_LEVEL])
    else:
        logging.basicConfig(
            filename=options.LOG_FILE, level=_LOG_LEVELS[options.LOG_LEVEL]
        )

    logging.debug("Begin options:")
    for option in options.__dict__:
        if options.__dict__[option] is not None:
            logging.debug("    %s = %s", option, options.__dict__[option])
    logging.debug("End options:")

    url = os.getenv("PP_APPLICATION", "http://localhost:8080/psquared/local/report/")

    config, items = _extract_config_and_items(args, options.FILE)
    debug = "DEBUG" == options.LOG_LEVEL
    psquared = PSquared(
        url,
        dump=debug,
        cert=options.CERTIFICATE,
        key=options.KEY,
        cacert=options.CA_CERTIFICATE,
    )

    if debug:
        psquared.debug_separator()

    transition = options.TRANSITION
    if options.SUBMIT:
        transition = _set_transition(transition, 'submit')
    if options.RESOLVED:
        transition = _set_transition(transition, 'resolved')
    if options.CANCEL:
        transition = _set_transition(transition, 'cancel')
    if options.RESET:
        transition = _set_transition(transition, 'reset')
    if options.ABANDON:
        transition = _set_transition(transition, 'abandon')
    if options.RECOVER:
        transition = _set_transition(transition, 'recover')

    try:
        run_default = True
        if options.TEMPLATE_FILE:
            psquared.write_template(options.TEMPLATE_FILE)
            run_default = False

        if options.CREATION_FILE:
            configuration_count, version_count = psquared.create_from_file(
                options.CREATION_FILE
            )
            if 0 != configuration_count:
                if 1 == configuration_count:
                    plural = ""
                else:
                    plural = "s"
                print("Added " + str(configuration_count) + " configuration" + plural)
            if 0 != version_count:
                if 1 == version_count:
                    plural = ""
                else:
                    plural = "s"
                print("Added " + str(version_count) + " version" + plural)
            run_default = False

        if options.INFO and None is not config:
            if None is options.VERSION:
                if 0 != len(items):
                    logging.error(
                        "%s: Version must be supplied when one of more items are specified",
                        MISSING_OPTION_MESSAGE,
                    )
                    sys.exit(MISSING_OPTION)
                configuration, _ = psquared.get_configuration(config)
                display.versions(configuration)
                run_default = False
            else:
                report, version = psquared.get_report(
                    config, options.VERSION, "latest", items=items
                )
                display.info(config, version, report, items)
                run_default = False
        else:
            transition = _resolve_transition(options)
            if "submit" == transition:
                report, version = psquared.submit_items(
                    config,
                    options.VERSION,
                    items,
                    options.MESSAGE,
                    options.QUIET,
                    options.SCHEDULER,
                    options.VETO,
                )
                if None is not report:
                    display.info(config, version, report, items)
                run_default = False
            elif None is not transition:
                report, version = psquared.get_report(
                    config, options.VERSION, "latest", items=items
                )
                result = psquared.execute_transitions(
                    config,
                    version,
                    report,
                    items,
                    transition,
                    options.MESSAGE,
                    options.QUIET,
                )
                display.info(config, version, result, items)
                run_default = False
            else:
                if options.HISTORY:
                    _verify_args(config, options.VERSION)
                    result, version = psquared.get_report(
                        config, options.VERSION, "history", items=items
                    )
                    display.histories(config, version, result, items)
                    run_default = False
                if options.EXECUTING:
                    _display_report(
                        psquared,
                        config,
                        options.VERSION,
                        "executing",
                        options.PAGE,
                        options.LENGTH,
                        _optional_items(items),
                    )
                    run_default = False
                if options.FAILED:
                    _display_report(
                        psquared,
                        config,
                        options.VERSION,
                        "failed",
                        options.PAGE,
                        options.LENGTH,
                        _optional_items(items),
                    )
                    run_default = False
                if options.PREPARED:
                    _display_report(
                        psquared,
                        config,
                        options.VERSION,
                        "prepared",
                        options.PAGE,
                        options.LENGTH,
                        _optional_items(items),
                    )
                    run_default = False
                if options.PROCESSED:
                    _display_report(
                        psquared,
                        config,
                        options.VERSION,
                        "processed",
                        options.PAGE,
                        options.LENGTH,
                        _optional_items(items),
                    )
                    run_default = False
                if options.UNPROCESSED:
                    _display_report(
                        psquared,
                        config,
                        options.VERSION,
                        "unprocessed",
                        options.PAGE,
                        options.LENGTH,
                        _optional_items(items),
                    )
                    run_default = False
                if options.WAITING:
                    _display_report(
                        psquared,
                        config,
                        options.VERSION,
                        "waiting",
                        options.PAGE,
                        options.LENGTH,
                        _optional_items(items),
                    )
                    run_default = False
                if options.TEMPLATE_FILE:
                    logging.fatal("Not yet implmented")
                    run_default = False
                if options.CREATION_FILE:
                    logging.fatal("Not yet implmented")
                    run_default = False
            if run_default or (options.INFO and None is config):
                # Default with nothing specified is to list all known configurations.
                application = psquared.get_application()
                display.configurations(application)

    except ResponseError as response_error:
        logging.error(response_error.message)
        sys.exit(response_error.code)
