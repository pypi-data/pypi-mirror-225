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

from typing import Union

from ory.components.pod import Pod
from ory.ext.exceptions import PodAlreadyExistsException, PriorityAlreadyExistsException, PermissionException
from ory.states.permission import Permission


class Pool:
    """
    A pool is a collection of pods that are registered to a specific conditions.
    """

    def __init__(self, name: str, permission: Permission, priority: int = 0) -> None:
        self.__name = name.lower()
        self.__permission = permission
        self.__priority = priority

        self.__pods = dict()

    def get_name(self) -> str:
        """
        Gets the name of the pool
        :return: name of the pool
        """

        return self.__name

    def get_permission(self) -> Permission:
        """
        Gets the permission of the pool
        :return: permission of the pool
        """

        return self.__permission

    def get_priority(self) -> int:
        """
        Gets the priority of the pool
        :return: priority of the pool
        """

        return self.__priority

    def register_pod(self, pod: Pod, override: bool = False) -> None:
        """
        Registers a pod to the pool
        :param pod: The pod to register
        :param override: If the pod should override an existing pod
        :return: None
        """

        if pod.get_name() in self.__pods and not override:
            raise PodAlreadyExistsException("Pod already registered")

        for registered_pod in self.__pods.values():
            if pod.get_priority() == registered_pod.get_priority() and pod.get_priority() != 0:
                raise PriorityAlreadyExistsException("Priority already exists")

            if pod.get_name() == registered_pod.get_name():
                raise PodAlreadyExistsException("Name already registered")

        if override and self.__permission == Permission.READ_ONLY:
            raise PermissionException("This pool is read only")

        self.__pods[pod.get_name()] = pod

    def register_pods(self, pods: list[Pod], override: bool = False) -> None:
        """
        Registers multiple pods to the pool
        :param pods: The pods to register
        :param override: If the pods should override an existing pod
        :return: None
        """

        for pod in pods:
            self.register_pod(pod, override)

    def unregister_pod(self, pod: Pod) -> None:
        """
        Unregisters a pod from the pool
        :param pod: The pod to unregister
        :return: None
        """

        if pod.get_name() not in self.__pods:
            raise PodAlreadyExistsException("Pod already registered")

        if self.__permission == Permission.READ_ONLY:
            raise PermissionException("This pool is read only")

        del self.__pods[pod.get_name()]

    def unregister_pods(self, pods: list[Pod]) -> None:
        """
        Unregisters multiple pods from the pool
        :param pods: The pods to unregister
        :return: None
        """

        for pod in pods:
            self.unregister_pod(pod)

    def get_all_pods(self) -> list:
        """
        Gets the pods of the pool
        :return: pods of the pool
        """

        return list(self.__pods.values())

    def get_pod_by_name(self, name: str) -> Union[Pod, None]:
        """
        Gets a pod by its name.
        :param name: name of the pod.
        :return: Union[Pod, None]
        """

        for pod in self.__pods.values():
            if pod.get_name() == name.lower():
                return pod

        return None

    def get_pod_by_priority(self, priority: int) -> Union[list[Pod], Pod, None]:
        """
        Gets a pod by its priority.
        :param priority: priority of the pod.
        :return: pod with the given priority.
        """

        if priority == 0:
            return [pod for pod in self.__pods.values() if pod.get_priority() == 0]

        for pod in self.__pods.values():
            if pod.get_priority() == priority:
                return pod

        return None

    def get_standard_pods(self) -> list[Pod]:
        """
        Gets all pods that are not prioritized.
        :return: list[Pod]
        """

        return [pod for pod in self.__pods.values() if pod.get_priority() == 0]
