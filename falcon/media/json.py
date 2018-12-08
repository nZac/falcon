from __future__ import absolute_import

import six

from falcon import errors
from falcon.media import BaseHandler
from falcon.util import json


class JSONHandler(BaseHandler):
    """JSON media handler.

    Keyword Arguments:
        dumps(function): a function which serializes response media into JSON format. By default
            this uses :py:mod:`json` with `ensure_ascii` disabled.

        loads(function): a function which consumes and deserializes the request stream from JSON
            format. By Default this uses :py:mod:`json`

        dumps_args(dict): other arguments to pass to `dumps` during serialization.

        loads_args(dict): other arguments to pass to `loads` during deserialization.
    """

    def __init__(self, dumps=None, loads=None, dumps_args=None, loads_args=None):
        self.dumps_args = {
            'enable_ascii': False
        }
        self.dumps_args.update(dump_args)

        self.loads_args = {
            'enable_ascii': False
        }
        self.loads_args.update(loads_args)

        self.dumps = dumps or json.dumps
        self.loads = loads or json.loads

    def deserialize(self, stream, content_type, content_length):
        try:
            return self.loads(stream.read().decode('utf-8'), **self.loads_args)
        except ValueError as err:
            raise errors.HTTPBadRequest(
                'Invalid JSON',
                'Could not parse JSON body - {0}'.format(err)
            )

    def serialize(self, media, content_type):
        result = self.dumps(media, **self.dumps_args)
        if six.PY3 or not isinstance(result, bytes):
            return result.encode('utf-8')

        return result
