"""
Defines the PSquared class
"""

from typing import Callable, Dict, List, Optional, Tuple, Union

import logging
import os
from pathlib import Path
import xml.dom.minidom
import xml.etree.ElementTree as ET

import requests

from .psquared_utils import (
    _DEBUG_SEPARATOR,
    _HEADERS,
    _check_status,
    _extract_default_version,
    _extract_text,
    _get_application_uri,
    _get_client_dir,
    _get_exit_url,
    _import_variable,
    _prepare_attachment,
    _prepare_configuration,
    _prepare_selection,
    _prepare_submission,
    _prepare_version,
)
from .request_error import RequestError
from .response_error import ResponseError


class PSquared:
    """
    This class provides programatic access to a PSquared instance
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        url: str = "http://localhost:8080/psquared/local/report/",
        dump: bool = False,
        cert: Optional[str] = None,
        key: Optional[str] = None,
        cacert: Optional[Path] = None,
    ):
        """
        An Object that talks to the specified **PSquared** server.

        Args:
            url: the URL of the PSquared instance.
            dump: True if the raw XML exchanges should be dumped.
            cert: path to the file containing the client\'s x509
                certificate, (default
                ``${HOME}/.psquared/client/cert/psquared_client.pem``
                ).
            key: path to the file containing path to the client\'s
                private x509 key (default
                ``${HOME}/.psquared/client/private/psquared_client.
                key`` ).
            cacert: path to the file containing one or more CA x509
                certificates, (default
                ``${HOME}/.psquared/client/cert/cacert.pem``).

        The ``cert`` and ``key`` will only be used if the files
        containing them exist, otherwise they are ignored.

        The alternate ``cacert`` location is only used if the specified
        directory exists.
        """

        self.__url = url
        self.__debug = dump
        self.__session = requests.Session()
        if None is cert:
            cert = _get_client_dir() + "/cert/psquared_client.pem"  # Client certificate
        if None is key:
            key = (
                _get_client_dir() + "/private/psquared_client.key"
            )  # Client private key
        if None is cacert:
            cacert = Path(_get_client_dir() + "/cert/cacert.pem")  # CA certificate file
        if os.path.exists(cert) and os.path.exists(key):
            self.__session.cert = (cert, key)
        if os.path.exists(cacert):
            self.__session.verify = str(cacert)

    def create_from_file(self, path: str) -> Tuple[int, int]:
        """
        Creates new configurations and version from the specified file.

        Args:
            path: the path to the file holding the configurations and version to be added.

        Returns:
            the number of new configurations and the number of new versions created.

        Raise:
            ResponseError: If the status code of the response is not what was expected.
        """

        if path.endswith(".py"):
            path_to_use = path[:-3]
        else:
            path_to_use = path

        # Start with configurations
        configurations = _import_variable(path_to_use, "configurations")
        configuration = _import_variable(path_to_use, "configuration")
        if None is not configuration:
            if None is configurations:
                configurations = []
            configurations.insert(0, configuration)

        versions = _import_variable(path_to_use, "versions")
        version = _import_variable(path_to_use, "version")
        if None is not version:
            if None is versions:
                versions = []
            versions.insert(0, version)

        return self._execute_creations(configurations, versions)

    def debug_separator(self) -> None:
        """
        Outputs the debug separator.
        """
        logging.debug(_DEBUG_SEPARATOR)

    def _execute_creation(
        self,
        creation_type: str,
        definition: Dict[str, str],
        preparation: Callable[[ET.Element, Dict[str, str]], Optional[ET.Element]],
    ) -> Optional[str]:
        """
        Submits the definition to be added to the existing set of definitions.

        Args:
            creation_type: the type of reaction to be done
            definition: the definition of the configuration to be added.
            preparation: the method to use to prepare the definitions creation document.

        Returns:
            the URL of the created definition.

        Raise:
            ResponseError: If the status code of the response is not
                what was expected.
        """

        create_url, application = self.__get_create_command_url(creation_type)
        creation_request = preparation(application, definition)
        if None is creation_request:
            return None
        self.__pretty_print(create_url, ET.tostring(creation_request), False)
        response = self.__session.post(
            create_url, data=ET.tostring(creation_request), headers=_HEADERS
        )
        try:
            _check_status(create_url, response, 201)
            if "" != response.text:
                report = ET.fromstring(response.text)
                self.__pretty_print(create_url, ET.tostring(report))
            return response.headers["Location"]
        except ResponseError as _:
            return None

    def _execute_creations(
        self,
        configurations: Optional[List[Dict[str, str]]],
        versions: Optional[List[Dict[str, str]]],
    ) -> Tuple[int, int]:
        """
        Submits a collections of configuration and version
                definitions to be added to the existing set.

        configurations: the collection of configurations to be added.
        versions: the collection of versions to be added.

        Returns:
            the number of new configurations and the number of new
                versions created.

        Raise:
            ResponseError: If the status code of the response is not
                what was expected.
        """
        configuration_count = 0
        if None is not configurations and 0 != len(configurations):
            for config in configurations:
                result = self._execute_creation(
                    "configuration", config, _prepare_configuration
                )
                if None is not result:
                    configuration_count += 1
        version_count = 0
        if None is not versions and 0 != len(versions):
            for vers in versions:
                result = self._execute_creation("version", vers, _prepare_version)
                if None is not result:
                    version_count += 1
        return configuration_count, version_count

    def _execute_transition(
        self, uri: str, message: Optional[str] = None
    ) -> ET.Element:
        """
        Requests the PSquared instance create a new realized state.

        Args:
            uri: The URI of the destination of the transition.
            message: The message, if any, to attach to the transition.

        Returns:
            The XML document that was the response to the request.

        Raise:
            ResponseError: If the status code of the response is not what was expected.
        """
        # Prepare attachment document
        attachment = _prepare_attachment(message)
        if self.__debug:
            self.__pretty_print(uri, str(ET.tostring(attachment), "utf-8"), False)
        #        if self.__use_mock_server:
        #            response = mock_server.post(uri)
        #        else:
        response = self.__session.post(
            uri, data=ET.tostring(attachment), headers=_HEADERS
        )
        if 404 == response.status_code:
            raise ResponseError(
                f'Exit request "{uri}" not found', response.status_code, response.text
            )
        if 409 == response.status_code:
            raise ResponseError(
                "Another process has changed the processing of this request, so this attempt will"
                + " halt",
                response.status_code,
                response.text,
            )
        if 201 == response.status_code:
            if self.__debug:
                self.__pretty_print(uri, response.text)
            return ET.fromstring(response.text)
        raise ResponseError(
            f'Unexpected status ({str(response.status_code)}) returned from "{uri}"',
            response.status_code,
            response.text,
        )

    def execute_transitions(  # pylint:disable=too-many-arguments,too-many-locals, too-many-branches
        self,
        configuration: str,
        version: str,
        report: ET.Element,
        items: List[str],
        transition: str,
        message: Optional[str] = None,
        quiet=False,
    ) -> ET.Element:
        """Requests the execution of a transition into a new realized state be made.

        Args
            configuration: the name of the configuration whose command URL should be returned.
            version: the version of the named configuration whose command URL should be returned.
            ElementTree report: the report containing the latest states for the requested items.
            list[str] items: the set of items to be tranistioned.
            str transition: the name of the exit from which the transition should start.
            str message: a message, if any, to be attached to the transistion.
            bool quiet: True if a detailed report is not required.

        Returns:
            the report on the result of each item in the requested transition.
        :rtype: ElementTree

        Raise:
            ResponseError: if the server response in not OK.
        """
        realized_states = ET.Element("realized-states")
        states = report.findall("realized-state")
        index = 0
        if index == len(states):
            state = None
        else:
            state = states[index]
        for item in items:
            if None is not state:
                item_element = state.find("item")
                if None is not item_element and item == item_element.text:
                    try:
                        exit_url = _get_exit_url(state, transition)
                        if quiet:
                            exit_url = exit_url + "?details=None"
                        result = self._execute_transition(exit_url, message)
                    #                    note = None
                    except ResponseError as response_error:
                        if 409 == response_error.code:
                            logging.error(  # pylint: disable = logging-not-lazy
                                'It is not possible to "%s item "%s" with version "%s" of'
                                + ' configuration "%s" due to its current state.',
                                transition,
                                item,
                                version,
                                configuration,
                            )
                        else:
                            logging.error(response_error.message)
                        result = ET.fromstring(response_error.response)
                        result.append(ET.Element("unchanged"))
                    if None is not result:
                        realized_states.append(result)
                index += 1
                if index == len(states):
                    state = None
                else:
                    state = states[index]
            else:
                print(
                    'Item "'
                    + item
                    + '" is not being processed with version "'
                    + version
                    + '" of configuration "'
                    + configuration
                    + '", so it is not possible to '
                    + transition
                    + " it"
                )
        self.__pretty_print("Missing URL - Fix this!", ET.tostring(realized_states))
        return realized_states

    def get_application(self) -> ET.Element:
        """
        Returns
            the application document at the URL

        Raises:
            ResponseError: if the server response in not OK.
        """
        logging.debug("Executing GET for URL : %s", self.__url)
        response = self.__session.get(self.__url)
        _check_status(self.__url, response, 200)
        application = ET.fromstring(response.text)
        self.__pretty_print(self.__url, ET.tostring(application))
        return application

    def get_configuration(self, name: str, **kwargs) -> Tuple[ET.Element, ET.Element]:
        """
        return the configuration document the named configuration.

        Args:
            name: the name of the configuration that should be
                returned.
            options: an optional dictionary of options determining
                how much detail to include in the returned
                configuration.

        Returns:
            the configuration document the named configuration.

        Raises:
            ResponseError: if the server response is not OK.
        """
        configuration_url, application = self.__get_configuration_url(name)
        url_to_use = configuration_url + self.__prepare_query(kwargs)
        logging.debug("Executing GET for URL : %s", url_to_use)
        response = self.__session.get(url_to_use)
        _check_status(url_to_use, response, 200)
        configuration = ET.fromstring(response.text)
        self.__pretty_print(url_to_use, ET.tostring(configuration))
        return configuration, application

    def __get_create_command_url(self, creation_type) -> Tuple[str, ET.Element]:
        """
        Returns the URL for the named creation command

        Args:
            creation_type: the type of definition ('configuration' or
                'version') whose create command URL should be
                returned.

        Returns
            the URL to use to create the requested type.

        Raises:
            ResponseError: if the server response is not OK.
        """

        application = self.get_application()
        action = application.find(
            'actions/[name="creation"]/action/[name="' + creation_type + '"]'
        )
        if None is not action:
            action_element = action.find("uri")
            if None is not action_element:
                command_url = action_element.text
                if None is not command_url:
                    return str(command_url), application
        raise ResponseError(
            'Creation of "'
            + creation_type
            + '" is not available from "'
            + _get_application_uri(application)
            + '"',
            1,
            ET.tostring(application),
        )

    def __get_configuration_url(self, name: str) -> Tuple[str, ET.Element]:
        """
        Returns the URL of the named configuration, the application
        document at the URL

        Args:
            name: the name of the configuration whose URL should be returned.

        Returns:
            the URL of the named configuration, the application document at the URL

        Raise:
            ResponseError: if the server response in not OK.
        """

        application = self.get_application()
        configurations = application.findall("configurations/configuration")
        for configuration in configurations:
            name_element = configuration.find("name")
            if None is not name_element and name == name_element.text:
                config_element = configuration.find("uri")
                if None is not config_element:
                    configuration_url = config_element.text
                    if None is configuration_url:
                        raise RequestError(
                            'Configuration "'
                            + name
                            + '" has no URL for "'
                            + _extract_text(application, "uri")
                            + '"'
                        )
                    return configuration_url, application
        raise RequestError(
            'Configuration "'
            + name
            + '" is not available from "'
            + _extract_text(application, "uri")
            + '"'
        )

    def __get_named_resource_url(
        self, name: str, vers: str, group: str, xpath: str, resource_name: str
    ) -> Tuple[str, str, ET.Element]:
        """
        Args:
            name: the name of the configuration to which the Named
                Resource should belong.
            vers: the version of the named configuration to which the
                Named Resource should belong.
            group: the name of the Resource group that contains the
                Named Resource.
            xpath: the xpath to the Named Resources within a Named
                Resource group that contains the Named Resource.
            resource_name: the name of the resource whose URL should be
                returned.

        Returns:
            the URI of a Named Resource for the specified
            configuration/version, the name of the version used and the
            application's document.

        Raise:
            ResponseError: if the server response in not OK.
        """
        version, _, application = self.get_version(
            name, vers, options=("details", group)
        )
        version_name = _extract_text(version, "name")
        cmd = version.find(group + "/" + xpath + '/[name="' + resource_name + '"]')
        if None is cmd:
            raise ResponseError(
                'The version, "'
                + version_name
                + '", of configuration "'
                + name
                + '" does not support the "'
                + resource_name
                + '" command',
                2,
                ET.tostring(version),
            )
        uri = _extract_text(cmd, "uri")
        return uri, version_name, application

    def get_report(  # pylint: disable=too-many-arguments
        self,
        name: str,
        version: str,
        report: str,
        page: Optional[int] = None,
        length: Optional[int] = None,
        items: Optional[List[str]] = None,
    ) -> Tuple[ET.Element, str]:
        """
        Returns a report about the contents of the PSquared server.

        Args:
            name: the name of the configuration whose command URL
                should be returned.
            version: the version of the named configuration whose
                command URL should be returned.
            report: the type of report that should be returned.
            page: the page number of the paginated results to return.
            length: the length of a page for the paginated results.
            items: the set of items that should be included in the
                results.

        Returns:
            the specified report for the list of items for the specified
            configuration/version, and the name of the version used.

        Raises:
            ResponseError: if the server response in not OK.
        """
        if None is items:
            xpath = '[name="summary"]/report'
        else:
            xpath = '[name="itemized"]/report'
        report_url, vers, _ = self.__get_named_resource_url(
            name, version, "reports", xpath, report
        )
        if None is items:
            selection = None
            if None is not length:
                report_url = report_url + "?length=" + str(length)
                if None is not page:
                    report_url = report_url + "&page=" + str(page)
            logging.debug("Executing GET for URL : %s", report_url)
            response = self.__session.get(report_url, headers=_HEADERS)
        else:
            selection = _prepare_selection(items)
            self.__pretty_print(report_url, ET.tostring(selection), False)
            logging.debug("Executing GET for URL : %s", report_url)
            response = self.__session.get(
                report_url, data=ET.tostring(selection), headers=_HEADERS
            )
        _check_status(report_url, response, 200)
        result = ET.fromstring(response.text)
        self.__pretty_print(report_url, ET.tostring(result))
        return result, vers

    def get_version(  # pylint: disable=too-many-locals
        self, name: str, vers: Optional[str] = None, **kwargs
    ) -> Tuple[ET.Element, ET.Element, ET.Element]:
        """
        Args:
            config: the name of the configuration who version should
                be returned.
            vers: the name of the version of the specified
                configuration to be returned.
            options: an optional dictionary of options determining
                how much detail to include in the returned version.

        Returns:
            the version document the named configuration/version.

        Raises:
            ResponseError: if the server response is not OK.
        """

        configuration, application = self.get_configuration(
            name, options=("details", "summary")
        )
        url = _extract_text(application, "uri")
        if None is vers:
            vers_to_use = _extract_default_version(name, configuration, url)
        else:
            vers_to_use = vers
        version_element = configuration.find(
            'known-versions/known-version/[name="' + vers_to_use + '"]'
        )
        if None is version_element:
            raise RequestError(
                'Version "'
                + vers_to_use
                + '" of configuration "'
                + name
                + '" is not available from '
                + url
            )
        uri = _extract_text(version_element, "uri")
        uri_to_use = uri + self.__prepare_query(kwargs)
        logging.debug("Executing GET for URL : %s", uri_to_use)
        response = self.__session.get(uri_to_use)
        _check_status(uri_to_use, response, 200)
        version = ET.fromstring(response.text)
        self.__pretty_print(uri_to_use, ET.tostring(version))
        return version, configuration, application

    def __prepare_query(self, options):
        """
        Args:
            options: an optional dictionary of options determining
                how much detail to include in the returned
                configuration.

        Returns:
            the query string to be added to a URL.
        """
        query = ""
        if None is not options and 0 != len(options):
            conjunction = "?"
            for _, value in options.items():
                query = query + conjunction + value[0] + "=" + value[1]
        return query

    def __pretty_print(
        self,
        url: Union[bytes, str],
        document: Union[bytes, str],
        is_response: bool = True,
    ) -> None:
        """
        Prints out a formatted version of the supplied XML

        Args:
            url: the URL to which the request was made.
            document: the XML document to print.
            is_response: True is the XML is the reponse to a request.
        """
        if self.__debug:
            if None is not url:
                if is_response:
                    logging.debug("URL : Response : %s", str(url))
                else:
                    logging.debug("URL : Request :  %s", str(url))
            logging.debug(xml.dom.minidom.parseString(document).toprettyxml())
            self.debug_separator()

    def submit_items(  # pylint: disable=too-many-arguments
        self,
        configuration: str,
        version: str,
        items: List[str],
        message: Optional[str] = None,
        quiet: Optional[bool] = None,
        scheduler: Optional[str] = None,
        veto: Optional[str] = None,
    ) -> Tuple[Optional[ET.Element], Optional[str]]:
        """
        Submits the list of items for processing with the specified
        version of the named configuration

        Args:
            configuration: the name of the configuration whose
                command URL should be returned.
            version: the version of the named configuration whose
                command URL should be returned.
            items: the items that should be submitted.
            message: any message associated with the submission
                (default None).
            quiet: True if no detailed response is required (default
                None).
            scheduler: the name of the scheduler that should schedule
                the execution. (default None)
            veto: the name of the veto, is any, to apply to the
                submission (default None).

        Returns:
            the current report for the list of items for the specified
            configuration/version, and the name of the version used.

        Raise:
            ResponseError: if the server response in not OK.
        """

        submit_url, vers, application = self.__get_named_resource_url(
            configuration, version, "actions", '[name="submission"]/action', "submit"
        )
        query_string = "?"
        if quiet:
            query_string = query_string + "details=None"
        if None is not veto:
            query_string = query_string + "veto=" + veto
        if 1 != len(query_string):
            submit_url = submit_url + query_string
        submission = _prepare_submission(application, items, message, scheduler)
        self.__pretty_print(submit_url, ET.tostring(submission), False)
        response = self.__session.post(
            submit_url, data=ET.tostring(submission), headers=_HEADERS
        )
        _check_status(submit_url, response, 200)
        if "" == response.text:
            return None, None
        report = ET.fromstring(response.text)
        self.__pretty_print(submit_url, ET.tostring(report))
        return report, vers

    def write_template(self, path: str) -> None:
        """Writes out a creation template to the specified file.

        Args:
            path: the path to the file where the template should be written.
        """

        print(path)
        contents = """#
# Delete the configuration/version template you are not using.
#

configuration = {

    # The name of the configuration (set to None to be ignored).
    'name' : None

    # Optional description of the configuration (recommended)
    'description' : None
}


version = {

    # The name of the version, must be unique with associated configuration  (set to None to be ignored).
    'name' : None

    # Optional description of the version (recommended)
    'description' : None

    # The name of the configuration for which this is a version
    'configuration' : None

    # The UNIX command, i.e. single word, to run to process an item with this version.
    'process' : None

    # The set of arguments (and psquared substitutions) commands for this version will receive
    'args' : None,

    # The name of the default scheduler with which to execute this version.                                                                                
    'default_scheduler'    : None
}
"""
        with open(path, "w", encoding="utf-8") as template_file:
            template_file.write(contents)
