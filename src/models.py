from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    UniqueConstraint,
    CheckConstraint,
    func,
    or_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from database import database as db
import strings as s
from configuration import conf


Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<City(id='%s', name='%s')>" % (self.id, self.name)

    @staticmethod
    def by(name):
        return db.session.query(City).filter(City.name == name).first()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship(City, backref=backref('users', uselist=True))
    is_blocked = Column(Boolean, default=False)

    def __repr__(self):
        return "<User(id='%s', tg_id='%s', city='%s')>" % (self.id, self.tg_id, self.city)

    @staticmethod
    def create(tg_id, city):
        user = User(tg_id=tg_id, city=city)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def by(tg_id):
        return db.session.query(User).filter(User.tg_id == tg_id).first()

    def update(self, city: City):
        self.city = city
        db.session.commit()
        return self

    @property
    def can_create_new_events(self):
        """
        Check if the person allowed to create a new event today based on 'max_events_ideas_per_day'
        configuration parameter
        """
        created_today = db.session.query(func.count(Event.id)).filter(
            Event.creator == self, Event.created >= datetime.now().date()).scalar()
        return created_today < conf.max_events_ideas_per_day

    def get_not_finished_validation(self):
        '''
        returns a validation if there is one in progress for today
        '''
        validation_in_progress = db.session.query(Validation) \
            .filter(Validation.validator == self,
                    # note: Validation.call_to_violence != True will not work
                    Validation.call_to_violence == None) \
            .order_by(Validation.created.desc()) \
            .first()
        if validation_in_progress and validation_in_progress.created.date() == datetime.now().date():
            return validation_in_progress
        return None

    @property
    def can_validate_today(self):
        '''
        returns true if user has not reached the limit yet
        '''
        today_validations = db.session.query(Validation) \
            .filter(Validation.validator == self,
                    func.date(Validation.created) == datetime.now().date()) \
            .all()
        return len(today_validations) < conf.max_events_validations_per_day

    def pick_event_for_validation(self):
        events = self.available_events_for_validation()
        # TODO: should we pick some random event from top N?
        return events[0] if events else []

    def available_events_for_validation(self):
        # - exclude events submitted by the user
        # - exclude blocked events
        # - exclude already validated events
        # - get events with deadline > now
        # - completed_validations < threshold
        # - events from user city and geo-independent events should have
        #   a priority, then all other events
        events = db.session.query(Event) \
            .filter(Event.creator != self,
                    Event.is_blocked == False,
                    Event.completed_validations < conf.required_validations,
                    # TODO: add some delta to now()
                    Event.start_date > datetime.now(),
                    or_(Event.city == self.city, Event.city == None)) \
            .order_by(Event.validation_priority.desc()) \
            .all()

        if not events:
            # exclude city priority
            events = db.session.query(Event) \
                .filter(Event.creator != self,
                        Event.is_blocked == False,
                        Event.completed_validations < conf.required_validations,
                        Event.start_date > datetime.now()) \
                .order_by(Event.validation_priority.desc()) \
                .all()
        return events


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship(User, backref=backref('events', uselist=True))
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship(City, backref=backref('events', uselist=True))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created = Column(DateTime, default=datetime.now())\

    # the following columns are updated on every completed validation
    is_blocked = Column(Boolean, default=False)
    blocked_users_count = Column(Integer, default=0)
    completed_validations = Column(Integer, default=0)
    quality_rating = Column(Float, default=0)
    interest_rating = Column(Float, default=0)

    __table_args__ = (CheckConstraint(
        'end_date >= start_date', name='ck_end_date_gt_start_date'),)

    @hybrid_property
    def validation_priority(self):
        return (conf.new_event_priority_factor * conf.new_event_weighted_position +
                self.completed_validations * (self.quality_rating + self.interest_rating) / 2) / \
            (conf.new_event_priority_factor + self.completed_validations)

    def __repr__(self):
        return "<Event(id='%s', creator='%s', city='%s' name='%s', description='%s', created='%s')>" % \
            (self.id, self.creator, self.city,
             self.name, self.description, self.created)

    @staticmethod
    def create(creator, city, name, description, start_date, end_date):
        event = Event(creator=creator,
                      city=city,
                      name=name,
                      description=description,
                      start_date=start_date,
                      end_date=end_date)
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def by(id):
        return db.session.query(Event).filter(Event.id == id).first()

    @property
    def time(self):
        time = self.start_date.strftime(conf.date_format)
        if self.start_date != self.end_date:
            time += ' - {}'.format(self.end_date.strftime(conf.date_format))
        return time

    def html_full_description(self):
        return s.event_description_format.format(
            self.city.name if self.city else s.geo_independent_event,
            self.name,
            self.time,
            self.description)

    def html_short_description(self):
        return s.event_short_description_format.format(self.name, self.time)

    def html_participants(self):
        return s.confirmed_participants.format(len(self.participations))

    @staticmethod
    def get_top_validated_events(user):
        # Take events with:
        # - same as user city or geo-independent
        # - valid time constraint
        # - blocked == False
        # - completed validations >= conf.required_validations
        # - sorted by quality rating
        # - take top N cadidates (configuration parameter)
        # - sort by interest rating
        # - return top M (configuration parameter)
        return db.session.query(Event) \
            .filter(or_(Event.city == user.city, Event.city == None),
                    func.date(Event.start_date) == datetime.now().date(),
                    Event.start_date > datetime.now(),
                    Event.is_blocked == False,
                    Event.completed_validations >= conf.required_validations) \
            .order_by(Event.quality_rating.desc()) \
            .limit(conf.polling_candidates_by_quality_rating) \
            .from_self() \
            .order_by(Event.interest_rating.desc()) \
            .limit(conf.polling_candidates) \
            .all()


