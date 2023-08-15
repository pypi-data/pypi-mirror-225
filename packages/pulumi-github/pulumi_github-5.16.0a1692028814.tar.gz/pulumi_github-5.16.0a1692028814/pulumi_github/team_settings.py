# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['TeamSettingsArgs', 'TeamSettings']

@pulumi.input_type
class TeamSettingsArgs:
    def __init__(__self__, *,
                 team_id: pulumi.Input[str],
                 review_request_delegation: Optional[pulumi.Input['TeamSettingsReviewRequestDelegationArgs']] = None):
        """
        The set of arguments for constructing a TeamSettings resource.
        :param pulumi.Input[str] team_id: The GitHub team id or the GitHub team slug
        :param pulumi.Input['TeamSettingsReviewRequestDelegationArgs'] review_request_delegation: The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        """
        pulumi.set(__self__, "team_id", team_id)
        if review_request_delegation is not None:
            pulumi.set(__self__, "review_request_delegation", review_request_delegation)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Input[str]:
        """
        The GitHub team id or the GitHub team slug
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="reviewRequestDelegation")
    def review_request_delegation(self) -> Optional[pulumi.Input['TeamSettingsReviewRequestDelegationArgs']]:
        """
        The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        """
        return pulumi.get(self, "review_request_delegation")

    @review_request_delegation.setter
    def review_request_delegation(self, value: Optional[pulumi.Input['TeamSettingsReviewRequestDelegationArgs']]):
        pulumi.set(self, "review_request_delegation", value)


@pulumi.input_type
class _TeamSettingsState:
    def __init__(__self__, *,
                 review_request_delegation: Optional[pulumi.Input['TeamSettingsReviewRequestDelegationArgs']] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 team_slug: Optional[pulumi.Input[str]] = None,
                 team_uid: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TeamSettings resources.
        :param pulumi.Input['TeamSettingsReviewRequestDelegationArgs'] review_request_delegation: The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        :param pulumi.Input[str] team_id: The GitHub team id or the GitHub team slug
        :param pulumi.Input[str] team_slug: The slug of the Team within the Organization.
        :param pulumi.Input[str] team_uid: The unique ID of the Team on GitHub. Corresponds to the ID of the 'github_team_settings' resource.
        """
        if review_request_delegation is not None:
            pulumi.set(__self__, "review_request_delegation", review_request_delegation)
        if team_id is not None:
            pulumi.set(__self__, "team_id", team_id)
        if team_slug is not None:
            pulumi.set(__self__, "team_slug", team_slug)
        if team_uid is not None:
            pulumi.set(__self__, "team_uid", team_uid)

    @property
    @pulumi.getter(name="reviewRequestDelegation")
    def review_request_delegation(self) -> Optional[pulumi.Input['TeamSettingsReviewRequestDelegationArgs']]:
        """
        The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        """
        return pulumi.get(self, "review_request_delegation")

    @review_request_delegation.setter
    def review_request_delegation(self, value: Optional[pulumi.Input['TeamSettingsReviewRequestDelegationArgs']]):
        pulumi.set(self, "review_request_delegation", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> Optional[pulumi.Input[str]]:
        """
        The GitHub team id or the GitHub team slug
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="teamSlug")
    def team_slug(self) -> Optional[pulumi.Input[str]]:
        """
        The slug of the Team within the Organization.
        """
        return pulumi.get(self, "team_slug")

    @team_slug.setter
    def team_slug(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_slug", value)

    @property
    @pulumi.getter(name="teamUid")
    def team_uid(self) -> Optional[pulumi.Input[str]]:
        """
        The unique ID of the Team on GitHub. Corresponds to the ID of the 'github_team_settings' resource.
        """
        return pulumi.get(self, "team_uid")

    @team_uid.setter
    def team_uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_uid", value)


class TeamSettings(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 review_request_delegation: Optional[pulumi.Input[pulumi.InputType['TeamSettingsReviewRequestDelegationArgs']]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource manages the team settings (in particular the request review delegation settings) within the organization

        Creating this resource will alter the team Code Review settings.

        The team must both belong to the same organization configured in the provider on GitHub.

        > **Note**: This resource relies on the v4 GraphQl GitHub API. If this API is not available, or the Stone Crop schema preview is not available, then this resource will not work as intended.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_github as github

        # Add a repository to the team
        some_team = github.Team("someTeam", description="Some cool team")
        code_review_settings = github.TeamSettings("codeReviewSettings",
            team_id=some_team.id,
            review_request_delegation=github.TeamSettingsReviewRequestDelegationArgs(
                algorithm="ROUND_ROBIN",
                member_count=1,
                notify=True,
            ))
        ```

        ## Import

        GitHub Teams can be imported using the GitHub team ID, or the team slug e.g.

        ```sh
         $ pulumi import github:index/teamSettings:TeamSettings code_review_settings 1234567
        ```

         or,

        ```sh
         $ pulumi import github:index/teamSettings:TeamSettings code_review_settings SomeTeam
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['TeamSettingsReviewRequestDelegationArgs']] review_request_delegation: The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        :param pulumi.Input[str] team_id: The GitHub team id or the GitHub team slug
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TeamSettingsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource manages the team settings (in particular the request review delegation settings) within the organization

        Creating this resource will alter the team Code Review settings.

        The team must both belong to the same organization configured in the provider on GitHub.

        > **Note**: This resource relies on the v4 GraphQl GitHub API. If this API is not available, or the Stone Crop schema preview is not available, then this resource will not work as intended.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_github as github

        # Add a repository to the team
        some_team = github.Team("someTeam", description="Some cool team")
        code_review_settings = github.TeamSettings("codeReviewSettings",
            team_id=some_team.id,
            review_request_delegation=github.TeamSettingsReviewRequestDelegationArgs(
                algorithm="ROUND_ROBIN",
                member_count=1,
                notify=True,
            ))
        ```

        ## Import

        GitHub Teams can be imported using the GitHub team ID, or the team slug e.g.

        ```sh
         $ pulumi import github:index/teamSettings:TeamSettings code_review_settings 1234567
        ```

         or,

        ```sh
         $ pulumi import github:index/teamSettings:TeamSettings code_review_settings SomeTeam
        ```

        :param str resource_name: The name of the resource.
        :param TeamSettingsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TeamSettingsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 review_request_delegation: Optional[pulumi.Input[pulumi.InputType['TeamSettingsReviewRequestDelegationArgs']]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TeamSettingsArgs.__new__(TeamSettingsArgs)

            __props__.__dict__["review_request_delegation"] = review_request_delegation
            if team_id is None and not opts.urn:
                raise TypeError("Missing required property 'team_id'")
            __props__.__dict__["team_id"] = team_id
            __props__.__dict__["team_slug"] = None
            __props__.__dict__["team_uid"] = None
        super(TeamSettings, __self__).__init__(
            'github:index/teamSettings:TeamSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            review_request_delegation: Optional[pulumi.Input[pulumi.InputType['TeamSettingsReviewRequestDelegationArgs']]] = None,
            team_id: Optional[pulumi.Input[str]] = None,
            team_slug: Optional[pulumi.Input[str]] = None,
            team_uid: Optional[pulumi.Input[str]] = None) -> 'TeamSettings':
        """
        Get an existing TeamSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['TeamSettingsReviewRequestDelegationArgs']] review_request_delegation: The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        :param pulumi.Input[str] team_id: The GitHub team id or the GitHub team slug
        :param pulumi.Input[str] team_slug: The slug of the Team within the Organization.
        :param pulumi.Input[str] team_uid: The unique ID of the Team on GitHub. Corresponds to the ID of the 'github_team_settings' resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TeamSettingsState.__new__(_TeamSettingsState)

        __props__.__dict__["review_request_delegation"] = review_request_delegation
        __props__.__dict__["team_id"] = team_id
        __props__.__dict__["team_slug"] = team_slug
        __props__.__dict__["team_uid"] = team_uid
        return TeamSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="reviewRequestDelegation")
    def review_request_delegation(self) -> pulumi.Output[Optional['outputs.TeamSettingsReviewRequestDelegation']]:
        """
        The settings for delegating code reviews to individuals on behalf of the team. If this block is present, even without any fields, then review request delegation will be enabled for the team. See GitHub Review Request Delegation below for details. See [GitHub's documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/managing-code-review-settings-for-your-team#configuring-team-notifications) for more configuration details.
        """
        return pulumi.get(self, "review_request_delegation")

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Output[str]:
        """
        The GitHub team id or the GitHub team slug
        """
        return pulumi.get(self, "team_id")

    @property
    @pulumi.getter(name="teamSlug")
    def team_slug(self) -> pulumi.Output[str]:
        """
        The slug of the Team within the Organization.
        """
        return pulumi.get(self, "team_slug")

    @property
    @pulumi.getter(name="teamUid")
    def team_uid(self) -> pulumi.Output[str]:
        """
        The unique ID of the Team on GitHub. Corresponds to the ID of the 'github_team_settings' resource.
        """
        return pulumi.get(self, "team_uid")

