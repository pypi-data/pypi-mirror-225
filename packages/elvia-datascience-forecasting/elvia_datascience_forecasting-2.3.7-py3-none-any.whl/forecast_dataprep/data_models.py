from dataclasses import dataclass
from enum import Enum
import json
import re
from typing import List, Optional, Union

import pandas as pd


### Abstractions to represent (a list of) either meteringpoints or substations
class ForecastTargetLevel(Enum):

    METERING_POINT = 1
    SUBSTATION = 2


class ForecastTarget:

    def __init__(self, identifier: Union[int, str]):
        if ForecastTargetList.get_type(identifier) is not None:
            self.identifier = identifier
        else:
            raise ValueError

    @property
    def level(self) -> ForecastTargetLevel:
        return ForecastTargetList.get_type(self.identifier)


class ForecastTargetList:

    def __init__(self,
                 identifiers: List[Union[str, int, ForecastTarget]],
                 allow_duplicates: bool = False,
                 enforce_int_meteringpoints: bool = True,
                 enforce_str_substations: bool = True) -> None:
        """
        Mixing strings and ints when instantiating is allowed, but the identifiers must all belong to the same ForecastTargetLevel
        """
        if not identifiers:
            raise ValueError
        if not isinstance(identifiers, list):
            raise TypeError

        self.identifiers: list = []
        self.allow_duplicates = allow_duplicates
        self.enforce_int_meteringpoints = enforce_int_meteringpoints
        self.enforce_str_substations = enforce_str_substations

        for i in identifiers:
            self.put(i)
            

    def put(self, identifier: Union[int, str, ForecastTarget]) -> None:
        level = self.get_type(identifier)
        if level is None:
            raise ValueError('The identifier does not look right')
        if level == ForecastTargetLevel.METERING_POINT:
            self._add_if_match_existing(identifier if not isinstance(
                identifier, ForecastTarget) else identifier.identifier)
        if level == ForecastTargetLevel.SUBSTATION:
            self._add_if_match_existing(identifier if not isinstance(
                identifier, ForecastTarget) else identifier.identifier)

    def _add_if_match_existing(self, identifier: Union[str, int]):
        if not self.identifiers or self.get_type(identifier) == self.get_type(
                self.identifiers[0]):
            if self.allow_duplicates or identifier not in set(
                    self.identifiers):
                if self.enforce_int_meteringpoints and self.get_type(
                        identifier) == ForecastTargetLevel.METERING_POINT:
                    self.identifiers.append(int(identifier))
                elif self.enforce_str_substations and self.get_type(
                        identifier) == ForecastTargetLevel.SUBSTATION:
                    self.identifiers.append(str(identifier))
                else:
                    self.identifiers.append(identifier)
            else:
                raise ValueError(
                    f'Duplicates were not allowed in this {__class__.__name__} instance'
                )
        else:
            raise ValueError(
                'Forecast targets must all be either substation or meteringpoint'
            )

    @staticmethod
    def get_type(
        identifier: Union[str, int, ForecastTarget]
    ) -> Optional[ForecastTargetLevel]:
        if isinstance(identifier, ForecastTarget):
            return identifier.level
        elif isinstance(
                identifier, int
        ) and identifier > 707057500014300000 and identifier < 707057500087400700:
            return ForecastTargetLevel.METERING_POINT
        elif isinstance(identifier, str) and re.fullmatch(
                r"7070575000[\d]{8}", identifier):
            return ForecastTargetLevel.METERING_POINT
        elif isinstance(identifier, str) and re.fullmatch(
                r"[A-ZÆØÅ\d\- ]+",
                identifier.upper()) and len(identifier) >= 4:
            return ForecastTargetLevel.SUBSTATION
        return None

    @property
    def level(self) -> ForecastTargetLevel:
        return self.get_type(self.identifiers[0])

    @staticmethod
    def from_json(target_model_list: str) -> 'ForecastTargetList':
        return ForecastTargetList(json.loads(target_model_list))

    def to_json(self) -> str:
        return json.dumps(self.identifiers)


### Dataframe groupings


@dataclass
class EnrichmentFeaturesBundle:
    """
    Dataframes used in the enrichment stage
    """
    weekly_average: pd.DataFrame
    school_holidays: pd.DataFrame
    national_holidays: pd.DataFrame
    prices: pd.DataFrame


@dataclass
class Dataframes:
    """
    This class is a convenient encapsulation of diverse dataframes
    """
    hourly_consumption: pd.DataFrame
    ingested: EnrichmentFeaturesBundle


@dataclass
class IngestmentOutput:
    """
    Dataframes that result from the ingestion process
    """
    ingested_hourly_data: pd.DataFrame
    ingested_metadata: pd.DataFrame
    enrichment_features: EnrichmentFeaturesBundle
