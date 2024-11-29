from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

DifyExternalKnowledgeAPIErrorCode = Literal[1001, 1002, 2001]


class DifyExternalKnowledgeAPIRetrievalSetting(BaseModel):
    top_k: int
    score_threshold: int


class DifyExternalKnowledgeAPIRecord(BaseModel):
    content: str
    score: float
    titie: str
    metadata: Optional[Dict[str, Any]]


class DifyExternalKnowledgeAPIRequest(BaseModel):
    knowledge_id: str
    query: str
    retrieval_setting: DifyExternalKnowledgeAPIRetrievalSetting


class DifyExternalKnowledgeAPIResponse(BaseModel):
    records: List[DifyExternalKnowledgeAPIRecord]


class DifyExternalKnowledgeAPIErrorResponse(BaseModel):
    error_code: DifyExternalKnowledgeAPIErrorCode
    error_msg: str
