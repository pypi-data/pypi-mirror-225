"""
Displays the ElementTree instances created as a response from a **PSquared** server.
"""

from typing import List, Optional

import xml.etree.ElementTree as ET

__PADDING = len("  1970-01-01T00:00:000000-00:00 SUBMITTED ")


def configurations(application: ET.ElementTree):
    """
    Displays all the configurations contained in an application document

    Args:
        application: the application document whose configurations
                should be displayed.
    """

    configs = application.findall("configurations/configuration")
    print("Currently active configurations:")
    for config in configs:
        name_element = config.find("name")
        if None is name_element or None is name_element.text:
            name = "UNKNOWN"
        else:
            name = name_element.text
        description_element = config.find("description")
        if None is description_element or None is description_element.text:
            description = ""
        else:
            description = ": " + description_element.text
        print("  " + name + description)
    print()


def entry(
    element,
    name: Optional[str] = None,
    max_width: int = 0,
    changed: bool = False,
) -> None:
    """
    Displays the state of the specified entry.

    Args:
        element: the element containing the entry to be displayed.
        name: the name of the entry.
        max_width: the maximum print width of the label of the entry.
        changed: True if the entry should be maked a having changed.
    """

    if None is name:
        label = ""
    else:
        padding = max_width - len(name)
        if 0 > padding:
            label = name + " " * padding
        else:
            label = name[0:max_width]
        label = label + " : "
    if None is changed:
        status = "C    "
    else:
        status = "    "
    header = (
        status
        + label
        + element.find("completed").text
        + " "
        + element.find("state").text
    )
    message = element.find("message")
    if None is message or None is message.text:
        message_to_use = ""
    else:
        message_to_use = message.text.replace("\n", "\n" + " " * (__PADDING))
    print(header + " " * (__PADDING + (max_width + 3) - len(header)) + message_to_use)


def histories(
    name: str, version: str, report: ET.ElementTree, items: Optional[List[str]]
) -> None:
    """
    Displays the histories of items as contained in the specified report.

    Args:
        name: the name of the configuration whose items are being
                supplied.
        version: the version of the named configuration whose items
                are being supplied.
        report: the report document containing the states to be
                displayed.
        items: the subset of items in the report to be display, any
                not in the report will be ignored.
    """
    if None is items or 0 == len(items):
        return
    history_elements = report.findall("history")
    index = 0
    if index == len(history_elements):
        history = None
        print(
            'There is no History for the requested item with version "'
            + version
            + '" of configuration "'
            + name
            + '"'
        )
        return
    history = history_elements[index]
    for item in items:
        if None is not history:
            item_element = history.find("current-state/item")
            if None is not item_element and item == item_element.text:
                print(
                    'History of "'
                    + item
                    + '" with version "'
                    + version
                    + '" of configuration "'
                    + name
                    + '"'
                )
                entries = history.findall(".//entry")
                entries.reverse()
                for line in entries:
                    entry(line)
                index += 1
                if index == len(history_elements):
                    history = None
                else:
                    history = history_elements[index]
        else:
            print(
                'There is no History of "'
                + item
                + '" with version "'
                + version
                + '" of configuration "'
                + name
                + '"'
            )
            print()


def info(  # pylint: disable=too-many-branches,too-many-locals
    name: str,
    version: str,
    report: ET.Element,
    items: Optional[List[str]] = None,
    note: Optional[str] = None,
) -> None:
    """
    Displays the state of items as contained in the specified report.

    Args:
        name: the name of the configuration whose items are being
                supplied.
        version: the version of the named configuration whose items
                are being supplied.
        report: the report document containing the states to be
                displayed.
        items: the subset of items in the report to be display, any
                not in the report will be ignored.
        note: the alternate note to be printed before each entry.
    """
    element_for_item = "realized-state"
    item_entry = "entry"
    states = report.findall(element_for_item)
    if None is states or 0 == len(states):
        element_for_item = "synopsis"
        item_entry = "."
        states = report.findall(element_for_item)
    item_xpath = element_for_item + "/item"
    if None is items:
        # This is the case when there was no set of items explicitly requested.
        if 0 == len(states):
            print(
                'There are no items to report on for version "'
                + version
                + '" of configuration "'
                + name
                + '"'
            )
            return
        print('Results for version "' + version + '" of configuration "' + name + '"')
        names = report.findall(item_xpath)
        max_width = 0
        for name_element in names:
            if None is not name_element:
                item_name = name_element.text
                if None is not item_name:
                    if len(item_name) > max_width:
                        max_width = len(item_name)
        for state in states:
            state_element = state.find("item")
            if None is not state_element:
                entry(state.find(item_entry), state_element.text, max_width)
        return

    if 0 == len(items):
        print(
            'There are no items to report on for version "'
            + version
            + '" of configuration "'
            + name
            + '"'
        )
        return

    index = 0
    if index == len(states):
        state_element = None
    else:
        state_element = states[index]
    for item in items:
        if None is not state_element:
            item_element = state_element.find("item")
            if None is not item_element:
                item_name = item_element.text
                if None is item_name:
                    item_name = "MISSING"
                if None is note:
                    print(
                        'Current state of "'
                        + item_name
                        + '" with version "'
                        + version
                        + '" of configuration "'
                        + name
                        + '"'
                    )
                else:
                    print(note)
                entry(
                    state_element.find(item_entry),
                    changed=(None is state_element.find("unchanged")),
                )
                print()
                index += 1
                if index == len(states):
                    state_element = None
                else:
                    state_element = states[index]
        else:
            print(
                'There has been no processing of "'
                + item
                + '" with version "'
                + version
                + '" of configuration "'
                + name
                + '"'
            )
            print()


def versions(configuration: ET.Element) -> None:
    """Displays all the versions of a named configuration

    Args:
        configuration: the configuration document whose versions
                should be displayed.
    """

    default_version = configuration.find("default-version")
    if None is default_version or None is default_version.text:
        default_url = None
        default_note = ""
    else:
        default_url = default_version.text
        default_note = " (* indicates the default version)"
    known_versions = configuration.findall("known-versions/known-version")
    name_element = configuration.find("name")
    if None is not name_element:
        name = name_element.text
        if None is not name:
            print(
                'Currently active version for configuration "'
                + name
                + '"'
                + default_note
            )
    for vers in known_versions:
        uri_element = vers.find("uri")
        if None is not uri_element and default_url == uri_element.text:
            header = "* "
        else:
            header = "  "
        description_element = vers.find("description")
        if None is description_element or None is description_element.text:
            description_to_use = ""
        else:
            description_to_use = ": " + description_element.text
        vers_name_element = vers.find("name")
        if None is vers_name_element or None is vers_name_element.text:
            vers_name = "*missing*"
        else:
            vers_name = vers_name_element.text
        print(header + vers_name + description_to_use)
    print()
