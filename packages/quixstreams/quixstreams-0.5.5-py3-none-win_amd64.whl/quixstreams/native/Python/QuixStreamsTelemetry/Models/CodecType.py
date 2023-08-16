from enum import Enum

class CodecType(Enum):
    Json = 0
    CompactJsonForBetterPerformance = 1
    Protobuf = 2
