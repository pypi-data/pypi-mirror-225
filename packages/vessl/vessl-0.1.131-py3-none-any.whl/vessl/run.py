import datetime
import time
from typing import List, Optional, TextIO

import yaml
from halo import Halo

from openapi_client import ExperimentYamlImportAPIInput, WorkspaceYamlImportAPIInput
from openapi_client.models import ResponseExperimentInfo
from vessl import __version__, vessl_api
from vessl.experiment import list_experiment_logs, read_experiment_by_id
from vessl.kernel_cluster import list_clusters
from vessl.organization import _get_organization_name
from vessl.project import _get_project_name
from vessl.util.constant import LOGO, WEB_HOST, colors
from vessl.workspace import read_workspace


def get_dt():
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dt = f"{colors.GREY}[{dt}]{colors.ENDC}"
    return dt


def wrap_str(string, color="default", end="", do_print=True):
    if color == "cyan":
        wrapped = f"{get_dt()}{colors.OKCYAN}{string}{end}{colors.ENDC}"
    elif color == "green":
        wrapped = f"{get_dt()}{colors.OKGREEN}{string}{end}{colors.ENDC}"
    elif color == "red":
        wrapped = f"{get_dt()}{colors.FAIL}{string}{end}{colors.ENDC}"
    elif color == "warn":
        wrapped = f"{get_dt()}{colors.WARNING}{string}{end}{colors.ENDC}"
    else:
        wrapped = f"{get_dt()}{string}{end}"
    if do_print:
        print(wrapped)
    else:
        return wrapped


