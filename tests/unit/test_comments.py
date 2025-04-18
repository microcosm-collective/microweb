from core.api.resources import Comment

import mwcomments.views


def test_comment_create_redirect():
    # TODO: use a Factory to create a Comment instance
    # TODO: verify this sample data is valid
    data = {}
    data["id"] = 17730922
    data["itemType"] = "comment"
    data["itemId"] = "17730922"
    data["revisions"] = ""
    data["markdown"] = "# Test Title\n\nTest comment"
    data["html"] = "<h1>Test Title</h1><p>Test comment</p>"
    data["meta"] = {
        "links": [
            {
                "href": "https://www.lfgss.com/comments/17730922/",
                "rel": "/comments/17730922/",
            }
        ]
    }

    comment = Comment.from_api_response(data)
    assert (
        mwcomments.views.build_comment_location(comment)
        == "/comments/17730922/#comment17730922"
    )
