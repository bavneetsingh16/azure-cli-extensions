# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "providerhub authorized-application wait",
)
class Wait(AAZWaitCommand):
    """Place the CLI in a waiting state until a condition is met.
    """

    _aaz_info = {
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.providerhub/providerregistrations/{}/authorizedapplications/{}", "2024-04-01-preview"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.application_id = AAZUuidArg(
            options=["-n", "--name", "--application-id"],
            help="The application ID.",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.provider_namespace = AAZStrArg(
            options=["--provider-namespace"],
            help="The name of the resource provider hosted within ProviderHub.",
            required=True,
            id_part="name",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AuthorizedApplicationsGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=False)
        return result

    class AuthorizedApplicationsGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/providers/Microsoft.ProviderHub/providerRegistrations/{providerNamespace}/authorizedApplications/{applicationId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "applicationId", self.ctx.args.application_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "providerNamespace", self.ctx.args.provider_namespace,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2024-04-01-preview",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType()
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.data_authorizations = AAZListType(
                serialized_name="dataAuthorizations",
            )
            properties.provider_authorization = AAZObjectType(
                serialized_name="providerAuthorization",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )

            data_authorizations = cls._schema_on_200.properties.data_authorizations
            data_authorizations.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.data_authorizations.Element
            _element.resource_types = AAZListType(
                serialized_name="resourceTypes",
            )
            _element.role = AAZStrType(
                flags={"required": True},
            )

            resource_types = cls._schema_on_200.properties.data_authorizations.Element.resource_types
            resource_types.Element = AAZStrType()

            provider_authorization = cls._schema_on_200.properties.provider_authorization
            provider_authorization.managed_by_role_definition_id = AAZStrType(
                serialized_name="managedByRoleDefinitionId",
            )
            provider_authorization.role_definition_id = AAZStrType(
                serialized_name="roleDefinitionId",
            )

            system_data = cls._schema_on_200.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            return cls._schema_on_200


class _WaitHelper:
    """Helper class for Wait"""


__all__ = ["Wait"]
