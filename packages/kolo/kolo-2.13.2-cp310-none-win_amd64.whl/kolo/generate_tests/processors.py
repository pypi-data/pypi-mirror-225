from datetime import datetime
from importlib import import_module

import click

from .outbound import parse_outbound_frames
from .queries import parse_sql_queries
from .request import (
    get_query_params,
    get_request_body,
    get_request_headers,
    parse_request_frames,
)
from ..db import SchemaNotFoundError, load_schema_for_commit_sha
from ..django_schema import get_schema
from ..git import COMMIT_SHA


SCHEMA_NOT_FOUND_WARNING = """\
Warning: Could not find a Django schema for commit: {0}.

Falling back to the current commit's schema.

For more reliable results, run `kolo store-django-model-schema` from {0}
then retry this command.
"""


def process_django_schema(context):
    commit_sha = context["_trace"]["current_commit_sha"]
    db_path = context["_db_path"]
    wal_mode = context["_wal_mode"]
    if commit_sha == COMMIT_SHA:
        schema_data = get_schema()  # pragma: no cover
    else:
        try:
            schema_data = load_schema_for_commit_sha(db_path, commit_sha, wal_mode)
        except SchemaNotFoundError:
            click.echo(SCHEMA_NOT_FOUND_WARNING.format(commit_sha), err=True)
            schema_data = get_schema()
    return {"schema_data": schema_data}


def process_sql_queries(context):
    frames = context["_frames"]
    schema_data = context["schema_data"]
    sql_queries = [frame for frame in frames if frame["type"] == "end_sql_query"]

    if not sql_queries:
        return {
            "asserts": [],
            "imports": [],
            "sql_fixtures": [],
        }

    sql_fixtures, imports, asserts = parse_sql_queries(sql_queries, schema_data)
    return {
        "asserts": asserts,
        "imports": sorted(imports),
        "sql_fixtures": sql_fixtures,
    }


def process_django_request(context):
    frames = context["_frames"]
    served_request_frames = parse_request_frames(frames)

    request = served_request_frames[0]["request"] if served_request_frames else None
    response = served_request_frames[0]["response"] if served_request_frames else None
    request_headers = get_request_headers(request)
    prettified_request_body = get_request_body(request, request_headers)
    query_params = get_query_params(request)
    if request:
        request_timestamp = datetime.utcfromtimestamp(request["timestamp"]).isoformat(
            timespec="seconds"
        )
    else:
        request_timestamp = ""
    template_names = (
        served_request_frames[0]["templates"] if served_request_frames else []
    )

    return {
        "prettified_request_body": prettified_request_body,
        "query_params": query_params,
        "request": request,
        "request_headers": request_headers,
        "request_timestamp": request_timestamp,
        "response": response,
        "template_names": template_names,
    }


def process_outbound_requests(context):
    frames = context["_frames"]
    outbound_request_frames = parse_outbound_frames(frames)
    return {"outbound_request_frames": outbound_request_frames}


def process_django_version(context):
    try:
        from django import __version__ as django_version
    except ImportError:  # pragma: no cover
        django_version = ""
    return {"django_version": django_version}


def import_processor(processor):
    module_path, _sep, filter_name = processor.rpartition(".")
    module = import_module(module_path)
    return getattr(module, filter_name)


def load_processors(config):
    try:
        raw_processors = config["test_generation"]["trace_processors"]
    except KeyError:
        return (
            process_django_version,
            process_django_schema,
            process_django_request,
            process_outbound_requests,
            process_sql_queries,
        )

    return tuple(map(import_processor, raw_processors))
