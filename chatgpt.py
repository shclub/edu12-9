import sqlalchemy as sql

# Create a connection to the SQLite database
engine = sql.create_engine('sqlite:///example.db')

# Define a function to perform CRUD operations on the database
def crud(action, params):
    # Create a session to execute queries
    with engine.begin() as conn:
        # Use a dictionary to map actions to SQLAlchemy query methods
        queries = {
            'create': lambda: conn.execute(sql.insert(table).values(**params)),
            'read': lambda: conn.execute(sql.select([table]).where(table.columns.field == params)),
            'update': lambda: conn.execute(sql.update(table).where(table.columns.id == params[0]).values(field=params[1])),
            'delete': lambda: conn.execute(sql.delete(table).where(table.columns.id == params)),
        }
        # Execute the query and return the result
        return queries[action]()

# Define the AWS Lambda handler function
#def lambda_handler(event, context):
#    # Use the CRUD function to perform operations on the database
#    crud('create', {'id': 1, 'field': 'value1'})
#    crud('read', 1)
#    crud('update', (1, 'value2'))
#    crud('delete', 1)
