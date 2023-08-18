import json

from autoapi.api.schema_presenter.interface import ISchemaPresenter
from autoapi.schema.empty import Empty
from autoapi.api.encoders import JsonEncoder
from autoapi.schema.data import Type, Annotation, ServiceSchema, MethodSchema, ParamSchema


class OpenAPIPresenter(ISchemaPresenter):

    def present(self, schemas: list[ServiceSchema], models: dict[str, Type]) -> str:
        openapi_schema = self._info()
        openapi_schema['tags'] = self._tags(schemas)
        openapi_schema['paths'] = self._paths(schemas)
        openapi_schema['components'] = self._components(models)
        return json.dumps(openapi_schema, cls=JsonEncoder)

    def _info(self):
        return dict(
            openapi='3.0.0',
            info=dict(
                version=self.settings.explorer_version,
                title=self.settings.explorer_title,
                license=dict(
                    name=self.settings.license_name
                ),
            ),
            servers=[
                dict(
                    url=self.settings.host
                ),
            ],
        )

    def _tags(self, schemas: list[ServiceSchema]) -> list[dict]:
        return [
            {
                'name': schema.name,
                'description': schema.description,
            }
            for schema in schemas
        ]

    def _paths(self, schemas: list[ServiceSchema]) -> dict:
        paths = {}
        for service in schemas:
            for method in service.methods:
                url = '/' + self.url_builder.build(service, method)
                path = self._path(service, method)
                paths[url] = dict(get=path) if method.idempotency else dict(post=path)
        return paths

    def _path(self, service: ServiceSchema, method: MethodSchema) -> dict:
        result = dict(
            summary=method.description,
            operationId=f'{service.name}.{method.name}',
            tags=[service.name],
        )
        if method.returns.type.name == 'File':
            result['responses'] = {
                '200': {
                    'description': method.return_description,
                    'content': {
                        'image/*': {}
                    }
                }
            }
        else:
            result['responses'] = {
                '200': {
                    'description': method.return_description,
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'ok': {
                                        'type': 'boolean'
                                    },
                                    'result': self._type_ref(method.returns),
                                    'error': {
                                        'type': 'object',
                                        'default': None
                                    } if not method.raises else {
                                        'oneOf': [
                                            self._type_ref(raise_t)
                                            for raise_t in method.raises
                                        ]
                                    },
                                    'panic': {
                                        'type': 'object',
                                        'default': None
                                    }
                                }
                            }
                        }
                    }
                },
            }
        if method.idempotency:
            result['parameters'] = [
                self._get_param(param)
                for param in method.params
            ]
        else:
            result['requestBody'] = self._body_definition(method)
        return result

    def _get_prop_schema(self, annotation: Annotation) -> dict:
        for parser in self.components_properties_parsers:
            if parser.check(annotation):
                return parser.parse(annotation)
        raise ValueError(f'Cannot found OpenAPI component property parser for type = {annotation.type.name}')

    def _components(self, models: dict[str, Type]) -> dict:
        schemas = {}
        for model_path, model in models.items():
            properties = {}
            for prop_name, prop in model.model_fields.items():
                prop_schema = self._type_ref(prop)
                properties[prop_name] = prop_schema
            schemas[model.name] = {
                'type': 'object',
                'properties': properties,
            }
        return { 'schemas': schemas }

    def _get_param(self, param: ParamSchema) -> dict:
        data = {
            'name': param.name,
            'in': 'query',
            'description': param.description,
            'required': param.default is Empty,
            'schema': self._type_ref(param.annotation)
        }
        data.update(dict(default=param.default)) if param.default is not Empty else None
        return data

    def _post_param(self, param: ParamSchema) -> dict:
        result = {
            'name': param.name,
            'in': 'body',
            'description': param.description,
            'required': param.default is Empty,
        }
        result.update(self._type_ref(param.annotation))
        return result

    def _body_definition(self, method: MethodSchema) -> dict:
        return {
            'description': method.description,
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            param.name: self._post_param(param)
                            for param in method.params
                        }
                    }
                }
            },
        }

    def _type_ref(self, annotation: Annotation) -> dict:
        if annotation.is_generic and annotation.type.name == 'list':
            return {
                'type': 'array',
                'items': self._type_ref(annotation.generic_annotations[0]),
            }
        return self._get_prop_schema(annotation)
