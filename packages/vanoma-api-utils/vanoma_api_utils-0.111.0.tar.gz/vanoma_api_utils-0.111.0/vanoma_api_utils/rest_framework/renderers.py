from rest_framework.renderers import JSONRenderer
from djangorestframework_camel_case.render import CamelCaseJSONRenderer  # type: ignore
from ..http import USER_AGENT


class CustomJsonRenderer(CamelCaseJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get("request")
        if not request:
            super().render(data, accepted_media_type=None, renderer_context=None)

        # Avoid camelizing the response for requests from internal services
        user_agent = request.headers.get("User-Agent")
        if user_agent == USER_AGENT:
            return super(CamelCaseJSONRenderer, self).render(
                data, accepted_media_type=None, renderer_context=None
            )

        return super().render(data, accepted_media_type=None, renderer_context=None)
