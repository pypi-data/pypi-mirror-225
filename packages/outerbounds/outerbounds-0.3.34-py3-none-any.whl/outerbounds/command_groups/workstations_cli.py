import click
import yaml
import requests
import base64
import datetime
import hashlib
import json
import os
from os import path
from pathlib import Path
from ..utils import kubeconfig, metaflowconfig
from requests.exceptions import HTTPError
import platform
import subprocess
from subprocess import CalledProcessError
from ..utils.schema import (
    OuterboundsCommandResponse,
    CommandStatus,
    OuterboundsCommandStatus,
)
from tempfile import NamedTemporaryFile

KUBECTL_INSTALL_MITIGATION = "Please install kubectl manually from https://kubernetes.io/docs/tasks/tools/#kubectl"


@click.group()
def cli(**kwargs):
    pass


@cli.command(help="Generate a token to use your cloud workstation", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
def generate_workstation_token(config_dir=None, profile=None):
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        auth_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_AUTH_SERVER"
        )
        k8s_response = requests.get(
            f"{auth_url}/generate/k8s", headers={"x-api-key": metaflow_token}
        )
        try:
            k8s_response.raise_for_status()
            k8s_response_json = k8s_response.json()
            token = k8s_response_json["token"]
            token_data = base64.b64decode(token.split(".")[1] + "==")
            exec_creds = {
                "kind": "ExecCredential",
                "apiVersion": "client.authentication.k8s.io/v1beta1",
                "spec": {},
                "status": {
                    "token": token,
                    "expirationTimestamp": datetime.datetime.fromtimestamp(
                        json.loads(token_data)["exp"], datetime.timezone.utc
                    ).isoformat(),
                },
            }
            click.echo(json.dumps(exec_creds))
        except HTTPError:
            click.secho("Failed to generate workstation token.", fg="red")
            click.secho("Error: {}".format(json.dumps(k8s_response.json(), indent=4)))
    except Exception as e:
        click.secho("Failed to generate workstation token.", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Configure a cloud workstation", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-b",
    "--binary",
    default="outerbounds",
    help="Path to the location of your outerbounds binary",
)
@click.option(
    "-o",
    "--output",
    default="",
    help="Show output in the specified format.",
    type=click.Choice(["json", ""]),
)
def configure_cloud_workstation(config_dir=None, profile=None, binary=None, output=""):
    configure_response = OuterboundsCommandResponse()
    kubeconfig_configure_step = CommandStatus(
        "ConfigureKubeConfig", OuterboundsCommandStatus.OK, "Kubeconfig is configured"
    )

    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        auth_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_AUTH_SERVER"
        )
        k8s_response = requests.get(
            f"{auth_url}/generate/k8s", headers={"x-api-key": metaflow_token}
        )

        try:
            k8s_response.raise_for_status()
            k8s_response_json = k8s_response.json()
            token_data = base64.b64decode(
                k8s_response_json["token"].split(".")[1] + "=="
            )
            ws_namespace = "ws-{}".format(
                hashlib.md5(
                    bytes(json.loads(token_data)["username"], "utf-8")
                ).hexdigest()
            )

            kubeconfig.set_context(
                "outerbounds-workstations",
                "outerbounds-cluster",
                ws_namespace,
                "obp-user",
            )
            kubeconfig.set_cluster(
                "outerbounds-cluster", k8s_response_json["endpoint"], True
            )
            kubeconfig.add_user_with_exec_credential(
                "obp-user", binary, config_dir, profile
            )
            if output == "json":
                configure_response.add_step(kubeconfig_configure_step)
                click.echo(json.dumps(configure_response.as_dict(), indent=4))
        except HTTPError:
            click.secho("Failed to configure cloud workstation", fg="red", err=True)
            click.secho(
                "Error: {}".format(json.dumps(k8s_response.json(), indent=4)), err=True
            )
            if output == "json":
                kubeconfig_configure_step.update(
                    OuterboundsCommandStatus.FAIL,
                    json.dumps(k8s_response.json(), indent=4),
                    "",
                )
                configure_response.add_step(kubeconfig_configure_step)
                click.echo(json.dumps(configure_response.as_dict(), indent=4))
        except kubeconfig.KubeconfigError as ke:
            click.secho("Failed to configure cloud workstation", fg="red", err=True)
            click.secho("Error: {}".format(str(ke)), err=True)
            if output == "json":
                kubeconfig_configure_step.update(
                    OuterboundsCommandStatus.FAIL, str(ke), ""
                )
                configure_response.add_step(kubeconfig_configure_step)
                click.echo(json.dumps(configure_response.as_dict(), indent=4))
    except Exception as e:
        click.secho("Failed to configure cloud workstation", fg="red", err=True)
        click.secho("Error: {}".format(str(e)), err=True)
        if output == "json":
            kubeconfig_configure_step.update(OuterboundsCommandStatus.FAIL, str(e), "")
            configure_response.add_step(kubeconfig_configure_step)
            click.echo(json.dumps(configure_response.as_dict(), indent=4))


