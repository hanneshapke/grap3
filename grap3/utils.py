import csv
import redis

from sqlalchemy.sql import exists, text
from collections import Counter
from .models import Grocery, List
from .app import db
from .decorators import timer

__CSV_FILE__ = '/Users/hannes/Downloads/groceries.csv'


def is_grocery(name):
    ''' Checks if grocery item exists '''
    return db.session.query(exists().where(Grocery.name == name)).scalar()


def is_grocery_by_id(id):
    ''' Checks if grocery item exists (by id) '''
    return db.session.query(exists().where(Grocery.id == id)).scalar()


def get_grocery(name):
    ''' Returns a grocery item by name '''
    return Grocery.query.filter_by(name=name).first()


def get_grocery_by_id(id):
    ''' Returns a grocery item by id '''
    return Grocery.query.get(id)


def get_or_create_grocery(name):
    ''' creates if not existing '''
    item = get_grocery(name)
    if not item:
        item = Grocery(name=name)
        db.session.add(item)
        db.session.commit()
    return item


def get_existing_groceries(query_string):
    if query_string:
        groceries = query_string.replace(' ', '').split(',')
        # filter all non existing groceries
        tmp = [grocery for grocery in groceries if is_grocery(grocery)]
        # return ids
        return [get_grocery(grocery).id for grocery in tmp]
    return None


def get_sql_query_params(grocery_ids):
    ''' returns params for the sql query for list selection '''
    num_grocery_ids = len(grocery_ids)
    if num_grocery_ids == 1:
        grocery_ids = "".join(["(", str(grocery_ids[0]), ")"])
    else:
        grocery_ids = tuple(grocery_ids)
    return (grocery_ids, num_grocery_ids)


def get_grocery_lists(grocery_ids):
    ''' Returns the lists with given grocery ids (no matches are excluded)'''

    params = get_sql_query_params(grocery_ids)
    # create db connection for raw execution
    connection = db.engine.connect()

    sql_query = \
        ''' SELECT DISTINCT list_id FROM grocery_to_list
                WHERE list_id IN( SELECT list_id
                FROM grocery_to_list
                    WHERE grocery_id IN %s
                GROUP BY list_id
                HAVING COUNT(*) = %s)''' \
            % (params[0], params[1])
    lists = connection.execute(text(sql_query))

    return [List.query.get(x) for x in lists]


def remove_grocery_item_from_recommendation(grocery_list, existing_groceries):
    for grocery in existing_groceries:
        remove_item = get_grocery_by_id(grocery)
        while remove_item in grocery_list:
            grocery_list.remove(remove_item)
    return grocery_list


def get_highest_match(lists, existing_groceries, num_most_common=3):
    tmp = []
    for grocery_list in lists:
        for groceries in grocery_list.groceries:
            tmp.append(groceries)
    # exclude existing groceries
    tmp = remove_grocery_item_from_recommendation(tmp, existing_groceries)
    # compute most common
    num_groceries = len(tmp)
    common_groceries = (Counter(tmp).most_common(num_most_common))
    return [(i[0], i[1] / num_groceries) for i in common_groceries]


@timer
def get_highest_match_from_groceries(query_string, num_most_common=4):
    '''
    The method `get_highest_match_from_groceries` takes a raw string of
    params and returns the n most common groceries missing in the shopping list
    '''

    groceries = get_existing_groceries(query_string)
    if groceries:
        grocery_lists = get_grocery_lists(groceries)
        return get_highest_match(grocery_lists, groceries, num_most_common)
    return None


def set_all_grocery_to_db():
    ''' creates grocery items in db if no record found '''
    grocery_list = []
    with open(__CSV_FILE__, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for grocery_list in data:
            for item in grocery_list:
                if item not in grocery_list:
                    grocery_list.append(item)
    ''' creating a list first and write to db is faster
    than write individual items to db '''
    for item in grocery_list:
        get_or_create_grocery(item)


def set_all_grocery_lists():
    ''' set grocery lists for given sample set '''
    with open(__CSV_FILE__, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for grocery_list in data:
            glist = List()
            for item in grocery_list:
                glist.groceries.append(get_or_create_grocery(item))
            db.session.add(glist)
            db.session.commit()
            if glist.id % 1000 == 0:
                print("Added grocery list %s" % glist.id)

#######
# REDIS
#######


def set_all_grocery_lists_to_redis():
    ''' set grocery lists for given sample set '''
    # import time
    conn = redis.Redis()
    with open(__CSV_FILE__, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        index = 0
        for grocery_list in data:
            for item in grocery_list:
                conn.sadd(index, item)
                conn.sadd(item, index)
            index += 1
            if index % 1000 == 0:
                print("Added grocery list %s" % index)


def get_union_list(sublist, union_list):
    return [val for val in union_list if val in sublist]


def get_grocery_lists_from_redis(grocery_params):
    ''' '''
    conn = redis.Redis()
    grocery_items = grocery_params.split(',')

    results = []
    for grocery in grocery_items:
        results.append(list(conn.smembers(grocery)))
    redis_results = sorted(results, key=len)
    lists = results[0]
    for result in redis_results:
        lists = get_union_list(result, lists)
    return lists, grocery_items


@timer
def get_highest_match_from_redis(lists, existing_groceries, num_most_common=3):
    conn = redis.Redis()
    tmp = []
    for grocery_list in lists:
        for groceries in conn.smembers(grocery_list):
            tmp.append(groceries)
    # exclude existing groceries
    # tmp = remove_grocery_item_from_recommendation(tmp, existing_groceries)
    for i in existing_groceries:
        while str.encode(i) in tmp:
            tmp.remove(str.encode(i))
    # compute most common
    num_groceries = len(tmp)
    common_groceries = (Counter(tmp).most_common(num_most_common))
    return [(i[0], i[1] / num_groceries) for i in common_groceries]


@timer
def get_highest_match_from_groceries_from_redis(
        query_string, num_most_common=4):
    tmp = get_grocery_lists_from_redis(query_string)
    if tmp[0] is None:
        return (500, None)
    return (200, get_highest_match_from_redis(tmp[0], tmp[1], num_most_common))
