# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs

from openstack_dashboard import fiware_api
from openstack_dashboard.dashboards.idm.myApplications \
            import tables as application_tables
from openstack_dashboard.dashboards.idm.myApplications \
            import tabs as application_tabs
from openstack_dashboard.dashboards.idm.myApplications \
            import forms as application_forms


class IndexView(tabs.TabbedTableView):
    tab_group_class = application_tabs.PanelTabs
    template_name = 'idm/myApplications/index.html'

  
class CreateView(forms.ModalFormView):
    form_class = application_forms.CreateApplicationForm
    template_name = 'idm/myApplications/create.html'
    

class UploadImageView(forms.ModalFormView):
    form_class = application_forms.UploadImageForm
    template_name = 'idm/myApplications/upload.html'
    

class RolesView(tables.MultiTableView):
    """ Logic for the asynchronous widget to manage roles and permissions at the
    application level.
    """
    template_name = 'idm/myApplications/roles.html'
    table_classes = (application_tables.RolesTable,
                     application_tables.PermissionsTable)

    # def get_context_data(self, **kwargs):
    #     context = super(RolesView, self).get_context_data(**kwargs)
    #     try:
    #         context['roles'] = fiware_api.keystone.role_list(self.request)
    #         context['selected_role'] = context['roles'][0] 
    #     except Exception:
    #         exceptions.handle(self.request,
    #                           _('Unable to retrieve roles list.'))
    #     return context
    def get_roles_data(self):
        roles = []
        try:
            roles = fiware_api.keystone.role_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                               _('Unable to retrieve roles list.'))
    
        return roles

    def get_permissions_data(self):
        permissions = []
        try:
            permissions = fiware_api.keystone.permission_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                               _('Unable to retrieve permissions list.'))
    
        return permissions