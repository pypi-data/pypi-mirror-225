"""Utility functions for CLI interface."""
import json
import os
import re
import unicodedata
from typing import Dict

from importlib.metadata import version
from prometheus_client import Metric
from prometheus_client.parser import text_string_to_metric_families

from cmem.cmempy.dp.admin import get_prometheus_data
from cmem.cmempy.dp.proxy.graph import get_graphs_list

NAMESPACES = {
    "void": "http://rdfs.org/ns/void#",
    "di": "https://vocab.eccenca.com/di/",
    "shui": "https://vocab.eccenca.com/shui/",
    "dsm": "https://vocab.eccenca.com/dsm/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "sd": "http://www.w3.org/ns/sparql-service-description#"
}


def get_version():
    """Get the current version or SNAPSHOT."""
    # pylint: disable=import-outside-toplevel
    return version('cmem-cmemc')


def extract_error_message(error):
    """Extract a message from an exception."""
    # exceptions with response is HTTPError
    message = type(error).__name__ + ": " + str(error) + "\n"
    try:
        # try to load Problem Details for HTTP API JSON
        details = json.loads(error.response.text)
        message += type(error).__name__ + ": "
        if 'title' in details:
            message += details["title"] + ": "
        if 'detail' in details:
            message += details["detail"]
    except (AttributeError, ValueError):
        # is not json or any other issue, output plain response text
        pass
    return message


def is_completing():
    """Test for environment which indicates that we are in completion mode.

    Returns true if in validation mode, otherwise false.

    Returns: boolean
    """
    comp_words = os.getenv("COMP_WORDS", default=None)
    cmemc_complete = os.getenv("_CMEMC_COMPLETE", default=None)
    if comp_words is not None:
        return True
    if cmemc_complete is not None:
        return True
    return False


def iri_to_qname(iri):
    """Return a qname for an IRI based on well known namespaces.

    In case of no matching namespace, the full IRI is returned.

    Args:
        iri:

    Returns: string
    """
    for prefix, namespace in NAMESPACES.items():
        iri = iri.replace(namespace, prefix + ":")
    return iri


def read_rdf_graph_files(directory_path):
    """Read all files from directory_path and output as tuples.

    The tuple format is (filepath, graph_name),
    for example ("/tmp/rdf.nt", "http://example.com")
    """
    rdf_graphs = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            full_file_path = os.path.join(root, _file)
            graph_file_name = _file + ".graph"
            full_graph_file_name_path = os.path.join(
                root,
                graph_file_name
            )
            if (not _file.endswith(".graph")
               and os.path.exists(full_graph_file_name_path)):
                graph_name = read_file_to_string(
                    full_graph_file_name_path
                ).strip()
                rdf_graphs.append(
                    (full_file_path, graph_name)
                )
    return rdf_graphs


def read_file_to_string(file_path):
    """Read file to string."""
    with open(file_path, "rb") as _file:
        return _file.read().decode("utf-8")


def get_graphs(writeable=True, readonly=True):
    """Retrieve list of accessible graphs from DP endpoint.

    readonly=True|writeable=True outputs all graphs
    readonly=False|writeable=True outputs only writeable graphs
    readonly=True|writeable=False outputs graphs without write access
    (but read access)
    """
    all_graphs = get_graphs_list()
    filtered_graphs = []
    for graph in all_graphs:
        if graph['writeable'] and writeable:
            filtered_graphs.append(graph)
        if not graph['writeable'] and readonly:
            filtered_graphs.append(graph)
    return filtered_graphs


def get_graphs_as_dict(writeable=True, readonly=True):
    """Get the graph response as dict with IRI as main key."""
    graph_dict = {}
    for graph in get_graphs(writeable=writeable, readonly=readonly):
        graph_dict[graph["iri"]] = graph
    return graph_dict


def convert_uri_to_filename(value, allow_unicode=False):
    """Convert URI to unix friendly filename.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert / to underscore. Convert to lowercase.
    Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value)\
            .encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'\.', '_', value.lower())
    value = re.sub(r'/', '_', value.lower())
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def struct_to_table(source, table=None, prefix=""):
    """Prepare flat key/value table from a deep structure.

    This function takes structure and creates a flat table out of it,
    key by key, value by value. For each level deeper it prefixes the
    father keys.

    Example input:  {'k1': '1', 'k2': {'k3': '3', 'k4': '4'}}
    Example output: [['k1', '1'], ['k2:k3', '3'], ['k2:k4', '4']]

    Args:
        source (any): The structure which is transformed into a flat table.
        table (list): The table where the key/value rows will be appended.
        prefix (str): A prefix which is used to indicate the level.

    Returns:
        The input table extended with rows from the input source.
    """
    if table is None:
        table = []
    if type(source) in (str, bool, int, float):
        table.append([prefix, source])
        return table
    if isinstance(source, dict):
        if len(prefix) != 0:
            prefix = prefix + "."
        for key in source:
            table = struct_to_table(source[key], table, prefix + key)
        return table
    if isinstance(source, list):
        for value in source:
            table = struct_to_table(value, table, prefix)
        return table
    return table


def split_task_id(task_id):
    """Validate and split cmemc task ID.

    Args:
        task_id (str): The task ID in the workspace.

    Raises:
        ValueError: in case the task ID is not splittable
    """
    try:
        project_part = task_id.split(":")[0]
        task_part = task_id.split(":")[1]
    except IndexError as error:
        raise ValueError(
            f"{task_id} is not a valid task ID."
        ) from error
    return project_part, task_part


def metric_get_labels(family: Metric, clean=True) -> Dict[str, list[str]]:
    """
    Get the labels of a metric family.

    Args:
        family: the metric family
        clean : remove keys with only one dimension

    Returns: labels as dict
    """
    labels: Dict[str, list[str]] = {}
    # build tree structure
    for sample in family.samples:
        for label in sample.labels:
            value = sample.labels[label]
            if label not in labels:
                labels[label] = []
            if value not in labels[label]:
                labels[label].append(value)
    if clean:
        labels = dict(filter(lambda elem: len(elem[1]) > 1, labels.items()))
    return labels


def metrics_get_dict(job_id="DP"):
    """Get metrics data as dict."""
    data = {}
    if job_id == "DP":
        for family in text_string_to_metric_families(
                get_prometheus_data().text
        ):
            data[family.name] = family
        return data
    raise ValueError(
        f"job name {job_id} unknown."
    )


def metrics_get_family(job_id, metric_id):
    """Get family data.

    This function returns a dictionary of metric families.
    """
    try:
        return metrics_get_dict(job_id=job_id)[metric_id]
    except KeyError as error:
        raise ValueError(
            f"The job {job_id} does not have a metric {metric_id}."
        ) from error
