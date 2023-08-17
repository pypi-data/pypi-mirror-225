"""
CycloneDX data models
"""
from __future__ import annotations

import functools
import sys
import uuid

from pathlib import Path
from typing import Annotated, Any, Callable, ClassVar, Iterator, Literal, MutableMapping, TypeAlias, TypeVar

import hoppr_cyclonedx_models.cyclonedx_1_4

from pydantic import BaseModel, Extra, Field, create_model, root_validator, validator
from rapidfuzz import fuzz
from requests import HTTPError

import hoppr.net
import hoppr.utils

from hoppr.exceptions import HopprLoadDataError
from hoppr.models.base import HopprBaseModel
from hoppr.models.types import LocalFile, OciFile, UrlFile

DictStrAny: TypeAlias = dict[str, Any]

__all__ = []

AnyCycloneDXModel = TypeVar("AnyCycloneDXModel", bound="CycloneDXBaseModel")
SbomRef = Annotated[LocalFile | OciFile | UrlFile, Field(..., description="Reference to a local or remote SBOM file")]
SbomRefMap = Annotated[MutableMapping[SbomRef, "Sbom"], Field(default=...)]
UniqueIDMap = Annotated[MutableMapping[str, AnyCycloneDXModel], Field(default={})]

FUZZY_MATCH_THRESHOLD = 85


