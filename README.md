# Welcome to the Club Sports Organization Event Partner API Guide Repository

Version: 2.6.0

**High-Level Breakdown of How this Works**
>To fully create an event, we start with the **Event** itself (pk = `event_id`). We would then run a `GET` for the ** Divisions & Pools** (fk = `event_id` and the pks are `division_id` and `pool_id`. Next is the **Teams** that compete in the event (fk, once again, is `event_id` and the pk = `team_id`. Now we have the event, all the divisions and pools, and the teams.

>The games break down into 2 types: 1) **Pool Play** and 2) **Brackets** (if applicable) . We know if there are bracket games by checking the boolean `playoffs_exist_YN` from the "*<org_id>_events*" endpoint (decribed below). "1" (int) means the event has playoff brackets while "0" means that no playoff brackets exist. **`game_id`** is the primary key for both **Pool Play** and **Bracket** games. 
***
## Table that Describes Endpoints, Keys, and Filters
>
**Description**|**Endpoint**|**Key**|**Searchable Fields**
-----|-----|-----|-----
Event Details|<org\_id>\_events|event\_id|event\_id event\_startdate event\_enddate sport\_id
Teams|<org\_id>\_teams|team\_id|team\_id event\_id division\_id pool\_id
Divisions & Pools|<org\_id>\_divs_pools|division\_id|event\_id division\_id pool\_id
Pool Play Games|<org\_id>\_poolplay|game_id |game\_id schedule\_id event\_id
Brackets Games|<org\_id>\_brackets|game\_id|game\_id bracket\_id event\_id
## API Root Endpoints

TESTING:
- Private: https://api.tourneymaster.org/private/

PROD:
- Private: https://api.tourneymaster.org/privateprod/

### GET Requests

Returns a JSON list of records.

```GET https://api.tourneymaster.org/{version}/{resource}?{querystring}```

Headers:

- Content-Type: application/json
- Authorization: Bearer {token from Cognito}

Body:
{empty}

### Additional Options One Can Attach to the End of the Endpoint
After the endpoint, add a "?" to add parameters such as keys and searchable (filterable) fields.
Sample Querystring: 
```<root>/endpoint>? param1=value&param2=value (don’t forget to urlencode)```

**Wildcards**

A "%" can be used as a wildcard to filter columns matching a pattern.

**Pagination**

Using `offset` and `limit` parameters will return not more than `limit` records beginning from `offset`.
`limit` cannot exceed 1000.
`limit` equals to 100 by default.

Multiple values can be passed separated by comma to return records matching any of these values.

**Examples:**
org_id sample = 'ABCD1234'

- All records (limit 10000):
  https://api.tourneymaster.org/private/ABCD1234_divs_pools

- By primary key:
  https://api.tourneymaster.org/private/ABCD1234_events?event_id=dsfdsf43

- By a combination of search fields:
  https://api.tourneymaster.org/private/ABCD1234_poolplay?schedule_id=SCHD0001&event_id=XYZ12345

- By any other field (not limited to foreign keys. E.g. email:
  https://api.tourneymaster.org/private/ABCD1234_events?start_date=2021-01-02

- Using a wildcard to search for data that is LIKE something.

  https://api.tourneymaster.org/private/ABCD1234_events?start_date=2021% will return all dictionary of items in the year “2021”

  https://api.tourneymaster.org/private/ABCD1234_events?event_name=%25Lax% will return any string that **_contains_** the string `lax`. Please note the `%25` encoding only on the front of the search string.


- Multiple values for a parameter

https://api.tourneymaster.org/private/ABCD1234_events?event_id=ABC123,ABC124,ABC125

- Pagination

https://api.tourneymaster.org/private/ABCD1234_events?event_id=ABC123&offset=5&limit=10 will return 10 events starting from the 5th


### Authentication

- API Client authenticates via AWS Cognito and sends in the Bearer JWT **IDToken** in Authorization header with every call to the API
- AWS API Gateway authenticates the IDToken and forwards the request to ClubSports API
- ClubSports API decodes the JWT token, reads the email address from the token

Tokens can be recreated by developers many ways. We offer the below **Sample Python script** that will generate your **IDToken**.
```
import boto3

def authenticate_and_get_token(username: str, password: str, 
                               user_pool_id: str, app_client_id: str) -> None:
    client = boto3.client('cognito-idp')

    resp = client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=app_client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )
    print("ID token:", resp['AuthenticationResult']['IdToken'])

# Tourney Master Credentials
user_pool_id = 'us-east-1_KCFCcxsf4'
app_client_id = '4e6uq8b4f1f4q5ql8qe10cqfdc'
username = '<enter the admin email address here>'
password = '<enter admin password here>'

# The below line generates the IDToken
authenticate_and_get_token(username=username, password=password,user_pool_id=user_pool_id,app_client_id=app_client_id)
```
![Alt](https://tourneymaster.s3.amazonaws.com/public/Event+Producers/SampleAPIInsomniaGraphic.png)
