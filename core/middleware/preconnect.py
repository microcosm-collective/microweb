class PreconnectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_response(request, self.get_response(request))

    def process_response(self, request, response):

        if response.get('Content-Type') == 'text/html; charset=utf-8':
            response['Link'] = '<//fonts.googleapis.com>; rel=preconnect, <https://fonts.gstatic.com>; rel=preconnect; crossorigin'

        return response