def msg_box(msg):
    indent = 1
    lines = msg.split("\n")
    space = " " * indent
    width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    box += "".join([f"║{space}{line:<{width}}{space}║\n" for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


def print_logs(logs: List[str]):
    timezone = datetime.datetime.now().astimezone().tzinfo
    for log in logs:
        ts = datetime.datetime.fromtimestamp(log.timestamp, tz=timezone).strftime("%H:%M:%S.%f")
        message = (
            log.message.replace("\\r", "\r")
            .replace("\\n", "\n")
            .replace("\\b", "\b")
            .replace("\\t", "\t")
            .replace("\\u001b", "\u001b")
        )
        for x in message.split("\n"):
            print(f"[{ts}] {x}")


# Check different stuffs in verify_yaml.
def verify_yaml(yaml_str, spinner):
    # replace \t to double space
    yaml_str = yaml_str.replace("\t", "  ")
    yaml_obj = yaml.safe_load(yaml_str)
    out_str = ""

    # Step 1: Check if all necessary keys exist.
    necessary_keys = [["image"], ["resources"]]
    for keyset in necessary_keys:
        _yaml = yaml_obj
        for key in keyset:
            if key not in _yaml.keys():
                wrap_str(f" Field {key} does not exist! Please specify them in your yaml.", "red"),
                return False, False, False
            _yaml = _yaml[key]

    # Check interactive
    is_interactive = True if "interactive" in yaml_obj.keys() else False

    # Check resources
    yaml_resource = yaml_obj["resources"]
    if "cluster" in yaml_resource:
        # Collect possible cluster and gpus
        cluster = yaml_resource["cluster"]
        cluster_cands = list_clusters()
        cluster_ids = dict()
        cluster_gpus = dict()
        for e in cluster_cands:
            cluster_ids[e.name] = e.id
            cluster_gpus[e.name] = e.available_gpus

        # Verify cluster
        if cluster not in cluster_ids.keys():
            wrap_str(
                f" {cluster} cluster does not exist! Please select among {list(cluster_ids.keys())}.",
                "red",
            )
            return False, False, False
        else:
            out_str += wrap_str(f"   ✓ Cluster verified", "cyan", "\n", do_print=False)

        # Verify accelerators
        if "accelerators" in yaml_resource.keys():
            accelerator = yaml_resource["accelerators"]
            accl_type, accl_num = accelerator.split(":")
            if accl_type not in cluster_gpus[cluster]:
                wrap_str(
                    f" {accl_type} gpu does not exist in cluster! Please select among {cluster_gpus[cluster]}",
                    "red",
                )
                return False, False, False
            else:
                out_str += wrap_str("   ✓ Accelerator verified", "cyan", "\n", do_print=False)

    # Check ports if exists
    if is_interactive:
        out_str += wrap_str("   ✓ Mode: Interactive", "cyan", do_print=False)
        ports = (
            yaml_obj["interactive"]["ports"] if "ports" in yaml_obj["interactive"].keys() else []
        )
        for port in ports:
            if str(port) in ["22", "8888"]:
                out_str += wrap_str(
                    f"   - ⚠️  WARNING: Port {str(port)} is used for ssh by default.",
                    "warn",
                    "\n",
                    do_print=False,
                )
    else:
        out_str += wrap_str("   - 💡 Mode: Non-Interactive", "cyan", do_print=False)

    return is_interactive, out_str, yaml_obj


# Get yaml, verify yaml
def run_from_yaml(
    yaml_file: TextIO,
    yaml_body: str,
    yaml_file_name: str,
    **kwargs,
) -> ResponseExperimentInfo:
    if yaml_body == "":
        body = yaml_file.read()
    else:
        body = yaml_body
    yaml_file_name = yaml_file_name.split("/")[-1]

    wrap_str(" Launch VESSL Run 👟", "green")
    organization = _get_organization_name(**kwargs)
    project = _get_project_name(**kwargs)
    wrap_str(f"   > Organization: {organization}", "cyan")
    wrap_str(f"   > Project: {project}", "cyan")

    spinner = Halo(text="Verifying YAML", text_color="cyan", spinner="dots", placement="right")
    spinner.start()
    interactive, out_str, yaml_obj = verify_yaml(body, spinner)
    if yaml_obj == False:
        spinner.stop_and_persist(
            symbol="😢", text=wrap_str(" YAML verification failed!", "red", do_print=False)
        )
        return
    else:
        spinner.stop_and_persist(
            symbol="✅", text=wrap_str(" YAML definition verified!", "green", do_print=False)
        )
    print(out_str)
    wrap_str(f" Running: {yaml_file_name} ➡️", "green")
    yaml_obj["run"][0]["command"] = yaml_obj["run"][0]["command"].strip()
    clean_yaml_str = yaml.dump(yaml_obj)
    msg_box(clean_yaml_str)

    # workspace run
    if interactive:
        run_interactive_from_yaml(organization, body)
    else:
        run_batch_from_yaml(organization, project, body)
    return


# Applies yaml to cluster
def apply_yaml(organization, body, project=None, is_workspace=True):
    if is_workspace:
        workload = "workspace"
    else:
        workload = "experiment"
    spinner = Halo(
        text="Submitting Run definition to cluster ..",
        text_color="cyan",
        spinner="dots",
        placement="right",
    )
    spinner.start()
    if is_workspace:
        response = vessl_api.workspace_yaml_import_api(
            organization_name=organization,
            workspace_yaml_import_api_input=WorkspaceYamlImportAPIInput(
                data=body,
            ),
        )
    else:
        response = vessl_api.experiment_yaml_import_api(
            organization_name=organization,
            project_name=project,
            experiment_yaml_import_api_input=ExperimentYamlImportAPIInput(
                data=body,
            ),
        )
    spinner.stop_and_persist(
        symbol="✅", text=wrap_str(" Your Run is submitted to the cluster.", "green", do_print=False)
    )
    if is_workspace:
        link = f"{WEB_HOST}/{response.organization.name}/workspaces/{response.id}"
    else:
        link = f"{WEB_HOST}/{response.organization.name}/{response.project.name}/experiments/{response.number}"
    hlink = f"\033]8;;{link}\033\\{link}\033]8;;\033\\"
    wrap_str(
        f" Check your Run at {hlink}",
        "cyan",
    )
    return response


# Check if workload have started
def check_started(response, is_workspace=True):
    if is_workspace:
        workload = "Workspace"
        workspace_id = response.id
    else:
        workload = "Experiment"
        experiment_id = response.id

    spinner = Halo(
        text="Cluster Pending ..",
        text_color="cyan",
        spinner="dots",
        placement="right",
    )
    spinner.start()
    not_started = True
    terminated = False
    while not_started and (not terminated):
        if is_workspace:
            status = read_workspace(workspace_id=workspace_id).status
        else:
            status = read_experiment_by_id(experiment_id).status
        if status != "pending":
            not_started = False
        if status in ["failed", "stopped"]:
            terminated = True

    if terminated:
        spinner.stop_and_persist(
            symbol="🏝️", text=wrap_str(f" {workload} terminated!", "green", do_print=False)
        )
        return False
    spinner.stop_and_persist(
        symbol="✅",
        text=wrap_str(f"> Your Run is assigned to the cluster.", "green", do_print=False),
    )

    spinner = Halo(
        text="Cluster Initializing .. ",
        text_color="cyan",
        spinner="dots",
        placement="right",
    )
    spinner.start()
    not_started = True
    while not_started and (not terminated):
        if is_workspace:
            status = read_workspace(workspace_id=workspace_id).status
        else:
            status = read_experiment_by_id(experiment_id).status
        if status == "running":
            not_started = False
        if status in ["failed", "stopped"]:
            terminated = True
    if terminated:
        spinner.stop_and_persist(
            symbol="🏝️", text=wrap_str(f" {workload} terminated!", "green", do_print=False)
        )
        return False
    spinner.stop_and_persist(
        symbol="✅", text=wrap_str(f"> Run has started!", "green", do_print=False)
    )
    print(LOGO)
    wrap_str(f" VESSL Run has succesfully launched! 🚀", "green")
    return True


def run_interactive_from_yaml(organization, body):
    response = apply_yaml(organization, body, is_workspace=True)
    started = check_started(response, is_workspace=True)
    if not started:
        return
    endpoints = response.endpoints.manually_defined_endpoints
    for endpoint in endpoints:
        wrap_str(f"📍 Endpoint {endpoint.name}: {endpoint.endpoint}")


def run_batch_from_yaml(organization, project, body):
    response = apply_yaml(organization, body, project, is_workspace=False)
    experiment_id = response.id
    experiment_number = response.number
    started = check_started(response, is_workspace=False)
    if not started:
        return
    wrap_str(f" Showing experiment logs from now !", "green")

    # fetch pod outputs
    experiment_finished_dt = None
    after = 0
    first_log = True
    while True:
        if (
            read_experiment_by_id(experiment_id).status not in ["pending", "running"]
            and experiment_finished_dt is None
        ):
            experiment_finished_dt = time.time()

        if experiment_finished_dt is not None and (time.time() - experiment_finished_dt) > 5:
            break

        # worker number: 0 since we do not handle distributed exps
        logs = list_experiment_logs(
            experiment_number=experiment_number,
            before=int(time.time() - 5),
            after=after,
            worker_numer=0,
        )
        # do not print first log - generated while cluster was pending.
        if not first_log:
            print_logs(logs)
        else:
            first_log = False
        if len(logs) > 0:
            after = logs[-1].timestamp + 0.000001
        time.sleep(3)
