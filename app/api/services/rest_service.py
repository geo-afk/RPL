from typing import List, Optional
from fastapi import APIRouter
from fastapi.routing import APIRoute
from pydantic import BaseModel, ValidationError, Field
import inspect
import json

from sqlmodel import SQLModel


class RouteInfo(BaseModel):
    name: str
    summary: Optional[str] = None
    description: Optional[str] = None
    methods: List[str]
    path: str
    endpoint_name: str
    endpoint_module: str

    # Old
    response_model: Optional[str] = None

    # NEW
    response_model_schema: Optional[str] = None

    dependencies: List[str] = Field(default_factory=list)
    path_params: List[str] = Field(default_factory=list)
    query_params: List[str] = Field(default_factory=list)

    # Old
    body_model: Optional[str] = None

    # NEW
    body_model_schema: Optional[str] = None

    tags: List[str] = Field(default_factory=list)
    status_code: Optional[int] = None


def model_schema_to_string(model: type) -> str | None:
    """
    Return JSON schema as a formatted string for:
    - Pydantic v1
    - Pydantic v2
    - SQLModel
    """

    try:
        # Pydantic v2
        if hasattr(model, "model_json_schema"):
            schema_dict = model.model_json_schema()
            return json.dumps(schema_dict, indent=2)

        # SQLModel (inherits from Pydantic, sometimes exposes .schema())
        if hasattr(model, "schema"):
            schema_dict = model.schema()
            return json.dumps(schema_dict, indent=2)

        if issubclass(model, SQLModel):
            return json.dumps(model.model_json_schema(), indent=2)

        # Fallback: repr()
        return repr(model)

    except Exception as e:
        return f"error: {type(e).__name__}: {e}"



def extract_router_routes(router: APIRouter) -> List[RouteInfo]:
    """
    Extracts metadata from all APIRoute routes in a router,
    including printable response & body model schemas.
    """
    route_infos: List[RouteInfo] = []

    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue

        try:
            name = getattr(route, "name", "")
            summary = getattr(route, "summary", None)
            description = getattr(route, "description", None)
            methods = list(getattr(route, "methods", []))
            path = (router.prefix or "") + getattr(route, "path", "")
            endpoint = route.endpoint
            endpoint_name = getattr(endpoint, "__name__", repr(endpoint))
            endpoint_module = getattr(endpoint, "__module__", "")

            # ---------------- RESPONSE MODEL ----------------
            response_model = None
            response_schema = None

            rm = getattr(route, "response_model", None)
            if rm is not None:
                response_model = f"{rm.__module__}.{rm.__name__}"
                response_schema = model_schema_to_string(rm)

            # ---------------- DEPENDENCIES ----------------
            deps = []
            for dep in getattr(route, "dependencies", []):
                dep_func = getattr(dep, "dependency", None)
                if callable(dep_func):
                    deps.append(getattr(dep_func, "__name__", repr(dep_func)))
                else:
                    deps.append(repr(dep))

            # ---------------- PARAMETER INSPECTION ----------------
            sig = inspect.signature(endpoint)

            path_params = []
            query_params = []
            body_model = None
            body_schema = None

            for pname, param in sig.parameters.items():
                if pname in ("self", "cls"):
                    continue

                annotation = param.annotation
                default = param.default

                # If it's a Pydantic model → body
                try:
                    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
                        body_model = f"{annotation.__module__}.{annotation.__name__}"
                        body_schema = model_schema_to_string(annotation)
                        continue
                except Exception:
                    pass

                # Rough guesses
                if default is inspect._empty:
                    path_params.append(pname)
                else:
                    query_params.append(pname)

            # ---------------- FINAL MODEL ----------------
            info = RouteInfo(
                name=name,
                summary=summary,
                description=description,
                methods=methods,
                path=path,
                endpoint_name=endpoint_name,
                endpoint_module=endpoint_module,
                response_model=response_model,
                response_model_schema=response_schema,
                dependencies=deps,
                path_params=path_params,
                query_params=query_params,
                body_model=body_model,
                body_model_schema=body_schema,
                tags=getattr(route, "tags", []),
                status_code=getattr(route, "status_code", None),
            )

            route_infos.append(info)

        except ValidationError as ve:
            print(f"Failed to parse route {route}: {ve}")

    return route_infos
