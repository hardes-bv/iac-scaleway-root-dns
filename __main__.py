from typing import Dict, Any, List

import pulumi
import pulumiverse_scaleway as scw

config = pulumi.Config()
dns_zone = config.require("zone")

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
    args = scw.domain.RecordArgs(dns_zone=dns_zone, type="CNAME", **data)
    scw.domain.Record(name, args)

srvRecords: Dict[str, Any] = config.get_object("srv", {})
for name, data in srvRecords.items():
    args = scw.domain.RecordArgs(dns_zone=dns_zone, type="SRV", **data)
    scw.domain.Record(name, args)

zones: List[str] = config.get_object("zones", [])
for zone in zones:
    subdomain = scw.domain.Zone(
        zone,
        scw.domain.ZoneArgs(
            domain=dns_zone,
            subdomain=zone,
        ),
    )

    args = scw.domain.RecordArgs(
        name=zone,
        dns_zone=dns_zone,
        type="NS",
        data="ns0.dom.scw.cloud."
    )
    scw.domain.Record(
        f"{zone}-ns-1",
        args,
        opts=pulumi.ResourceOptions(
            depends_on=[subdomain],
        )
    )

    args.data = "ns1.dom.scw.cloud."
    scw.domain.Record(
        f"{zone}-ns-2",
        args,
        opts=pulumi.ResourceOptions(
            depends_on=[subdomain],
        )
    )
