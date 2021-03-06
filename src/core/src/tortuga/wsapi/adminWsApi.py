# Copyright 2008-2018 Univa Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=no-member

import json
import urllib.error
import urllib.parse
import urllib.request

from tortuga.exceptions.tortugaException import TortugaException
from tortuga.objects.admin import Admin
from tortuga.utility.helper import str2bool

from .tortugaWsApi import TortugaWsApi


class AdminWsApi(TortugaWsApi):
    """Admin WS API class"""

    def getAdmin(self, adminName):
        """Get admin information

            Returns:
                admin
            Throws:
                UserNotAuthorized
                AdminNotFound
                TortugaException
        """

        url = 'admins/%s' % (urllib.parse.quote_plus(adminName))

        try:
            responseDict = self.get(url)

            return Admin.getFromDict(responseDict.get(Admin.ROOT_TAG))
        except TortugaException:
            raise
        except Exception as ex:
            raise TortugaException(exception=ex)

    def getAdminById(self, admin_id):
        """Get admin information

            Returns:
                admin
            Throws:
                UserNotAuthorized
                AdminNotFound
                TortugaException
        """

        url = 'admins/%s' % (admin_id)

        try:
            responseDict = self.get(url)

            return Admin.getFromDict(responseDict.get(Admin.ROOT_TAG))
        except TortugaException:
            raise
        except Exception as ex:
            raise TortugaException(exception=ex)

    def getAdminList(self):
        """Get admin list.

            Returns:
                [admins]
            Throws:
                UserNotAuthorized
                TortugaException
        """

        url = 'admins/'

        try:
            responseDict = self.get(url)

            return Admin.getListFromDict(responseDict)
        except TortugaException:
            raise
        except Exception as ex:
            raise TortugaException(exception=ex)

    def addAdmin(self, username, password, isCrypted=False, realname=None,
                 description=None): \
            # pylint: disable=too-many-arguments
        """
        Add an admin using rule name/password.

        Raises:
            UserNotAuthorized
            FileNotFound
            InvalidXml
            AdminAlreadyExists
            TortugaException
        """

        url = 'admins/'

        postdata = {
            'isCrypted': isCrypted,
            'admin': {
                'username': username,
                'password': password,
            }
        }

        if realname is not None:
            postdata['admin']['realname'] = realname

        if description is not None:
            postdata['admin']['description'] = description

        try:
            self.post(url, postdata)

        except TortugaException:
            raise

        except Exception as ex:
            raise TortugaException(exception=ex)

    def deleteAdmin(self, admin):
        """Delete admin.

            Returns:
                None
            Throws:
                UserNotAuthorized
                AdminNotFound
                TortugaException
        """

        url = 'admins/%s' % (urllib.parse.quote_plus(admin))

        try:
            self.delete(url)
        except TortugaException:
            raise
        except Exception as ex:
            raise TortugaException(exception=ex)

    def updateAdmin(self, adminObject, isCrypted=True):
        """
        Update admin.

            Returns:
                None
            Throws:
                UserNotAuthorized
                AdminNotFound
                TortugaException
        """

        url = 'admins/%s' % (adminObject.getId())

        postdata = {
            'admin': adminObject.getCleanDict(),
            'isCrypted': isCrypted,
        }

        realname = adminObject.getRealname()
        if realname is not None:
            postdata['realname'] = realname

        description = adminObject.getDescription()
        if description is not None:
            postdata['description'] = description

        try:
            self.put(url, postdata)

        except TortugaException:
            raise

        except Exception as ex:
            raise TortugaException(exception=ex)

    def authenticate(self, adminUsername, adminPassword):
        """
        Check if the credentials are valid.

            Returns:
                True if username and password match a valid user in the system
            Throws:
                UserNotAuthorized
                TortugaException
        """

        url = 'authenticate/%s' % (urllib.parse.quote_plus(adminUsername))

        postdata = {'password': adminPassword}

        try:
            responseDict = self.post(url, postdata)

            return str2bool(responseDict.get('authenticate'))
        except TortugaException:
            raise
        except Exception as ex:
            raise TortugaException(exception=ex)
