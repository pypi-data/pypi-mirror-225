# imports - standard imports
import getpass
import os

# imports - third partyimports
import click

# imports - module imports
import brik
from brik.app import use_rq
from brik.brik import Brik
from brik.config.common_site_config import (
	get_gunicorn_workers,
	update_config,
	get_default_max_requests,
	compute_max_requests_jitter,
)
from brik.utils import exec_cmd, which, get_brik_name


def generate_systemd_config(
	brik_path,
	user=None,
	yes=False,
	stop=False,
	create_symlinks=False,
	delete_symlinks=False,
):

	if not user:
		user = getpass.getuser()

	config = Brik(brik_path).conf

	brik_dir = os.path.abspath(brik_path)
	brik_name = get_brik_name(brik_path)

	if stop:
		exec_cmd(
			f"sudo systemctl stop -- $(systemctl show -p Requires {brik_name}.target | cut -d= -f2)"
		)
		return

	if create_symlinks:
		_create_symlinks(brik_path)
		return

	if delete_symlinks:
		_delete_symlinks(brik_path)
		return

	number_of_workers = config.get("background_workers") or 1
	background_workers = []
	for i in range(number_of_workers):
		background_workers.append(
			get_brik_name(brik_path) + "-criscostack-default-worker@" + str(i + 1) + ".service"
		)

	for i in range(number_of_workers):
		background_workers.append(
			get_brik_name(brik_path) + "-criscostack-short-worker@" + str(i + 1) + ".service"
		)

	for i in range(number_of_workers):
		background_workers.append(
			get_brik_name(brik_path) + "-criscostack-long-worker@" + str(i + 1) + ".service"
		)

	web_worker_count = config.get(
		"gunicorn_workers", get_gunicorn_workers()["gunicorn_workers"]
	)
	max_requests = config.get(
		"gunicorn_max_requests", get_default_max_requests(web_worker_count)
	)

	brik_info = {
		"brik_dir": brik_dir,
		"sites_dir": os.path.join(brik_dir, "sites"),
		"user": user,
		"use_rq": use_rq(brik_path),
		"http_timeout": config.get("http_timeout", 120),
		"redis_server": which("redis-server"),
		"node": which("node") or which("nodejs"),
		"redis_cache_config": os.path.join(brik_dir, "config", "redis_cache.conf"),
		"redis_queue_config": os.path.join(brik_dir, "config", "redis_queue.conf"),
		"webserver_port": config.get("webserver_port", 8000),
		"gunicorn_workers": web_worker_count,
		"gunicorn_max_requests": max_requests,
		"gunicorn_max_requests_jitter": compute_max_requests_jitter(max_requests),
		"brik_name": get_brik_name(brik_path),
		"worker_target_wants": " ".join(background_workers),
		"brik_cmd": which("brik"),
	}

	if not yes:
		click.confirm(
			"current systemd configuration will be overwritten. Do you want to continue?",
			abort=True,
		)

	setup_systemd_directory(brik_path)
	setup_main_config(brik_info, brik_path)
	setup_workers_config(brik_info, brik_path)
	setup_web_config(brik_info, brik_path)
	setup_redis_config(brik_info, brik_path)

	update_config({"restart_systemd_on_update": False}, brik_path=brik_path)
	update_config({"restart_supervisor_on_update": False}, brik_path=brik_path)


def setup_systemd_directory(brik_path):
	if not os.path.exists(os.path.join(brik_path, "config", "systemd")):
		os.makedirs(os.path.join(brik_path, "config", "systemd"))


def setup_main_config(brik_info, brik_path):
	# Main config
	brik_template = brik.config.env().get_template("systemd/criscostack-brik.target")
	brik_config = brik_template.render(**brik_info)
	brik_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + ".target"
	)

	with open(brik_config_path, "w") as f:
		f.write(brik_config)


def setup_workers_config(brik_info, brik_path):
	# Worker Group
	brik_workers_target_template = brik.config.env().get_template(
		"systemd/criscostack-brik-workers.target"
	)
	brik_default_worker_template = brik.config.env().get_template(
		"systemd/criscostack-brik-criscostack-default-worker.service"
	)
	brik_short_worker_template = brik.config.env().get_template(
		"systemd/criscostack-brik-criscostack-short-worker.service"
	)
	brik_long_worker_template = brik.config.env().get_template(
		"systemd/criscostack-brik-criscostack-long-worker.service"
	)
	brik_schedule_worker_template = brik.config.env().get_template(
		"systemd/criscostack-brik-criscostack-schedule.service"
	)

	brik_workers_target_config = brik_workers_target_template.render(**brik_info)
	brik_default_worker_config = brik_default_worker_template.render(**brik_info)
	brik_short_worker_config = brik_short_worker_template.render(**brik_info)
	brik_long_worker_config = brik_long_worker_template.render(**brik_info)
	brik_schedule_worker_config = brik_schedule_worker_template.render(**brik_info)

	brik_workers_target_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + "-workers.target"
	)
	brik_default_worker_config_path = os.path.join(
		brik_path,
		"config",
		"systemd",
		brik_info.get("brik_name") + "-criscostack-default-worker@.service",
	)
	brik_short_worker_config_path = os.path.join(
		brik_path,
		"config",
		"systemd",
		brik_info.get("brik_name") + "-criscostack-short-worker@.service",
	)
	brik_long_worker_config_path = os.path.join(
		brik_path,
		"config",
		"systemd",
		brik_info.get("brik_name") + "-criscostack-long-worker@.service",
	)
	brik_schedule_worker_config_path = os.path.join(
		brik_path,
		"config",
		"systemd",
		brik_info.get("brik_name") + "-criscostack-schedule.service",
	)

	with open(brik_workers_target_config_path, "w") as f:
		f.write(brik_workers_target_config)

	with open(brik_default_worker_config_path, "w") as f:
		f.write(brik_default_worker_config)

	with open(brik_short_worker_config_path, "w") as f:
		f.write(brik_short_worker_config)

	with open(brik_long_worker_config_path, "w") as f:
		f.write(brik_long_worker_config)

	with open(brik_schedule_worker_config_path, "w") as f:
		f.write(brik_schedule_worker_config)


