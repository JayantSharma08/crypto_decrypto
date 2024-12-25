from typing import Literal

from price_predictor import PricePredictor
from quixstreams import Application


def run(
    # the kafka topic that triggers the inference service
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    # information about the model to use for inference
    pair_to_predict: str,
    candle_seconds: int,
    prediction_seconds: int,
    model_status: Literal['Development', 'Staging', 'Production'],
    # where to save the predictions
    elastic_search_sink,
):
    """
    Run the inference job as a Quix Streams application.

    Steps:
    1 - Load the model from the model registry
    2 - Generate predictions
    2 - Save predictions to Elastic Search

    Args:
        kafka_broker_address: the address of the Kafka broker
        kafka_input_topic: the topic to listen to for new data
        kafka_consumer_group: the consumer group to use
        pair_to_predict: the pair to predict
        candle_seconds: the number of seconds per candle
        prediction_seconds: the number of seconds into the future to predict
        model_status: the status of the model in the model registry
        elastic_search_sink: the sink to save the predictions to
    """
    # Quix Streams application to handles all low-level communication with Kafka
    app = Application(
        broker_address=kafka_broker_address,
        consumer_config=kafka_consumer_group,
    )

    input_topic = app.topic(name=kafka_input_topic, value_deserializer='json')

    # Load the model from the model registry and the necessary metadata at initialization
    # It exposes a `predict` method that can be used to generate predictions
    price_predictor = PricePredictor(
        pair_to_predict=pair_to_predict,
        candle_seconds=candle_seconds,
        prediction_seconds=prediction_seconds,
        model_status=model_status,
    )

    # Streaming Dataframe to define the business logic, aka the transformations from
    # input data to output data
    sdf = app.dataframe(input_topic)

    # We only react to candles with the given `candle_seconds` frequency
    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    # Generate a new prediction
    sdf = sdf.apply(lambda _: price_predictor.predict())

    # Save the predictions to Elastic Search sink
    sdf.sink(elastic_search_sink)

    app.run()


if __name__ == '__main__':
    from config import inference_config as config

    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        pair_to_predict=config.pair_to_predict,
        candle_seconds=config.candle_seconds,
        prediction_seconds=config.prediction_seconds,
        model_status=config.model_status,
        elastic_search_sink=None,
    )
