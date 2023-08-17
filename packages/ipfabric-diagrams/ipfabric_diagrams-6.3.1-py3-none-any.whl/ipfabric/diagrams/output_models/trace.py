from typing import Optional, List, Union, Literal

try:
    from typing import Annotated  # py38 required Annotated
except ImportError:
    from typing_extensions import Annotated


from pydantic import BaseModel, Field

from .protocols import PROTOCOLS


class SeverityInfo(BaseModel):
    name: str
    severity: int
    topic: str
    details: Optional[List[str]] = Field(default_factory=list)


class PacketDataMatch(BaseModel):
    field: str
    value: Union[str, List[str], None]
    type: Literal["packet data match"]


class RemoveHeader(BaseModel):
    index: int
    headerType: str
    type: Literal["remove header"]


class Filter(BaseModel):
    label: Optional[int] = None
    mask: Optional[int] = None
    vrf: Optional[str] = None
    prefix: Optional[str] = None
    ip: Optional[str] = None
    groupIp: Optional[str] = None
    sourceIp: Optional[str] = None
    inIfaceName: Optional[str] = None
    mac: Optional[str] = None
    vlanNum: Optional[int] = None


class TableEntry(BaseModel):
    filter: Filter
    table: str


class TableEntryMatch(TableEntry, BaseModel):
    type: Literal["table entry match"]


class TableEntryNotFound(TableEntry, BaseModel):
    type: Literal["table entry not found"]


class InsertHeader(BaseModel):
    header: PROTOCOLS
    headerType: str
    index: int
    type: Literal["insert header"]


class Patch(BaseModel):
    stack: Optional[List[int]] = None
    ttl: Optional[int] = None


class PatchHeader(BaseModel):
    patch: Patch
    index: int
    type: Literal["patch header"]


class DropPacket(BaseModel):
    type: Literal["drop packet"]
    reason: str
    severityInfo: Optional[SeverityInfo] = None


class SeverityEvent(BaseModel):
    type: Literal["severity event"]
    severityInfo: Optional[SeverityInfo] = None


class BaseEvent(BaseModel):
    decidingPolicyName: Optional[str] = None
    decidingRule: Optional[List[int]] = None
    protocolId: str
    securityType: str
    severityInfo: Optional[SeverityInfo] = None


class SecurityCheck(BaseEvent, BaseModel):
    type: Literal["security check"]


class SecurityCheckIgnored(BaseEvent, BaseModel):
    type: Literal["security check ignored"]


class VirtualRouting(BaseModel):
    type: Literal["virtual routing"]
    ifaceName: str


class AcceptPacket(BaseModel):
    type: Literal["accept packet"]


class DestinationNAT(BaseEvent, BaseModel):
    type: Literal["destination NAT"]
    field: Optional[str] = None


class SourceNAT(BaseEvent, BaseModel):
    type: Literal["source NAT"]
    field: str


class PolicyBasedRouting(BaseEvent, BaseModel):
    type: Literal["policy based routing"]
    field: Optional[str] = None


EVENT = Annotated[
    Union[
        PacketDataMatch,
        RemoveHeader,
        TableEntryMatch,
        TableEntryNotFound,
        VirtualRouting,
        AcceptPacket,
        InsertHeader,
        PatchHeader,
        DropPacket,
        SeverityEvent,
        SecurityCheckIgnored,
        SecurityCheck,
        DestinationNAT,
        PolicyBasedRouting,
        SourceNAT,
    ],
    Field(discriminator="type"),
]


class Trace(BaseModel):
    chain: str
    phase: str
    events: List[EVENT]
