# Welcome to the Club Sports Organization Partners API Guide Repository

Version: 2.6.0

**What you will need and it's Description**
**Description**|**Endpoint**|**Key**|**Searchable Fields**
-----|-----|-----|-----
Event Details|<org\_id>\_events|event\_id|event\_id event\_startdate event\_enddate sport\_id
Teams|<org\_id>\_teams|team\_id|team\_id event\_id division\_id pool\_id
Divisions & Pools|<org\_id>\_divisions|division\_id|event\_id division\_id pool\_id
Pool Play Games|<org\_id>\_pool\_games| |schedule\_id event\_id
Brackets Games|<org\_id>\_bracket\_games|bracket\_id|bracket\_id event\_id
## API Endpoints

TESTING:
- Private: https://api.tourneymaster.org/private/

PROD:
- Private: https://api.tourneymaster.org/privateprod/

### GET

Returns a list of records.

GET https://api.tourneymaster.org/{version}/{resource}?{querystring}

Headers:

- Content-Type: application/json
- Authorization: Bearer {token from Cognito}

Body:
{empty}

Version: v2

Things you will need to replicate everything within our tournaments: 
1. Event Details
1. Teams
1. Divisions & Pools
1. Pool Play Games
1. Bracket Games

Querystring: param1=value&param2=value (don’t forget to urlencode)

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
  https://api.tourneymaster.org/private/ABCD1234_divisions_pools

- By primary key:
  https://api.tourneymaster.org/private/ABCD1234_events?event_id=dsfdsf43

- By a combination of search fields:
  https://api.tourneymaster.org/private/ABCD1234_pool_games?schedule_id=SCHD0001&event_id=XYZ12345

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
