# Copyright 2023 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

from asyncio import Queue
from asyncio import QueueEmpty
import os
from pathlib import Path
import platform
from random import shuffle

from colcon_core.plugin_system import satisfies_version
from colcon_core.plugin_system import SkipExtensionException
from colcon_core.shell import logger
from colcon_core.shell import ShellExtensionPoint


class ROSDomainIDShell(ShellExtensionPoint):
    """Set a different ROS_DOMAIN_ID environment variable for each task."""

    # The priority should be higher than any usable shells
    PRIORITY = 900

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(ShellExtensionPoint.EXTENSION_POINT_VERSION, '^2.2')

        self.free_ids = Queue()

        all_ids = []
        system = platform.system()

        # TODO(cottsay): Determine usable IDs based on the system's
        #                network configuration
        if system in ('Darwin', 'Windows'):
            all_ids.extend(range(1, 167))
        else:
            all_ids.extend(range(1, 102))
            all_ids.extend(range(215, 233))

        shuffle(all_ids)
        for i in all_ids:
            self.free_ids.put_nowait(str(i))

    def get_file_extensions(self):  # noqa: D102
        return ()

    def create_prefix_script(self, prefix_path, merge_install):  # noqa: D102
        return []

    def create_package_script(  # noqa: D102
        self, prefix_path, pkg_name, hooks
    ):
        return []

    def create_hook_set_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, value,
    ):
        return Path('ros_domain_id.txt')

    def create_hook_append_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, subdirectory,
    ):
        return Path('ros_domain_id.txt')

    def create_hook_prepend_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, subdirectory,
    ):
        return Path('ros_domain_id.txt')

    async def generate_command_environment(  # noqa: D102
        self, task_name, build_base, dependencies,
    ):
        try:
            domain_id = self.free_ids.get_nowait()
        except QueueEmpty:
            logger.warn(f"No free ROS_DOMAIN_ID to assign for '{task_name}'")
            os.environ.pop('ROS_DOMAIN_ID', None)
            domain_id = None
        else:
            os.environ['ROS_DOMAIN_ID'] = domain_id
            logger.debug(
                f"Allocated ROS_DOMAIN_ID={domain_id} for '{task_name}'")

            # Place the ID at the end of the FIFO to be reused if needed
            self.free_ids.put_nowait(domain_id)

        # This extension can't actually perform command environment generation
        raise SkipExtensionException()
