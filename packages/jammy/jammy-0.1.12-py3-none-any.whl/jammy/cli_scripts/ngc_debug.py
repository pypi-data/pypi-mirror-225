#!/usr/bin/env python3
# pylint: disable=global-variable-not-assigned, global-statement
import os
import os.path as osp
import json
import time
import hydra
from omegaconf import DictConfig, OmegaConf
from jammy.cli.keyboard import yes_or_no

from jammy.logging import get_logger
from jammy.utils.process import run_simple_command

logger = get_logger()

job_cmd = []
job_cfg = {
    'aceId': 257,
    'aceInstance': 'dgx1v.16g.1.norm',
    'aceName': 'nv-us-west-2',
    'name': 'ml-model.qsh.16g.1_debug',
    'publishedContainerPorts': [9999, 8888],
    'dockerImageName': 'nvidian/lpr-imagine/imaginaire_qsh:1.1',
    'command': 'cd /mnt/qsh_ws;tmux new-session -d -s dv \"nvitop\"; sleep 7d',
    'minAvailability': 1,
    'replicaCount': 1,
    'arrayType': 'PYTORCH',
    'runPolicy': {'totalRuntimeSeconds': 604800, 'preemptClass': 'RUNONCE'},
    'resultContainerMountPoint': '/result',
    'workspaceMounts': [
    ],
    'datasetMounts': [
    ],
}

def parse_all(cfg):
    if cfg.img is not None:
        job_cfg['dockerImageName'] = cfg.img
    if cfg.name is not None:
        job_cfg['name'] = "ml-model.qsh_debug."+cfg.name
    else:
        job_cfg['name'] = f"ml-model.qsh_debug.{cfg.device}"
    parse_device(cfg)
    parse_cmd(cfg)
    parse_ws_qsh(cfg)
    parse_extra_ws(cfg)
    parse_dataset(cfg)

def parse_device(cfg):
    if cfg.device is not None:
        cfg.device = str(cfg.device)
        if "x" in cfg.device:
            if cfg.device.count("x") == 1:
                num_node = 1
                gpu_mem = cfg.device.split("x")[0]
                gpu_per_node = int(cfg.device.split("x")[1])
            elif cfg.device.count("x") == 2:
                num_node = int(cfg.device.split("x")[0])
                gpu_mem = cfg.device.split("x")[1]
                gpu_per_node = int(cfg.device.split("x")[2])
            elif cfg.device.count("x") > 2:
                raise ValueError(f"device format error {cfg.device}")
        else:
            num_node = 1
            gpu_mem = cfg.device
            gpu_per_node = 1
        job_cfg["aceInstance"] = {
            "cpu": "cpu.x86.tiny",
            "16": f"dgx1v.16g.{gpu_per_node}.norm",
            "32": f"dgx1v.32g.{gpu_per_node}.norm",
            "32b": f"dgx1v.32g.{gpu_per_node}.norm.beta",
            "40": f"dgxa100.40g.{gpu_per_node}.norm",
            "40b": f"dgxa100.40g.{gpu_per_node}.norm",
            "40c": f"dgxa100.40g.{gpu_per_node}.norm",
            "48": f"ovxa40.48g.{gpu_per_node}",
            "80": f"dgxa100.80g.{gpu_per_node}.norm",
            "80b": f"dgxa100.80g.{gpu_per_node}.norm",
        }[str(gpu_mem)]

    else:
        num_node = 1
        gpu_mem = "cpu"
        gpu_per_node = 1

        job_cfg["aceInstance"] = "cpu.x86.tiny"
    job_cfg["minAvailability"] = job_cfg["replicaCount"] = num_node

    job_ace = {
        "cpu": "nv-us-west-2",
        "16": "nv-us-west-2",
        "32": "nv-us-west-2",
        "32b": "nv-us-west-2",
        "40": "nv-us-east-1",
        "40b": "nv-us-west-2",
        "40c": "nv-us-west-2",
        "48": "ov-us-west-2",
        "80": "nv-us-east-1",
        "80b": "nv-us-west-3",
    }[str(gpu_mem)]

    job_team = "deep-imagination" if "dgxa100" in job_cfg["aceInstance"] else "lpr-imagine"
    if str(gpu_mem) == "40c":
        job_team = "lpr-imagine"
    job_cmd.append(
        f"--team {job_team} --ace {job_ace} --label qsh_debug --priority HIGH --order 1 --preempt RUNONCE"
    )

    cfg.job_ace = job_ace

