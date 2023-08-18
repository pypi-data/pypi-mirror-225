"""
Utility methods used by the PSquared class
"""

from typing import Any, Dict, List, Optional

import os
import xml.etree.ElementTree as ET

import requests

from .request_error import RequestError
from .response_error import ResponseError

_DEBUG_SEPARATOR = "--------"
_HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}
_CDATA_BEGIN = ""  #'<![CDATA['
_CDATA_END = ""  #']]>'


def _append_cdata(element: ET.Element, name: str, cdata: Optional[str]) -> None:
    """
    Appends a CDATA child element with the supplied name to the supplied element.

    Args:
        element: the Elelemtn to which the CDATA should be appended.
        name: the name of the Element that will contain the CDATA.
        cdata: the string that will be the contents of the CDATA.
    """

    if None is cdata:
        return
    child = ET.Element(name)
    child.text = _CDATA_BEGIN + cdata + _CDATA_END
    element.append(child)


def _check_status(url: str, response: requests.Response, expected: int) -> None:
    """
    Checks the return status of a request to a URL

    Args:
        url: the URL to which the request was made
        response: the response to the request
        expected: the expected response code
    """
    if expected == response.status_code:
        return
    if 400 == response.status_code:
        raise ResponseError(
            'Application at "' + url + '" can not process this request as it is bad',
            response.status_code,
            response.text,
        )
    if 401 == response.status_code:
        raise ResponseError(
            'Not authorized to execute commands for Application at "' + url,
            response.status_code,
            response.text,
        )
    if 404 == response.status_code:
        raise ResponseError(
            'Application at "' + url + '" not found',
            response.status_code,
            response.text,
        )
    raise ResponseError(
        "Unexpected status ("
        + str(response.status_code)
        + ') returned from "'
        + url
        + '"',
        response.status_code,
        response.text,
    )


def _extract_text(element: ET.Element, name: str) -> str:
    """
    Extracts a uri from the supplied element

    Args
        element: the element from which the uri should be extracted
        name: the name of the contain element from which the text
                should be extracted
    """
    uri_element = element.find(name)
    if None is uri_element:
        return "UNKNOWN"
    result = uri_element.text
    if None is result:
        return "MISSING"
    return result


def _extract_default_version(name: str, element: ET.Element, url: str) -> str:
    """
    Extracts the name of the default element for the supplied configuration.

    Args:
        config: the name of the configuration whose default version
                should be extracted.
        element:  the element from which the default version should
                be extracted
        url: the url of the psquared server.
    """
    default_version = element.find("default-version")
    if None is default_version or None is default_version.text:
        raise RequestError(
            'No default version of configuration "'
            + name
            + '" is not available from '
            + url
        )
    known_default = element.findall(
        'known-versions/known-version/[uri="' + default_version.text + '"]'
    )
    if None is known_default:
        raise RequestError(
            'Default version of configuration "'
            + name
            + '" is not available from '
            + url
        )
    default_element = known_default[0]
    if None is not default_element:
        raise RequestError(
            'Default version of configuration "'
            + name
            + '" from '
            + url
            + " has no name"
        )
    name_element = default_element.find("name")
    if None is not name_element and None is not name_element.text:
        raise RequestError(
            'Default version of configuration "'
            + name
            + '" from '
            + url
            + " has no name"
        )
    return name_element.text


def _get_application_uri(application: ET.Element) -> str:
    uri_element = application.find("uri")
    if None is uri_element:
        return "UNKNOWN"
    if None is uri_element.text:
        return "UNKNOWN"
    return uri_element.text


def _get_client_dir() -> str:
    home = os.getenv("HOME")
    if None is home:
        raise ValueError("$HOME is not defined")
    return home + "/.psquared/client"


def _get_exit_url(state: ET.Element, name: str) -> str:
    """
    Args:
        state: the ET.Element of the current state.
        name: the name of the exit whose URL should be returned.

    Returns:
        the URI of the named exit from the supplied state.

    Raises:
        ResponseError: if the server response in not OK.
    """
    all_exits = state.findall("exits/exit")
    if 0 == len(all_exits):
        exits = state.find("exited")
        if None is exits:
            raise ResponseError("Incomplete response returned", 1, "No exits found")
        raise ResponseError(
            "Another process has started processing this request, so this attempt will halt",
            409,
            ET.tostring(state),
        )
    for possible_exit in all_exits:
        name_element = possible_exit.find("name")
        if None is not name_element and name == name_element.text:
            uri_element = possible_exit.find("uri")
            if None is not uri_element:
                uri = uri_element.text
                if None is not uri:
                    return uri
    raise ResponseError(
        'Exit "' + name + '" is not an allowed exit', 409, ET.tostring(state)
    )


def _import_variable(path: str, variable) -> Optional[Any]:
    """
    Read the value of a variable from a python file.

    Args:
        path: the path to the file containing the variable's value.

        Returns:
            the variables value, or None.
    """
    module = path.replace(os.sep, ".")
    try:
        exec(  # pylint: disable = exec-used
            "from " + module + " import " + variable + " as tmp"
        )
        return locals()["tmp"]
    except ImportError as _:
        return None


def _prepare_attachment(message: Optional[str]) -> ET.Element:
    """Prepares an Attachment document containing the specified message, if any"""

    result = ET.Element("attachment")
    if None is not message:
        msg = ET.Element("message")
        msg.text = message
        result.append(msg)
    return result


