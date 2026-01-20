from app.services.server_service import run_command




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


def docker_start_container(client, container_name: str):
    cmd = f"docker start {container_name}"
    output, err = run_command(client, cmd)
    if err:
        return {"error": err}
    return {"status": "started", "container": container_name, "output": output}


def docker_stop_container(client, container_name: str):
    cmd = f"docker stop {container_name}"
    output, err = run_command(client, cmd)
    if err:
        return {"error": err}
    return {"status": "stopped", "container": container_name, "output": output}


def docker_restart_container(client, container_name: str):
    cmd = f"docker restart {container_name}"
    output, err = run_command(client, cmd)
    if err:
        return {"error": err}
    return {"status": "restarted", "container": container_name, "output": output}
