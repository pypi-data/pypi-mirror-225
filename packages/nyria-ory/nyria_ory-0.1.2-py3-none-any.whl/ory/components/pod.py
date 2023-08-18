#  Copyright 2023 Nyria
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

from typing import Any

from ory.ext.exceptions import PermissionException
from ory.states.permission import Permission


class Pod:
    """
    This class represents a wrapper for class or functions. It stores the class/function and its arguments.
    """

    def __init__(self, name: str, instance: Any, permission: Permission, priority: int = 0) -> None:
        self.__name = name.lower()
        self.__instance = instance
        self.__permission = permission
        self.__priority = priority

    def get_name(self) -> str:
        """
        Gets the name of the pod
        :return: name of the pod
        """

        return self.__name

    def get_instance(self) -> Any:
        """
        Gets the stored callable instance
        :return:  of the pod
        """

        return self.__instance

    def get_permission(self) -> Permission:
        """
        Gets the permission of the pod
        :return: permission of the pod
        """

        return self.__permission

    def get_priority(self) -> int:
        """
        Gets the priority of the pod
        :return: priority of the pod
        """

        return self.__priority

    def set_new_instance(self, instance: Any) -> None:
        """
        Sets a new instance of the pod
        :param instance: new instance
        """

        if self.__permission != Permission.ALL:
            raise PermissionException("Cannot change instance of read only pod")

        self.__instance = instance

    def set_new_priority(self, priority: int) -> None:
        """
        Sets a new priority of the pod
        :param priority: new priority
        """

        if self.__permission == Permission.READ_ONLY:
            raise PermissionException("Cannot change priority of read only pod")

        self.__priority = priority

    def set_new_name(self, name: str) -> None:
        """
        Sets a new name of the pod
        :param name: new name
        """

        if self.__permission == Permission.READ_ONLY:
            raise PermissionException("Cannot change name of read only pod")

        self.__name = name
