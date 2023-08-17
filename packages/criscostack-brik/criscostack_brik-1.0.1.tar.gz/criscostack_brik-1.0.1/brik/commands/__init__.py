# imports - third party imports
import click

# imports - module imports
from brik.utils.cli import (
	MultiCommandGroup,
	print_brik_version,
	use_experimental_feature,
	setup_verbosity,
)


@click.group(cls=MultiCommandGroup)
@click.option(
	"--version",
	is_flag=True,
	is_eager=True,
	callback=print_brik_version,
	expose_value=False,
)
@click.option(
	"--use-feature",
	is_eager=True,
	callback=use_experimental_feature,
	expose_value=False,
)
@click.option(
	"-v",
	"--verbose",
	is_flag=True,
	callback=setup_verbosity,
	expose_value=False,
)
def brik_command(brik_path="."):
	import brik

	brik.set_criscostack_version(brik_path=brik_path)


from brik.commands.make import (
	drop,
	exclude_app_for_update,
	get_app,
	include_app_for_update,
	init,
	new_app,
	pip,
	remove_app,
)

brik_command.add_command(init)
brik_command.add_command(drop)
brik_command.add_command(get_app)
brik_command.add_command(new_app)
brik_command.add_command(remove_app)
brik_command.add_command(exclude_app_for_update)
brik_command.add_command(include_app_for_update)
brik_command.add_command(pip)


from brik.commands.update import (
	retry_upgrade,
	switch_to_branch,
	switch_to_develop,
	update,
)

brik_command.add_command(update)
brik_command.add_command(retry_upgrade)
brik_command.add_command(switch_to_branch)
brik_command.add_command(switch_to_develop)


from brik.commands.utils import (
	backup_all_sites,
	brik_src,
	disable_production,
	download_translations,
	find_brikes,
	migrate_env,
	renew_lets_encrypt,
	restart,
	set_mariadb_host,
	set_nginx_port,
	set_redis_cache_host,
	set_redis_queue_host,
	set_redis_socketio_host,
	set_ssl_certificate,
	set_ssl_certificate_key,
	set_url_root,
	start,
)

brik_command.add_command(start)
brik_command.add_command(restart)
brik_command.add_command(set_nginx_port)
brik_command.add_command(set_ssl_certificate)
brik_command.add_command(set_ssl_certificate_key)
brik_command.add_command(set_url_root)
brik_command.add_command(set_mariadb_host)
brik_command.add_command(set_redis_cache_host)
brik_command.add_command(set_redis_queue_host)
brik_command.add_command(set_redis_socketio_host)
brik_command.add_command(download_translations)
brik_command.add_command(backup_all_sites)
brik_command.add_command(renew_lets_encrypt)
brik_command.add_command(disable_production)
brik_command.add_command(brik_src)
brik_command.add_command(find_brikes)
brik_command.add_command(migrate_env)

from brik.commands.setup import setup

brik_command.add_command(setup)


from brik.commands.config import config

brik_command.add_command(config)

from brik.commands.git import remote_reset_url, remote_set_url, remote_urls

brik_command.add_command(remote_set_url)
brik_command.add_command(remote_reset_url)
brik_command.add_command(remote_urls)

from brik.commands.install import install

brik_command.add_command(install)
