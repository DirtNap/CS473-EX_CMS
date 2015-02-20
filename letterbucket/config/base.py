import inspect
import md5
import os.path

class BaseConfig(object):
    PROJECT_NAME = 'Letter Bucket'
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(inspect.stack()[0][1])))

    SECRET_KEY = str(md5.new(PROJECT_NAME))

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
