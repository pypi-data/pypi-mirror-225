# imports - standard imports
import grp
import os
import pwd
import shutil
import sys

# imports - module imports
import brik
from brik.utils import (
	exec_cmd,
	get_process_manager,
	log,
	run_criscostack_cmd,
	sudoers_file,
	which,
	is_valid_criscostack_branch,
)
from brik.utils.brik import build_assets, clone_apps_from
from brik.utils.render import job


@job(title="Initializing Brik {path}", success="Brik {path} initialized")
def init(
	path,
	apps_path=None,
	no_procfile=False,
	no_backups=False,
	criscostack_path=None,
	criscostack_branch=None,
	verbose=False,
	clone_from=None,
	skip_redis_config_generation=False,
	clone_without_update=False,
	skip_assets=False,
	python="python3",
	install_app=None,
):
	"""Initialize a new brik directory

	* create a brik directory in the given path
	* setup logging for the brik
	* setup env for the brik
	* setup config (dir/pids/redis/procfile) for the brik
	* setup patches.txt for brik
	* clone & install criscostack
	        * install python & node dependencies
	        * build assets
	* setup backups crontab
	"""

	# Use print("\033c", end="") to clear entire screen after each step and re-render each list
	# another way => https://stackoverflow.com/a/44591228/10309266

	import brik.cli
	from brik.app import get_app, install_apps_from_path
	from brik.brik import Brik

	verbose = brik.cli.verbose or verbose

	brik = Brik(path)

	brik.setup.dirs()
	brik.setup.logging()
	brik.setup.env(python=python)
	brik.setup.config(redis=not skip_redis_config_generation, procfile=not no_procfile)
	brik.setup.patches()

	# local apps
	if clone_from:
		clone_apps_from(
			brik_path=path, clone_from=clone_from, update_app=not clone_without_update
		)

	# remote apps
	else:
		criscostack_path = criscostack_path or "https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack.git"
		is_valid_criscostack_branch(criscostack_path=criscostack_path, criscostack_branch=criscostack_branch)
		get_app(
			criscostack_path,
			branch=criscostack_branch,
			brik_path=path,
			skip_assets=True,
			verbose=verbose,
			resolve_deps=False,
		)

		# fetch remote apps using config file - deprecate this!
		if apps_path:
			install_apps_from_path(apps_path, brik_path=path)

	# getting app on brik init using --install-app
	if install_app:
		get_app(
			install_app,
			branch=criscostack_branch,
			brik_path=path,
			skip_assets=True,
			verbose=verbose,
			resolve_deps=False,
		)

	if not skip_assets:
		build_assets(brik_path=path)

	if not no_backups:
		brik.setup.backups()


def setup_sudoers(user):
	from brik.config.lets_encrypt import get_certbot_path

	if not os.path.exists("/etc/sudoers.d"):
		os.makedirs("/etc/sudoers.d")

		set_permissions = not os.path.exists("/etc/sudoers")
		with open("/etc/sudoers", "a") as f:
			f.write("\n#includedir /etc/sudoers.d\n")

		if set_permissions:
			os.chmod("/etc/sudoers", 0o440)

	template = brik.config.env().get_template("criscostack_sudoers")
	criscostack_sudoers = template.render(
		**{
			"user": user,
			"service": which("service"),
			"systemctl": which("systemctl"),
			"nginx": which("nginx"),
			"certbot": get_certbot_path(),
		}
	)

	with open(sudoers_file, "w") as f:
		f.write(criscostack_sudoers)

	os.chmod(sudoers_file, 0o440)
	log(f"Sudoers was set up for user {user}", level=1)


def start(no_dev=False, concurrency=None, procfile=None, no_prefix=False, procman=None):
	program = which(procman) if procman else get_process_manager()
	if not program:
		raise Exception("No process manager found")

	os.environ["PYTHONUNBUFFERED"] = "true"
	if not no_dev:
		os.environ["DEV_SERVER"] = "true"

	command = [program, "start"]
	if concurrency:
		command.extend(["-c", concurrency])

	if procfile:
		command.extend(["-f", procfile])

	if no_prefix:
		command.extend(["--no-prefix"])

	os.execv(program, command)


def migrate_site(site, brik_path="."):
	run_criscostack_cmd("--site", site, "migrate", brik_path=brik_path)


def backup_site(site, brik_path="."):
	run_criscostack_cmd("--site", site, "backup", brik_path=brik_path)


def backup_all_sites(brik_path="."):
	from brik.brik import Brik

	for site in Brik(brik_path).sites:
		backup_site(site, brik_path=brik_path)


def fix_prod_setup_perms(brik_path=".", criscostack_user=None):
	from glob import glob
	from brik.brik import Brik

	criscostack_user = criscostack_user or Brik(brik_path).conf.get("criscostack_user")

	if not criscostack_user:
		print("criscostack user not set")
		sys.exit(1)

	globs = ["logs/*", "config/*"]
	for glob_name in globs:
		for path in glob(glob_name):
			uid = pwd.getpwnam(criscostack_user).pw_uid
			gid = grp.getgrnam(criscostack_user).gr_gid
			os.chown(path, uid, gid)


def setup_fonts():
	fonts_path = os.path.join("/tmp", "fonts")

	if os.path.exists("/etc/fonts_backup"):
		return

	exec_cmd("git clone https://anikets_0612@bitbucket.org/criscoconsultingin/fonts.git", cwd="/tmp")
	os.rename("/etc/fonts", "/etc/fonts_backup")
	os.rename("/usr/share/fonts", "/usr/share/fonts_backup")
	os.rename(os.path.join(fonts_path, "etc_fonts"), "/etc/fonts")
	os.rename(os.path.join(fonts_path, "usr_share_fonts"), "/usr/share/fonts")
	shutil.rmtree(fonts_path)
	exec_cmd("fc-cache -fv")
