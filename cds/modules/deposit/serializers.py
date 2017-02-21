# -*- coding: utf-8 -*-
#
# This file is part of CDS.
# Copyright (C) 2017 CERN.
#
# CDS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CDS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CDS. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Serializer for deposits that resolves video $references."""

from __future__ import absolute_import, print_function

from cds.modules.deposit.links import video_links_factory
from invenio_records_rest.serializers import JSONSerializer
from invenio_records_rest.serializers import RecordSchemaJSONV1
from invenio_records_rest.serializers import search_responsify

from cds.modules.deposit.api import record_unbuild_url, video_resolver


class ResolveRefSerializer(JSONSerializer):
    """Serializer for deposits that resolves video $references."""

    def transform_search_hit(self, pid, record_hit, links_factory=None):
        """Transform search result hit to resolve references."""
        json = super(ResolveRefSerializer, self)\
            .transform_search_hit(pid, record_hit, links_factory)
        videos_json = json['metadata'].get('videos')
        if videos_json:
            videos_refs = [record_unbuild_url(video['$reference'])
                           for video in videos_json]
            videos_serialized = [
                self.transform_record(video.pid, video,
                                      links_factory=video_links_factory)
                for video in video_resolver(videos_refs)]
            json['metadata']['videos'] = videos_serialized
        return json


json_v1 = ResolveRefSerializer(RecordSchemaJSONV1)
json_v1_search = search_responsify(json_v1, 'application/json')
