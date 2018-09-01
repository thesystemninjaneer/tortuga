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

import datetime
import json

from sqlalchemy.orm.session import Session


from tortuga.db.models.nodeRequest import NodeRequest
from tortuga.events.types import AddNodeRequestQueued
from tortuga.resourceAdapter.tasks import add_nodes

from .addHostManager import AddHostManager


def enqueue_addnodes_request(session: Session, addNodesRequest: dict):
    request = _init_node_add_request(addNodesRequest)
    session.add(request)
    session.commit()

    #
    # Fire the add node request queued event
    #
    AddNodeRequestQueued.fire(request_id=request.id,
                              request=addNodesRequest['addNodesRequest'])

    #
    # Run async task
    #
    add_nodes.delay(request.addHostSession)

    return request.addHostSession


def _init_node_add_request(addNodesRequest):
    request = NodeRequest(
        request=json.dumps(addNodesRequest['addNodesRequest']),
        timestamp=datetime.datetime.utcnow(),
        addHostSession=AddHostManager().createNewSession(),
        action='ADD'
    )

    if 'metadata' in addNodesRequest and \
            'admin_id' in addNodesRequest['metadata']:
        request.admin_id = addNodesRequest['metadata']['admin_id']

    return request
