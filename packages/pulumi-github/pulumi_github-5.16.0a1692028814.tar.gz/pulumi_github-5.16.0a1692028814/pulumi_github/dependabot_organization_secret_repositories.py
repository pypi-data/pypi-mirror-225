# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['DependabotOrganizationSecretRepositoriesArgs', 'DependabotOrganizationSecretRepositories']

@pulumi.input_type
class DependabotOrganizationSecretRepositoriesArgs:
    def __init__(__self__, *,
                 secret_name: pulumi.Input[str],
                 selected_repository_ids: pulumi.Input[Sequence[pulumi.Input[int]]]):
        """
        The set of arguments for constructing a DependabotOrganizationSecretRepositories resource.
        :param pulumi.Input[str] secret_name: Name of the existing secret.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] selected_repository_ids: An array of repository ids that can access the organization secret.
        """
        pulumi.set(__self__, "secret_name", secret_name)
        pulumi.set(__self__, "selected_repository_ids", selected_repository_ids)

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> pulumi.Input[str]:
        """
        Name of the existing secret.
        """
        return pulumi.get(self, "secret_name")

    @secret_name.setter
    def secret_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "secret_name", value)

    @property
    @pulumi.getter(name="selectedRepositoryIds")
    def selected_repository_ids(self) -> pulumi.Input[Sequence[pulumi.Input[int]]]:
        """
        An array of repository ids that can access the organization secret.
        """
        return pulumi.get(self, "selected_repository_ids")

    @selected_repository_ids.setter
    def selected_repository_ids(self, value: pulumi.Input[Sequence[pulumi.Input[int]]]):
        pulumi.set(self, "selected_repository_ids", value)


@pulumi.input_type
class _DependabotOrganizationSecretRepositoriesState:
    def __init__(__self__, *,
                 secret_name: Optional[pulumi.Input[str]] = None,
                 selected_repository_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None):
        """
        Input properties used for looking up and filtering DependabotOrganizationSecretRepositories resources.
        :param pulumi.Input[str] secret_name: Name of the existing secret.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] selected_repository_ids: An array of repository ids that can access the organization secret.
        """
        if secret_name is not None:
            pulumi.set(__self__, "secret_name", secret_name)
        if selected_repository_ids is not None:
            pulumi.set(__self__, "selected_repository_ids", selected_repository_ids)

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the existing secret.
        """
        return pulumi.get(self, "secret_name")

    @secret_name.setter
    def secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_name", value)

    @property
    @pulumi.getter(name="selectedRepositoryIds")
    def selected_repository_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        An array of repository ids that can access the organization secret.
        """
        return pulumi.get(self, "selected_repository_ids")

    @selected_repository_ids.setter
    def selected_repository_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "selected_repository_ids", value)


class DependabotOrganizationSecretRepositories(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 secret_name: Optional[pulumi.Input[str]] = None,
                 selected_repository_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 __props__=None):
        """
        Create a DependabotOrganizationSecretRepositories resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] secret_name: Name of the existing secret.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] selected_repository_ids: An array of repository ids that can access the organization secret.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DependabotOrganizationSecretRepositoriesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a DependabotOrganizationSecretRepositories resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param DependabotOrganizationSecretRepositoriesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DependabotOrganizationSecretRepositoriesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 secret_name: Optional[pulumi.Input[str]] = None,
                 selected_repository_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DependabotOrganizationSecretRepositoriesArgs.__new__(DependabotOrganizationSecretRepositoriesArgs)

            if secret_name is None and not opts.urn:
                raise TypeError("Missing required property 'secret_name'")
            __props__.__dict__["secret_name"] = secret_name
            if selected_repository_ids is None and not opts.urn:
                raise TypeError("Missing required property 'selected_repository_ids'")
            __props__.__dict__["selected_repository_ids"] = selected_repository_ids
        super(DependabotOrganizationSecretRepositories, __self__).__init__(
            'github:index/dependabotOrganizationSecretRepositories:DependabotOrganizationSecretRepositories',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            secret_name: Optional[pulumi.Input[str]] = None,
            selected_repository_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None) -> 'DependabotOrganizationSecretRepositories':
        """
        Get an existing DependabotOrganizationSecretRepositories resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] secret_name: Name of the existing secret.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] selected_repository_ids: An array of repository ids that can access the organization secret.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DependabotOrganizationSecretRepositoriesState.__new__(_DependabotOrganizationSecretRepositoriesState)

        __props__.__dict__["secret_name"] = secret_name
        __props__.__dict__["selected_repository_ids"] = selected_repository_ids
        return DependabotOrganizationSecretRepositories(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> pulumi.Output[str]:
        """
        Name of the existing secret.
        """
        return pulumi.get(self, "secret_name")

    @property
    @pulumi.getter(name="selectedRepositoryIds")
    def selected_repository_ids(self) -> pulumi.Output[Sequence[int]]:
        """
        An array of repository ids that can access the organization secret.
        """
        return pulumi.get(self, "selected_repository_ids")

