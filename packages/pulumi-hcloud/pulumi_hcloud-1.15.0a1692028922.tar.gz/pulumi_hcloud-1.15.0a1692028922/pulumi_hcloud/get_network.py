# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetNetworkResult',
    'AwaitableGetNetworkResult',
    'get_network',
    'get_network_output',
]

@pulumi.output_type
class GetNetworkResult:
    """
    A collection of values returned by getNetwork.
    """
    def __init__(__self__, delete_protection=None, expose_routes_to_vswitch=None, id=None, ip_range=None, labels=None, most_recent=None, name=None, with_selector=None):
        if delete_protection and not isinstance(delete_protection, bool):
            raise TypeError("Expected argument 'delete_protection' to be a bool")
        pulumi.set(__self__, "delete_protection", delete_protection)
        if expose_routes_to_vswitch and not isinstance(expose_routes_to_vswitch, bool):
            raise TypeError("Expected argument 'expose_routes_to_vswitch' to be a bool")
        pulumi.set(__self__, "expose_routes_to_vswitch", expose_routes_to_vswitch)
        if id and not isinstance(id, int):
            raise TypeError("Expected argument 'id' to be a int")
        pulumi.set(__self__, "id", id)
        if ip_range and not isinstance(ip_range, str):
            raise TypeError("Expected argument 'ip_range' to be a str")
        pulumi.set(__self__, "ip_range", ip_range)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if with_selector and not isinstance(with_selector, str):
            raise TypeError("Expected argument 'with_selector' to be a str")
        pulumi.set(__self__, "with_selector", with_selector)

    @property
    @pulumi.getter(name="deleteProtection")
    def delete_protection(self) -> bool:
        """
        (bool) Whether delete protection is enabled.
        """
        return pulumi.get(self, "delete_protection")

    @property
    @pulumi.getter(name="exposeRoutesToVswitch")
    def expose_routes_to_vswitch(self) -> bool:
        """
        (bool) Indicates if the routes from this network should be exposed to the vSwitch connection. The exposing only takes effect if a vSwitch connection is active.
        """
        return pulumi.get(self, "expose_routes_to_vswitch")

    @property
    @pulumi.getter
    def id(self) -> int:
        """
        Unique ID of the Network.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipRange")
    def ip_range(self) -> Optional[str]:
        """
        IPv4 prefix of the Network.
        """
        return pulumi.get(self, "ip_range")

    @property
    @pulumi.getter
    def labels(self) -> Optional[Mapping[str, Any]]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the Network.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="withSelector")
    def with_selector(self) -> Optional[str]:
        return pulumi.get(self, "with_selector")


class AwaitableGetNetworkResult(GetNetworkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkResult(
            delete_protection=self.delete_protection,
            expose_routes_to_vswitch=self.expose_routes_to_vswitch,
            id=self.id,
            ip_range=self.ip_range,
            labels=self.labels,
            most_recent=self.most_recent,
            name=self.name,
            with_selector=self.with_selector)


def get_network(id: Optional[int] = None,
                ip_range: Optional[str] = None,
                labels: Optional[Mapping[str, Any]] = None,
                most_recent: Optional[bool] = None,
                name: Optional[str] = None,
                with_selector: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    network1 = hcloud.get_network(id=1234)
    network2 = hcloud.get_network(name="my-network")
    network3 = hcloud.get_network(with_selector="key=value")
    ```


    :param int id: ID of the Network.
    :param str ip_range: IPv4 prefix of the Network.
    :param str name: Name of the Network.
    :param str with_selector: Label Selector. For more information about possible values, visit the [Hetzner Cloud Documentation](https://docs.hetzner.cloud/#overview-label-selector).
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['ipRange'] = ip_range
    __args__['labels'] = labels
    __args__['mostRecent'] = most_recent
    __args__['name'] = name
    __args__['withSelector'] = with_selector
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('hcloud:index/getNetwork:getNetwork', __args__, opts=opts, typ=GetNetworkResult).value

    return AwaitableGetNetworkResult(
        delete_protection=pulumi.get(__ret__, 'delete_protection'),
        expose_routes_to_vswitch=pulumi.get(__ret__, 'expose_routes_to_vswitch'),
        id=pulumi.get(__ret__, 'id'),
        ip_range=pulumi.get(__ret__, 'ip_range'),
        labels=pulumi.get(__ret__, 'labels'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        name=pulumi.get(__ret__, 'name'),
        with_selector=pulumi.get(__ret__, 'with_selector'))


@_utilities.lift_output_func(get_network)
def get_network_output(id: Optional[pulumi.Input[Optional[int]]] = None,
                       ip_range: Optional[pulumi.Input[Optional[str]]] = None,
                       labels: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                       most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                       name: Optional[pulumi.Input[Optional[str]]] = None,
                       with_selector: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    network1 = hcloud.get_network(id=1234)
    network2 = hcloud.get_network(name="my-network")
    network3 = hcloud.get_network(with_selector="key=value")
    ```


    :param int id: ID of the Network.
    :param str ip_range: IPv4 prefix of the Network.
    :param str name: Name of the Network.
    :param str with_selector: Label Selector. For more information about possible values, visit the [Hetzner Cloud Documentation](https://docs.hetzner.cloud/#overview-label-selector).
    """
    ...
