from typing import Any, Dict, Optional

from vicmiko.junos import JunOSDriver

from nornir.core.configuration import Config


CONNECTION_NAME = "nornir_junos"


class nornir_junos:
    """
    This plugin connects to the device using the NAPALM driver and sets the
    relevant connection.
    The dictionary passed via ``extras`` is passed directly as kwargs to the
    napalm constructor. This means you could pass the dictionary::
        {"optional_args" :{ "global_delay_factor": 2}}
    To tell napalm to pass that option to netmiko.
    """

    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        extras = extras or {}

        parameters: Dict[str, Any] = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "optional_args": {},
        }

        try:
            parameters["optional_args"][
                "ssh_config_file"
            ] = configuration.ssh.config_file  # type: ignore
        except AttributeError:
            pass

        parameters.update(extras)

        if port and "port" not in parameters["optional_args"]:
            parameters["optional_args"]["port"] = port

        if "auto_probe" not in parameters["optional_args"]:
            parameters["optional_args"]["auto_probe"] = 5

        connection = JunOSDriver(**parameters)
        connection.open()
        self.connection = connection

    def close(self) -> None:
        self.connection.close()