# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

import collections
from string import Template

from bika.lims import _
from bika.lims import api
from bika.lims.api.security import check_permission
from bika.lims.config import PRIORITIES
from bika.lims.interfaces import IBatch, IClient
from bika.lims.utils import get_image, get_link_for, get_progress_bar_html, getUsers
from DateTime import DateTime
from plone.memoize import view
from senaite.app.listing import ListingView
from senaite.core.api import dtime
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.i18n import translate as t
from senaite.core.interfaces import ISamples, ISamplesView
from senaite.core.permissions import AddAnalysisRequest, TransitionSampleSample
from senaite.core.permissions.worksheet import can_add_worksheet
from zope.interface import implementer

ANALYSES_NUM_TPL = Template("$not_submitted/$to_be_verified/$verified/$total")

@implementer(ISamplesView)
class SamplesView(ListingView):

    def __init__(self, context, request):
        super(SamplesView, self).__init__(context, request)

        self.catalog = SAMPLE_CATALOG
        self.contentFilter = {
            "sort_on": "created",
            "sort_order": "descending",
            "isRootAncestor": True,
        }

        self.title = self.context.translate(_("Samples"))
        self.show_select_column = True
        self.form_id = "samples"
        self.context_actions = {}
        self.icon = "{}{}".format(self.portal_url, "/senaite_theme/icon/sample")
        self.url = api.get_url(self.context)

        sampling_enabled = api.get_setup().getSamplingWorkflowEnabled()
        now = DateTime().strftime("%Y-%m-%d %H:%M")

        self.columns = collections.OrderedDict((
            ("Priority", {"title": "", "index": "getPrioritySortkey"}),
            ("Progress", {"title": _("Progress"), "index": "getProgress"}),
            ("getId", {"title": _("Sample ID"), "attr": "getId", "replace_url": "getURL"}),
            ("Creator", {"title": _("Creator"), "index": "Creator"}),
            ("Created", {"title": _("Date Registered"), "index": "created"}),
            ("getDateSampled", {"title": _("Date Sampled"), "type": "datetime", "max": now}),
            ("Client", {"title": _("Client"), "index": "getClientTitle", "attr": "getClientTitle"}),
            ("getSampleTypeTitle", {"title": _("Sample Type")}),
            ("getAnalysesNum", {"title": _("Analyses")}),
            ("state_title", {"title": _("State"), "index": "review_state"}),
        ))

        self.review_states = [{
            "id": "default",
            "title": _("Active"),
            "contentFilter": {
                "review_state": (
                    "sample_received",
                    "to_be_verified",
                    "verified",
                ),
                "sort_on": "created",
                "sort_order": "descending",
            },
            "columns": self.columns.keys(),
        }]

    def update(self):
        super(SamplesView, self).update()
        self.workflow = api.get_tool("portal_workflow")
        self.member = self.mtool.getAuthenticatedMember()
        self.roles = self.member.getRoles()

    def folderitem(self, obj, item, index):
        item = super(SamplesView, self).folderitem(obj, item, index)
        if not item:
            return None

        # Creator
        item["Creator"] = self.user_fullname(obj.Creator)

        # Priority
        priority_sort_key = obj.getPrioritySortkey or "3.%s" % obj.created.ISO8601()
        priority = priority_sort_key.split(".")[0]
        priority_text = PRIORITIES.getValue(priority)

        item["replace"]["Priority"] = f"""
        <div class="priority-ico priority-{priority}">
            <span class="notext">{priority_text}</span>
        </div>
        """

        # Analyses count
        analysesnum = obj.getAnalysesNum
        if analysesnum:
            numbers = {
                "verified": analysesnum[0],
                "total": analysesnum[1],
                "not_submitted": analysesnum[2],
                "to_be_verified": analysesnum[3],
            }
            item["getAnalysesNum"] = ANALYSES_NUM_TPL.safe_substitute(numbers)

        # Progress
        progress_perc = obj.getProgress
        item["Progress"] = progress_perc
        item["replace"]["Progress"] = get_progress_bar_html(progress_perc)

        # Dates
        item["getDateSampled"] = self.str_date(obj.getDateSampled)
        item["Created"] = self.ulocalized_time(obj.created, long_format=1)

        # Client contact
        contact = self.get_object_by_uid(obj.getContactUID)
        if contact:
            item['ClientContact'] = contact.getFullname()
            item['replace']['ClientContact'] = get_link_for(contact)

        # ================================
        # 🚨 DETECCIÓN OUT OF RANGE (FIX)
        # ================================
        try:
            is_out_of_range = False
            analyses = obj.getAnalyses(full_objects=True)

            for analysis in analyses:
                if analysis.getResultOutOfRange():
                    is_out_of_range = True
                    break

            if is_out_of_range:
                current_css = item.get('css_class', '')
                item['css_class'] = (current_css + ' out-of-range-row').strip()

        except Exception as e:
            logger = api.get_logger(__name__)
            logger.error(f"Error en Sample {obj.getId}: {e}")

        return item

    @view.memoize
    def get_object_by_uid(self, uid):
        return api.get_object_by_uid(uid, default=None)

    def str_date(self, date, long_format=1, default=""):
        if not date:
            return default
        return self.ulocalized_time(date, long_format=long_format)
