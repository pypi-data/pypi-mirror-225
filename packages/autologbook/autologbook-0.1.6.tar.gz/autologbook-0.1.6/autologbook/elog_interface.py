from __future__ import annotations
import elog
import configparser
from PyQt5.QtCore import QSettings
from autologbook import autoconfig, autoerror
import logging

log = logging.getLogger('__main__')


class ELOGConnectionParameters:
    def __init__(self, hostname: str, port: int, user: str, password: str, use_ssl: bool,
                 encrypt_pwd: bool = False, *args, **kwargs):
        self.elog_hostname = hostname
        self.elog_port = port
        self.elog_user = user
        self.elog_password = password
        self.elog_use_ssl = use_ssl
        self.elog_encrypt_pwd = encrypt_pwd

    @classmethod
    def from_configuration(cls, config: configparser.ConfigParser) -> ELOGConnectionParameters:
        return cls(
            hostname=config['elog']['elog_hostname'],
            port=config.getint('elog', 'elog_port'),
            user=config['elog']['elog_user'],
            password=config['elog']['elog_password'],
            use_ssl=config.getboolean('elog', 'use_ssl'),
            encrypt_pwd=False)

    @classmethod
    def from_qsettings(cls, settings: QSettings) -> ELOGConnectionParameters:
        return cls(
            hostname=settings.value('elog_hostname'),
            port=int(settings.value('elog_port', defaultValue=8080)),
            user=settings.value('elog_user_name'),
            password=settings.value('elog_password'),
            use_ssl=bool(settings.value('elog_use_ssl')),
            encrypt_pwd=False
        )

    @classmethod
    def from_config_module(cls) -> ELOGConnectionParameters:
        return cls(
            hostname=autoconfig.ELOG_HOSTNAME,
            port=autoconfig.ELOG_PORT,
            user=autoconfig.ELOG_USER,
            password=autoconfig.ELOG_PASSWORD,
            use_ssl=autoconfig.USE_SSL,
            encrypt_pwd=False
        )

    def to_dict(self) -> dict:
        return {
            'hostname': self.elog_hostname,
            'port': self.elog_port,
            'user': self.elog_user,
            'password': self.elog_password,
            'use_ssl': self.elog_use_ssl,
            'encrypt_pwd': self.elog_encrypt_pwd
        }

    def __eq__(self, other):
        identical = True
        for key in self.__dict__:
            identical = identical and self.__dict__[key] == other.__dict__[key]
        return identical


class ELOGHandleFactory:
    def __init__(self, connection_parameters: ELOGConnectionParameters = None):
        self._elog_connection_parameters = connection_parameters
        self._existing_handles = dict()

    def set_connection_parameters(self, connection_parameters: ELOGConnectionParameters):
        if self._elog_connection_parameters != connection_parameters:
            self._elog_connection_parameters = connection_parameters
            self._existing_handles.clear()

    def get_logbook_handle(self, logbook: str) -> AdvLogbook:
        if logbook in self._existing_handles:
            return self._existing_handles[logbook]
        else:
            if logbook == autoconfig.PROTOCOL_LIST_LOGBOOK:
                class_ = ListLogbook
            else:
                class_ = AnalysisLogbook
            new_handle = class_(**self._elog_connection_parameters.to_dict(), logbook=logbook)
            self._existing_handles[logbook] = new_handle
            return new_handle


elog_handle_factory = ELOGHandleFactory(ELOGConnectionParameters.from_config_module())


class AdvLogbook(elog.Logbook):
    timeout = autoconfig.ELOG_TIMEOUT
    protocol_id_key = ''

    def __init__(self, hostname: str, port: int, user: str, password: str, use_ssl: bool, encrypt_pwd: bool,
                 logbook: str = None, *args, **kwargs):
        super().__init__(hostname=hostname, logbook=logbook, port=port, user=user, password=password, use_ssl=use_ssl,
                         encrypt_pwd=encrypt_pwd, *args, **kwargs)
        self._connection_verified = False
        self._connection_parameters = ELOGConnectionParameters(hostname, port, user, password, use_ssl, encrypt_pwd)

    def get_connection_parameters(self) -> ELOGConnectionParameters:
        return self._connection_parameters

    @property
    def connection_verified(self) -> bool:
        return self._connection_verified

    @connection_verified.setter
    def connection_verified(self, status: bool):
        self._connection_verified = status

    def get_base_url(self) -> str:
        return self._url.rstrip('/')

    def get_msg_ids(self, protocol_id: int | str) -> list[int]:

        log.info('Getting message IDs for this protocol entry')
        msg_ids = self.search({self.protocol_id_key: protocol_id}, timeout=self.timeout)
        real_ids = list()

        for msg_id in msg_ids:
            _, attributes, __ = self.read(msg_id, timeout=self.timeout)

            if attributes[self.protocol_id_key] == protocol_id:
                real_ids.append(msg_id)

        return real_ids

    def check_connection(self):
        try:
            self.get_last_message_id(timeout=self.timeout)
            self._connection_verified = True
        except elog.LogbookError as e:
            self._connection_verified = False
            raise e

    def refresh(self) -> AdvLogbook:
        return elog_handle_factory.get_logbook_handle(self.logbook)



class AnalysisLogbook(AdvLogbook):
    protocol_id_key = 'Protocol ID'

    def get_parent_msg_id(self, protocol_id: int | str) -> int:
        msg_ids = self.get_msg_ids(protocol_id)
        parents = list()
        for msg_id in msg_ids:
            parent = self.get_parent(msg_id, timeout=self.timeout)
            if parent:
                parents.append(parent)

        if len(parents) == 1:
            return parents[0]
        else:
            raise autoerror.InvalidParent

    def verify_message_hierarchy(self, ids: list[int]) -> tuple[bool, list[int]]:
        # we expect to have one top level id and all the other should be its children.
        # the top level should have the lowest id, that's why we sort it

        # the hierarchy is ok if
        # 1. there is one parent
        # 2. all children are in the list
        # 3. there are no other id in the list (in other words, the size of ids is 1 bigger than the children

        hierarchy_ok = False
        ordered_id = list()
        for msg_id in sorted(ids):
            if self.get_parent(msg_id, timeout=self.timeout) is None:
                # then this msg_id is the parent.
                # get all its children
                children = self.get_children(msg_id, timeout=self.timeout)
                hierarchy_ok = all(i in ids for i in children) and len(children) == len(ids) - 1
                if hierarchy_ok:
                    ordered_id = [msg_id, *children]
                break
        return hierarchy_ok, ordered_id


class ListLogbook(AdvLogbook):
    protocol_id_key = 'Protocol number'

    def get_msg_id(self, protocol_id: int | str) -> int | None:
        l = self.get_msg_ids(protocol_id)
        if len(l):
            return l[0]
        else:
            return None
