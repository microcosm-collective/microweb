from pytest import raises
from httmock import urlmatch, HTTMock
import re
import pdb
import json

from core.api.resources import join_path_fragments, Site, Attachment


def test_api_resources_join_path_fragments():
    joined = join_path_fragments(['path','to','nowhere'])
    assert joined == "/path/to/nowhere"

    joined = join_path_fragments(['double','/','slash'])
    assert joined == "/double//slash"

    with raises(Exception):
        joined = join_path_fragments(['bad','mix/ed','slash'])


@urlmatch(netloc=r'(.*\.)?microco\.sm$')
def microcosm_mock(url, request):
    if url.path == '/api/v1/hosts/microco.sm':
        return "yepyep"
    if url.path == '/api/v1/comments/1/attachments':
        return json.dumps(
            {
                "error": "",
                "data": {
                    "attachments": {
                        "total": 0,
                        "limit": 100,
                        "offset": 0,
                        "maxOffset": 0,
                        "totalPages": 1,
                        "page": 1,
                        "type": "",
                    },
                    "meta": {
                        "created": "",
                        
                    },
                    "items": []
                }
            }
        )

def test_api_resources_resolve_cname():
    # nb. the host "microc.osm" will resolve to e.g.
    # "http://microco.sm/api/v1/hosts/microc.osm"
    test_host = "microco.sm"
    with HTTMock(microcosm_mock):
        blah = Site.resolve_cname(test_host)
        assert blah == "yepyep"


def test_attachment_retrieve():
    # nb. set local_settings API_SCHEME to http
    # & the value of test_host to match settings.API_DOMAIN_NAME
    test_host = "microco.sm"
    c_id = 1
    with HTTMock(microcosm_mock):
        c_attachments = Attachment.retrieve(test_host, "comments", c_id)

    assert c_attachments.items == []
