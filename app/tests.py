import json

from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import FluxStructureEncoder

bucket = "cube"
org = "backend"
token = "GDd2-WGghz9WlCvPht7AOzqwiwBdWjtanJzFsL7fm_rpq86Ciap_0dFURqU1gnAuaQLEaQfgqIvxZAZPOANR1g=="


def bytes2gb(b: float):
    return round(b / 1024 / 1024 / 1024, 2)


with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    query = """
    from(bucket: "cube")
    |> range(start: -1m)
    |> filter(fn: (r) => r._field == "mem_percent" or r._field == "cpu_percent")
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> filter(fn: (r) => r.host == "ubuntu-1" and r.cpu_percent < 6.9)
    |> limit(n: 5)
    """
    tables = client.query_api().query(query, org=org)

    output = json.dumps(tables, cls=FluxStructureEncoder, indent=2)
    print(output)

    for table in tables:
        for record in table.records:
            print(record)
