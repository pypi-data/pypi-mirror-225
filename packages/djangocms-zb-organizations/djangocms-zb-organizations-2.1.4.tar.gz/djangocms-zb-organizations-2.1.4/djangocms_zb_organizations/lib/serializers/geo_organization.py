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
# Date: 11/10/2022 7:16 a. m.
# Project: Djangocms-pruebas
# Module Name: geo_organization
# ****************************************************************

from rest_framework_gis import serializers

from djangocms_zb_organizations.models import GeoOrganization
from rest_framework import serializers as rfserializers


class GeoOrganizationSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = GeoOrganization
        fields = "__all__"
        geo_field = "polygon"



class GeoSubregionSerializer(rfserializers.ModelSerializer):
    nuclear_coordinate = rfserializers.SerializerMethodField(default=[])
    name = rfserializers.SerializerMethodField(default="")
    organization_code = rfserializers.SerializerMethodField()
    @staticmethod
    def get_name(instance):
            return instance.organization.name

    @staticmethod
    def get_organization_code(instance):
        return instance.organization.id

    @staticmethod
    def get_nuclear_coordinate(instance):
        nuclear_coordinate = {
            "type": "Point",
            "coordinates": [
                instance.organization.latitude,
                instance.organization.longitude
            ]
        }

        return nuclear_coordinate

    class Meta:
        model = GeoOrganization
        fields = ["organization_code", "name", "nuclear_coordinate", "polygon"]