@cli.command(help="List all existing workstations", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
def list_workstations(config_dir=None, profile=None):
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        workstations_response = requests.get(
            f"{api_url}/v1/workstations", headers={"x-api-key": metaflow_token}
        )
        try:
            workstations_response.raise_for_status()
            click.echo(json.dumps(workstations_response.json(), indent=4))
        except HTTPError:
            click.secho("Failed to generate workstation token.", fg="red")
            click.secho(
                "Error: {}".format(json.dumps(workstations_response.json(), indent=4))
            )
    except Exception as e:
        click.secho("Failed to list workstations", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Hibernate workstation", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-w",
    "--workstation",
    default="",
    help="The ID of the workstation to hibernate",
)
def hibernate_workstation(config_dir=None, profile=None, workstation=None):
    if workstation is None or workstation == "":
        click.secho("Please specify a workstation ID", fg="red")
        return
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        hibernate_response = requests.put(
            f"{api_url}/v1/workstations/hibernate/{workstation}",
            headers={"x-api-key": metaflow_token},
        )
        try:
            hibernate_response.raise_for_status()
            response_json = hibernate_response.json()
            if len(response_json) > 0:
                click.echo(json.dumps(response_json, indent=4))
            else:
                click.secho("Success", fg="green", bold=True)
        except HTTPError:
            click.secho("Failed to hibernate workstation", fg="red")
            click.secho(
                "Error: {}".format(json.dumps(hibernate_response.json(), indent=4))
            )
    except Exception as e:
        click.secho("Failed to hibernate workstation", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Restart workstation to the int", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-w",
    "--workstation",
    default="",
    help="The ID of the workstation to restart",
)
def restart_workstation(config_dir=None, profile=None, workstation=None):
    if workstation is None or workstation == "":
        click.secho("Please specify a workstation ID", fg="red")
        return
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        restart_response = requests.put(
            f"{api_url}/v1/workstations/restart/{workstation}",
            headers={"x-api-key": metaflow_token},
        )
        try:
            restart_response.raise_for_status()
            response_json = restart_response.json()
            if len(response_json) > 0:
                click.echo(json.dumps(response_json, indent=4))
            else:
                click.secho("Success", fg="green", bold=True)
        except HTTPError:
            click.secho("Failed to restart workstation", fg="red")
            click.secho(
                "Error: {}".format(json.dumps(restart_response.json(), indent=4))
            )
    except Exception as e:
        click.secho("Failed to restart workstation", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Install dependencies needed by workstations", hidden=True)
@click.option(
    "-d",
    "--install-dir",
    default=path.expanduser("~/.metaflowconfig/bin"),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    default="",
    help="Show output in the specified format.",
    type=click.Choice(["json", ""]),
)
def install_workstation_dependencies(install_dir=None, output=""):
    install_response = OuterboundsCommandResponse()
    install_response.add_or_update_metadata("RELOAD_REQUIRED", False)
    kubectl_install_step = CommandStatus(
        "kubectl", OuterboundsCommandStatus.OK, "kubectl is installed."
    )

    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    # Check if kubectl exists
    try:
        # Check if kubectl can be executed from the command line
        subprocess.run(["which", "kubectl"], capture_output=True, check=True)
        click.echo("kubectl already installed", err=True)
        click.secho("Success", fg="green", bold=True, err=True)
        if output == "json":
            install_response.add_step(kubectl_install_step)
            click.echo(json.dumps(install_response.as_dict(), indent=4))
        return
    except CalledProcessError:
        pass

    plt = platform.system()
    arch_info = platform.machine()

    kubectl_url = ""
    if plt == "Darwin":
        if arch_info == "arm64":
            kubectl_url = f"https://dl.k8s.io/release/v1.27.3/bin/darwin/arm64/kubectl"
        elif arch_info == "x86_64":
            kubectl_url = f"https://dl.k8s.io/release/v1.27.3/bin/darwin/amd64/kubectl"
    elif plt == "Linux":
        if arch_info == "x86_64":
            kubectl_url = f"https://dl.k8s.io/release/v1.27.3/bin/linux/amd64/kubectl"
        elif arch_info == "aarch64":
            kubectl_url = f"https://dl.k8s.io/release/v1.27.3/bin/linux/arm64/kubectl"

    if kubectl_url == "":
        message = f"No kubectl install URL available for platform: {plt}/{arch_info}"
        click.secho(f"{message}. {KUBECTL_INSTALL_MITIGATION}", fg="red", err=True)
        if output == "json":
            kubectl_install_step.update(
                OuterboundsCommandStatus.FAIL, message, KUBECTL_INSTALL_MITIGATION
            )
            install_response.add_step(kubectl_install_step)
            click.echo(json.dumps(install_response.as_dict(), indent=4))
        return

    # Download kubectl
    try:
        click.echo(f"Downloading kubectl from {kubectl_url}", err=True)
        kubectl_response = requests.get(kubectl_url)
        kubectl_response.raise_for_status()

        with NamedTemporaryFile(dir=install_dir, delete=False) as f:
            f.write(kubectl_response.content)
            temp_file_name = f.name

        if os.path.exists(f"{install_dir}/kubectl"):
            os.remove(f"{install_dir}/kubectl")

        os.rename(temp_file_name, f"{install_dir}/kubectl")
        os.chmod(f"{install_dir}/kubectl", 0o755)

        # check if install_dir is already in PATH
        if install_dir not in os.environ["PATH"]:
            if plt == "Darwin":
                fname = f"{path.expanduser('~')}/.zshrc"
            elif plt == "Linux":
                fname = f"{path.expanduser('~')}/.bashrc"

            install_dir_path_str = f"\nexport PATH=$PATH:{install_dir}"

            click.echo(f"Placing {install_dir} in PATH by adding to {fname}", err=True)

            with open(fname, "a+") as f:
                if install_dir_path_str not in f.read():
                    f.write("\n# Added by Outerbounds\n")
                    f.write(install_dir_path_str)

            install_response.add_or_update_metadata("RELOAD_REQUIRED", True)

        else:
            click.echo(f"{install_dir} is already in PATH", err=True)

        click.secho("Success", fg="green", bold=True, err=True)
        if output == "json":
            install_response.add_step(kubectl_install_step)
            click.echo(json.dumps(install_response.as_dict(), indent=4))
        return
    except Exception as e:
        reason = "Failed to install kubectl"
        click.secho(f"Error: {str(e)}", err=True)
        click.secho(f"{reason}. {KUBECTL_INSTALL_MITIGATION}", fg="red", err=True)
        if output == "json":
            kubectl_install_step.update(
                OuterboundsCommandStatus.FAIL, reason, KUBECTL_INSTALL_MITIGATION
            )
            install_response.add_step(kubectl_install_step)
            click.echo(json.dumps(install_response.as_dict(), indent=4))
        return
