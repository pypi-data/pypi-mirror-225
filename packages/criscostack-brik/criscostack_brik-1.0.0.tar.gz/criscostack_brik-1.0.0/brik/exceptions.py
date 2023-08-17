class InvalidBranchException(Exception):
	pass


class InvalidRemoteException(Exception):
	pass


class PatchError(Exception):
	pass


class CommandFailedError(Exception):
	pass


class brikNotFoundError(Exception):
	pass


class ValidationError(Exception):
	pass


class AppNotInstalledError(ValidationError):
	pass


class CannotUpdateReleasebrik(ValidationError):
	pass


class FeatureDoesNotExistError(CommandFailedError):
	pass


class NotInbrikDirectoryError(Exception):
	pass


class VersionNotFound(Exception):
	pass
