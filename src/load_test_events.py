import sqla_yaml_fixtures
from database import database as db
from models import Base
from datetime import datetime, timedelta
from configuration import conf


# run only locally with already registered test user
def main():
    soon = datetime.now() + timedelta(hours=1)
    fixture = """
    - User:
      - tg_id: 0
        city_id: 1
    - Event:
      - creator_id: 1
        name: Not validated event 1
        description: Not validated event 1
        start_date: {0}
        end_date: {0}
      - creator_id: 1
        name: Validated event 1
        description: Validated event 1
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 10
        interest_rating: 5
      - creator_id: 1
        name: Validated event 2
        description: Validated event 2
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 9
        interest_rating: 6
      - creator_id: 1
        name: Validated event 3
        description: Validated event 3
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 8
        interest_rating: 6
      - creator_id: 1
        name: Validated event 4
        description: Validated event 4
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 7
        interest_rating: 7
      - creator_id: 1
        name: Validated event 5
        description: Validated event 5
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 7
        interest_rating: 6
      - creator_id: 1
        name: Validated event 6
        description: Validated event 6
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 5
        interest_rating: 5
      - creator_id: 1
        name: Validated event 7
        description: Validated event 7
        start_date: {0}
        end_date: {0}
        completed_validations: {1}
        quality_rating: 5
        interest_rating: 6
    """.format(soon, conf.required_validations)
    Base.metadata.create_all(db.engine)
    sqla_yaml_fixtures.load(Base, db.session, fixture)


if __name__ == '__main__':
    main()
