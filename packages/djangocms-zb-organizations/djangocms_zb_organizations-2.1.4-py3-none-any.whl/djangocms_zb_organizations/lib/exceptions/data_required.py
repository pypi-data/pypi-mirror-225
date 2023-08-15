# -*- coding: utf-8 -*-

#  Copyright (C)  2022. CQ Inversiones SAS.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ****************************************************************
# IDE: PyCharm
# Developed by: JhonyAlexanderGonzal
# Date: 2/08/2023 1:06 p. m.
# Project: Djangocms-pruebas
# Module Name: data_required
# ****************************************************************

from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
class DataRequired(APIException):
    """Custom Exception"""
    status_code = 406
    default_detail = _("Data required at request not found.")
    default_code = 'Invalid_Data'