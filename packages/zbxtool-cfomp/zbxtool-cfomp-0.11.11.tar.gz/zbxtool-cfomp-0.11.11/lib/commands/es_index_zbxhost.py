#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gary
# Datetime: 2022/12/19 18:19
# IDE: PyCharm
"""
    获取 Zabbix 主机 inventory 信息并生成 ES 索引。
"""
import argparse
import logging
import time
from datetime import datetime
from lib.utils.zbxapis import ZabbixApiGet
from lib.utils.esapis import ESManager
from lib.utils.format import jmes_search, get_value

body = {
    "order": "500",
    "index_patterns": [
        "zabbix-raw-host-info-*"
    ],
    "mappings": {
        "properties": {
            "hostid": {
                "type": "integer"
            },
            "proxy_hostid": {
                "type": "integer"
            },
            "status": {
                "type": "byte"
            },
            "disable_until": {
                "type": "date"
            },
            "available": {
                "type": "byte"
            },
            "errors_from": {
                "type": "date"
            },
            "lastaccess": {
                "type": "byte"
            },
            "ipmi_authtype": {
                "type": "byte"
            },
            "ipmi_privilege": {
                "type": "byte"
            },
            "ipmi_disable_until": {
                "type": "date"
            },
            "ipmi_available": {
                "type": "byte"
            },
            "snmp_disable_until": {
                "type": "date"
            },
            "snmp_available": {
                "type": "byte"
            },
            "maintenanceid": {
                "type": "integer"
            },
            "maintenance_status": {
                "type": "byte"
            },
            "maintenance_type": {
                "type": "byte"
            },
            "maintenance_from": {
                "type": "date"
            },
            "ipmi_errors_from": {
                "type": "date"
            },
            "snmp_errors_from": {
                "type": "date"
            },
            "jmx_disable_until": {
                "type": "date"
            },
            "jmx_available": {
                "type": "byte"
            },
            "jmx_errors_from": {
                "type": "date"
            },
            "flags": {
                "type": "byte"
            },
            "templateid": {
                "type": "integer"
            },
            "tls_connect": {
                "type": "byte"
            },
            "tls_accept": {
                "type": "byte"
            },
            "auto_compress": {
                "type": "byte"
            },
            "groups": {
                "properties": {
                    "groupid": {
                        "type": "integer"
                    },
                    "internal": {
                        "type": "byte"
                    },
                    "flags": {
                        "type": "byte"
                    },
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "interfaces": {
                "properties": {
                    "ip": {
                        "type": "ip"
                    },
                    "interfaceid": {
                        "type": "integer"
                    },
                    "hostid": {
                        "type": "integer"
                    },
                    "main": {
                        "type": "byte"
                    },
                    "type": {
                        "type": "byte"
                    },
                    "useip": {
                        "type": "byte"
                    },
                    "port": {
                        "type": "integer"
                    },
                    "bulk": {
                        "type": "byte"
                    }
                }
            },
            "inventory": {
                "properties": {
                    "hostid": {
                        "type": "integer"
                    },
                    "inventory_mode": {
                        "type": "byte"
                    },
                    "alias": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "asset_tag": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "chassis": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "host_netmask": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "host_networks": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "hw_arch": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "location": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "macaddress_a": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "macaddress_b": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "model": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "oob_ip": {
                        "type": "text"
                    },
                    "os": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "os_full": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "os_short": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "poc_1_name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "poc_2_name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "serialno_a": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "site_rack": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "tag": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "type": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "type_full": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "vendor": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "主机组": {
                "type": "alias",
                "path": "groups.name"
            },
            "接口地址": {
                "type": "alias",
                "path": "interfaces.ip"
            },
            "主机别名": {
                "type": "alias",
                "path": "inventory.alias"
            },
            "资产标签": {
                "type": "alias",
                "path": "inventory.asset_tag"
            },
            "机架": {
                "type": "alias",
                "path": "inventory.chassis"
            },
            "子网掩码": {
                "type": "alias",
                "path": "inventory.host_netmask"
            },
            "主机网络": {
                "type": "alias",
                "path": "inventory.host_networks"
            },
            "硬件架构": {
                "type": "alias",
                "path": "inventory.hw_arch"
            },
            "机房": {
                "type": "alias",
                "path": "inventory.location"
            },
            "MAC_A": {
                "type": "alias",
                "path": "inventory.macaddress_a"
            },
            "MAC_B": {
                "type": "alias",
                "path": "inventory.macaddress_b"
            },
            "型号": {
                "type": "alias",
                "path": "inventory.model"
            },
            "主机名称": {
                "type": "alias",
                "path": "inventory.name"
            },
            "管理IP": {
                "type": "alias",
                "path": "inventory.oob_ip"
            },
            "OS": {
                "type": "alias",
                "path": "inventory.os"
            },
            "OS_FULL": {
                "type": "alias",
                "path": "inventory.os_full"
            },
            "OS_SHORT": {
                "type": "alias",
                "path": "inventory.os_short"
            },
            "主负责人": {
                "type": "alias",
                "path": "inventory.poc_1_name"
            },
            "次负责人": {
                "type": "alias",
                "path": "inventory.poc_2_name"
            },
            "序列号": {
                "type": "alias",
                "path": "inventory.serialno_a"
            },
            "机柜": {
                "type": "alias",
                "path": "inventory.site_rack"
            },
            "标签": {
                "type": "alias",
                "path": "inventory.tag"
            },
            "类型": {
                "type": "alias",
                "path": "inventory.type"
            },
            "具体类型": {
                "type": "alias",
                "path": "inventory.type_full"
            },
            "供应商": {
                "type": "alias",
                "path": "inventory.vendor"
            }
        }
    }
}


def get_hosts(args, es_client, tpl_name):
    """
        获取 Zabbix 主机的 Inventory 信息：
    :param args:
    :param es_client:
    :param tpl_name:
    :return:
    """
    body_datas = []
    hosts = ZabbixApiGet(args.zapi).get_hts(
        output="extend",
        selectgroups="extend",
        selectinterfaces="extend",
        selectinventory="extend"
    )
    localtime = time.strftime("%Y.%m.%d", time.localtime())
    for host in hosts:
        host["@timestamp"] = datetime.utcfromtimestamp(time.time())
        inventory = host.get("inventory") if isinstance(host.get("inventory"), dict) else {}
        body_datas.append(
            {
                "_id": host.get("hostid"),
                "主机名称": inventory.get("name", host.get("host")),
                "主机别名": inventory.get("alias", host.get("host")),
                "接口地址": jmes_search(
                    jmes_rexp=get_value(section="JMES", option="SEARCH_HOST_IPS"),
                    data=host
                ),
                "主机组": jmes_search(
                    jmes_rexp=get_value(section="JMES", option="SEARCH_HOST_GROUP_NAMES"),
                    data=host
                ),
                "OS": inventory.get("os"),
                "OS_FULL": inventory.get("os_full"),
                "OS_SHORT": inventory.get("os_short"),
                "资产标签": inventory.get("asset_tag"),
                "主负责人": inventory.get("poc_1_name"),
                "次负责人": inventory.get("poc_2_name"),
                "机架": inventory.get("chassis"),
                "子网掩码": inventory.get("host_netmask"),
                "主机网络": inventory.get("host_networks"),
                "机房": inventory.get("location"),
                "机柜": inventory.get("site_rack"),
                "序列号": inventory.get("serialno_a"),
                "管理IP": inventory.get("oob_ip"),
                "MAC_A": inventory.get("macaddress_a"),
                "MAC_B": inventory.get("macaddress_b"),
                "硬件架构": inventory.get("hw_arch"),
                "标签": inventory.get("tag"),
                "类型": inventory.get("type"),
                "具体类型": inventory.get("type_full"),
                "型号": inventory.get("model"),
                "供应商": inventory.get("vendor"),
                "@timestamp": datetime.utcfromtimestamp(time.time())
            }
        )
    es_client.put_template(tpl_name=tpl_name, body=body)
    for host in hosts:
        host["_id"] = host["hostid"]
    index_of_raw_host = get_value(
        section="ELASTICSTACK",
        option="ZABBIX_RAW_HOST_INDEX"
    ) + localtime
    es_client.bulk(actions=hosts, index=index_of_raw_host)
    logging.info(
        "\033[32m成功生成 ES 索引：'(ES Host)%s' => '(ES INDEX)%s'\033[0m",
        args.es_url,
        index_of_raw_host
    )
    index_of_host = get_value(
        section="ELASTICSTACK",
        option="ZABBIX_HOST_INDEX"
    ) + localtime
    es_client.bulk(actions=body_datas, index=index_of_host)
    logging.info(
        "\033[32m成功生成 ES 索引：'(ES Host)%s' => '(ES INDEX)%s'\033[0m",
        args.es_url,
        index_of_host
    )


def main(args):
    """创建 ES 索引"""
    get_hosts(
        args=args,
        es_client=ESManager(args.es_url, args.es_user, args.es_passwd),
        tpl_name=args.es_tpl
    )


parser = argparse.ArgumentParser(description="Gather zabbix host informations and create es index")
parser.add_argument(
    "--es_url",
    type=str,
    required=True,
    help="ElasticSearch server ip"
)
parser.add_argument(
    "--es_user",
    default="",
    help="ElasticSearch server login user"
)
parser.add_argument(
    "--es_passwd",
    default="",
    help="ElasticSearch server login password"
)
parser.add_argument(
    "--es_tpl",
    required=True,
    help="ElasticSearch index template name"
)
parser.set_defaults(handler=main)
