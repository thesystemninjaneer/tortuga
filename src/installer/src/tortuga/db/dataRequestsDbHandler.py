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

# pylint: disable=not-callable,no-member,multiple-statements

from sqlalchemy.orm.session import Session

from tortuga.db.tortugaDbObjectHandler import TortugaDbObjectHandler

from .models.dataRequest import DataRequest


class DataRequestsDbHandler(TortugaDbObjectHandler):
    """Accessor methods for DataRequests table
    """

    def get_all(self, session: Session): \
            # pylint: disable=no-self-use
        return session.query(DataRequest).all()

    def get_by_id(self, session: Session, data_request_id: int): \
            # pylint: disable=no-self-use
        return session.query(DataRequest).get(data_request_id)

    def get_first_by_state(self, session: Session, state: str): \
            # pylint: disable=no-self-use
        return session.query(DataRequest).filter(
            DataRequest.state == state).first()

    def get_by_addHostSession(self, session: Session,
                              add_host_session: str): \
            # pylint: disable=no-self-use
        return session.query(DataRequest).filter(
            DataRequest.addHostSession == add_host_session).first()
