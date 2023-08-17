import os
import sys

import click

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart


@click.command()
@click.option(
    "--timeout", "ssh_timeout", default=60, required=False, type=int, help="SSH connection timeout in seconds"
)
@click.option(
    "-x",
    "--tart-executable",
    required=False,
    default="tart",
    type=str,
    help="Path to the tart executable.",
)
@click.option(
    "--shell",
    required=False,
    default="/bin/zsh",
    type=str,
    help="Path to the shell to be used for commands over ssh.",
)
@click.argument("script")
@click.argument("stage")
def run(ssh_timeout, tart_executable, shell, script, stage):
    """Run commands."""
    p = GitLabCustomCommandConfig()

    if not p.tart_executor_shell:
        p.tart_executor_shell = shell
    ######################################################################
    # Connect to VM
    ######################################################################
    tart = Tart(exec_path=tart_executable)
    tart_vm_name = p.vm_name()

    try:
        tart_ip = tart.ip(tart_vm_name, timeout=ssh_timeout)
        click.echo(f"[{stage}][INFO] Establishing SSH conntection to '{p.ssh_username}@{tart_ip}'")
    except:
        click.secho(
            f"[{stage}][ERROR] Could not establish SSH conntection to '{tart_vm_name}' after '{ssh_timeout}' seconds.",
            fg="red",
        )
        sys.exit(1)

    try:
        ssh_session = tart.ssh_session(name=p.vm_name(), username=p.ssh_username, password=p.ssh_password)
    except:
        click.secho(f"[{stage}][ERROR] Could not establish SSH session with '{p.ssh_username}@{tart_ip}'", fg="red")
        sys.exit(1)

    remote_temp_dir = "/opt/temp"
    script_name = os.path.basename(script)
    remote_script_path = os.path.join(remote_temp_dir, stage + "-" + script_name)

    sftp = ssh_session.ssh_client.open_sftp()
    sftp.put(script, remote_script_path)
    sftp.close()

    # ssh_session.exec_ssh_command(f"cd {remote_build_dir}")
    script_exit_code = ssh_session.exec_ssh_command(f"{p.shell} -l {remote_script_path}", get_pty=True)

    sys.exit(script_exit_code)
