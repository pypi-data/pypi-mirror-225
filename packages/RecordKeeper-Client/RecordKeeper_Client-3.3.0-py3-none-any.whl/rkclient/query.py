import ast
import json
from typing import Tuple, List, Optional, Any, Dict
from uuid import UUID
import logging
from importlib.metadata import version

from rkclient.entities import Artifact, PEM
from rkclient.request import _parse_sorting_filtering_params, RequestHelper, _handle_request, \
    _handle_request_with_response
from rkclient.serialization import ArtifactSerialization, PEMSerialization, _decode_from_base64, _encode_as_base64, \
    create_artifact_from_neo4j

log = logging.getLogger("rkclient")
RK_VERSION = version('RecordKeeper_Client')


class RKQuery:
    """
    Calls RK Query service to obtain data about RK from SQL db and from graph view.
    """

    def __init__(self,
                 receiver_url: str,
                 timeout_sec: int = 5,
                 insecure: bool = True,
                 user_auth: str = '',
                 puc_auth: str = ''):
        receiver_url = receiver_url.rstrip('/')
        self.receiver_request = RequestHelper(receiver_url, timeout_sec, insecure, user_auth, puc_auth, f'recordkeeper-client-{RK_VERSION}')
        log.info(f"ver {RK_VERSION}, connecting to: {receiver_url}")

    def get_info(self) -> Tuple[str, bool]:
        """
        Returns json with fields as in Info class - the Receiver state. Use `deserialize_info` for easy parsing.
        :return: check class description
        """
        def _get_info():
            return self.receiver_request.get("/info")

        return _handle_request_with_response(_get_info, "Getting info", True)

    def get_pem(self, pem_id: str) -> Tuple[Optional[PEM], str, bool]:
        """
        Returns pem from sql db. Warning: the artifacts will contain just names, without properties.
        :param pem_id: UUID, should be in hex format.
        :return: PEM or None. If didn't found, bool will be False.
        """
        def _get_pem() -> Tuple[Optional[PEM], str, bool]:
            text, ok = self.receiver_request.get(f"/pem/{pem_id}")
            if not ok:
                return None, text, False
            pem_json = json.loads(text)
            pem = PEMSerialization.from_dict(pem_json, True)
            return pem, 'OK', True

        return _handle_request(_get_pem, "Getting pem")

    def get_pems(self,
                 page_index: int = -1,
                 page_size: int = -1,
                 sort_field: str = '',
                 sort_order: str = '',
                 filters: Optional[Dict] = None) -> Tuple[List[PEM], str, bool]:
        """
        Returns pems from sql db.
        :param page_index:
        :param page_size:
        :param sort_field:
        :param sort_order:
        :param filters: contains dict of key:value pairs, which all have to be contained in PEM fields to be returned.
                ID, Predecessor should be hex values of UUID (without dashes).
        :return: first element: list of pems (as json string) or error message
                 The artifacts lists in PEM will contain only artifact ID
                 second element: True for success, False for error
        """

        def _get_pems() -> Tuple[List[Any], str, bool]:
            query_params: Dict[str, Any] = _parse_sorting_filtering_params(page_index, page_size,
                                                                           sort_field, sort_order, filters)
            text, ok = self.receiver_request.get("/pems", query_params)
            if not ok:
                return [], text, False
            pems = []
            pems_json = json.loads(text)
            for p in pems_json:
                pems.append(PEMSerialization.from_dict(p, True))
            return pems, 'OK', True

        return _handle_request(_get_pems, "Getting pems")

    def get_pems_count(self,
                       page_index: int = -1,
                       page_size: int = -1,
                       sort_field: str = '',
                       sort_order: str = '',
                       filters: Optional[Dict] = None) -> Tuple[int, str, bool]:
        """
        Returns amount of PEMs which match the filters. See `get_pems` for more info.
        """

        def _get_pems() -> Tuple[int, str, bool]:
            query_params: Dict[str, Any] = _parse_sorting_filtering_params(page_index, page_size,
                                                                           sort_field, sort_order, filters)
            text, ok = self.receiver_request.get("/pems_count", query_params)
            if not ok:
                return -1, text, False
            obj = json.loads(text)
            return int(obj['pems_count']), 'OK', True

        return _handle_request(_get_pems, "Getting pems count")

    def get_artifact(self, artifact_name: str, source: str = 'sqldb') -> Tuple[Optional[Artifact], bool]:
        # todo this could be improved by using different endpoint
        res, text, ok = self.get_artifacts(source)
        if not ok:
            log.error(f"Getting artifact failed: {text}")
            return None, False

        artifacts: List[Artifact] = res
        for a in artifacts:
            if a.Name == artifact_name:
                return a, True

        return None, True

    def get_artifact_latest(self, artifact_name: str) -> Tuple[Optional[Artifact], str, bool]:
        """
        Returns the newest Artifact whose name includes the string provided by the artifact_name argument.
        """
        artifacts, msg, ok = self.get_artifacts(
            sort_field='CreatedAt',
            sort_order='desc',
            page_size=1,
            filters={'Name': artifact_name}
        )
        if ok:
            if len(artifacts) > 0:
                return artifacts[0], "", True
            else:
                return None, "", True
        return None, msg, False

    def get_artifacts(self,
                      source: str = 'sqldb',
                      page_index: int = -1,
                      page_size: int = -1,
                      sort_field: str = '',
                      sort_order: str = '',
                      filters: Optional[Dict] = None) -> Tuple[List[Artifact], str, bool]:
        """
        :param source: from which db to return artifacts, 'sqldb' or 'graphdb'.
        :param page_index:
        :param page_size:
        :param sort_field:
        :param sort_order:
        :param filters: contains dict of key:value pairs, which all has to be contained in artifact to be returned
        :return: first element: list of artifact objs. Artifacts contain also the taxonomies ids and xml content.
                 second element: optional str error message
                 third element: True for success, False for error
        """
        if source == 'sqldb':
            query_params: Dict[str, Any] = _parse_sorting_filtering_params(page_index, page_size,
                                                                           sort_field, sort_order, filters)
            return self._get_artifacts_from_sql(query_params)
        elif source == 'graphdb':
            return self._get_artifacts_from_graph()
        else:
            return [], f"Getting artifacts: didn't recognize source: {source}", False

    def get_artifacts_count(self,
                            source: str = 'sqldb',
                            filters: Optional[Dict] = None) -> Tuple[int, str, bool]:
        """
        :param source: from which db to return artifacts, 'sqldb' or 'graphdb'.
        :param filters: contains dict of key:value pairs, which all has to be contained in artifact to be counted
        :return: first element: count of artifact objs
                 second element: optional str error message
                 third element: True for success, False for error
        """

        def _get_artifacts_count_from_sql() -> Tuple[int, str, bool]:
            query_params: Dict[str, Any] = _parse_sorting_filtering_params(-1, -1, "", "", filters)
            text, ok = self.receiver_request.get("/artifacts_count", query_params)
            if not ok:
                return -1, text, False
            objs = json.loads(text)
            return int(objs['artifacts_count']), "", True

        def _get_artifacts_count_from_graph() -> Tuple[int, str, bool]:
            text, ok = self.query_graph('MATCH (a:Artifact) RETURN count(a);', 'r')
            if not ok:
                return -1, text, False
            result = ast.literal_eval(text)
            return int(result[0][0]), "", True

        if source == 'sqldb':
            return _handle_request(_get_artifacts_count_from_sql, 'Getting artifacts count')
        elif source == 'graphdb':
            return _handle_request(_get_artifacts_count_from_graph, 'Getting artifacts count')
        else:
            return -1, f"Getting artifacts count: didn't recognize source: {source}", False

    def get_taxonomy_file(self, taxonomy_id: UUID) -> Tuple[str, bool]:
        text, ok = self.receiver_request.get(f"/taxonomy/{taxonomy_id.hex}")
        if not ok:
            return f"Getting taxonomy file failed: {text}", False
        return _decode_from_base64(text), True

    def get_tag(self, namespace: str, tag_name: str) -> Tuple[str, bool]:
        """
        Returned tag is UUID in hex (do: UUID(hex=result))
        :return: check class description
        """
        def _get_tag():
            tag_base64 = _encode_as_base64(tag_name)
            namespace_base64 = _encode_as_base64(namespace)
            return self.receiver_request.get(f"/tag/{namespace_base64}/{tag_base64}")

        return _handle_request_with_response(_get_tag, "Getting tag", True)

    def get_tags(self) -> Tuple[List[Dict], str, bool]:
        """
        :return: first element: list of metadata (as Dict), with fields: NamespaceID, Tag, EventID, UpdatedAt
                 second element: error message
                 third element: True for success, False for error
        """

        def _get_tags() -> Tuple[List[Any], str, bool]:
            text, ok = self.receiver_request.get("/tags")
            if not ok:
                return [], text, False
            tags = json.loads(text)
            return tags, 'OK', True

        return _handle_request(_get_tags, "Getting tags")

    def get_tags_count(self) -> Tuple[int, str, bool]:
        """
        Returns amount of tags.
        """

        def _get_tags() -> Tuple[int, str, bool]:
            text, ok = self.receiver_request.get("/tags_count")
            if not ok:
                return -1, text, False
            obj = json.loads(text)
            return int(obj['tags_count']), 'OK', True

        return _handle_request(_get_tags, "Getting tags count")

    def query_graph(self, query: str, query_type='rw') -> Tuple[str, bool]:
        """
        :return: first element: returned result (as str with format corresponding to what query requests) or error message
                 second element: True for success, False for error
        """
        query_fmt = f'"query": "{query}", "type": "{query_type}"'
        payload = '{' + query_fmt + '}'
        return self.receiver_request.post("/query", payload)

    def _get_artifacts_from_sql(self, query_params: Dict[str, Any]) -> Tuple[List[Artifact], str, bool]:
        text, ok = self.receiver_request.get("/artifacts", query_params)
        if not ok:
            return [], f"querying SQL failed: {text}", False

        objs = json.loads(text)
        artifacts: List[Artifact] = [ArtifactSerialization.from_dict(o) for o in objs]
        return artifacts, "", True

    def _get_artifacts_from_graph(self) -> Tuple[List[Artifact], str, bool]:
        text, ok = self.query_graph('MATCH (a:Artifact) RETURN a.rk_id AS rk_id, a.properties as properties, a.created_at as created_at')
        if not ok:
            return [], text, False

        # the text contains python like list [['<name>','<properties-as-json>'], ['<name>', ... ] ]
        objs = ast.literal_eval(text)
        artifacts: List[Artifact] = [
            create_artifact_from_neo4j(o)
            for o in objs
        ]
        return artifacts, "", True
