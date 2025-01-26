from pytest import raises
from httmock import urlmatch, HTTMock
import re
import pdb

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
    return "myarse"

def test_api_resources_resolve_cname():
    # nb. the host "microc.osm" will resolve to e.g. 
    # "http://microco.sm/api/v1/hosts/microc.osm"
    test_host = "microc.osm"
    with HTTMock(microcosm_mock):
        blah = Site.resolve_cname(test_host)
        assert blah == "myarse"

