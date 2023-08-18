import click
from publicsuffixlist import PublicSuffixList
import pyathena
from pyathena.arrow.cursor import ArrowCursor
import csv
import datetime
import lzma
import re

import tilelog.constants
import tilelog.aggregate
import tilelog.minimise
import tilelog.location
import tilelog.country


@click.command()
@click.option('--date', type=click.DateTime(["%Y-%m-%d"]),
              default=(datetime.datetime.utcnow() -
                       datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
              help="Date to generate logs for. Defaults to yesterday.")
@click.option('--staging',
              default="s3://openstreetmap-fastly-processed-logs/tilelogs/",
              help="AWS s3 location for Athena results")
@click.option('--generate-success', is_flag=True, default=False,
              help="Create logs of successful requests in Parquet")
@click.option('--generate-minimise', is_flag=True, default=False,
              help="Create minimised request logs in Parquet")
@click.option('--generate-location', is_flag=True, default=False,
              help="Create location request logs in Parquet")
@click.option('--region', default="eu-west-1", help="Region for Athena")
@click.option('--tile', type=click.File('wb'),
              help="File to output tile usage logs to")
@click.option('--host', type=click.File('w', encoding='utf-8'),
              help="File to output host usage logs to")
@click.option('--app', type=click.File('w', encoding='utf-8'),
              help="File to output app usage logs to")
@click.option('--country', type=click.File('w', encoding='utf-8'),
              help="File with country-level statistics")
def cli(date, staging, generate_success, generate_minimise, generate_location,
        region, tile, host, app, country):
    click.echo(f"Generating files for {date.strftime('%Y-%m-%d')}")
    with pyathena.connect(s3_staging_dir=staging, region_name=region,
                          cursor_class=ArrowCursor).cursor() as curs:

        # Aggregation must be run first, because the other tasks depend on it
        if generate_success:
            tilelog.aggregate.create_parquet(curs, date)
        if generate_minimise:
            tilelog.minimise.create_minimised(curs, date)
        if generate_location:
            tilelog.location.create_location(curs, date)
        if tile is not None:
            tile_logs(curs, date, tile)
        if host is not None:
            host_logs(curs, date, host)
        if app is not None:
            app_logs(curs, date, app)
        if country is not None:
            tilelog.country.country_logs(curs, date, country)


def tile_logs(curs, date, dest):
    click.echo("Querying for tile usage")
    query = f"""
SELECT z, x, y,
        COUNT(*)
FROM {tilelog.constants.FASTLY_PARQET_LOGS}
WHERE year = %(year)d
    AND month = %(month)d
    AND day = %(day)d
GROUP BY z, x, y
HAVING COUNT(DISTINCT ip) >= %(min_distinct)d
    AND COUNT(*) >= %(min_requests)d
ORDER BY z, x, y
    """
    curs.execute(query, {"year": date.year, "month": date.month,
                         "day": date.day,
                         "min_distinct": tilelog.constants.MIN_DISTINCT_TILE_REQUESTS,
                         "min_requests": tilelog.constants.MIN_TILE_REQUESTS})
    click.echo("Writing tile usage to file")
    with lzma.open(dest, "w") as file:
        for tile in curs:
            file.write(f"{tile[0]}/{tile[1]}/{tile[2]} {tile[3]}\n".encode('ascii'))


psl = PublicSuffixList()


def normalize_host(host):
    if host is None:
        return ""
    # IPs don't have a public/private suffix
    if re.match(r"^(\d+\.){3}\d+$", host):
        return host

    suffix = psl.privatesuffix(host)

    # Something like "localhost", or an invalid host like ".example.com" may return None,
    # so don't try to give just the suffix in those cases
    if suffix is None:
        return host
    return suffix


def host_logs(curs, date, dest):
    click.echo("Querying for host usage")
    query = f"""
SELECT
host,
cast(count(*) as double)/86400 AS tps,
cast(count(*) FILTER (WHERE cachehit = 'MISS') as double)/86400 AS tps_miss
FROM (
    SELECT regexp_extract(referer,
                          'https?://([^/]+?)(:[0-9]+)?/.*', 1) AS host,
    cachehit
FROM {tilelog.constants.FASTLY_PARQET_LOGS}
WHERE year = %(year)d
    AND month = %(month)d
    AND day = %(day)d
    AND referer != ''
    AND requestedwith = ''
    ) AS stripped_referers
GROUP BY host
ORDER BY COUNT(*) DESC;
    """
    curs.execute(query, {"year": date.year, "month": date.month,
                         "day": date.day})

    # Create a dict of lists of TPS
    grouped_hosts = {}
    for host in curs:
        stripped_hostname = normalize_host(host[0])
        if stripped_hostname not in grouped_hosts:
            grouped_hosts[stripped_hostname] = [host[1], host[2]]
        else:
            # TPS is host[1] and grouped_hosts[][0], so the indexes don't match up
            grouped_hosts[stripped_hostname] = [grouped_hosts[stripped_hostname][0] + host[1],
                                                grouped_hosts[stripped_hostname][1] + host[2]]

    sorted_hosts = sorted([[host, metrics[0], metrics[1]]
                           for (host, metrics) in grouped_hosts.items()
                           if metrics[0] >= tilelog.constants.MIN_TPS],
                          key=lambda host: host[1], reverse=True)  # Sort by TPS
    click.echo("Writing host usage to file")
    csvwriter = csv.writer(dest, dialect=csv.unix_dialect,
                           quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerows(sorted_hosts)


def app_logs(curs, date, dest):
    click.echo("Querying for app usage")
    query = fr"""
SELECT
app,
cast(count(*) as double)/86400 AS tps,
cast(count(*) filter (WHERE cachehit = 'MISS') as double)/86400 AS tps_miss
FROM (
    SELECT
    CASE
    WHEN requestedwith != '' THEN requestedwith
    WHEN useragent LIKE 'Mozilla/5.0 QGIS/%%' THEN 'Mozilla/5.0 QGIS/*'
    WHEN useragent LIKE 'qfield|%%|%%|%%| QGIS/%%' THEN 'qfield|*|*|*| QGIS/*'
    WHEN useragent LIKE 'Mozilla/5.0 (compatible; Marble/%%)' THEN 'Mozilla/5.0 (compatible; Marble/*)'
    WHEN useragent LIKE 'JOSM/1.5 %%' THEN 'JOSM/1.5 *'
    WHEN useragent LIKE 'OruxMaps %%' THEN 'OruxMaps *'
    WHEN useragent LIKE 'MapProxy-%%' THEN 'MapProxy-*'
    WHEN useragent LIKE 'Dart/%% (dart:io)' THEN 'Dart/* (dart:io)'
    WHEN useragent LIKE 'Wikiloc %%' THEN 'Wikiloc *'
    WHEN useragent LIKE 'Mapbox iOS SDK (%%)' THEN 'Mapbox iOS SDK (*)'
    WHEN useragent LIKE 'flutter_map (%%)' THEN 'flutter_map (*)'

    -- Extract app name from foo.bar/123.456
    WHEN regexp_like(useragent, '^([^./]+(\.[^./]+)*)/\d+(\.\d+)*$') THEN regexp_extract(useragent, '^([^./]+(\.[^./]+)*)/\d+(\.\d+)*$', 1) || '/*'
    -- Some apps have extra stuff after the name/version
    WHEN regexp_like(useragent, '^([^/ ]+)(/[^/ ]+) CFNetwork/[^/ ]+ Darwin/[^/ ]+$') THEN regexp_extract(useragent, '^([^/ ]+)(/[^/ ]+) CFNetwork/[^/ ]+ Darwin/[^/ ]+$', 1) || '/* CFNetwork/* Darwin/*'
    -- Mapbox apps follow the pattern Bikemap/22.0.2 Mapbox/5.13.0-pre.1 MapboxGL/0.0.0 (c6fb3581) iOS/15.5.0 (arm64)
    WHEN regexp_like(useragent, '^([^/ ]+)(/[^/ ]+) Mapbox/') THEN regexp_extract(useragent, '^([^/ ]+)(/[^/ ]+) Mapbox/', 1) || '/* Mapbox/*'
    WHEN regexp_like(useragent, '^([^/ ]+)(/[^/ ]+) GLMap/') THEN regexp_extract(useragent, '^([^/ ]+)(/[^/ ]+) GLMap/', 1) || '/* GLMap/*'

    WHEN useragent LIKE 'Mozilla/%%' AND referer != '' THEN referer -- This will only show referers that are not https ones, e.g. flash apps
    ELSE useragent END AS app,
    cachehit
    FROM {tilelog.constants.FASTLY_PARQET_LOGS}
WHERE year = %(year)d
    AND month = %(month)d
    AND day = %(day)d
    AND (
        requestedwith != '' -- Leaflet-based apps
        OR referer = '' -- Non-websites
        OR (referer NOT LIKE 'https://%%/%%' AND referer NOT LIKE 'http://%%/%%') -- Referer set, but not a website
    )
) AS combined_requests
GROUP BY app
HAVING COUNT(*) > %(tps)d*86400
ORDER BY COUNT(*) DESC
    """  # noqa: E501

    curs.execute(query, {"year": date.year, "month": date.month,
                         "day": date.day, "tps": tilelog.constants.MIN_TPS})
    click.echo("Writing host usage to file")
    csvwriter = csv.writer(dest, dialect=csv.unix_dialect,
                           quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerows(curs)
