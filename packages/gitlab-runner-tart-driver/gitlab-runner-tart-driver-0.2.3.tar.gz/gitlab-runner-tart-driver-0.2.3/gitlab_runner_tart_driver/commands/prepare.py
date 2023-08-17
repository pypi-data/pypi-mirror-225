import os
import sys

import click

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart
from gitlab_runner_tart_driver.modules.tart import TartVolume
from gitlab_runner_tart_driver.modules.utils import get_host_spec
from gitlab_runner_tart_driver.modules.utils import print_host_spec


@click.command()
@click.option("--cpu", required=False, default=None, type=int, help="Number of CPUs associated to VM")
@click.option("--memory", required=False, default=None, type=int, help="VM memory size in megabytes associated to VM")
@click.option(
    "--display",
    required=False,
    default=None,
    type=str,
    help="VM display resolution in a format of <width>x<height>. For example, 1200x800",
)
@click.option(
    "--auto-resources/--no-auto-resources",
    required=False,
    default=True,
    is_flag=True,
    type=bool,
    help="If enabled, the driver will divide system resources equally to the concurrent VMs.",
)
@click.option(
    "--concurrency",
    required=False,
    default=1,
    type=int,
    help="Number of concurrent processes that are supported. ATTENTION tart currently only support two concurrent VMs",
)
@click.option(
    "--cache-dir",
    required=False,
    default=None,
    type=str,
    help="Caching dir to be used.",
)
@click.option(
    "--builds-dir",
    required=False,
    default=None,
    type=str,
    help="Path to the builds directory.",
)
@click.option(
    "--timeout",
    required=False,
    default=60,
    type=int,
    help="Timeout in seconds for the VM to be reachable via SSH.",
)
@click.option(
    "--volume",
    "volumes",
    required=False,
    default=[],
    type=str,
    multiple=True,
    help="Volume mount definition with docker syntax. <host_dir>:<vm_dir>[:ro]",
)
@click.option(
    "--install-gitlab-runner",
    required=False,
    type=bool,
    is_flag=True,
    help="Will install the gitlab-runner if not present.",
)
@click.option(
    "--force-install-gitlab-runner",
    required=False,
    type=str,
    is_flag=True,
    help="This will force the installation of the GitLab Runner independent of a previously installed version",
)
@click.option(
    "--gitlab-runner-version",
    required=False,
    type=str,
    default="latest",
    help="The version of the GitLab Runner to be installed. Example '15.11.0'",
)
@click.option("-x", "--tart-executable", required=False, default="tart", type=str, help="Path to the tart executable.")
def prepare(
    cpu,
    memory,
    display,
    auto_resources,
    concurrency,
    cache_dir,
    builds_dir,
    timeout,
    volumes,
    install_gitlab_runner,
    force_install_gitlab_runner,
    gitlab_runner_version,
    tart_executable,
):
    """Prepare the environment and start the tart VM."""

    print_host_spec()

    p = GitLabCustomCommandConfig()

    if not p.tart_executor_display:
        p.tart_executor_display = display
    if not p.tart_executor_install_gitlab_runner:
        p.tart_executor_install_gitlab_runner = install_gitlab_runner
    if not p.tart_executor_timeout:
        p.tart_executor_timeout = timeout

    tart = Tart(exec_path=tart_executable)
    tart_images = tart.list()
    tart_vm_map = {}
    for i in tart_images:
        tart_vm_map[i.name] = i

    ######################################################################
    # OCI LOGIN
    ######################################################################
    click.echo(f"[INFO] Logging into GitLab Registry '{p.ci_registry}'")
    try:
        tart.login(username=p.ci_registry_user, password=p.ci_registry_password, host=p.ci_registry)
    except:
        click.secho(f"[ERROR] Failed to login to '{p.ci_registry}'", fg="red")

    if p.registry_username and p.registry_password and p.registry:
        click.echo(f"[INFO] Logging into OCI Registry '{p.registry}'")
        try:
            tart.login(username=p.registry_username, password=p.registry_password, host=p.registry)
        except:
            click.secho(f"[ERROR] Failed to login to '{p.registry}'", fg="red")

    if p.tart_registry_username and p.tart_registry_password and p.tart_registry:
        click.echo(f"[INFO] Logging into custom OCI Registry '{p.tart_registry}'")
        try:
            tart.login(username=p.tart_registry_username, password=p.tart_registry_password, host=p.tart_registry)
        except:
            click.secho(f"[ERROR] Failed to login to '{p.tart_registry}'", fg="red")

    ######################################################################
    # PULL
    ######################################################################
    if (
        (p.pull_policy == "always")
        or (p.ci_job_image not in tart_vm_map and p.pull_policy != "never")
        or (p.ci_job_image not in tart_vm_map and p.pull_policy == "if-not-present")
    ):
        click.echo(f"[INFO] Pulling '{p.ci_job_image}' [pull_policy={p.pull_policy}]")
        try:
            tart.pull(p.ci_job_image)
        except:
            click.secho(f"[ERROR] Failed to pull image '{p.ci_job_image}'", fg="red")
            sys.exit(1)
    else:
        click.echo(f"[INFO] Skipping '{p.ci_job_image}' [pull_policy={p.pull_policy}]")

    ######################################################################
    # Create VM
    ######################################################################
    tart_vm_name = p.vm_name()
    if tart_vm_name in tart_vm_map:
        if tart_vm_map[tart_vm_name].running:
            click.echo(f"[INFO] Found running VM '{tart_vm_name}'. Going to stop it...")
            tart.stop(tart_vm_name)
        click.echo(f"[INFO] Found VM '{tart_vm_name}'. Going to delete it...")
        tart.delete(tart_vm_name)

    # verfiy that the limit of running VMs is not exceeded
    list_running_vms = []
    for vm in tart.list():
        if vm.running:
            list_running_vms.append(vm)

    if len(list_running_vms) > p.tart_max_vm_count:
        click.secho(
            f"[ERROR] The limit of running VMs [{p.tart_max_vm_count}] is exceeded [{len(list_running_vms)}].", fg="red"
        )
        sys.exit(1)

    click.echo(f"[INFO] Cloning VM instance '{tart_vm_name}' from '{p.ci_job_image}'")
    try:
        tart.clone(p.ci_job_image, tart_vm_name)
    except:
        click.secho(f"[ERROR] failed to clone image f'{p.ci_job_image}'", fg="red")
        sys.exit(1)

    if cpu or memory or p.display:
        click.echo(f"[INFO] Configuring instance '{tart_vm_name}' from '{p.ci_job_image}'")
        click.echo(
            f"[INFO] {tart_vm_name} [cpu={cpu if cpu else 'default'}, memory={memory if memory else 'default'}, display={p.display if p.display else 'default'}]"
        )
        tart.set(tart_vm_name, cpu=cpu, memory=memory, display=display)
    elif auto_resources:
        click.echo("[INFO] Auto resource-disribution enabled.")
        host_spec = get_host_spec()
        tart.set(tart_vm_name, cpu=int(host_spec.cpu_count / concurrency), memory=int(host_spec.memory / concurrency))

    click.echo(f"[INFO] Starting VM instance '{tart_vm_name}'")

    remote_build_dir = "/opt/builds"
    remote_script_dir = "/opt/temp"
    remote_cache_dir = "/opt/cache"

    volume_mounts = []
    if cache_dir:
        cache_dir = os.path.abspath(os.path.expanduser(cache_dir))
        os.makedirs(cache_dir, exist_ok=True)
        click.echo(f"[INFO] Cache directory set to '{cache_dir}'")
        volume_mounts.append(TartVolume(source=cache_dir, dest=remote_cache_dir, name="cache", ro=False))
    if builds_dir:
        # Concurrency compatible builds directory
        # see https://docs.gitlab.com/runner/executors/shell.html#run-scripts-as-a-privileged-user
        # <builds_dir>/<short-token>/<concurrent-id>/<namespace>/<project-name>.
        builds_dir = os.path.join(
            os.path.abspath(os.path.expanduser(builds_dir)), p.ci_runner_short_token, p.ci_concurrent_project_id
        )
        os.makedirs(builds_dir, exist_ok=True)
        click.echo(f"[INFO] Builds directory set to '{builds_dir}'")
        volume_mounts.append(TartVolume(source=builds_dir, dest=remote_build_dir, name="builds", ro=False))

    for v in volumes:
        volume_mounts.append(TartVolume.from_string(v))

    try:
        tart.run(tart_vm_name, volume_mounts, no_graphics=p.headless, softnet=p.softnet_enabled)
    except:
        click.secho(f"[ERROR] Failed to start VM '{tart_vm_name}'", fg="red")
        sys.exit(1)

    try:
        ip = tart.ip(tart_vm_name, timeout=p.timeout)
    except:
        click.secho(f"[ERROR] Failed to get IP of VM '{tart_vm_name}'", fg="red")
        sys.exit(1)

    if not ip:
        click.echo(f"[ERROR] Error, VM was not reacheable after '{p.timeout}' seconds")
        sys.exit(1)

    try:
        ssh_session = tart.ssh_session(name=p.vm_name(), username=p.ssh_username, password=p.ssh_password)
        ssh_session.exec_ssh_command(
            f"sudo mkdir -p {remote_script_dir} && sudo chown {p.ssh_username}:{p.ssh_username} {remote_script_dir}",
        )

        for volume in volume_mounts:
            click.echo(f"[INFO] Setting up volume mount '{volume.name}'")
            ssh_session.exec_ssh_command(
                f"sudo mkdir -p $(dirname {volume.dest}); sudo ln -sf '/Volumes/My Shared Files/{volume.name}' {volume.dest}",
            )

        # if cache and builds volumes are not mounted, make sure to create them locally inside the VM
        if not cache_dir:
            ssh_session.exec_ssh_command(
                f"sudo mkdir -p {remote_cache_dir} && sudo chown {p.ssh_username}:{p.ssh_username} {remote_cache_dir}",
            )

        if not builds_dir:
            ssh_session.exec_ssh_command(
                f"sudo mkdir -p {remote_build_dir} && sudo chown {p.ssh_username}:{p.ssh_username} {remote_build_dir}",
            )
    except:
        click.secho(f"[ERROR] Failed so prepare VM '{tart_vm_name}'", fg="red")
        sys.exit(1)

    if p.install_gitlab_runner:
        click.echo(
            f"[INFO] Installing GitLab Runner '{gitlab_runner_version}' [force: '{force_install_gitlab_runner}']"
        )
        try:
            tart.install_gitlab_runner(name=tart_vm_name, username=p.ssh_username, password=p.ssh_password)
        except:
            click.secho(f"[ERROR] Failed to install GitLab Runner '{gitlab_runner_version}'", fg="red")
            sys.exit(1)

    tart.print_spec(tart_vm_name)

    sys.exit(0)