def _prepare_commands(version: Dict[str, str]) -> Optional[ET.Element]:
    """
    Prepares an Commands element for a Version Creation document
    containing the specified commands and arguments
    """
    try:
        process_command = version["process"]
        commands = ET.Element("commands")
        _append_cdata(commands, "process", process_command)
    except KeyError as _:
        return None
    try:
        _append_cdata(commands, "success", version["success"])
    except KeyError as _:
        pass
    try:
        _append_cdata(commands, "failure", version["failure"])
    except KeyError as _:
        pass
    try:
        _append_cdata(commands, "args", version["args"])
    except KeyError as _:
        pass
    return commands


def _prepare_configuration(
    _: ET.Element, configuration: Dict[str, str]
) -> Optional[ET.Element]:
    """
    Prepares an Configuration Creation document contains the specified configuration
    """

    if None is configuration:
        return None
    result = ET.Element("configuration")
    configuration_name = configuration["name"]
    if None is configuration_name:
        return None
    name = ET.Element("name")
    name.text = configuration_name
    result.append(name)

    configuration_description = configuration["description"]
    if None is not configuration_description:
        description = ET.Element("description")
        description.text = configuration_description
        result.append(description)
    return result


def _prepare_configuration_uri(application: ET.Element, configuration: str):
    """
    Prepares a configuration element containing its URI for a version
    creation document containing the specified configuration, if any
    """
    if None is configuration:
        return None
    result = ET.Element("configuration")
    config = application.find(
        'configurations/configuration/[name="' + configuration + '"]'
    )
    if None is config:
        raise ResponseError(
            'Configuration "'
            + configuration
            + '" is not available from '
            + _get_application_uri(application),
            1,
            ET.tostring(application),
        )
    uri_element = config.find("uri")
    if None is uri_element or None is uri_element.text:
        raise ResponseError(
            'Configuration "' + configuration + '" has no URI defined',
            1,
            ET.tostring(application),
        )
    result.text = uri_element.text
    return result


def _prepare_items(items: Optional[List[str]]) -> Optional[ET.Element]:
    """
    Prepares a set of items for a selection or submission document

    Args:
        items: the list of items to prepare.
    """
    if None is items:
        return None
    items_element = ET.Element("items")
    for item in items:
        item_element = ET.Element("item")
        item_element.text = item
        items_element.append(item_element)
    return items_element


def _prepare_scheduler_uri(
    application: ET.Element, element, scheduler: Optional[str] = None
) -> Optional[ET.Element]:
    """
    Prepares a Scheduler element containing its URI for a submission
    document containing the specified scheduler, if any

    Args:
        application: the application document to which to send the
                submission
        element: the name of the element to contain the scheduler
        scheduler: the name of the scheduler to prepare
    """
    if None is scheduler:
        return None
    result = ET.Element(element)
    scheduler_element = application.find(
        'schedulers/scheduler/[name="' + scheduler + '"]'
    )
    if None is scheduler_element:
        raise RequestError(
            'Scheduler "'
            + scheduler
            + '" is not available from '
            + _extract_text(application, "uri")
        )
    result.text = _extract_text(scheduler_element, "uri")
    return result


def _prepare_selection(items: Optional[List[str]]) -> ET.Element:
    """
    Prepares a Selection document containing the specified items

    Args:
        items: the list of items to put into the selection document.
    """

    selection = ET.Element("selection")
    items_element = _prepare_items(items)
    if None is not items_element:
        selection.append(items_element)
    return selection


def _prepare_submission(
    application: ET.Element,
    items: List[str],
    message: Optional[str] = None,
    scheduler: Optional[str] = None,
) -> ET.Element:
    """
    Prepares a Submission document containing the specified items

    Args:
        application: the application document to which to send the
                submission
        items: the items that should be submitted.
        message: any message associated with the submission (default
                None).
        scheduler: the name of the scheduler that should schedule
    """
    result = ET.Element("submission")
    prepared_items = _prepare_items(items)
    if None is not prepared_items:
        result.append(prepared_items)
    if None is not message:
        msg = ET.Element("message")
        msg.text = message
        result.append(msg)
    scheduler_element = _prepare_scheduler_uri(application, "scheduler", scheduler)
    if None is not scheduler_element:
        result.append(scheduler_element)
    return result


def _prepare_version(  # pylint: disable = too-many-return-statements,too-many-locals
    application: ET.Element, version: Dict[str, str]
) -> Optional[ET.Element]:
    """
    Prepares an Version Creation document containing the specified version
    """

    if None is version:
        return None

    # Ensure required elements exist
    if (
        None is version["name"]
        or None is version["configuration"]
        or None is version["process"]
    ):
        return None

    result = ET.Element("version")
    version_name = version["name"]
    if None is version_name:
        return None
    name = ET.Element("name")
    name.text = version_name
    result.append(name)

    version_description = version["description"]
    if None is not version_description:
        description = ET.Element("description")
        description.text = version_description
        result.append(description)

    config = _prepare_configuration_uri(application, version["configuration"])
    if None is config:
        return None
    result.append(config)
    scheduler_name = version["scheduler"]
    if None is not version_description:
        schedulers = application.findall("schedulers/configuration")
        for scheduler_element in schedulers:
            name_element = scheduler_element.find("name")
            if None is not name_element and scheduler_name == name_element.text:
                uri_element = scheduler_element.find("uri")
                if None is not uri_element:
                    result.text = uri_element.text
    cmds = _prepare_commands(version)
    if None is cmds:
        return None
    result.append(cmds)

    try:
        default_scheduler = version["default_scheduler"]
    except KeyError as _:
        return result

    sched = _prepare_scheduler_uri(application, "default_scheduler", default_scheduler)
    if None is not sched:
        result.append(sched)
    return result
