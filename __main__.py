from os import confstr_names
from typing import Dict, Any

import pulumi
import pulumiverse_scaleway as scw

config = pulumi.Config()
dns_zone = config.require("zone")

scaleway = scw.Provider('dns-project')

mxRecords: Dict[str, Any] = config.get_object("mx", {})
for name, data in mxRecords.items():
    args = scw.domain.RecordArgs(dns_zone=dns_zone, type="MX", **data)
    scw.domain.Record(name, args)

txtRecords: Dict[str, Any] = config.get_object("txt", {})
for name, data in txtRecords.items():
    args = scw.domain.RecordArgs(dns_zone=dns_zone, type="TXT", **data)
    scw.domain.Record(name, args)

cnameRecords: Dict[str, Any] = config.get_object("cname", {})
for name, data in cnameRecords.items():
    pulumi.log.info(f"Creating record {name} with value {data}")
    args = scw.domain.RecordArgs(dns_zone=dns_zone, type="CNAME", **data)
    scw.domain.Record(name, args)
