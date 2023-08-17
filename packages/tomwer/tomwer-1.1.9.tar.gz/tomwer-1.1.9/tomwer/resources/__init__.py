# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


import os
import importlib
import sys

# pkg_resources is useful when this package is stored in a zip
# When pkg_resources is not available, the resources dir defaults to the
# directory containing this module.
try:
    import pkg_resources
except ImportError:
    pkg_resources = None

# For packaging purpose, patch this variable to use an alternative directory
# E.g., replace with _RESOURCES_DIR = '/usr/share/silx/data'
_RESOURCES_DIR = None

# For packaging purpose, patch this variable to use an alternative directory
# E.g., replace with _RESOURCES_DIR = '/usr/share/silx/doc'
# Not in use, uncomment when functionality is needed
# _RESOURCES_DOC_DIR = None

# cx_Freeze frozen support
# See http://cx-freeze.readthedocs.io/en/latest/faq.html#using-data-files
if getattr(sys, "frozen", False):
    # Running in a frozen application:
    # We expect resources to be located either in a silx/resources/ dir
    # relative to the executable or within this package.
    _dir = os.path.join(os.path.dirname(sys.executable), "tomwer", "resources")
    if os.path.isdir(_dir):
        _RESOURCES_DIR = _dir


class _ResourceDirectory(object):
    """Store a source of resources"""

    def __init__(self, package_name, package_path=None, forced_path=None):
        if forced_path is None:
            if package_path is None:
                if pkg_resources is None:
                    # In this case we have to compute the package path
                    # Else it will not be used
                    module = importlib.import_module(package_name)
                    package_path = os.path.abspath(os.path.dirname(module.__file__))
        self.package_name = package_name
        self.package_path = package_path
        self.forced_path = forced_path


_TOMWER_DIRECTORY = _ResourceDirectory(
    package_name=__name__,
    package_path=os.path.abspath(os.path.dirname(__file__)),
    forced_path=_RESOURCES_DIR,
)

_RESOURCE_DIRECTORIES = {}
_RESOURCE_DIRECTORIES["tomwer"] = _TOMWER_DIRECTORY


def _get_package_and_resource(resource, default_directory=None):
    """
    Return the resource directory class and a cleaned resource name without
    prefix.

    :param str: resource: Name of the resource with resource prefix.
    :param str default_directory: If the resource is not prefixed, the resource
        will be searched on this default directory of the silx resource
        directory.
    :rtype: tuple(_ResourceDirectory, str)
    :raises ValueError: If the resource name uses an unregistred resource
        directory name
    """
    if ":" in resource:
        prefix, resource = resource.split(":", 1)
    else:
        prefix = "tomwer"
        if default_directory is not None:
            resource = os.path.join(default_directory, resource)
    if prefix not in _RESOURCE_DIRECTORIES:
        raise ValueError("Resource '%s' uses an unregistred prefix", resource)
    resource_directory = _RESOURCE_DIRECTORIES[prefix]
    return resource_directory, resource


def _resource_filename(resource, default_directory=None):
    """Return filename corresponding to resource.

     The existence of the resource is not checked.

     The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
     directory "silx". See also :func:`register_resource_directory`.

     :param str resource: Resource path relative to resource directory
                         using '/' path separator. It can be either a file or
                          a directory.
     :param str default_directory: If the resource is not prefixed, the resource
         will be searched on this default directory of the silx resource
         directory. It should only be used internally by silx.
     :return: Absolute resource path in the file system
     :rtype: str
    """
    resource_directory, resource_name = _get_package_and_resource(
        resource, default_directory=default_directory
    )
    if resource_directory.forced_path is not None:
        # if set, use this directory
        base_dir = resource_directory.forced_path
        resource_path = os.path.join(base_dir, *resource_name.split("/"))
        return resource_path
    elif pkg_resources is None:
        # Fallback if pkg_resources is not available
        base_dir = resource_directory.package_path
        resource_path = os.path.join(base_dir, *resource_name.split("/"))
        return resource_path
    else:
        # Preferred way to get resources as it supports zipfile package
        package_name = resource_directory.package_name
        return pkg_resources.resource_filename(package_name, resource_name)
