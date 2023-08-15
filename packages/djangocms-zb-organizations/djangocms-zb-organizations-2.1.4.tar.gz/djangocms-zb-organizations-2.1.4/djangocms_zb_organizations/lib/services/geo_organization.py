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
# Date: 2/08/2023 1:09 p. m.
# Project: Djangocms-pruebas
# Module Name: geo_organization
# ****************************************************************


from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from djangocms_zb_organizations.lib.exceptions import NotFound
from djangocms_zb_organizations.lib.exceptions import DataRequired

from djangocms_zb_organizations.models import GeoOrganization
from djangocms_zb_organizations.lib.serializers import GeoSubregionSerializer


class GeoOrganizationService(ModelViewSet):
    """
    Service class from operations Organization model
    """

    model_class = GeoOrganization
    permission_classes = [permissions.AllowAny]
    serializer_class = GeoSubregionSerializer

    def by_category(self, request, *args, **kwargs):
        """
        List of Organization in a category.

        Parameters
        ----------
        request: request from HTTP

        *args: Named args

        **kwargs: Dict Args

        Returns
        -------
        Response with a dataset with a list of organizations by category
        """
        try:
            request_data = request.data
            if "category_id" in request_data:
                queryset = self.model_class.objects.get_geo_organizations_by_category(request_data["category_id"])
                serializer = self.serializer_class(instance=queryset, many=True)
                data_return = serializer.data
                status_return = status.HTTP_200_OK if len(data_return) > 0 else status.HTTP_204_NO_CONTENT
                return Response(data=data_return, status=status_return)
            else:
                raise DataRequired()
        except DataRequired:
            raise DataRequired()
        except APIException as exc:
            raise APIException(msg=exc.detail.get("message"), error=exc.detail.get("detail"),
                               http_status=exc.status_code) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=data_return, status=status_return)
