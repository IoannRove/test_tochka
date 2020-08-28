from rest_framework import renderers
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {'errors': exc.get_full_details()}

    return response


class ApiRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {
            'status': renderer_context.get('response').status_code,
            'result': not renderer_context.get('response').exception,
            'addition': data,
            'description': {},
        }
        return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
