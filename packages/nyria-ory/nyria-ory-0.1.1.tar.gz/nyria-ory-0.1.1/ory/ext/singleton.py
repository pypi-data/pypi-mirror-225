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

class Singleton:
    """
    That class represents a singleton. Any class that inherits from this class will be a singleton.
    """

    _instance = None

    def __new__(cls, *args, **kwargs) -> object:
        """
        Creates a new instance of the class if it doesn't exist
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: Instance of the class
        """

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance
