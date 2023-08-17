# imports - standard imports
import json
import os
import subprocess
import unittest

# imports - third paty imports
import git

# imports - module imports
from brik.utils import exec_cmd
from brik.app import App
from brik.tests.test_base import CRISCOSTACK_BRANCH, TestBrikBase
from brik.brik import Brik


# changed from criscostack_theme because it wasn't maintained and incompatible,
# chat app & wiki was breaking too. hopefully criscostack_docs will be maintained
# for longer since docs.criscoerp.com is powered by it ;)
TEST_CRISCOSTACK_APP = "criscostack_docs"


class TestBrikInit(TestBrikBase):
	def test_utils(self):
		self.assertEqual(subprocess.call("brik"), 0)

	def test_init(self, brik_name="test-brik", **kwargs):
		self.init_brik(brik_name, **kwargs)
		app = App("file:///tmp/criscostack")
		self.assertTupleEqual(
			(app.mount_path, app.url, app.repo, app.app_name, app.org),
			("/tmp/criscostack", "file:///tmp/criscostack", "criscostack", "criscostack", "criscostack"),
		)
		self.assert_folders(brik_name)
		self.assert_virtual_env(brik_name)
		self.assert_config(brik_name)
		test_brik = Brik(brik_name)
		app = App("criscostack", brik=test_brik)
		self.assertEqual(app.from_apps, True)

	def basic(self):
		try:
			self.test_init()
		except Exception:
			print(self.get_traceback())

	def test_multiple_brikes(self):
		for brik_name in ("test-brik-1", "test-brik-2"):
			self.init_brik(brik_name, skip_assets=True)

		self.assert_common_site_config(
			"test-brik-1",
			{
				"webserver_port": 8000,
				"socketio_port": 9000,
				"file_watcher_port": 6787,
				"redis_queue": "redis://localhost:11000",
				"redis_socketio": "redis://localhost:13000",
				"redis_cache": "redis://localhost:13000",
			},
		)

		self.assert_common_site_config(
			"test-brik-2",
			{
				"webserver_port": 8001,
				"socketio_port": 9001,
				"file_watcher_port": 6788,
				"redis_queue": "redis://localhost:11001",
				"redis_socketio": "redis://localhost:13001",
				"redis_cache": "redis://localhost:13001",
			},
		)

	def test_new_site(self):
		brik_name = "test-brik"
		site_name = "test-site.local"
		brik_path = os.path.join(self.brikes_path, brik_name)
		site_path = os.path.join(brik_path, "sites", site_name)
		site_config_path = os.path.join(site_path, "site_config.json")

		self.init_brik(brik_name)
		self.new_site(site_name, brik_name)

		self.assertTrue(os.path.exists(site_path))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "backups")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "files")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "public", "files")))
		self.assertTrue(os.path.exists(site_config_path))

		with open(site_config_path) as f:
			site_config = json.loads(f.read())

			for key in ("db_name", "db_password"):
				self.assertTrue(key in site_config)
				self.assertTrue(site_config[key])

	def test_get_app(self):
		self.init_brik("test-brik", skip_assets=True)
		brik_path = os.path.join(self.brikes_path, "test-brik")
		exec_cmd(f"brik get-app {TEST_CRISCOSTACK_APP} --skip-assets", cwd=brik_path)
		self.assertTrue(os.path.exists(os.path.join(brik_path, "apps", TEST_CRISCOSTACK_APP)))
		app_installed_in_env = TEST_CRISCOSTACK_APP in subprocess.check_output(
			["brik", "pip", "freeze"], cwd=brik_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

	@unittest.skipIf(CRISCOSTACK_BRANCH != "develop", "only for develop branch")
	def test_get_app_resolve_deps(self):
		CRISCOSTACK_APP = "healthcare"
		self.init_brik("test-brik", skip_assets=True)
		brik_path = os.path.join(self.brikes_path, "test-brik")
		exec_cmd(f"brik get-app {CRISCOSTACK_APP} --resolve-deps --skip-assets", cwd=brik_path)
		self.assertTrue(os.path.exists(os.path.join(brik_path, "apps", CRISCOSTACK_APP)))

		states_path = os.path.join(brik_path, "sites", "apps.json")
		self.assertTrue(os.path.exists(states_path))

		with open(states_path) as f:
			states = json.load(f)

		self.assertTrue(CRISCOSTACK_APP in states)

	def test_install_app(self):
		brik_name = "test-brik"
		site_name = "install-app.test"
		brik_path = os.path.join(self.brikes_path, "test-brik")

		self.init_brik(brik_name, skip_assets=True)
		exec_cmd(
			f"brik get-app {TEST_CRISCOSTACK_APP} --branch master --skip-assets", cwd=brik_path
		)

		self.assertTrue(os.path.exists(os.path.join(brik_path, "apps", TEST_CRISCOSTACK_APP)))

		# check if app is installed
		app_installed_in_env = TEST_CRISCOSTACK_APP in subprocess.check_output(
			["brik", "pip", "freeze"], cwd=brik_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

		# create and install app on site
		self.new_site(site_name, brik_name)
		installed_app = not exec_cmd(
			f"brik --site {site_name} install-app {TEST_CRISCOSTACK_APP}",
			cwd=brik_path,
			_raise=False,
		)

		if installed_app:
			app_installed_on_site = subprocess.check_output(
				["brik", "--site", site_name, "list-apps"], cwd=brik_path
			).decode("utf8")
			self.assertTrue(TEST_CRISCOSTACK_APP in app_installed_on_site)

	def test_remove_app(self):
		self.init_brik("test-brik", skip_assets=True)
		brik_path = os.path.join(self.brikes_path, "test-brik")

		exec_cmd(
			f"brik get-app {TEST_CRISCOSTACK_APP} --branch master --overwrite --skip-assets",
			cwd=brik_path,
		)
		exec_cmd(f"brik remove-app {TEST_CRISCOSTACK_APP}", cwd=brik_path)

		with open(os.path.join(brik_path, "sites", "apps.txt")) as f:
			self.assertFalse(TEST_CRISCOSTACK_APP in f.read())
		self.assertFalse(
			TEST_CRISCOSTACK_APP
			in subprocess.check_output(["brik", "pip", "freeze"], cwd=brik_path).decode("utf8")
		)
		self.assertFalse(os.path.exists(os.path.join(brik_path, "apps", TEST_CRISCOSTACK_APP)))

	def test_switch_to_branch(self):
		self.init_brik("test-brik", skip_assets=True)
		brik_path = os.path.join(self.brikes_path, "test-brik")
		app_path = os.path.join(brik_path, "apps", "criscostack")

		# * chore: change to 14 when avalible
		prevoius_branch = "version-13"
		if CRISCOSTACK_BRANCH != "develop":
			# assuming we follow `version-#`
			prevoius_branch = f"version-{int(CRISCOSTACK_BRANCH.split('-')[1]) - 1}"

		successful_switch = not exec_cmd(
			f"brik switch-to-branch {prevoius_branch} criscostack --upgrade",
			cwd=brik_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(prevoius_branch, app_branch_after_switch)

		successful_switch = not exec_cmd(
			f"brik switch-to-branch {CRISCOSTACK_BRANCH} criscostack --upgrade",
			cwd=brik_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_second_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(CRISCOSTACK_BRANCH, app_branch_after_second_switch)


if __name__ == "__main__":
	unittest.main()
