from datetime import timedelta
import pandas as pd


def add_delayed_consumption_feature(hourly: pd.DataFrame,
                                    delay_hours: int) -> pd.DataFrame:
    """
    This function repeats the hourly consumption column, but the values are shifted forwards in 
    time by a certain amount of hours. This tells the model what the consumption was earlier that
    week, which happens to be a good predictor for future consumption.

    :param pd.DataFrame hourly: Dataframe with a DatetimeIndex index
    :param int delay_hours: The time shift of the column that will be added, in hours
    :returns: Dataframe with a DatetimeIndex index
    """

    shifted = hourly.groupby(by=['modelTargetId']).shift(freq=timedelta(
        hours=delay_hours))
    shifted_name = f'energyWh_{delay_hours}'
    shifted.rename(columns={'energyWh': shifted_name}, inplace=True)
    column_selection = ['modelTargetId', shifted_name]
    hourly = pd.merge(hourly.reset_index(),
                      shifted[column_selection].reset_index(),
                      how='left',
                      on=['modelTargetId',
                          'measurementTime']).set_index('measurementTime')
    return hourly
