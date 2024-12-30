from datetime import datetime, timezone

import hopsworks
from hsfs.feature import Feature
import pandas as pd

# from hopsworks.exceptions import FeatureStoreException
from loguru import logger
from quixstreams.sinks.base import BatchingSink, SinkBatch


class HopsworksFeatureStoreSink(BatchingSink):
    """
    Some sink writing data to a database
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],
        feature_group_event_time: str,
        feature_group_materialization_interval_minutes: int,
    ):
        """
        Establish a connection to the Hopsworks Feature Store
        """
        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version
        self.materialization_interval_minutes = feature_group_materialization_interval_minutes

        # Establish a connection to the Hopsworks Feature Store
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._fs = project.get_feature_store()
                # Define the schema for the feature group
        feature_group_schema = [
            Feature(name='pair', type='string'),
            Feature(name='timestamp_ms', type='bigint'),
            Feature(name='open', type='double'),
            Feature(name='high', type='double'),
            Feature(name='low', type='double'),
            Feature(name='close', type='double'),
            Feature(name='volume', type='double'),
            Feature(name='window_start_ms', type='bigint'),
            Feature(name='window_end_ms', type='bigint'),
            Feature(name='candle_seconds', type='bigint'),
            Feature(name='rsi_9', type='double'),
            Feature(name='rsi_14', type='double'),
            Feature(name='rsi_21', type='double'),
            Feature(name='macd', type='double'),
            Feature(name='macd_signal', type='double'),
            Feature(name='macd_hist', type='double'),
            Feature(name='bbands_upper', type='double'),
            Feature(name='bbands_middle', type='double'),
            Feature(name='bbands_lower', type='double'),
            Feature(name='stochrsi_fastk', type='double'),
            Feature(name='stochrsi_fastd', type='double'),
            Feature(name='adx', type='double'),
            Feature(name='volume_ema', type='double'),
            Feature(name='ichimoku_conv', type='double'),
            Feature(name='ichimoku_base', type='double'),
            Feature(name='ichimoku_span_a', type='double'),
            Feature(name='ichimoku_span_b', type='double'),
            Feature(name='mfi', type='double'),
            Feature(name='atr', type='double'),
            Feature(name='price_roc', type='double'),
            Feature(name='sma_7', type='double'),
            Feature(name='sma_14', type='double'),
            Feature(name='sma_21', type='double'),
            Feature(name='coin', type='string')
        ]

        # Get the feature group
        self._feature_group = self._fs.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,
            description="Feature group for storing technical indicators",
            features=feature_group_schema
        )

        # set the materialization interval
        try:
            self._feature_group.materialization_job.schedule(
                cron_expression=f'0 0/{self.materialization_interval_minutes} * ? * * *',
                start_time=datetime.now(tz=timezone.utc),
            )
        # TODO: handle the FeatureStoreException
        except Exception as e:
            logger.error(f'Failed to schedule materialization job: {e}')

        # call constructor of the base class to make sure the batches are initialized
        super().__init__()

    def write(self, batch: SinkBatch):
        # Transform the batch into a pandas DataFrame
        data = [item.value for item in batch]
        data = pd.DataFrame(data)
        data = data.fillna(0) 

        self._feature_group.insert(data)

        # try:
        #     # Try to write data to the db
        #     self._feature_group.insert(data)
        # except Exception as err:  # Capture the original exception
        #     # In case of timeout, tell the app to wait for 30s
        #     # and retry the writing later

        #     raise SinkBackpressureError(
        #         retry_after=30.0,
        #         topic=batch.topic,
        #         partition=batch.partition,
        #     ) from err  # Chain the exception
