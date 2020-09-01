from rest_framework import renderers
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Перехватывает ошибки и оптравляет их в рендереры.
    :param exc: возникший exception
    :param context: контекст запроса
    :return: Response
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {'errors': exc.get_full_details()}

    return response


class ApiRenderer(renderers.JSONRenderer):
    """
    Задаёт шаблон ответа в виде json.

    status — http статус запроса
    result — статус проведения текущей операции
    addition — поля для описания текущей операции (uuid, ФИО, сумма,
        статус и т.п.)
    description — дополнительные описания к текущей операции (прочие
        текстовые поля, если необходимо)
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {
            'status': renderer_context.get('response').status_code,
            'result': not renderer_context.get('response').exception,
            'addition': data,
            'description': {},
        }
        return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
