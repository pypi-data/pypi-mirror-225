import os
import shutil
import subprocess
import unittest

from brik.app import App
from brik.brik import Brik
from brik.exceptions import InvalidRemoteException
from brik.utils import is_valid_criscostack_branch


class TestUtils(unittest.TestCase):
	def test_app_utils(self):
		git_url = "https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack"
		branch = "develop"
		app = App(name=git_url, branch=branch, brik=Brik("."))
		self.assertTrue(
			all(
				[
					app.name == git_url,
					app.branch == branch,
					app.tag == branch,
					app.is_url is True,
					app.on_disk is False,
					app.org == "criscostack",
					app.url == git_url,
				]
			)
		)

	def test_is_valid_criscostack_branch(self):
		with self.assertRaises(InvalidRemoteException):
			is_valid_criscostack_branch(
				"https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack.git", criscostack_branch="random-branch"
			)
			is_valid_criscostack_branch(
				"https://github.com/random/random.git", criscostack_branch="random-branch"
			)

		is_valid_criscostack_branch(
			"https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack.git", criscostack_branch="develop"
		)
		is_valid_criscostack_branch(
			"https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack.git", criscostack_branch="v13.29.0"
		)

	def test_app_states(self):
		brik_dir = "./sandbox"
		sites_dir = os.path.join(brik_dir, "sites")

		if not os.path.exists(sites_dir):
			os.makedirs(sites_dir)

		fake_brik = Brik(brik_dir)

		self.assertTrue(hasattr(fake_brik.apps, "states"))

		fake_brik.apps.states = {
			"criscostack": {
				"resolution": {"branch": "develop", "commit_hash": "234rwefd"},
				"version": "14.0.0-dev",
			}
		}
		fake_brik.apps.update_apps_states()

		self.assertEqual(fake_brik.apps.states, {})

		criscostack_path = os.path.join(brik_dir, "apps", "criscostack")

		os.makedirs(os.path.join(criscostack_path, "criscostack"))

		subprocess.run(["git", "init"], cwd=criscostack_path, capture_output=True, check=True)

		with open(os.path.join(criscostack_path, "criscostack", "__init__.py"), "w+") as f:
			f.write("__version__ = '11.0'")

		subprocess.run(["git", "add", "."], cwd=criscostack_path, capture_output=True, check=True)
		subprocess.run(
			["git", "config", "user.email", "brik-test_app_states@gha.com"],
			cwd=criscostack_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "config", "user.name", "App States Test"],
			cwd=criscostack_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "commit", "-m", "temp"], cwd=criscostack_path, capture_output=True, check=True
		)

		fake_brik.apps.update_apps_states(app_name="criscostack")

		self.assertIn("criscostack", fake_brik.apps.states)
		self.assertIn("version", fake_brik.apps.states["criscostack"])
		self.assertEqual("11.0", fake_brik.apps.states["criscostack"]["version"])

		shutil.rmtree(brik_dir)

	def test_ssh_ports(self):
		app = App("git@github.com:22:criscostack/criscostack")
		self.assertEqual(
			(app.use_ssh, app.org, app.repo, app.app_name), (True, "criscostack", "criscostack", "criscostack")
		)