class CycloneDXBaseModel(BaseModel):
    """
    Base CycloneDX data model
    """

    class Config(HopprBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config options for CycloneDXBaseModel"

    # Defining as ClassVar to allow dynamic model creation using custom root types
    deep_merge: ClassVar[bool] = False
    flatten: ClassVar[bool] = False
    observers: ClassVar[dict[object, Callable]] = {}
    unique_id_map: ClassVar[UniqueIDMap]

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(self.unique_id_callback())

    def __init__(self, **data):
        super().__init__(**data)

        unique_id = self.unique_id_callback()
        type(self).unique_id_map[unique_id] = self

    def _has_field(self, field_name: str) -> bool:
        return hasattr(self, field_name) and (getattr(self, field_name) or field_name in list(self.__fields_set__))

    @staticmethod
    def _is_list_of(obj_type: type, field: Any) -> bool:
        """
        Checks if the provided field is a list of the specified type
        """
        return isinstance(field, list) and all(isinstance(item, obj_type) for item in field)

    def _merge_field(self, target_field_name: str, source_field: Any) -> None:
        """
        Merges `source_field` into the field referenced by `target_field_name`
        """
        merged_field = getattr(self, target_field_name)
        field_type = type(merged_field)

        if isinstance(field_type, type(BaseModel)):
            merged_field = CycloneDXBaseModel.create(model=merged_field)
            source_field = CycloneDXBaseModel.create(model=source_field)
            merged_field.merge(source_field)
        elif self._is_list_of(BaseModel, merged_field):
            merged_field = hoppr.utils.dedup_list([CycloneDXBaseModel.create(model=_field) for _field in merged_field])
            source_field = [CycloneDXBaseModel.create(model=_field) for _field in source_field or []]
            self._merge_field_items(merged_field, source_field)

        setattr(self, target_field_name, merged_field)

    @staticmethod
    def _merge_field_items(target_field: list[CycloneDXBaseModel], source_field: list[CycloneDXBaseModel]) -> None:
        """
        Merges the items from `source_field` into `target_field`
        """
        for source_item in source_field:
            if source_item in target_field:
                merged_item = target_field[target_field.index(source_item)]
                merged_item.merge(source_item)
            else:
                target_field.append(source_item)

    def unique_id_callback(self) -> str:
        """
        Default callback method to get a model object's unique ID
        """
        try:
            callback = {
                "Advisory": lambda obj: obj.url,
                "Commit": lambda obj: obj.uid,
                "Component": lambda obj: obj.bom_ref,
                "Copyright": lambda obj: obj.text,
                "Dependency": lambda obj: obj.ref,
                "ExternalReference": lambda obj: f"{obj.type}-{obj.url}",
                "License": lambda obj: obj.id or obj.name or repr(self),
                "LicenseChoice": lambda obj: obj.license or obj.expression or repr(self),
                "Note": lambda obj: obj.text,
                "Reference": lambda obj: obj.id,
                "Sbom": lambda obj: obj.serialNumber,
                "Service": lambda obj: obj.bom_ref or f"{obj.name}-{obj.version}",
                "Signer": lambda obj: obj.value,
                "Vulnerability": lambda obj: obj.id or repr(self),
            }[type(self).__name__]

            return callback(self)
        except KeyError:
            return repr(self)

    @classmethod
    def create(cls: type[AnyCycloneDXModel], model: BaseModel) -> AnyCycloneDXModel:
        """
        Update a BaseModel object with CycloneDXBaseModel attributes and methods

        Args:
            model (BaseModel): The BaseModel object to update

        Returns:
            AnyCycloneDXModel: The updated BaseModel object
        """
        model_cls = cls.make_model(name=type(model).__name__)
        return model_cls(**model.dict(by_alias=True, exclude_none=True, exclude_unset=True))  # pyright: ignore

    @classmethod
    @functools.cache
    def make_model(cls: type[AnyCycloneDXModel], name: str) -> type[AnyCycloneDXModel]:
        """
        Dynamically create a model class suitable for merging

        Args:
            name (str): Name of the existing model

        Returns:
            type[AnyCycloneDXModel]: The generated model class
        """
        # Return explicitly defined models directly
        if name in {"Component", "ExternalReference", "Hash", "License", "LicenseChoice", "Property"}:
            return sys.modules[__name__].__dict__[name]

        model_cls = hoppr_cyclonedx_models.cyclonedx_1_4.__dict__[name]

        merge_model = create_model(model_cls.__name__, __base__=(cls, model_cls), __module__=__name__)

        # Set model's pydantic `Config` class and `__hash__` method
        setattr(merge_model, "__config__", cls.Config)

        # Add `unique_id_map` class attribute for caching model objects
        merge_model.__class_vars__.add("unique_id_map")
        merge_model.__annotations__["unique_id_map"] = "ClassVar[UniqueIDMap]"
        setattr(merge_model, "unique_id_map", {})

        # Add updated model to current module and make importable from other modules
        setattr(sys.modules[__name__], merge_model.__name__, merge_model)
        __all__.append(merge_model.__name__)
        merge_model.update_forward_refs()

        return merge_model

    @classmethod
    def find(cls: type[AnyCycloneDXModel], unique_id: str) -> AnyCycloneDXModel | None:
        """
        Look up model object by its unique ID string

        Args:
            unique_id (str): Unique ID string to look up

        Returns:
            AnyCycloneDXModel | None: Model object if found, otherwise None
        """
        return cls.unique_id_map.get(unique_id)

    def merge(self: AnyCycloneDXModel, other: AnyCycloneDXModel) -> None:
        """
        Merge model instance of same type into self

        Args:
            other (AnyCycloneDXModel): Model object to merge
        """
        if (self_type := type(self).__name__) != (other_type := type(other).__name__):
            raise TypeError(f"Type '{other_type}' cannot be merged into '{self_type}'")

        self.notify(data=f"  Merging '{type(self).__qualname__}' attributes...")

        for field_name in self.__fields__:
            self.notify(data=f"    Merging field '{type(self).__qualname__}.{field_name}'...")

            source_field = getattr(other, field_name, None)

            if source_field is None:
                continue

            if not self._has_field(field_name):
                setattr(self, field_name, source_field)
            else:
                self._merge_field(field_name, source_field)

    def notify(self, data: str) -> None:
        """
        Call the callback function for all registered subscribers
        """
        for callback in self.observers.values():
            callback(data)

    def subscribe(self, observer: object, callback: Callable) -> None:
        """
        Register an observer
        """
        self.observers[observer] = callback

    def unsubscribe(self, observer: object) -> None:
        """
        Unregister an observer
        """
        self.observers.pop(observer, None)


def _extract_components(components: list[Component]) -> list[Component]:
    """
    Explicitly set scope of flattened components to `exclude`
    """
    for component in components:
        setattr(component, "scope", "excluded")

    return hoppr.utils.dedup_list(components)


def _extract_sbom_components(external_refs: list[ExternalReference]) -> list[Component]:
    """
    Extracts `external_refs` of type "bom" and returns the set of their components
    """
    components: list[Component] = []

    for ref in _get_bom_refs(external_refs):
        sbom = Sbom.load(_resolve_sbom_source(ref.url))
        sbom.components = _extract_components(sbom.components)
        components.extend(sbom.components)
        external_refs.remove(ref)

    return components


def _flatten_component(component: Component) -> list[Component]:
    """
    Helper function to flatten a component's subcomponents into a set
    """
    flattened = []

    for subcomponent in component.components or []:
        # Ensure validator is run to set `bom_ref`
        subcomponent = Component(**subcomponent.dict())
        setattr(subcomponent, "scope", "excluded")

        # Flatten nested components into top level components list
        flattened.append(subcomponent)

    component.components.clear()
    return flattened


def _get_bom_refs(external_refs: list[ExternalReference]) -> Iterator[ExternalReference]:
    """
    Get `externalReferences` of type "bom"
    """
    yield from (ref.copy(deep=True) for ref in (external_refs or []) if ref.type == "bom")


def _resolve_sbom_source(source: str) -> str | Path | DictStrAny:
    """
    Resolves an SBOM source as a file path, URL or `dict`
    """
    return Path(source.removeprefix("file://")).resolve() if source.startswith("file://") else source


def _validate_components(cls, components: list[Component]) -> list[Component]:
    """
    Validator to optionally flatten `components` list
    """
    if not cls.flatten:
        return components

    flattened = list(components)

    for component in components:
        flattened.extend(_flatten_component(component))

    return hoppr.utils.dedup_list(flattened)


def _validate_external_refs(cls, external_refs: list[ExternalReference], values: DictStrAny) -> list[ExternalReference]:
    """
    Validator to optionally resolve `externalReferences`
    """
    external_refs = [ExternalReference.create(ref) for ref in external_refs or []]

    if cls.deep_merge:
        external_ref_components = _extract_sbom_components(external_refs)
        values["components"] = hoppr.utils.dedup_list([*values.get("components", []), *external_ref_components])

    return external_refs


class ExternalReference(CycloneDXBaseModel, hoppr_cyclonedx_models.cyclonedx_1_4.ExternalReference):
    """
    ExternalReference data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for ExternalReference model"
        extra = Extra.allow

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Hash(CycloneDXBaseModel, hoppr_cyclonedx_models.cyclonedx_1_4.Hash):
    """
    Hash data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Hash model"
        extra = Extra.allow

    content: str = Field(
        default=...,
        examples=["3942447fac867ae5cdb3229b658f4d48"],
        title="Hash Content (value)",
        regex=r"^([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}|[a-fA-F0-9]{96}|[a-fA-F0-9]{128})$",
    )

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class License(CycloneDXBaseModel, hoppr_cyclonedx_models.cyclonedx_1_4.License):
    """
    License data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for License model"
        extra = Extra.allow

    unique_id_map: ClassVar[UniqueIDMap] = {}


class LicenseChoice(CycloneDXBaseModel):
    """
    LicenseChoice data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for LicenseChoice model"
        extra = Extra.allow

    license: License | None = None
    expression: str | None = Field(
        default=None,
        examples=["Apache-2.0 AND (MIT OR GPL-2.0-only)", "GPL-3.0-only WITH Classpath-exception-2.0"],
        title="SPDX License Expression",
    )

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Property(CycloneDXBaseModel, hoppr_cyclonedx_models.cyclonedx_1_4.Property):
    """
    Property data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Property model"
        extra = Extra.allow

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Component(CycloneDXBaseModel, hoppr_cyclonedx_models.cyclonedx_1_4.Component):
    """
    Component data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Component model"
        extra = Extra.allow

    bom_ref: str = Field(default=None, alias="bom-ref")  # type: ignore[assignment]
    components: list[Component] = Field(default=[])  # type: ignore[assignment]
    externalReferences: list[ExternalReference] = Field(default=[])  # type: ignore[assignment]
    hashes: list[Hash] = Field(default=[])  # type: ignore[assignment]
    licenses: list[LicenseChoice] = Field(default=[])  # type: ignore[assignment]
    properties: list[Property] = Field(default=[])  # type: ignore[assignment]

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}

    validate_components: classmethod = validator("components", allow_reuse=True, always=True)(_validate_components)
    validate_external_refs: classmethod = validator("externalReferences", allow_reuse=True)(_validate_external_refs)

    def __eq__(self, other: object) -> bool:
        try:
            if not isinstance(other, Component):
                raise TypeError

            self_purl = hoppr.utils.get_package_url(self.purl)
            other_purl = hoppr.utils.get_package_url(other.purl)
        except (TypeError, ValueError):
            return super().__eq__(other)

        qual_keys = hoppr.utils.dedup_list({**self_purl.qualifiers, **other_purl.qualifiers})

        def _qualifier_match(key: str) -> bool:
            # Compare only if both purls have a value for specified qualifier
            if key in self_purl.qualifiers and key in other_purl.qualifiers:
                return (
                    fuzz.ratio(self_purl.qualifiers.get(key, ""), other_purl.qualifiers.get(key, ""))
                    > FUZZY_MATCH_THRESHOLD
                )

            return True

        return all(
            [
                self_purl.name == other_purl.name,
                self_purl.type == other_purl.type,
                self_purl.namespace == other_purl.namespace,
                str(self_purl.version).removeprefix("v") == str(other_purl.version).removeprefix("v"),
                self_purl.subpath == other_purl.subpath,
                *[_qualifier_match(key) for key in qual_keys],
            ]
        )

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def validate_component(cls, values: DictStrAny) -> DictStrAny:
        """
        Validator to set a Component's `bom-ref` identifier if not set
        """
        if not any([values.get("purl"), values.get("bom-ref"), all([values.get("name"), values.get("version")])]):
            raise ValueError(
                "Either 'bom-ref' or 'purl' must be defined, or 'name' and 'version' must be defined on a component"
            )

        def _unescape_unicode(value: str) -> str:
            # Decode any unicode escape sequences, e.g. "\u0026" -> "&"
            return value.encode(encoding="utf-8").decode()

        if values.get("purl"):
            values["purl"] = _unescape_unicode(str(values["purl"]))

        bom_ref = str(
            values.get("purl")
            or f"{'@'.join(filter(None, [values.get('name'), values.get('version')]))}"
            or values.get("bom-ref")
        )

        values["bom-ref"] = _unescape_unicode(bom_ref)

        return values


