import logging
import math


class Configuration:
    # If you change this date format make sure to update messages in strings.py
    date_format = '%d.%m.%Y %H:%M'

    # The earliest start time from now in hours for new events. Events ideas should be validated that takes time.
    # Does not make scense to make this number too low.
    earliest_event_start_time_from_now = 4

    # The latest start time from now in hours for new events.
    # It does not make sence to propose new events that are too distant in future.
    latest_event_start_time_from_now = 24 * 7

    # Limitation on event name/description
    # When selecting an event for paricipation 'name' is displayed.
    # Description should take into considiration the 4096 symbols limit on message size in telegram.
    event_name_max_length = 100
    event_description_max_length = 3500

    # Limitation on the amount of events that any person can propose within a day
    max_events_ideas_per_day = 2

    # Limitation on the amount of events that any person can validatin within a day
    max_events_validations_per_day = 2

    # When picking events for validation, this number will be considered as pseudo-validations
    # with the highes possible rate to put new ideas to the higest priority for new validators.
    # E.g. for new_event_priority_factor = 3, new_event_weighted_position = 8 new events will
    # have a rating equal to 8.0, and after the first validation with
    # quality_rating = 9 and interest_rating = 6, the rating will become (3 * 8 + 1 * (9 + 6) / 2) / (3 + 1) = 7.875
    # The higher the rating, the more chances to pick this idea for new validators.
    new_event_priority_factor = 3
    new_event_weighted_position = 8

    # Minimum required amount of validations to consider event as validated
    required_validations = 15

    # Blocking validations is a validation with a "red flag":
    # - event calls to violence
    # - or event quality is super low (two zeros for quality rating and interest rating)
    # If blocking validations exceeds this number, the creator of the event will be blocked in the system as a creator / validator
    blocking_validations = math.ceil(required_validations / 3)

    # Amount of candidates for polling that will be sorted by interest rating
    # Both quality/interest ratings are formed by validators
    polling_candidates_by_quality_rating = 15

    # Amount of candidates presented to users
    # This number should be not more than 10
    polling_candidates = 3

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)


conf = Configuration()
