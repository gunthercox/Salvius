"""
Utils for automatically checking PyPi for Python package updates
and installing them if they exist.
"""

from os import environ
import logging
import pkg_resources
import pip


class PythonPackage(object):
    """
    An object with utility methods for obtaining information for a Python package.
    """

    logger = logging.getLogger(__name__)

    class PackageNotFoundException(Exception):
        """
        Exception raised when a package can not be found.
        """
        pass

    @classmethod
    def versions(cls, name):
        """
        Return a list of versions for a given package.
        """
        import requests

        url = 'https://pypi.python.org/pypi/{}/json'.format(name)
        response = requests.get(url)

        if response.status_code != 200:
            raise cls.PackageNotFoundException

        data = response.json()
        return sorted(data['releases'], key=pkg_resources.parse_version)

    @classmethod
    def latest_version(cls, name):
        """
        Return the latest version of a given Python Package.
        """
        versions = cls.versions(name)

        if len(versions) == 0:
            return -1

        return pkg_resources.parse_version(versions[-1])

    @classmethod
    def installed_version(cls, name):
        """
        Return the version of a locally installed package.
        """
        try:
            version = pkg_resources.get_distribution(name).version
        except pkg_resources.DistributionNotFound:
            return -1

        return pkg_resources.parse_version(version)

    @classmethod
    def upgrade(cls, name):
        """
        Upgrade the specified package.
        Returns true if the upgrade was sucessful.
        """
        cls.logger.info('Upgrading %s', name)

        pip_args = []

        # Check if a proxy is being used
        proxy = environ.get('http_proxy')
        if proxy:
            pip_args.extend(('--proxy', proxy, ))

        # Append multiple arguments to the pip args
        pip_args.extend(('install', name, '--upgrade', ))

        try:
            success = pip.main(args=pip_args)
        except TypeError:
            # As of pip version 0.6.0, initial_args changed to args
            success = pip.main(initial_args=pip_args)

        return success == 0

    @classmethod
    def has_updates(cls, name):
        """
        Check if a newer version exists on PyPi for a package.
        """
        try:
            current = cls.installed_version(name)
        except cls.PackageNotFoundException:
            cls.logger.info('The package %s is not currently installed.', name)
            return True

        try:
            latest = cls.latest_version(name)
        except cls.PackageNotFoundException:
            cls.logger.info('The package %s could not be found.', name)
            return False

        return latest > current

    @classmethod
    def upgrade_to_latest(cls, name):
        """
        Upgrade the package if there is a newer version available.
        """
        if cls.has_updates(name):
            cls.upgrade(name)
