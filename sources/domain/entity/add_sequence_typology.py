import pandas as pd


class SequenceTypes(str):
    court = "court"
    moyen = "moyen"
    long = "long"


def classify_sequence(sequence: tuple[str]) -> SequenceTypes:
    sequence_length = len(sequence)
    if sequence_length <= 5:
        return SequenceTypes.court
    if sequence_length <= 8:
        return SequenceTypes.moyen
    return SequenceTypes.long


def add_sequence_typology(df: pd.DataFrame) -> pd.DataFrame:
    df["typology"] = df["floor_sequence"].apply(classify_sequence)
    return df
