from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class OpenAPIJsonView(View):
    content_type: str = 'application/json'
    schema_json: str = None

    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(
            content=self.schema_json.encode('utf-8'),
            content_type=self.content_type,
        )


class SwaggerView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'autoapi/swagger.html')
