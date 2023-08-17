# imports - standard imports
import getpass
import json
import os
import shutil
import subprocess
import sys
import traceback
import unittest

# imports - module imports
from brik.utils import paths_in_brik, exec_cmd
from brik.utils.system import init
from brik.brik import Brik

PYTHON_VER = sys.version_info

CRISCOSTACK_BRANCH = "version-13-hotfix"
if PYTHON_VER.major == 3:
	if PYTHON_VER.minor >= 10:
		CRISCOSTACK_BRANCH = "develop"


class TestBrikBase(unittest.TestCase):
	def setUp(self):
		self.brikes_path = "."
		self.brikes = []

	def tearDown(self):
		for brik_name in self.brikes:
			brik_path = os.path.join(self.brikes_path, brik_name)
			brik = Brik(brik_path)
			mariadb_password = (
				"travis"
				if os.environ.get("CI")
				else getpass.getpass(prompt="Enter MariaDB root Password: ")
			)

			if brik.exists:
				for site in brik.sites:
					subprocess.call(
						[
							"brik",
							"drop-site",
							site,
							"--force",
							"--no-backup",
							"--root-password",
							mariadb_password,
						],
						cwd=brik_path,
					)
				shutil.rmtree(brik_path, ignore_errors=True)

	def assert_folders(self, brik_name):
		for folder in paths_in_brik:
			self.assert_exists(brik_name, folder)
		self.assert_exists(brik_name, "apps", "criscostack")

	def assert_virtual_env(self, brik_name):
		brik_path = os.path.abspath(brik_name)
		python_path = os.path.abspath(os.path.join(brik_path, "env", "bin", "python"))
		self.assertTrue(python_path.startswith(brik_path))
		for subdir in ("bin", "lib", "share"):
			self.assert_exists(brik_name, "env", subdir)

	def assert_config(self, brik_name):
		for config, search_key in (
			("redis_queue.conf", "redis_queue.rdb"),
			("redis_cache.conf", "redis_cache.rdb"),
		):

			self.assert_exists(brik_name, "config", config)

			with open(os.path.join(brik_name, "config", config)) as f:
				self.assertTrue(search_key in f.read())

	def assert_common_site_config(self, brik_name, expected_config):
		common_site_config_path = os.path.join(
			self.brikes_path, brik_name, "sites", "common_site_config.json"
		)
		self.assertTrue(os.path.exists(common_site_config_path))

		with open(common_site_config_path) as f:
			config = json.load(f)

		for key, value in list(expected_config.items()):
			self.assertEqual(config.get(key), value)

	def assert_exists(self, *args):
		self.assertTrue(os.path.exists(os.path.join(*args)))

	def new_site(self, site_name, brik_name):
		new_site_cmd = ["brik", "new-site", site_name, "--admin-password", "admin"]

		if os.environ.get("CI"):
			new_site_cmd.extend(["--mariadb-root-password", "travis"])

		subprocess.call(new_site_cmd, cwd=os.path.join(self.brikes_path, brik_name))

	def init_brik(self, brik_name, **kwargs):
		self.brikes.append(brik_name)
		criscostack_tmp_path = "/tmp/criscostack"

		if not os.path.exists(criscostack_tmp_path):
			exec_cmd(
				f"git clone https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack -b {CRISCOSTACK_BRANCH} --depth 1 --origin upstream {criscostack_tmp_path}"
			)

		kwargs.update(
			dict(
				python=sys.executable,
				no_procfile=True,
				no_backups=True,
				criscostack_path=criscostack_tmp_path,
			)
		)

		if not os.path.exists(os.path.join(self.brikes_path, brik_name)):
			init(brik_name, **kwargs)
			exec_cmd(
				"git remote set-url upstream https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack",
				cwd=os.path.join(self.brikes_path, brik_name, "apps", "criscostack"),
			)

	def file_exists(self, path):
		if os.environ.get("CI"):
			return not subprocess.call(["sudo", "test", "-f", path])
		return os.path.isfile(path)

	def get_traceback(self):
		exc_type, exc_value, exc_tb = sys.exc_info()
		trace_list = traceback.format_exception(exc_type, exc_value, exc_tb)
		return "".join(str(t) for t in trace_list)
