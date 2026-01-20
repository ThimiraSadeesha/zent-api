import paramiko
from typing import Optional, Dict
import logging
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# GLOBAL SSH CLIENT
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


def get_docker_stats(client):

    check_cmd = "docker --version 2>/dev/null"
    output, err = run_command(client, check_cmd)

    if not output:
        return {"docker_installed": False, "error": "Docker not found"}

    stats_cmd = """docker stats --no-stream --format '{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}|{{.PIDs}}' 2>/dev/null"""
    stats_output, stats_err = run_command(client, stats_cmd)

    status_cmd = "docker ps -a --format '{{.Names}}|{{.Status}}|{{.State}}|{{.Image}}' 2>/dev/null"
    status_output, status_err = run_command(client, status_cmd)

    if not stats_output and not status_output:
        return {"docker_installed": True, "total_containers": 0, "containers": []}

    status_map = {}
    if status_output:
        for line in status_output.split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    name, status, state, image = parts[0], parts[1], parts[2], parts[3]
                    status_map[name] = {
                        "status": status,
                        "state": state,
                        "image": image
                    }

    containers = []
    if stats_output:
        for line in stats_output.split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 7:
                    name = parts[0]
                    container_info = {
                        "name": name,
                        "cpu_percent": parts[1],
                        "memory_usage": parts[2],
                        "memory_percent": parts[3],
                        "network_io": parts[4],
                        "block_io": parts[5],
                        "pids": parts[6]
                    }
                    if name in status_map:
                        container_info.update(status_map[name])
                    containers.append(container_info)

    for name, info in status_map.items():
        if not any(c['name'] == name for c in containers):
            containers.append({
                "name": name,
                "status": info["status"],
                "state": info["state"],
                "image": info["image"],
                "cpu_percent": "N/A",
                "memory_usage": "N/A",
                "memory_percent": "N/A",
                "network_io": "N/A",
                "block_io": "N/A",
                "pids": "N/A"
            })

    return {
        "docker_installed": True,
        "total_containers": len(containers),
        "running_containers": sum(1 for c in containers if c.get("state") == "running"),
        "containers": containers
    }


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


def get_client():
    global ssh_client
    return ssh_client
