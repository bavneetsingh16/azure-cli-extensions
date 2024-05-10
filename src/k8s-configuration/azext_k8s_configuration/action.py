# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=protected-access

import argparse
from azure.cli.core.azclierror import InvalidArgumentValueError
from .vendored_sdks.v2024_04_01_preview.models import (
    KustomizationDefinition,
    KustomizationPatchDefinition,
)
from .validators import validate_kustomization
from . import consts
from .utils import parse_dependencies, parse_duration


class InternalKustomizationDefinition(KustomizationPatchDefinition):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # This call is after the call to super() to override the init method
        # making the self.name field null
        self.name = kwargs.get("name", "")

    def to_KustomizationDefinition(self):
        k_dict = dict(self.__dict__)
        del k_dict["additional_properties"]
        return KustomizationDefinition(**k_dict)

    def to_KustomizationPatchDefinition(self):
        k_dict = dict(self.__dict__)
        del k_dict["additional_properties"]
        return KustomizationPatchDefinition(**k_dict)


class KustomizationAddAction(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        validate_kustomization(values)
        dependencies = None
        sync_interval = None
        retry_interval = None
        timeout = None
        kwargs = {}
        for item in values:
            try:
                key, value = item.split("=", 1)
                if key in consts.DEPENDENCY_KEYS:
                    dependencies = parse_dependencies(value)
                elif key in consts.SYNC_INTERVAL_KEYS:
                    sync_interval = value
                elif key in consts.RETRY_INTERVAL_KEYS:
                    retry_interval = value
                elif key in consts.TIMEOUT_KEYS:
                    timeout = value
                else:
                    kwargs[key] = value
            except ValueError as ex:
                raise InvalidArgumentValueError(
                    "usage error: {} KEY=VALUE [KEY=VALUE ...]".format(option_string)
                ) from ex
        super().__call__(
            parser,
            namespace,
            InternalKustomizationDefinition(
                depends_on=dependencies,
                sync_interval_in_seconds=parse_duration(sync_interval),
                retry_interval_in_seconds=parse_duration(retry_interval),
                timeout_in_seconds=parse_duration(timeout),
                **kwargs
            ),
            option_string,
        )

class AddVerificationConfigSettings(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        settings = {}
        for item in values:
            try:
                key, value = item.split('=', 1)
                settings[key] = value
            except ValueError as ex:
                raise InvalidArgumentValueError('Usage error: {} verification_config_key=verification_config_value'.
                                         format(option_string)) from ex
        setattr(namespace, self.dest, settings)

class AddMatchOidcIdentitySettings(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        settings = getattr(namespace, self.dest, None)
        if settings is None:
            settings = []
        valid_keys = ['issuer', 'subject']
        if len(values) % 2 != 0:
            raise InvalidArgumentValueError('Each "issuer" should have a corresponding "subject".')
        for i in range(0, len(values), 2):
            identityDict = {}
            for j in range(i, i+2):
                try:
                    key, value = values[j].split('=', 1)
                    if key not in valid_keys:
                        raise InvalidArgumentValueError('Invalid key: {}. Only "issuer" and "subject" are allowed for matchOidcIdentity.'.
                                                        format(key))
                    identityDict[key] = value
                except ValueError as ex:
                    raise InvalidArgumentValueError('Usage error: {} match_oidc_identity_key=match_oidc_identity_value'.
                                                    format(option_string)) from ex
            settings.append(identityDict)
        setattr(namespace, self.dest, settings)
