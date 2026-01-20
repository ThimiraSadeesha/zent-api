import paramiko
from typing import Optional, Dict
import logging
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
ssh_client = None

def run_command(client, command: str):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    if error:
        return None, error
    return output, None


def get_ram_usage(client):
    cmd = "free -m | awk 'NR==2{printf \"%s,%s,%.2f\", $3,$2,$3*100/$2 }'"
    output, err = run_command(client, cmd)
    if output:
        used, total, percent = output.split(',')
        return {"used_mb": used, "total_mb": total, "percent": percent}
    return {"error": err}


def get_disk_usage(client):
    cmd = "df -h / | awk 'NR==2{printf \"%s,%s,%s\", $3,$2,$5 }'"
    output, err = run_command(client, cmd)
    if output:
        used, total, percent = output.split(',')
        return {"used": used, "total": total, "percent": percent}
    return {"error": err}


def get_cpu_usage(client):
    cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"
    output, err = run_command(client, cmd)
    return {"percent": output} if output else {"error": err}


def get_thread_usage(client):
    cmd = "ps -eLf | wc -l"
    output, err = run_command(client, cmd)
    return {"count": output} if output else {"error": err}


def get_uptime(client):
    cmd = "uptime | awk '{print $3,$4,$5\" | Load:\", $(NF-2), $(NF-1), $NF}'"
    output, err = run_command(client, cmd)
    return {"uptime": output} if output else {"error": err}


def get_os_info(client):
    cmd = "cat /etc/os-release | grep -E '^(NAME|VERSION)=' | cut -d'=' -f2 | tr -d '\"' | tr '\\n' '|'"
    output, err = run_command(client, cmd)
    if output:
        parts = output.strip('|').split('|')
        return {"name": parts[0] if len(parts) > 0 else "", "version": parts[1] if len(parts) > 1 else ""}
    return {"error": err}


def ssh_connect(host: str, username: str, password: Optional[str] = None,
                port: int = 22, key: Optional[str] = None) -> Dict:
    global ssh_client
    if ssh_client is not None:
        return {"message": "Already connected"}
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if key:
            pkey = paramiko.RSAKey.from_private_key_file(key)
            ssh_client.connect(hostname=host, username=username, pkey=pkey, port=port, timeout=10)
        else:
            ssh_client.connect(hostname=host, username=username, password=password, port=port, timeout=10)
        logger.info(f"✅ SSH login successful: {username}@{host}:{port}")

        data = {
            "ram": get_ram_usage(ssh_client),
            "disk": get_disk_usage(ssh_client),
            "cpu": get_cpu_usage(ssh_client),
            "threads": get_thread_usage(ssh_client),
            "uptime": get_uptime(ssh_client),
            "os": get_os_info(ssh_client),
        }

        return data

    except Exception as e:
        ssh_client = None
        logger.error(f"❌ SSH login failed: {username}@{host}:{port} | {str(e)}")
        raise e

def reboot_server(client):
    cmd = "sudo reboot"
    try:
        client.exec_command(cmd)
        return {"status": "rebooting"}
    except Exception as e:
        return {"error": str(e)}


def get_client():
    global ssh_client
    return ssh_client
