#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gary
# Datetime: 2022/12/19 20:54
# IDE: PyCharm
"""
    通过 vCenter Server 主机更新 Zabbix ESXI 类型主机的 Host Inventory 信息。
"""
import argparse
import sys
import logging
from urllib.parse import urlparse
from lib.utils.zbxtags import HostTags, InventoryTagDict
from lib.utils.zbxapis import ZabbixApiUpdate
from lib.utils.esxiapis import VMManger
from lib.utils.format import get_value, jmes_search


class UpdateZbxHost:
    """Mainly used to update the host inventory of zabbix 'ESXI' type host"""

    def __init__(self, zapi):
        self._zapi = zapi

    @property
    def zbx_grp(self):
        """
            用来获取 Zabbix "Hypervisors" 主机组下的所有主机信息：
                1. Zabbix 上 ESXI 类型的主机基本归于 "Hypervisors" 这个主机组，
                   要更新 ESXI 类型的主机信息就要获取 "Hypervisors" 主机组下的所有主机信息。
        :return:
        """
        return self._zapi.get_ht_grps(
            output=["groupid", "name"],
            selecthosts=["hostid", "name"],
            filter_={"name": "Hypervisors"}
        )

    def get_zbx_hts_info(self, grp_hosts: list):
        """
            用来根据 hostids 获取 Zabbix 主机的具体信息：
                1. 获取到的 Zabbix 主机信息包括 Inventory、Macro、Host Tags、Discoveries 等。
        :param grp_hosts:
        :return:
        """
        return self._zapi.get_hts(
            output=["hostid", "name", "inventory_mode"],
            hostids=jmes_search(
                get_value(
                    section="JMES",
                    option="SEARCH_HOSTIDS"
                ),
                data=grp_hosts
            ),
            selectmacros=["macro", "value"],
            selectinventory="extend",
            selecttags=["tag", "value"],
            selecthostdiscovery="extend"
        )

    @staticmethod
    def get_update_params(inventory: dict, host: dict):
        """
            用来获取 Zabbix 主机更新需要的字段信息：
                1. 首先是 Host Inventory，ESXI 类型主机的 Host Inventory 信息主要通过 vCenter Server 获取；
                2. 标签信息分为两种情况：
                    2.1 如果主机是自动发现类型的主机，Zabbix Api 接口提示自动发现主机是不能添加 Host Tags 的，
                        那就只能添加 Host Inventory Tag；
                    2.2 如果主机不是自动发现类型的主机，则可以添加 Host Tags，Host Inventory Tag 则不再添加。
        :param inventory:
        :param host:
        :return:
        """
        if host.get("hostDiscovery"):
            inventory_tags = InventoryTagDict(host.get("inventory").get("tag"))
            inventory_tags["Esxi"] = None
            inventory.update({"tag": str(inventory_tags)})
            return {
                "hostid": host.get("hostid"),
                "inventory": inventory
            }
        return {
            "hostid": host.get("hostid"),
            "tags": HostTags(host.get("tags")).added_tags(
                tag_name="Esxi",
                tag_value=""
            ),
            "inventory": inventory
        }

    @staticmethod
    def get_esxi_info(vcenter_ip: str, host: dict):
        """
            根据 vCenter Server 获取 ESXI 主机信息：
        :param vcenter_ip:
        :param host:
        :return:
        """
        return VMManger(
            host=vcenter_ip,
            user=jmes_search(
                jmes_rexp=get_value(
                    section="JMES",
                    option="SEARCH_ESXI_MACRO",
                    raw=True
                ) % "{$USERNAME}",
                data=host.get("macros")
            ),
            passwd=jmes_search(
                jmes_rexp=get_value(
                    section="JMES",
                    option="SEARCH_ESXI_MACRO",
                    raw=True
                ) % "{$PASSWORD}",
                data=host.get("macros")
            )
        ).fetch_esxi(esxi_name=host.get("name"))


def main(args):
    """Main Function"""
    zapi = ZabbixApiUpdate(args.zapi)
    zbx = UpdateZbxHost(zapi)
    if not zbx.zbx_grp:
        sys.exit()
    grp_hosts = zbx.zbx_grp[0].get("hosts")
    # 如指定 limit 参数, 则仅处理列表中的 host
    if args.limit:
        grp_hosts = [ht for ht in grp_hosts if ht.get("name") in args.limit]
    # 调用 zapi 查询 host 的 macros 信息
    hosts = zbx.get_zbx_hts_info(grp_hosts)
    for host in hosts:
        vcenter_ip = urlparse(
            jmes_search(
                jmes_rexp=get_value(
                    section="JMES",
                    option="SEARCH_ESXI_MACRO",
                    raw=True
                ) % "{$URL}",
                data=host.get("macros")
            )
        ).hostname
        logging.info(
            "\033[32m搜索 ESXI 主机成功，vCenter => '%s', ESXI Host => '%s'\033[0m",
            vcenter_ip,
            host.get("name")
        )
        update_params = zbx.get_update_params(
            inventory=zbx.get_esxi_info(vcenter_ip=vcenter_ip, host=host),
            host=host
        )
        if host["inventory_mode"] == "-1":  # disabled
            update_params["inventory_mode"] = "1"  # Auto
        zapi.update_host(update_params)
        logging.info(
            "\033[32mESXI主机Inventory信息更新成功，Host => '%s'\033[0m",
            host.get("name")
        )


parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--limit",
    action="append",
    help="Specify ip address of 'ESXI' type hosts"
)
parser.set_defaults(handler=main)
