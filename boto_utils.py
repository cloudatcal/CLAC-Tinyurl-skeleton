import boto3 as b3
from botocore.exceptions import ProfileNotFound
from constants import TABLE_NAME
from datetime import datetime
from local_constants import AWS_PROFILE_NAME


# locally lambda will find a config file, but once deployed it will use cloud context
try:
    # Change the region name to the one that you are using for your project. I used "us-west-2"
    # but you might be using "us-west-1".
    dynamodb = b3.session.Session(region_name="us-west-2").resource('dynamodb')
except ProfileNotFound as err:
    dynamodb = b3.resource('dynamodb')
    print(err)


# This method will check if a table exists with the given table name.
# @:param t_name -> the name of the table to be checked
# @:returns -> boolean value indicating whether or not table exist
def table_exists(t_name):
    # TODO: Find if t_name exists in dynamodb. 
    # Hint: You may want to use "dynamodb.tables.all()" 
    # Link to Documentation for the function dynamodb.tables.all():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables
    
    # Any amount of lines is fine, hence the lack of blanks to fill

    return _____


# This method will run a one time DB migration. This method will provision our DynamoDB table.
# This method will be used to create a table of urls of the proper schema required for CLUrkel
# @:param t_name -> the name of the table to be created
# @:returns -> response indicating success or of table creation
def migration(t_name=TABLE_NAME):
    # TODO: If the given table already exists in DynamoDB, delete the table and wait until the
    # table is completely deleted and does not exist anymore
    # Hint: Refer back to boto_utils.py for a useful helper function, as well as the dynamodb documentation
    # Documentation link: 
    if ________:
        print('found pre-existing table')
        table = dynamodb.Table(_______)
        table._______()
        table._______()

    created_table = dynamodb.create_table(
        TableName=_____,
        KeySchema=[
            {
                'AttributeName': 'redirect_url',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'redirect_url',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return created_table


# This method will execute put requests to dynamo URL table.
# @:param original_url -> string of original url
# @:param redirect_hash -> string of new hash
# @:param expiration_date -> string of the expiration date of the redirect url
# @:param user -> string of user id
# @:param table_name -> string of name of table to be queried (defaults to TABLE_NAME in constants.py)
# @:returns -> response of put request if table exists; returns False otherwise
def put(original_url: str, redirect_hash: str, expiration_date: str, user: str, t_name=TABLE_NAME):
    # TODO: Error Handling: if the given table does not exist in DynamoDB, print out "That table does not exist!"
    # and return false
    # Hint: Refer back to boto_utils.py for a useful helper function
    if ____________:
        _______________
        return ______

    # TODO: This next part will put a new item into an existing DynamoDB table
    # You may need to refer to dyanmodb documentation to find a function you can use
    # to put an item into a dyanmodb.Table object
    # Fill in the blanks

    table = dynamodb.Table(______)
    response = table.______(
        Item={
            'redirect_url': ______,
            'original_url': ______,
            'creation_date': datetime.now().strftime('%S'),
            'expiration_date': ______,
            'user': ______
        }
    )
    return response


# simple utility to get base off of hash
def get(redirect_url, t_name=TABLE_NAME):

    # TODO: This function will retrieve an item from an existing DynamoDB table
    # If it does not exist, print out an error statement and return False
    # Hint: Find a function in the dyanmodb documentation you can use to get 
    # an item from a dyanmodb.Table object

    if _______:
        print("That table does not exist!")
        return False
    table = dynamodb.Table(______)
    return table.______(Key={
        'redirect_url': _______
    }, ProjectionExpression= 'original_url')


def library_loaded():
    return 'congrats! layers have worked properly. Now you can use any home-built boto utils'

if __name__ == '__main__':
    migration()