class Validation(Base):
    __tablename__ = 'validations'

    id = Column(Integer, primary_key=True)
    validator_id = Column(Integer, ForeignKey('users.id'))
    validator = relationship(
        User, backref=backref('validations', uselist=True))
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship(Event, backref=backref('validations', uselist=True))
    call_to_violence = Column(Boolean, nullable=True)
    quality_rating = Column(Integer, nullable=True)
    interest_rating = Column(Integer, nullable=True)
    created = Column(DateTime, default=datetime.now())

    __table_args__ = (UniqueConstraint(
        'validator_id', 'event_id', name='uq_validator_event'),)

    def __repr__(self):
        return "<Validation(id='%s', validator='%s', event='%s', call_to_violence='%s', quality_rating='%s', interest_rating='%s', created='%s')>" % \
            (self.id, self.validator, self.event, self.call_to_violence,
             self.quality_rating, self.interest_rating, self.created)

    @staticmethod
    def create(validator, event):
        validation = Validation(validator=validator, event=event)
        db.session.add(validation)
        db.session.commit()
        return validation

    @property
    def is_completed(self):
        return self.call_to_violence or \
            (self.call_to_violence is not None and
             self.quality_rating is not None and
             self.interest_rating is not None)

    def update(self, call_to_violence=None, quality_rating=None, interest_rating=None):
        """
        Makes necessary checks and updates event and related event fields.
        """
        if call_to_violence is not None:
            self.call_to_violence = call_to_violence
        if quality_rating is not None:
            self.quality_rating = quality_rating
        if interest_rating is not None:
            self.interest_rating = interest_rating

        if self.is_completed:
            # never None
            if self.call_to_violence:
                self.event.blocked_users_count += 1
            else:
                # never None
                self.event.quality_rating = (self.event.quality_rating * self.event.completed_validations +
                                             self.quality_rating) / (self.event.completed_validations + 1)
                self.event.interest_rating = (self.event.interest_rating * self.event.completed_validations +
                                              self.interest_rating) / (self.event.completed_validations + 1)

                # if both quality_rating and interest_rating equal to zero this is a red flag
                if self.quality_rating == 0 and self.interest_rating == 0:
                    self.event.blocked_users_count += 1

            self.event.completed_validations += 1

            is_blocked = self.event.blocked_users_count >= conf.blocking_validations
            self.event.is_blocked = is_blocked
            self.event.creator.is_blocked = is_blocked

        db.session.commit()


class Participation(Base):
    __tablename__ = 'participation'

    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey('users.id'))
    participant = relationship(
        User, backref=backref('participations', uselist=True))
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship(Event, backref=backref(
        'participations', uselist=True))
    confirmation = Column(Boolean, nullable=True)
    success_rating = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint(
        'participant_id', 'event_id', name='uq_participant_event'),)

    def __repr__(self):
        return "<Participation(id='%s', participant='%s', event='%s', confirmation='%s', success_rating='%s')>" % \
            (self.id, self.participant, self.event,
             self.confirmation, self.success_rating)

    @staticmethod
    def create(participant, event):
        participation = Participation(participant=participant, event=event)
        db.session.add(participation)
        db.session.commit()
        return participation

    def update(self, confirmation=None, success_rating=None):
        if confirmation is not None:
            self.confirmation = confirmation
        if success_rating is not None:
            self.success_rating = success_rating
        db.session.commit()

    @staticmethod
    def delete_active(user):
        participation = Participation.active(user=user)
        db.session.delete(participation)
        db.session.commit()

    @staticmethod
    def active(user):
        return db.session.query(Participation).filter(
            Participation.participant == user,
            Participation.confirmation == None).first()

    def html_checkout_question(self):
        return s.did_you_participate.format(self.event.name, self.event.time)
