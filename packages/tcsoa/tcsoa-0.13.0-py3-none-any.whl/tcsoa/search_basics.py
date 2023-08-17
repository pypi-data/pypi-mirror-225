from typing import Optional, Dict, List

from tcsoa.basics import TcSoaBasics
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Query.services import SavedQueryService
from tcsoa.gen.Query._2019_06.SavedQuery import BusinessObjectQueryInput3
from tcsoa.gen.Query._2010_09.SavedQuery import BusinessObjectQueryClause


class TcSearchBasics:
    _cached_queries: Dict[str, BusinessObject] = None

    @classmethod
    def get_query_by_name(cls, query_name) -> Optional[BusinessObject]:     # returns: ImanQuery
        if cls._cached_queries is None:
            cls._cached_queries = dict()
            saved_queries_response = SavedQueryService.getSavedQueries()
            model_objs = saved_queries_response.serviceData.modelObjects
            for query in saved_queries_response.queries:
                cls._cached_queries[query.name] = model_objs[query.query.uid]
        return cls._cached_queries.get(query_name, None)

    @classmethod
    def exec_query(cls, query: BusinessObject, args: Dict[str, any], limit: int = 0, apply_defaults=True) -> List[BusinessObject]:
        entries, values = [], []
        if args:
            for k, v in args.items():
                entries.append(k)
                values.append(v)

        if apply_defaults:
            query_desc_resp = SavedQueryService.describeSavedQueries([query])
            for field in query_desc_resp.fieldLists[0].fields:
                if field.entryName and field.value and field.entryName not in entries:
                    entries.append(field.entryName)
                    values.append(field.value)

        exec_result = SavedQueryService.executeSavedQuery(
            query=query,
            entries=entries,
            values=values,
            limit=limit,
        )
        return exec_result.objects

    @classmethod
    def search_bo(cls, bo_name: str, props: Dict[str, str], max_result_num: int = 1):
        response = SavedQueryService().executeBOQueriesWithSort([
            BusinessObjectQueryInput3(
                boTypeName=bo_name,
                maxNumToReturn=max_result_num,
                requestId='abc',
                clientId='abc',
                clauses=[
                    BusinessObjectQueryClause(
                        propName=prop_name,
                        propValue=prop_val,
                        mathOperator='=',
                        logicOperator='AND'
                    )
                    for prop_name, prop_val in props.items()
                ],
            )
        ])
        found_obj_uids = response.arrayOfResults[0].objectUIDS
        return list(TcSoaBasics.load_objects(found_obj_uids).values())
