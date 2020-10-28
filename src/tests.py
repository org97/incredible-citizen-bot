import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base, User, Event
from database import database as db
import sqla_yaml_fixtures
from datetime import datetime, timedelta
from configuration import conf


class TestUserModelLogic(unittest.TestCase):
    def setUp(self):
        # inject test database and session
        db.engine = create_engine('sqlite:///:memory:',
                                  echo=True)
        Session = sessionmaker(bind=db.engine)
        db.session = Session()
        Base.metadata.create_all(db.engine)
        conf.max_events_validations_per_day = 1

    def test__get_not_finished_validation__true_if_there_is_one_for_today(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 1
                event_id: 1
            """
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).first()
        self.assertTrue(user.get_not_finished_validation(),
                        "User should have not finished validation if there is one from today")

    def test__get_not_finished_validation__false_if_there_is_one_for_yesterday(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 1
                event_id: 1
                call_to_violence: False
                quality_rating: 5
                created: {}
            """.format(datetime.now() - timedelta(1))
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).first()
        self.assertFalse(user.get_not_finished_validation(),
                         "User should not have not finished validation if there is one from yesterday")

    def test__get_not_finished_validation__false_if_there_is_one_finished_today(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 1
                event_id: 1
                call_to_violence: True
            """
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).first()
        self.assertFalse(user.get_not_finished_validation(),
                         "User should not have not finished validation if there is finished from today")

    def test__can_validate__true_if_did_not_validate_at_all(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 1
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 2
                event_id: 1
                quality_rating: 5
                interest_rating: 5
            """
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).first()
        self.assertTrue(user.can_validate_today,
                        "User should be able to validate if there were no validations done before")

    def test__can_validate__true_if_did_not_validate_yet_today(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 1
                event_id: 1
                quality_rating: 5
                interest_rating: 5
                created: {}
            """.format(datetime.now() - timedelta(1))
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).filter(User.tg_id == 1).first()
        self.assertTrue(user.can_validate_today,
                        "User should be able to validate if there were no validations done today")

    def test__can_validate__false_if_has_not_finished_validation_today(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 1
                event_id: 1
                call_to_violence: False
                quality_rating: 5
            """.format(datetime.now() + timedelta(1))
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).filter(User.tg_id == 1).first()
        self.assertFalse(user.can_validate_today,
                         "User should be able to validate if today's validation is not finished yet")

    def test__can_validate__false_if_already_validated_today(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
              - creator_id: 2
                name: Event 2
                description: short 2
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            - Validation:
              - validator_id: 1
                event_id: 1
                quality_rating: 5
                interest_rating: 5
                created: {}
              - validator_id: 1
                event_id: 2
                call_to_violence: True
            """.format(datetime.now() - timedelta(1))
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        user = db.session.query(User).filter(User.tg_id == 1).first()
        self.assertFalse(user.can_validate_today,
                         "User should not be able to validate if there were a validation done today")

    def test__available_events__excludes_events_posted_by_user(self):
        fixture = """
            - User:
              - tg_id: 1
            - Event:
              - creator_id: 1
                name: Event 1
                description: short 1
                start_date: 2020-10-25 14:00:00
                end_date: 2020-10-25 14:00:00
            """
        sqla_yaml_fixtures.load(Base, db.session, fixture)

        events = self.available_events()
        self.assertEqual(
            len(events), 0, "We should exclude events posted by the user")

    def test__available_events__selects_event_with_active_start_date(self):
        fixture = """
            - User:
              - tg_id: 1
              - tg_id: 2
            - Event:
              - creator_id: 2
                name: Event 1
                description: short 1
                start_date: 2030-10-25 14:00:00
                end_date: 2030-10-25 14:00:00
              - creator_id: 2
                name: Event 2
                description: short 2
                start_date: {}
                end_date: 2046-10-25 14:00:00
            """.format(datetime.now() - timedelta(1))
        sqla_yaml_fixtures.load(Base, db.session, fixture)

        events = self.available_events()
        self.assertEqual(
            len(events), 1, "We have only one event with start date in future")
        self.assertEqual(events[0].name, 'Event 1')

    def available_events(self):
        user = db.session.query(User).first()
        return user.available_events_for_validation()


class TestEventsModelLogic(unittest.TestCase):
    def setUp(self):
        # inject test database and session
        db.engine = create_engine('sqlite:///:memory:',
                                  echo=True)
        Session = sessionmaker(bind=db.engine)
        db.session = Session()
        Base.metadata.create_all(db.engine)
        # inject test configuration params
        conf.required_validations = 1

    def test__get_top_validated_events__time_constraints(self):
        soon = datetime.now() + timedelta(seconds=1)
        shortly_before = datetime.now() - timedelta(hours=1)
        fixture = """
            - User:
              - tg_id: 1
            - Event:
              - creator_id: 1
                name: Event 1
                description: Valid time constraints
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 1
                quality_rating: 1
                interest_rating: 1
              - creator_id: 1
                name: Event 2
                description: Start date is today, but time is in past
                start_date: {1}
                end_date: {1}
                is_blocked: False
                completed_validations: 1
                quality_rating: 1
                interest_rating: 1
            """.format(soon, shortly_before)
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        events = Event.get_top_validated_events(user=User.by(tg_id=1))
        self.assertTrue(len(events) == 1,
                        "User should get validated events with valid time constraints")
        self.assertTrue(events[0].name == 'Event 1', "Wrong event is picked")

    def test__get_top_validated_events__returns_not_blocked_events(self):
        soon = datetime.now() + timedelta(seconds=1)
        fixture = """
            - User:
              - tg_id: 1
            - Event:
              - creator_id: 1
                name: Event 1
                description: Not blocked
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 1
                quality_rating: 1
                interest_rating: 1
              - creator_id: 1
                name: Event 2
                description: Blocked
                start_date: {0}
                end_date: {0}
                is_blocked: True
                completed_validations: 1
                quality_rating: 1
                interest_rating: 1
            """.format(soon)
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        events = Event.get_top_validated_events(user=User.by(tg_id=1))
        self.assertTrue(len(events) == 1,
                        "User should get not blocked events")
        self.assertTrue(events[0].name == 'Event 1', "Wrong event is picked")

    def test__get_top_validated_events__returns_validated_events(self):
        conf.required_validations = 2
        soon = datetime.now() + timedelta(seconds=1)
        fixture = """
            - User:
              - tg_id: 1
            - Event:
              - creator_id: 1
                name: Event 1
                description: Enough validations
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 2
                quality_rating: 1
                interest_rating: 1
              - creator_id: 1
                name: Event 2
                description: Not enough validations
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 1
                quality_rating: 1
                interest_rating: 1
              - creator_id: 1
                name: Event 3
                description: No validations
                start_date: {0}
                end_date: {0}
            """.format(soon)
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        events = Event.get_top_validated_events(user=User.by(tg_id=1))
        self.assertTrue(len(events) == 1,
                        "User should get only validated events")
        self.assertTrue(events[0].name == 'Event 1', "Wrong event is picked")

    def test__get_top_validated_events__returns_properly_sorted_events(self):
        conf.polling_candidates_by_quality_rating = 2
        conf.polling_candidates = 1
        soon = datetime.now() + timedelta(seconds=1)
        fixture = """
            - User:
              - tg_id: 1
            - Event:
              - creator_id: 1
                name: Event 1
                description: Top quality rating, lowest interest rating.
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 1
                quality_rating: 3
                interest_rating: 1
              - creator_id: 1
                name: Event 2
                description: Lowest quality rating, top interest rating.
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 1
                quality_rating: 1
                interest_rating: 3
              - creator_id: 1
                name: Event 3
                description: Mid quality and interest rating.
                start_date: {0}
                end_date: {0}
                is_blocked: False
                completed_validations: 1
                quality_rating: 2
                interest_rating: 2
            """.format(soon)
        sqla_yaml_fixtures.load(Base, db.session, fixture)
        events = Event.get_top_validated_events(user=User.by(tg_id=1))
        self.assertTrue(len(events) == 1,
                        "User should get only properly sorted events")
        self.assertTrue(events[0].name == 'Event 3', "Wrong event is picked")


if __name__ == '__main__':
    unittest.main()
