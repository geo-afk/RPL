import structlog

from app.api.utils.rpl_analyzer import RPLAnalyzerService
from typing import Dict, List, Type, TypeVar, Any

from app.models.llm_result import Finding
from app.models.role import Role
from sqlmodel import SQLModel
from app.models.user import User
from app.models.group import Group
from app.models.resource import Resource


from app.api.database.database import DatabaseHandler, next_session


service = RPLAnalyzerService()


T = TypeVar("T", bound=SQLModel)

async def save_items(model: Type[T], items: Dict[str, T]) -> List[T]:
    handler = DatabaseHandler(next_session, model)
    return handler.create_all(items.values())


async def save_llm_findings(model: Type[T], items: List[Finding]) -> List[T]:
    handler = DatabaseHandler(next_session, model)
    return handler.create_all(items)



async def analyze_policies(code: str, use_llm: bool = False) -> Dict[str, Any] | None:

    result = await service.analyze(code, use_llm)


    if result.get("symbol_table"):
        table = result["symbol_table"]
        roles: Dict[str, Role] = table["roles"]
        users: Dict[str, User] = table["users"]
        resources: Dict[str, Resource] = table["resources"]
        groups: Dict[str, Group] = table["groups"]

        saved_roles = await save_items(Role, roles)
        saved_users = await save_items(User, users)
        saved_resources = await save_items(Resource, resources)
        saved_groups = await save_items(Group, groups)


        return {
            "saved": {
                "roles": saved_roles,
                "users": saved_users,
                "resources": saved_resources,
                "groups": saved_groups,
            },
        }


    if result.get("errors"):
        return result


    if use_llm and result.get("semantic_analysis"):
        llm_analysis: Dict[str, Any] = result.get("llm_analysis")
        llm_findings: List[Finding] = llm_analysis.get("findings")
        findings = save_llm_findings(Finding, llm_findings)
        return {
                "findings": findings,
                "risk_score": llm_analysis.get("risk_score"),
        }


    return None

