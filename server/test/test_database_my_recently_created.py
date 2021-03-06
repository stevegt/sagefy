from conftest import create_user_in_db
from database.my_recently_created import get_my_recent_proposals, \
    get_proposal_entity_versions, get_my_recently_created_units, \
    get_my_recently_created_subjects
import rethinkdb as r


def create_some_proposals(posts_table, units_table, subjects_table, db_conn):
    """
    Create some proposals to check the calls.
    """

    posts_table.insert([{
        'kind': 'proposal',
        'user_id': 'abcd1234',
        'entity_versions': [{
            'kind': 'subject', 'id': 'A1',
        }, {
            'kind': 'unit', 'id': 'D1',
        }],
    }, {
        'kind': 'proposal',
        'user_id': '5678xywz',
        'entity_versions': [{
            'kind': 'subject', 'id': 'B1',
        }, {
            'kind': 'unit', 'id': 'E1',
        }],
    }, {
        'kind': 'proposal',
        'user_id': 'abcd1234',
        'entity_versions': [{
            'kind': 'subject', 'id': 'C1',
        }, {
            'kind': 'unit', 'id': 'F1',
        }],
    }]).run(db_conn)
    subjects_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'status': 'accepted',
        'created': r.now(),
    }, {
        'id': 'B1',
        'entity_id': 'B',
        'status': 'accepted',
        'created': r.now(),
    }, {
        'id': 'C1',
        'entity_id': 'C',
        'status': 'accepted',
        'created': r.now(),
    }]).run(db_conn)
    units_table.insert([{
        'id': 'D1',
        'entity_id': 'D',
        'status': 'accepted',
        'created': r.now(),
    }, {
        'id': 'E1',
        'entity_id': 'E',
        'status': 'accepted',
        'created': r.now(),
    }, {
        'id': 'F1',
        'entity_id': 'F',
        'status': 'accepted',
        'created': r.now(),
    }]).run(db_conn)


def test_get_my_recent_proposals(db_conn, posts_table, users_table,
                                 units_table, subjects_table):
    """
    Get the user's most recent proposals.
    """

    create_user_in_db(users_table, db_conn)
    current_user = users_table.get('abcd1234').run(db_conn)
    create_some_proposals(posts_table, units_table, subjects_table, db_conn)
    proposals = get_my_recent_proposals(current_user, db_conn)
    assert len(proposals) == 2


def test_get_proposal_entities():
    """
    Pull out the entity ids matching the kind.
    """

    proposals = [{
        'entity_versions': [{
            'kind': 'unit',
            'id': 'A',
        }, {
            'kind': 'subject',
            'id': 'B',
        }, {
            'kind': 'unit',
            'id': 'C',
        }]
    }]
    kind = 'unit'
    entity_ids = get_proposal_entity_versions(proposals, kind)
    assert len(entity_ids) == 2
    assert entity_ids[0] == 'A'
    assert entity_ids[1] == 'C'


def test_get_my_recently_created_units(db_conn, posts_table, subjects_table,
                                       units_table, users_table):
    """
    Get the user's most recent units.
    """

    create_user_in_db(users_table, db_conn)
    current_user = users_table.get('abcd1234').run(db_conn)
    create_some_proposals(posts_table, units_table, subjects_table, db_conn)
    units = get_my_recently_created_units(current_user, db_conn)
    assert len(units) == 2
    assert units[0]['entity_id'] == 'D'
    assert units[1]['entity_id'] == 'F'


def test_get_my_recently_created_subjects(db_conn, posts_table, units_table,
                                          subjects_table, users_table):
    """
    Get the user's most recent subjects.
    """

    create_user_in_db(users_table, db_conn)
    current_user = users_table.get('abcd1234').run(db_conn)
    create_some_proposals(posts_table, units_table, subjects_table, db_conn)
    subjects = get_my_recently_created_subjects(current_user, db_conn)
    assert len(subjects) == 2
    assert subjects[0]['entity_id'] == 'A'
    assert subjects[1]['entity_id'] == 'C'
