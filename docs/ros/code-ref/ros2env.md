# ROS2 환경설정

ROS2 환경 설정 도구


[View full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/ros2env/){ .md-button }

#### `ros2env/ros2env/__init__.py`

```python

```

#### `ros2env/ros2env/verb/__init__.py`

```python
from ros2cli.plugin_system import PLUGIN_SYSTEM_VERSION
from ros2cli.plugin_system import satisfies_version


class VerbExtension:
    """
    The extension point for 'env' verb extensions.

    The following properties must be defined:
    * `NAME` (will be set to the entry point name)

    The following methods must be defined:
    * `main`

    The following methods can be defined:
    * `add_arguments`
    """

    NAME = None
    EXTENSION_POINT_VERSION = "0.1"

    def __init__(self):
        super(VerbExtension, self).__init__()
        satisfies_version(PLUGIN_SYSTEM_VERSION, "^0.1")

    def add_arguments(self, parser, cli_name):
        pass

    def main(self, *, args):
        raise NotImplementedError()

```

#### `ros2env/ros2env/command/__init__.py`

```python

```

#### `ros2env/ros2env/api/__init__.py`

```python
import os


def get_ros_env_list():
    ros_version = os.getenv("ROS_VERSION", "None")
    ros_distro = os.getenv("ROS_DISTRO", "None")
    ros_python_version = os.getenv("ROS_PYTHON_VERSION", "None")
    ros_env_list = "ROS_VERSION        = {0}\n\
ROS_DISTRO         = {1}\n\
ROS_PYTHON_VERSION = {2}\n".format(
        ros_version, ros_distro, ros_python_version
    )
    return ros_env_list


def get_dds_env_list():
    ros_domain_id = os.getenv("ROS_DOMAIN_ID", "None")
    rmw_implementation = os.getenv("RMW_IMPLEMENTATION", "None")
    dds_env_list = "ROS_DOMAIN_ID      = {0}\n\
RMW_IMPLEMENTATION = {1}\n".format(
        ros_domain_id, rmw_implementation
    )
    return dds_env_list


def get_all_env_list():
    ros_env_list = get_ros_env_list()
    dds_env_list = get_dds_env_list()
    all_env_list = ros_env_list + dds_env_list
    return all_env_list


def set_ros_env(env_name, env_value):
    os.environ[env_name] = env_value
    value = os.getenv(env_name, "None")
    return "{0} = {1}".format(env_name, value)

```

#### `ros2env/ros2env/command/env.py`

```python
from ros2cli.command import add_subparsers_on_demand
from ros2cli.command import CommandExtension


class EnvCommand(CommandExtension):
    """Various env related sub-commands."""

    def add_arguments(self, parser, cli_name):
        self._subparser = parser

        # add arguments and sub-commands of verbs
        add_subparsers_on_demand(
            parser, cli_name, "_verb", "ros2env.verb", required=False
        )

    def main(self, *, parser, args):
        if not hasattr(args, "_verb"):
            # in case no verb was passed
            self._subparser.print_help()
            return 0

        extension = getattr(args, "_verb")

        # call the verb's main method
        return extension.main(args=args)

```


*... and 4 more files. [See full source on GitHub](https://github.com/OWNER/study-site/tree/main/source/ros2env/)*