def parse_cmd(cfg):
    cmds = []
    if cfg.ws_qsh:
        cmds.append("cd /mnt/qsh_ws")
    if cfg.cmd is not None:
        cmd = cfg.cmd
        if type(cmd) is str:
            cmd = [cmd]
        cmds.extend(cmd)
    if cfg.debug:
        cmds.append("tmux new-session -d -s dv \"nvitop\"; sleep 7d")
    job_cfg['command'] = ";".join(cmds)


def parse_ws_qsh(cfg):
    if cfg.key_qsh:
        keys_ws = {
            'nv-us-east-1': 'qsh_keys1',
            'nv-us-west-2': 'qsh_keys',
            'nv-us-west-3': 'qsh_keys3',
        }[cfg.job_ace]
        job_cfg['workspaceMounts'].append({
            "containerMountPoint": "/mnt/qsh_keys",
            "id": keys_ws,
            "mountMode": "RW"
        })
    if cfg.ws_qsh:
        ws = {
            'nv-us-east-1': 'qsh_ws_e1',
            'nv-us-west-2': 'qsh_ws',
            'nv-us-west-3': 'qsh_ws_w3',
        }[cfg.job_ace]
        job_cfg['workspaceMounts'].append({
            "containerMountPoint": "/mnt/qsh_ws",
            "id": ws,
            "mountMode": "RW"
        })

def parse_extra_ws(cfg):
    if cfg.extra_ws is not None:
        for ws, target_loc in cfg.extra_ws.items():
            job_cfg['workspaceMounts'].append({
                "containerMountPoint": target_loc,
                "id": ws,
                "mountMode": "RW"
            })

def parse_dataset(cfg):
    if cfg.dataset is not None:
        for dataset_id, target_loc in cfg.dataset.items():
            job_cfg['datasetMounts'].append({
                "containerMountPoint": target_loc,
                "id": dataset_id,
            })

def read_local_cfg(cfg):
    cfg_path = hydra.utils.to_absolute_path(cfg.file)
    if not osp.exists(cfg_path):
        return cfg
    logger.info("readding config from: " + cfg_path)
    local_cfg = OmegaConf.load(cfg_path)
    cli_cfg = OmegaConf.from_cli()
    cfg = OmegaConf.merge(cfg, local_cfg, cli_cfg)
    return cfg

@hydra.main(config_path="conf", config_name="ngc", version_base="1.1.0")
def my_app(cfg: DictConfig) -> None:
    OmegaConf.set_struct(cfg, False)
    cfg = read_local_cfg(cfg)
    parse_all(cfg)

    job_cfg, job_cmd
    job_name = job_cfg["name"]
    json_fname = f"/tmp/{job_name}.json"
    os.makedirs(os.path.dirname(json_fname), exist_ok=True)
    with open(json_fname, "w") as file:
        json.dump(job_cfg, file, indent=4)

    system_cmd = f"ngc batch run -f {json_fname} " + " ".join(job_cmd)
    logger.info(system_cmd)
    is_submit = cfg.submit
    if not is_submit and cfg.debug:
        is_submit = yes_or_no("submit job?", default="yes")
    if is_submit:
        stdout, stderr = run_simple_command(system_cmd)
        if not stderr:
            if cfg.debug and cfg.exec:
                id_info = stdout.split('\n')[2]
                job_id = id_info.split(' ')[-1]
                logger.warning(f"ngc batch exec {job_id}")
                while True:
                    rtn_value = os.system(f"ngc batch exec {job_id}")
                    if rtn_value != 0:
                        logger.warning(f"ERROR VALUE {rtn_value}: ngc batch exec {job_id} failed, retrying...")
                        time.sleep(5)
                    else:
                        break
        if stderr:
            print(stderr)


if __name__ == "__main__":
    my_app()  # pylint: disable=no-value-for-parameter
