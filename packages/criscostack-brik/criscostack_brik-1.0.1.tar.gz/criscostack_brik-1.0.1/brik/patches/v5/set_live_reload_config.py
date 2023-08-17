from brik.config.common_site_config import update_config


def execute(brik_path):
	update_config({"live_reload": True}, brik_path)
