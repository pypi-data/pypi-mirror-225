VERSION = "1.0.0"
PROJECT_NAME = "criscostack-brik"
CRISCOSTACK_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []


def set_criscostack_version(brik_path="."):
	from .utils.app import get_current_criscostack_version

	global CRISCOSTACK_VERSION
	if not CRISCOSTACK_VERSION:
		CRISCOSTACK_VERSION = get_current_criscostack_version(brik_path=brik_path)
