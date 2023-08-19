from dataclasses import dataclass, field
from django.conf import settings

DEFAULT_BODY = {
    "label": "---",
    "description": "Sample description",
    "trigger": {
        "simpleTrigger": {
            "timezone": "America/Costa_Rica",
            "startType": 1,
            "occurrenceCount": 1,
            "recurrenceInterval": 1,
            "recurrenceIntervalUnit": "DAY"
        }
    },
    "baseOutputFilename": "-----",
    "exportType": "DEFAULT",
    "outputLocale": "es_CR",
    "outputTimeZone": "America/Costa_Rica",
    "source": {
        "reportUnitURI": "--------",
        "parameters": {
            "parameterValues": {}  # parameter
        }
    },
    "outputFormats": {
        "outputFormat": [
            "PDF"
        ]
    },
    "repositoryDestination": {
        "folderURI": "/CARPETA_DE_PRUEBA",
        "overwriteFiles": True,
        "sequentialFilenames": False,
        "saveToRepository": False,
        "usingDefaultReportOutputFolderURI": False,
        "outputFTPInfo": {}
    }
}


DEFAULT_URL = 'http://jasperserver.dev.istmocenter.com/jasperserver/rest_v2/jobs/'


OUTPUT_FTP_INFO = {
    "userName": "system",
    "password": "None123",
    "folderPath": "----",
    "serverName": "nfs.dev.istmocenter.com",
    "type": "sftp",
    "port": 22,
    "implicit": True,
    "pbsz": 0,
    "propertiesMap": {}
}


def get_default_body():
    return settings.PDF_DEFAULT_BODY if hasattr(
        settings, 'PDF_DEFAULT_BODY') else DEFAULT_BODY


def get_default_url():
    return settings.PDF_DEFAULT_URL if hasattr(
        settings, 'PDF_DEFAULT_URL') else DEFAULT_URL


def get_default_ftp():
    return settings.PDF_OUTPUT_FTP_INFO if hasattr(
        settings, 'PDF_OUTPUT_FTP_INFO') else OUTPUT_FTP_INFO


@dataclass
class PdfItem:
    default_body: dict = field(default_factory=get_default_body)
    default_url: dict = field(default_factory=get_default_url)
    default_ftp: dict = field(default_factory=get_default_ftp)
    username: str = settings.PDF_DEFAULT_USERNAME if hasattr(
        settings, 'PDF_DEFAULT_USERNAME') else 'jasperadmin'
    password: str = settings.PDF_DEFAULT_PASSWORD if hasattr(
        settings, 'PDF_DEFAULT_PASSWORD') else 'bitnami'


@dataclass
class ConfigItem:
    pdf: PdfItem = PdfItem()


config = ConfigItem()