def setup_web_config(brik_info, brik_path):
	# Web Group
	brik_web_target_template = brik.config.env().get_template(
		"systemd/criscostack-brik-web.target"
	)
	brik_web_service_template = brik.config.env().get_template(
		"systemd/criscostack-brik-criscostack-web.service"
	)
	brik_node_socketio_template = brik.config.env().get_template(
		"systemd/criscostack-brik-node-socketio.service"
	)

	brik_web_target_config = brik_web_target_template.render(**brik_info)
	brik_web_service_config = brik_web_service_template.render(**brik_info)
	brik_node_socketio_config = brik_node_socketio_template.render(**brik_info)

	brik_web_target_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + "-web.target"
	)
	brik_web_service_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + "-criscostack-web.service"
	)
	brik_node_socketio_config_path = os.path.join(
		brik_path,
		"config",
		"systemd",
		brik_info.get("brik_name") + "-node-socketio.service",
	)

	with open(brik_web_target_config_path, "w") as f:
		f.write(brik_web_target_config)

	with open(brik_web_service_config_path, "w") as f:
		f.write(brik_web_service_config)

	with open(brik_node_socketio_config_path, "w") as f:
		f.write(brik_node_socketio_config)


def setup_redis_config(brik_info, brik_path):
	# Redis Group
	brik_redis_target_template = brik.config.env().get_template(
		"systemd/criscostack-brik-redis.target"
	)
	brik_redis_cache_template = brik.config.env().get_template(
		"systemd/criscostack-brik-redis-cache.service"
	)
	brik_redis_queue_template = brik.config.env().get_template(
		"systemd/criscostack-brik-redis-queue.service"
	)

	brik_redis_target_config = brik_redis_target_template.render(**brik_info)
	brik_redis_cache_config = brik_redis_cache_template.render(**brik_info)
	brik_redis_queue_config = brik_redis_queue_template.render(**brik_info)

	brik_redis_target_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + "-redis.target"
	)
	brik_redis_cache_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + "-redis-cache.service"
	)
	brik_redis_queue_config_path = os.path.join(
		brik_path, "config", "systemd", brik_info.get("brik_name") + "-redis-queue.service"
	)

	with open(brik_redis_target_config_path, "w") as f:
		f.write(brik_redis_target_config)

	with open(brik_redis_cache_config_path, "w") as f:
		f.write(brik_redis_cache_config)

	with open(brik_redis_queue_config_path, "w") as f:
		f.write(brik_redis_queue_config)


def _create_symlinks(brik_path):
	brik_dir = os.path.abspath(brik_path)
	etc_systemd_system = os.path.join("/", "etc", "systemd", "system")
	config_path = os.path.join(brik_dir, "config", "systemd")
	unit_files = get_unit_files(brik_dir)
	for unit_file in unit_files:
		filename = "".join(unit_file)
		exec_cmd(
			f'sudo ln -s {config_path}/{filename} {etc_systemd_system}/{"".join(unit_file)}'
		)
	exec_cmd("sudo systemctl daemon-reload")


def _delete_symlinks(brik_path):
	brik_dir = os.path.abspath(brik_path)
	etc_systemd_system = os.path.join("/", "etc", "systemd", "system")
	unit_files = get_unit_files(brik_dir)
	for unit_file in unit_files:
		exec_cmd(f'sudo rm {etc_systemd_system}/{"".join(unit_file)}')
	exec_cmd("sudo systemctl daemon-reload")


def get_unit_files(brik_path):
	brik_name = get_brik_name(brik_path)
	unit_files = [
		[brik_name, ".target"],
		[brik_name + "-workers", ".target"],
		[brik_name + "-web", ".target"],
		[brik_name + "-redis", ".target"],
		[brik_name + "-criscostack-default-worker@", ".service"],
		[brik_name + "-criscostack-short-worker@", ".service"],
		[brik_name + "-criscostack-long-worker@", ".service"],
		[brik_name + "-criscostack-schedule", ".service"],
		[brik_name + "-criscostack-web", ".service"],
		[brik_name + "-node-socketio", ".service"],
		[brik_name + "-redis-cache", ".service"],
		[brik_name + "-redis-queue", ".service"],
	]
	return unit_files
