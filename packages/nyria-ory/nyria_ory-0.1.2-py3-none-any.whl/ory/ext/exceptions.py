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

class PermissionException(Exception):
    """
    This error is raised when the programm tries to change states it is not allowed to do
    """

    def __init__(self, message: str):
        super().__init__(message)


class PodAlreadyExistsException(Exception):
    """
    This error is raised when the programm tries to register a pod that already exists
    """

    def __init__(self, message: str):
        super().__init__(message)


class PriorityAlreadyExistsException(Exception):
    """
    This error is raised when the programm tries to register a pod that have the same priority
    """

    def __init__(self, message: str):
        super().__init__(message)


class PoolAlreadyExistsException(Exception):
    """
    This error is raised when the programm tries to register a pool that already exists
    """

    def __init__(self, message: str):
        super().__init__(message)
