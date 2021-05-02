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
    print("ID token:", resp['AuthenticationResult']['IdToken'])   #tourneymaster

# Tourney Master Credentials
user_pool_id = 'us-east-1_KCFCcxsf4'
app_client_id = '4e6uq8b4f1f4q5ql8qe10cqfdc'
username = '<enter the admin email address here>'
password = '<enter admin password here>'

authenticate_and_get_token(username=username, password=password,user_pool_id=user_pool_id,app_client_id=app_client_id)
