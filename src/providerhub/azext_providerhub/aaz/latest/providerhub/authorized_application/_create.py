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
    "providerhub authorized-application create",
)
class Create(AAZCommand):
    """Create the authorized application.

    :example: authorized-application create
        az providerhub authorized-application create -n "8b51e6a7-7814-42bd-aa17-3fb1837b3b7a" --data-authorizations "[{{role:ServiceOwner}}]" --provider-namespace "{providerNamespace}"
    """

    _aaz_info = {
        "version": "2024-04-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.providerhub/providerregistrations/{}/authorizedapplications/{}", "2024-04-01-preview"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

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
        )
        _args_schema.provider_namespace = AAZStrArg(
            options=["--provider-namespace"],
            help="The name of the resource provider hosted within ProviderHub.",
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.data_authorizations = AAZListArg(
            options=["--data-authorizations"],
            arg_group="Properties",
            help="The authorizations that determine the level of data access permissions on the specified resource types.",
        )
        _args_schema.provider_authorization = AAZObjectArg(
            options=["--provider-authorization"],
            arg_group="Properties",
            help="The resource provider authorization.",
        )

        data_authorizations = cls._args_schema.data_authorizations
        data_authorizations.Element = AAZObjectArg()

        _element = cls._args_schema.data_authorizations.Element
        _element.resource_types = AAZListArg(
            options=["resource-types"],
            help="The resource types from the defined resource types in the provider namespace that the application can access. If no resource types are specified and the role is service owner, the default is * which is all resource types",
        )
        _element.role = AAZStrArg(
            options=["role"],
            help="The ownership role the application has on the resource types. The service owner role gives the application owner permissions. The limited owner role gives elevated permissions but does not allow all the permissions of a service owner, such as read/write on internal metadata.",
            required=True,
            enum={"LimitedOwner": "LimitedOwner", "ServiceOwner": "ServiceOwner"},
        )

        resource_types = cls._args_schema.data_authorizations.Element.resource_types
        resource_types.Element = AAZStrArg()

        provider_authorization = cls._args_schema.provider_authorization
        provider_authorization.managed_by_role_definition_id = AAZStrArg(
            options=["managed-by-role-definition-id"],
            help="The managed by role definition ID for the application.",
        )
        provider_authorization.role_definition_id = AAZStrArg(
            options=["role-definition-id"],
            help="The role definition ID for the application.",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.AuthorizedApplicationsCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class AuthorizedApplicationsCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/providers/Microsoft.ProviderHub/providerRegistrations/{providerNamespace}/authorizedApplications/{applicationId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

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
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("properties", AAZObjectType)

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("dataAuthorizations", AAZListType, ".data_authorizations")
                properties.set_prop("providerAuthorization", AAZObjectType, ".provider_authorization")

            data_authorizations = _builder.get(".properties.dataAuthorizations")
            if data_authorizations is not None:
                data_authorizations.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.dataAuthorizations[]")
            if _elements is not None:
                _elements.set_prop("resourceTypes", AAZListType, ".resource_types")
                _elements.set_prop("role", AAZStrType, ".role", typ_kwargs={"flags": {"required": True}})

            resource_types = _builder.get(".properties.dataAuthorizations[].resourceTypes")
            if resource_types is not None:
                resource_types.set_elements(AAZStrType, ".")

            provider_authorization = _builder.get(".properties.providerAuthorization")
            if provider_authorization is not None:
                provider_authorization.set_prop("managedByRoleDefinitionId", AAZStrType, ".managed_by_role_definition_id")
                provider_authorization.set_prop("roleDefinitionId", AAZStrType, ".role_definition_id")

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.properties = AAZObjectType()
            _schema_on_200_201.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200_201.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200_201.properties
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

            data_authorizations = cls._schema_on_200_201.properties.data_authorizations
            data_authorizations.Element = AAZObjectType()

            _element = cls._schema_on_200_201.properties.data_authorizations.Element
            _element.resource_types = AAZListType(
                serialized_name="resourceTypes",
            )
            _element.role = AAZStrType(
                flags={"required": True},
            )

            resource_types = cls._schema_on_200_201.properties.data_authorizations.Element.resource_types
            resource_types.Element = AAZStrType()

            provider_authorization = cls._schema_on_200_201.properties.provider_authorization
            provider_authorization.managed_by_role_definition_id = AAZStrType(
                serialized_name="managedByRoleDefinitionId",
            )
            provider_authorization.role_definition_id = AAZStrType(
                serialized_name="roleDefinitionId",
            )

            system_data = cls._schema_on_200_201.system_data
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

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""


__all__ = ["Create"]
