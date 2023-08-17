"""
This module provides the DummyPackageTester class for testing the DummyPackage class.
"""

import os.path
from dummy_package_manager import DummyPackage


class DummyPackageTester(DummyPackage):
    """
    A class for testing the DummyPackage class and its functionality.
    """

    def install_tester(self):
        """
        Tester function for DummyPackage.install.
        """
        self.install()

    def uninstall_tester(self):
        """
        Tester function for DummyPackage.uninstall.
        Tester function for DummyPackage.uninstall.
        """
        self.uninstall()


def __exit___tester(tester):
    """
    Verify the cleanup of the package's temporary directory and its module(s) after exiting the context.

    Args:
        tester (DummyPackageTester): The DummyPackageTester instance representing the package tester to be verified.

    Returns:
        bool: True if the package's temporary directory and module(s) are cleaned up, False otherwise.
    """
    is_path = os.path.exists(tester.temp_dir)
    is_module = tester.package["is_installed"] and all(dep["is_installed"] for dep in tester.package["deps"])
    return not is_path and not is_module
