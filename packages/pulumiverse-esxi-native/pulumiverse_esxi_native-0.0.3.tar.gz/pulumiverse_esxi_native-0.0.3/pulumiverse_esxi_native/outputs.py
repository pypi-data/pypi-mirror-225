# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from ._enums import *

__all__ = [
    'KeyValuePair',
    'NetworkInterface',
    'Uplink',
    'VMVirtualDisk',
]

@pulumi.output_type
class KeyValuePair(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class NetworkInterface(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "virtualNetwork":
            suggest = "virtual_network"
        elif key == "macAddress":
            suggest = "mac_address"
        elif key == "nicType":
            suggest = "nic_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkInterface. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkInterface.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkInterface.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 virtual_network: str,
                 mac_address: Optional[str] = None,
                 nic_type: Optional[str] = None):
        pulumi.set(__self__, "virtual_network", virtual_network)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if nic_type is not None:
            pulumi.set(__self__, "nic_type", nic_type)

    @property
    @pulumi.getter(name="virtualNetwork")
    def virtual_network(self) -> str:
        return pulumi.get(self, "virtual_network")

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[str]:
        return pulumi.get(self, "mac_address")

    @property
    @pulumi.getter(name="nicType")
    def nic_type(self) -> Optional[str]:
        return pulumi.get(self, "nic_type")


@pulumi.output_type
class Uplink(dict):
    def __init__(__self__, *,
                 name: str):
        """
        :param str name: Uplink name.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Uplink name.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class VMVirtualDisk(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "virtualDiskId":
            suggest = "virtual_disk_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VMVirtualDisk. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VMVirtualDisk.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VMVirtualDisk.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 virtual_disk_id: str,
                 slot: Optional[str] = None):
        """
        :param str slot: SCSI_Ctrl:SCSI_id. Range '0:1' to '0:15'. SCSI_id 7 is not allowed.
        """
        pulumi.set(__self__, "virtual_disk_id", virtual_disk_id)
        if slot is not None:
            pulumi.set(__self__, "slot", slot)

    @property
    @pulumi.getter(name="virtualDiskId")
    def virtual_disk_id(self) -> str:
        return pulumi.get(self, "virtual_disk_id")

    @property
    @pulumi.getter
    def slot(self) -> Optional[str]:
        """
        SCSI_Ctrl:SCSI_id. Range '0:1' to '0:15'. SCSI_id 7 is not allowed.
        """
        return pulumi.get(self, "slot")


