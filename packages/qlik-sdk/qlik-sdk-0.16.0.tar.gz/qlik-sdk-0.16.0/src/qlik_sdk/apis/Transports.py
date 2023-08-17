# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Literal

from ..auth import Auth, Config


@dataclass
class Email:
    """

    Attributes
    ----------
    body: str
      email body
    recipient: str
      email recipient (email address)
    subject: str
      email subject
    """

    body: str = None
    recipient: str = None
    subject: str = None

    def __init__(self_, **kvargs):
        if "body" in kvargs and kvargs["body"] is not None:
            self_.body = kvargs["body"]
        if "recipient" in kvargs and kvargs["recipient"] is not None:
            self_.recipient = kvargs["recipient"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmailConfigFieldPatch:
    """
    A JSON Patch document as defined in https://datatracker.ietf.org/doc/html/rfc6902.

    Attributes
    ----------
    op: Literal["replace, remove, add"]
      The operation to be performed.
    path: Literal["/username", "/serverAddress", "/serverPort", "/securityType", "/emailAddress", "/emailPassword"]
      The path for the given resource field to patch.
    value: str
      The value to be used for this operation.
    """

    op: Literal["replace, remove, add"] = None
    path: Literal[
        "/username",
        "/serverAddress",
        "/serverPort",
        "/securityType",
        "/emailAddress",
        "/emailPassword",
    ] = None
    value: str = None

    def __init__(self_, **kvargs):
        if "op" in kvargs and kvargs["op"] is not None:
            self_.op = kvargs["op"]
        if "path" in kvargs and kvargs["path"] is not None:
            self_.path = kvargs["path"]
        if "value" in kvargs and kvargs["value"] is not None:
            self_.value = kvargs["value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmailConfigGet:
    """

    Attributes
    ----------
    authFailures: float
      Number of authentication failures
    emailAddress: str
      used for SMTP authentication
    isValid: bool
      Is the configuration valid
    modificationTime: str
      Last modification time. Formatted as a ISO 8601 string.
    passwordExists: bool
      Indicates if password is defined for this smtp config. The password itself is not returned!
    securityType: str
      one of none, StartTLS or SSL/TLS
    serverAddress: str
      domain name or IP address of SMTP server
    serverPort: float
      smtp server listening port
    status: SmtpConfigStatus
      Contains statusCode and statusReason
    tenantId: str
      The tenant Id
    username: str
      user name
    """

    authFailures: float = None
    emailAddress: str = None
    isValid: bool = None
    modificationTime: str = None
    passwordExists: bool = None
    securityType: str = None
    serverAddress: str = None
    serverPort: float = None
    status: SmtpConfigStatus = None
    tenantId: str = None
    username: str = None

    def __init__(self_, **kvargs):
        if "authFailures" in kvargs and kvargs["authFailures"] is not None:
            self_.authFailures = kvargs["authFailures"]
        if "emailAddress" in kvargs and kvargs["emailAddress"] is not None:
            self_.emailAddress = kvargs["emailAddress"]
        if "isValid" in kvargs and kvargs["isValid"] is not None:
            self_.isValid = kvargs["isValid"]
        if "modificationTime" in kvargs and kvargs["modificationTime"] is not None:
            self_.modificationTime = kvargs["modificationTime"]
        if "passwordExists" in kvargs and kvargs["passwordExists"] is not None:
            self_.passwordExists = kvargs["passwordExists"]
        if "securityType" in kvargs and kvargs["securityType"] is not None:
            self_.securityType = kvargs["securityType"]
        if "serverAddress" in kvargs and kvargs["serverAddress"] is not None:
            self_.serverAddress = kvargs["serverAddress"]
        if "serverPort" in kvargs and kvargs["serverPort"] is not None:
            self_.serverPort = kvargs["serverPort"]
        if "status" in kvargs and kvargs["status"] is not None:
            if (
                type(kvargs["status"]).__name__
                == EmailConfigGet.__annotations__["status"]
            ):
                self_.status = kvargs["status"]
            else:
                self_.status = SmtpConfigStatus(**kvargs["status"])
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "username" in kvargs and kvargs["username"] is not None:
            self_.username = kvargs["username"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmailConfigPatch(List["EmailConfigFieldPatch"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(EmailConfigFieldPatch(**e))


@dataclass
class SmtpCheck:
    """

    Attributes
    ----------
    isValid: bool
      true if smtp config is correct and complete. Will return false if smtp-config does not exist at all
    """

    isValid: bool = None

    def __init__(self_, **kvargs):
        if "isValid" in kvargs and kvargs["isValid"] is not None:
            self_.isValid = kvargs["isValid"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SmtpConfigStatus:
    """
    Contains statusCode and statusReason

    Attributes
    ----------
    statusCode: float
      Status code
    statusReason: str
      Status reason
    """

    statusCode: float = None
    statusReason: str = None

    def __init__(self_, **kvargs):
        if "statusCode" in kvargs and kvargs["statusCode"] is not None:
            self_.statusCode = kvargs["statusCode"]
        if "statusReason" in kvargs and kvargs["statusReason"] is not None:
            self_.statusReason = kvargs["statusReason"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SmtpResult:
    """

    Attributes
    ----------
    connectionFailed: bool
      could not resolve domain name, connection refused, connection timed out, SSL mismatch
    message: str
      error message from SMTP middleware .. a bit technical but could be useful to administrator
    smtpResponseCode: int
      smtp result code string from the SMTP server. eg. "250 2.6.0"
    success: bool
      was SMTP operation successful or not. Other fields herein provide more detail
    """

    connectionFailed: bool = None
    message: str = None
    smtpResponseCode: int = None
    success: bool = None

    def __init__(self_, **kvargs):
        if "connectionFailed" in kvargs and kvargs["connectionFailed"] is not None:
            self_.connectionFailed = kvargs["connectionFailed"]
        if "message" in kvargs and kvargs["message"] is not None:
            self_.message = kvargs["message"]
        if "smtpResponseCode" in kvargs and kvargs["smtpResponseCode"] is not None:
            self_.smtpResponseCode = kvargs["smtpResponseCode"]
        if "success" in kvargs and kvargs["success"] is not None:
            self_.success = kvargs["success"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Transports:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def send_test_email_email_config(self, data: Email) -> SmtpResult:
        """
        Send a test mail with the supplied email info (subject, body, recipient). Email config from database is used for the connection.

        Parameters
        ----------
        data: Email
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/transports/email-config/actions/send-test-email",
            method="POST",
            params={},
            data=data,
        )
        obj = SmtpResult(**response.json())
        obj.auth = self.auth
        return obj

    def validate_email_config(self) -> SmtpCheck:
        """
        Returns the isValid value for the email configuration for the tenant. Will return false if no email configuration exists.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/transports/email-config/actions/validate",
            method="POST",
            params={},
            data=None,
        )
        obj = SmtpCheck(**response.json())
        obj.auth = self.auth
        return obj

    def verify_connection_email_config(self) -> SmtpResult:
        """
        Verifies connection to email server for tenant provided via JWT

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/transports/email-config/actions/verify-connection",
            method="POST",
            params={},
            data=None,
        )
        obj = SmtpResult(**response.json())
        obj.auth = self.auth
        return obj

    def delete_email_config(self) -> None:
        """
        Deletes email configuration for a given tenant id (retrieved from JWT).

        Parameters
        ----------
        """
        self.auth.rest(
            path="/transports/email-config",
            method="DELETE",
            params={},
            data=None,
        )

    def get_email_config(self) -> EmailConfigGet:
        """
        Returns the email configuration for a given tenant id (retrieved from JWT).

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/transports/email-config",
            method="GET",
            params={},
            data=None,
        )
        obj = EmailConfigGet(**response.json())
        obj.auth = self.auth
        return obj

    def patch_email_config(self, data: EmailConfigPatch) -> None:
        """
        Patch the email configuration for a given tenant id (retrieved from JWT).

        Parameters
        ----------
        data: EmailConfigPatch
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/transports/email-config",
            method="PATCH",
            params={},
            data=data,
        )
