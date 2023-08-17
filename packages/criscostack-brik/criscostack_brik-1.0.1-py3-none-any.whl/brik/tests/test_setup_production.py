# imports - standard imports
import getpass
import os
import pathlib
import re
import subprocess
import time
import unittest

# imports - module imports
from brik.utils import exec_cmd, get_cmd_output, which
from brik.config.production_setup import get_supervisor_confdir
from brik.tests.test_base import TestBrikBase


class TestSetupProduction(TestBrikBase):
	def test_setup_production(self):
		user = getpass.getuser()

		for brik_name in ("test-brik-1", "test-brik-2"):
			brik_path = os.path.join(os.path.abspath(self.brikes_path), brik_name)
			self.init_brik(brik_name)
			exec_cmd(f"sudo brik setup production {user} --yes", cwd=brik_path)
			self.assert_nginx_config(brik_name)
			self.assert_supervisor_config(brik_name)
			self.assert_supervisor_process(brik_name)

		self.assert_nginx_process()
		exec_cmd(f"sudo brik setup sudoers {user}")
		self.assert_sudoers(user)

		for brik_name in self.brikes:
			brik_path = os.path.join(os.path.abspath(self.brikes_path), brik_name)
			exec_cmd("sudo brik disable-production", cwd=brik_path)

	def production(self):
		try:
			self.test_setup_production()
		except Exception:
			print(self.get_traceback())

	def assert_nginx_config(self, brik_name):
		conf_src = os.path.join(
			os.path.abspath(self.brikes_path), brik_name, "config", "nginx.conf"
		)
		conf_dest = f"/etc/nginx/conf.d/{brik_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			for key in (
				f"upstream {brik_name}-criscostack",
				f"upstream {brik_name}-socketio-server",
			):
				self.assertTrue(key in f)

	def assert_nginx_process(self):
		out = get_cmd_output("sudo nginx -t 2>&1")
		self.assertTrue(
			"nginx: configuration file /etc/nginx/nginx.conf test is successful" in out
		)

	def assert_sudoers(self, user):
		sudoers_file = "/etc/sudoers.d/criscostack"
		service = which("service")
		nginx = which("nginx")

		self.assertTrue(self.file_exists(sudoers_file))

		if os.environ.get("CI"):
			sudoers = subprocess.check_output(["sudo", "cat", sudoers_file]).decode("utf-8")
		else:
			sudoers = pathlib.Path(sudoers_file).read_text()
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {service} nginx *" in sudoers)
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {nginx}" in sudoers)

	def assert_supervisor_config(self, brik_name, use_rq=True):
		conf_src = os.path.join(
			os.path.abspath(self.brikes_path), brik_name, "config", "supervisor.conf"
		)

		supervisor_conf_dir = get_supervisor_confdir()
		conf_dest = f"{supervisor_conf_dir}/{brik_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			tests = [
				f"program:{brik_name}-criscostack-web",
				f"program:{brik_name}-redis-cache",
				f"program:{brik_name}-redis-queue",
				f"group:{brik_name}-web",
				f"group:{brik_name}-workers",
				f"group:{brik_name}-redis",
			]

			if not os.environ.get("CI"):
				tests.append(f"program:{brik_name}-node-socketio")

			if use_rq:
				tests.extend(
					[
						f"program:{brik_name}-criscostack-schedule",
						f"program:{brik_name}-criscostack-default-worker",
						f"program:{brik_name}-criscostack-short-worker",
						f"program:{brik_name}-criscostack-long-worker",
					]
				)

			else:
				tests.extend(
					[
						f"program:{brik_name}-criscostack-workerbeat",
						f"program:{brik_name}-criscostack-worker",
						f"program:{brik_name}-criscostack-longjob-worker",
						f"program:{brik_name}-criscostack-async-worker",
					]
				)

			for key in tests:
				self.assertTrue(key in f)

	def assert_supervisor_process(self, brik_name, use_rq=True, disable_production=False):
		out = get_cmd_output("supervisorctl status")

		while "STARTING" in out:
			print("Waiting for all processes to start...")
			time.sleep(10)
			out = get_cmd_output("supervisorctl status")

		tests = [
			r"{brik_name}-web:{brik_name}-criscostack-web[\s]+RUNNING",
			# Have commented for the time being. Needs to be uncommented later on. Brik is failing on travis because of this.
			# It works on one brik and fails on another.giving FATAL or BACKOFF (Exited too quickly (process log may have details))
			# "{brik_name}-web:{brik_name}-node-socketio[\s]+RUNNING",
			r"{brik_name}-redis:{brik_name}-redis-cache[\s]+RUNNING",
			r"{brik_name}-redis:{brik_name}-redis-queue[\s]+RUNNING",
		]

		if use_rq:
			tests.extend(
				[
					r"{brik_name}-workers:{brik_name}-criscostack-schedule[\s]+RUNNING",
					r"{brik_name}-workers:{brik_name}-criscostack-default-worker-0[\s]+RUNNING",
					r"{brik_name}-workers:{brik_name}-criscostack-short-worker-0[\s]+RUNNING",
					r"{brik_name}-workers:{brik_name}-criscostack-long-worker-0[\s]+RUNNING",
				]
			)

		else:
			tests.extend(
				[
					r"{brik_name}-workers:{brik_name}-criscostack-workerbeat[\s]+RUNNING",
					r"{brik_name}-workers:{brik_name}-criscostack-worker[\s]+RUNNING",
					r"{brik_name}-workers:{brik_name}-criscostack-longjob-worker[\s]+RUNNING",
					r"{brik_name}-workers:{brik_name}-criscostack-async-worker[\s]+RUNNING",
				]
			)

		for key in tests:
			if disable_production:
				self.assertFalse(re.search(key, out))
			else:
				self.assertTrue(re.search(key, out))


if __name__ == "__main__":
	unittest.main()
