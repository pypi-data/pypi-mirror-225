from __future__ import annotations

import requests
from typing import Dict, Optional
from .config import config
from dataclasses import dataclass
from base64 import b64encode


def parameter_convert(parameters: Dict) -> Dict:
    keys = parameters.keys()
    result = {f"{key}": [parameters[key]] for key in keys}
    return result


@dataclass
class PfdParameters:
    output_file_name: str
    report_unit_uri: str
    parameters: Optional[dict] = None
    ftp_config: Optional[dict] = None
    ftp_output_path: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class Job:

    def __init__(self, config_parameters: PfdParameters) -> None:
        self.output_file_name = config_parameters.output_file_name
        self.report_unit_uri = config_parameters.report_unit_uri
        self.parameters = config_parameters.parameters
        self.ftp_config = config_parameters.ftp_config
        self.ftp_output_path = config_parameters.ftp_output_path
        self.username = config_parameters.username if config_parameters.username else config.pdf.username
        self.password = config_parameters.password if config_parameters.password else config.pdf.password

    def generate_pdf_ftp_now(self):
        body = parameter_convert(self.parameters) if self.parameters else None
        data = config.pdf.default_body
        data["label"] = self.output_file_name
        data["baseOutputFilename"] = self.output_file_name
        data["source"]["reportUnitURI"] = self.report_unit_uri
        if body:
            data["source"]["parameters"]["parameterValues"] = body
        if self.ftp_config:
            data["repositoryDestination"]["outputFTPInfo"] = self.ftp_config
        if self.ftp_output_path:
            default_ftp = config.pdf.default_ftp
            default_ftp["folderPath"] = self.ftp_output_path
            data["repositoryDestination"]["outputFTPInfo"] = default_ftp

        headers = {
            "Content-Type": "application/job+json",
            "Authorization": "Basic " + b64encode(bytes(f"{self.username}:{self.password}", 'utf-8')).decode("utf-8")
        }

        response = requests.put(
            url=config.pdf.default_url, json=data, headers=headers)
        return response
