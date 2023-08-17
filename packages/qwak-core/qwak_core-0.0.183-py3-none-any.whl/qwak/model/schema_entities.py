from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from _qwak_proto.qwak.builds.builds_pb2 import (
    BatchFeatureV1 as ProtoBatchFeatureV1,
    Entity as ProtoEntity,
    ExplicitFeature as ProtoExplicitFeature,
    Feature as ProtoFeature,
    InferenceOutput as ProtoInferenceOutput,
    Prediction as ProtoPrediction,
    RequestInput as ProtoRequestInput,
    SourceFeature as ProtoSourceFeature,
    ValueType,
)


@dataclass(unsafe_hash=True)
class Entity:
    name: str
    type: Type = str

    def to_proto(self):
        return ProtoEntity(
            name=self.name, type=ValueType(type=_type_conversion(self.type))
        )


@dataclass
class BaseFeature(ABC):
    name: str

    @abstractmethod
    def to_proto(self):
        pass


@dataclass(unsafe_hash=True)
class ExplicitFeature(BaseFeature):
    type: Type

    def to_proto(self):
        return ProtoFeature(
            explicit_feature=ProtoExplicitFeature(
                name=self.name, type=ValueType(type=_type_conversion(self.type))
            )
        )

    def to_source_proto(self):
        return ProtoSourceFeature(
            explicit_feature=ProtoExplicitFeature(
                name=self.name, type=ValueType(type=_type_conversion(self.type))
            )
        )


@dataclass(unsafe_hash=True)
class RequestInput(BaseFeature):
    type: Type

    def to_proto(self):
        return ProtoFeature(
            request_input=ProtoRequestInput(
                name=self.name, type=ValueType(type=_type_conversion(self.type))
            )
        )

    def to_source_proto(self):
        return ProtoSourceFeature(
            request_input=ProtoRequestInput(
                name=self.name, type=ValueType(type=_type_conversion(self.type))
            )
        )


@dataclass(unsafe_hash=True)
class FeatureStoreInput(BaseFeature):
    entity: Entity

    def to_proto(self):
        return ProtoFeature(
            batch_feature_v1=ProtoBatchFeatureV1(
                name=self.name, entity=self.entity.to_proto()
            )
        )

    def to_source_proto(self):
        return ProtoSourceFeature(
            batch_feature_v1=ProtoBatchFeatureV1(
                name=self.name, entity=self.entity.to_proto()
            )
        )


@dataclass(unsafe_hash=True)
class InferenceOutput:
    name: str
    type: type

    def to_proto(self):
        return ProtoInferenceOutput(
            name=self.name, type=ValueType(type=_type_conversion(self.type))
        )


@dataclass(unsafe_hash=True)
class Prediction:
    name: str
    type: type

    def to_proto(self):
        return ProtoPrediction(
            name=self.name, type=ValueType(type=_type_conversion(self.type))
        )


def _type_conversion(type):
    if type == int:
        return ValueType.INT32
    elif type == str:
        return ValueType.STRING
    elif type == bytes:
        return ValueType.BYTES
    elif type == bool:
        return ValueType.BOOL
    elif type == float:
        return ValueType.FLOAT
