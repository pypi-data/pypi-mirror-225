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

__all__ = [
    'GetFirewallResult',
    'AwaitableGetFirewallResult',
    'get_firewall',
    'get_firewall_output',
]

@pulumi.output_type
class GetFirewallResult:
    """
    A collection of values returned by getFirewall.
    """
    def __init__(__self__, apply_tos=None, id=None, labels=None, most_recent=None, name=None, rules=None, with_selector=None):
        if apply_tos and not isinstance(apply_tos, list):
            raise TypeError("Expected argument 'apply_tos' to be a list")
        pulumi.set(__self__, "apply_tos", apply_tos)
        if id and not isinstance(id, int):
            raise TypeError("Expected argument 'id' to be a int")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if with_selector and not isinstance(with_selector, str):
            raise TypeError("Expected argument 'with_selector' to be a str")
        pulumi.set(__self__, "with_selector", with_selector)

    @property
    @pulumi.getter(name="applyTos")
    def apply_tos(self) -> Optional[Sequence['outputs.GetFirewallApplyToResult']]:
        """
        Configuration of the Applied Resources
        """
        return pulumi.get(self, "apply_tos")

    @property
    @pulumi.getter
    def id(self) -> Optional[int]:
        """
        (int) Unique ID of the Firewall.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def labels(self) -> Optional[Mapping[str, Any]]:
        """
        (map) User-defined labels (key-value pairs)
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        (string) Name of the Firewall.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.GetFirewallRuleResult']]:
        """
        (string)  Configuration of a Rule from this Firewall.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="withSelector")
    def with_selector(self) -> Optional[str]:
        return pulumi.get(self, "with_selector")


class AwaitableGetFirewallResult(GetFirewallResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirewallResult(
            apply_tos=self.apply_tos,
            id=self.id,
            labels=self.labels,
            most_recent=self.most_recent,
            name=self.name,
            rules=self.rules,
            with_selector=self.with_selector)


def get_firewall(apply_tos: Optional[Sequence[pulumi.InputType['GetFirewallApplyToArgs']]] = None,
                 id: Optional[int] = None,
                 labels: Optional[Mapping[str, Any]] = None,
                 most_recent: Optional[bool] = None,
                 name: Optional[str] = None,
                 rules: Optional[Sequence[pulumi.InputType['GetFirewallRuleArgs']]] = None,
                 with_selector: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirewallResult:
    """
    Provides details about a specific Hetzner Cloud Firewall.

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    sample_firewall1 = hcloud.get_firewall(name="sample-firewall-1")
    sample_firewall2 = hcloud.get_firewall(id=4711)
    ```


    :param Sequence[pulumi.InputType['GetFirewallApplyToArgs']] apply_tos: Configuration of the Applied Resources
    :param int id: ID of the firewall.
    :param Mapping[str, Any] labels: (map) User-defined labels (key-value pairs)
    :param bool most_recent: Return most recent firewall if multiple are found.
    :param str name: Name of the firewall.
    :param Sequence[pulumi.InputType['GetFirewallRuleArgs']] rules: (string)  Configuration of a Rule from this Firewall.
    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    """
    __args__ = dict()
    __args__['applyTos'] = apply_tos
    __args__['id'] = id
    __args__['labels'] = labels
    __args__['mostRecent'] = most_recent
    __args__['name'] = name
    __args__['rules'] = rules
    __args__['withSelector'] = with_selector
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getFirewall:getFirewall', __args__, opts=opts, typ=GetFirewallResult).value

    return AwaitableGetFirewallResult(
        apply_tos=pulumi.get(__ret__, 'apply_tos'),
        id=pulumi.get(__ret__, 'id'),
        labels=pulumi.get(__ret__, 'labels'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        name=pulumi.get(__ret__, 'name'),
        rules=pulumi.get(__ret__, 'rules'),
        with_selector=pulumi.get(__ret__, 'with_selector'))


@_utilities.lift_output_func(get_firewall)
def get_firewall_output(apply_tos: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetFirewallApplyToArgs']]]]] = None,
                        id: Optional[pulumi.Input[Optional[int]]] = None,
                        labels: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                        most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                        name: Optional[pulumi.Input[Optional[str]]] = None,
                        rules: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetFirewallRuleArgs']]]]] = None,
                        with_selector: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirewallResult]:
    """
    Provides details about a specific Hetzner Cloud Firewall.

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    sample_firewall1 = hcloud.get_firewall(name="sample-firewall-1")
    sample_firewall2 = hcloud.get_firewall(id=4711)
    ```


    :param Sequence[pulumi.InputType['GetFirewallApplyToArgs']] apply_tos: Configuration of the Applied Resources
    :param int id: ID of the firewall.
    :param Mapping[str, Any] labels: (map) User-defined labels (key-value pairs)
    :param bool most_recent: Return most recent firewall if multiple are found.
    :param str name: Name of the firewall.
    :param Sequence[pulumi.InputType['GetFirewallRuleArgs']] rules: (string)  Configuration of a Rule from this Firewall.
    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    """
    ...