Component.update_forward_refs()


class Sbom(CycloneDXBaseModel, hoppr_cyclonedx_models.cyclonedx_1_4.CyclonedxSoftwareBillOfMaterialsStandard):
    """
    Sbom data model derived from CycloneDXBaseModel
    """

    class Config(CycloneDXBaseModel.Config):  # pylint: disable=too-few-public-methods
        "Config for Sbom model"

    bomFormat: Literal["CycloneDX"] = "CycloneDX"  # type: ignore[assignment]
    components: list[Component] = Field(default=[])  # type: ignore[assignment]
    externalReferences: list[ExternalReference] = Field(default=[])  # type: ignore[assignment]
    serialNumber: str = Field(
        default="",
        regex=r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    )
    specVersion: str = "1.4"
    version: int = 1

    # Attributes not included in schema
    field_schema: Literal["http://cyclonedx.org/schema/bom-1.4.schema.json"] | None = Field(  # type: ignore[assignment]
        default=None, exclude=True, alias="$schema"
    )
    loaded_sboms: ClassVar[SbomRefMap] = {}
    unique_id_map: ClassVar[UniqueIDMap] = {}

    validate_components: classmethod = validator("components", allow_reuse=True, always=True)(_validate_components)
    validate_external_refs: classmethod = validator("externalReferences", allow_reuse=True)(_validate_external_refs)

    @validator("serialNumber", allow_reuse=True, always=True, pre=True)
    @classmethod
    def validate_serial_number(cls, serial_number: str | None) -> str:
        """
        Validator to generate SBOM serial number if None
        """
        return serial_number or uuid.uuid4().urn

    @classmethod
    def find_ref(cls, ref_type: Literal["local", "oci", "url"], location: str | Path) -> Sbom | None:
        """
        Look up SBOM object by reference

        Args:
            ref_type (Literal["local", "oci", "url"]): Type of SBOM reference
            location (str | Path): Location of SBOM reference

        Returns:
            Sbom | None: SBOM object if found, otherwise None
        """
        # pylint: disable=duplicate-code
        match ref_type:
            case "local":
                return cls.loaded_sboms.get(LocalFile(local=Path(location)), None)
            case "oci":
                return cls.loaded_sboms.get(OciFile(oci=str(location)), None)
            case "url":
                return cls.loaded_sboms.get(UrlFile(url=str(location)), None)
            case _:
                return None

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Sbom:
        """
        Load SBOM from local file, URL, or dict
        """
        # pylint: disable=duplicate-code
        match source:
            case dict():
                sbom = cls(**source)
            case Path():
                # Convert source to relative path if in current working directory subpath
                source = source.resolve()
                source = source.relative_to(Path.cwd()) if source.is_relative_to(Path.cwd()) else source

                sbom = cls.parse_file(source)
                cls.loaded_sboms[LocalFile(local=source)] = sbom
            case str():
                try:
                    sbom_dict = hoppr.net.load_url(source)
                    if not isinstance(sbom_dict, dict):
                        raise TypeError("URL SBOM was not loaded as dictionary")

                    sbom = cls.parse_obj(sbom_dict)
                    url_ref = UrlFile(url=source)
                    cls.loaded_sboms[url_ref] = sbom
                except (HopprLoadDataError, HTTPError) as ex:
                    raise HopprLoadDataError from ex

        return sbom
