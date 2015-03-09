import hashlib
import inspect
import os.path

class BaseConfig(object):
    """Sets base options for all configuration objects."""
    PROJECT_NAME = 'Letter Bucket'
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(inspect.stack()[0][1])))

    md5 = hashlib.md5()
    md5.update(PROJECT_NAME)
    SECRET_KEY = md5.hexdigest()
    del md5

    @classmethod
    def GetFileSystemPath(cls, name, *paths):
        """Provides the full path to a file in the application.

        This method prevents other classes from needing to import os.path.

        Arguments:
            name: the name of the file or directory whose path is desired.
            paths: one or more path components relative to the application root.

        Returns:
            A string representation of the path to name.
        """
        parts = list(paths)
        parts.append(name)
        return os.path.join(cls.PROJECT_ROOT, *parts)

    @classmethod
    def Initialize(cls):
        """Perform any necssary set-up before the config class is to be used.

        In general, this should be overridden by cconfigs which need to perform
        some code operations before use.
        """
        pass
