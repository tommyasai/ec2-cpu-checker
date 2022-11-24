import os
import boto3.session


class Session(boto3.session.Session):
  def __init__(
      self,
      aws_access_key_id=None,
      aws_secret_access_key=None,
      aws_session_token=None,
      region_name=None,
      botocore_session=None,
      profile_name=None
  ):
    if botocore_session is not None:
        self._session = botocore_session
    else:
        # Create a new default session
        self._session = aiobotocore.session.get_session()

    # Setup custom user-agent string if it isn't already customized
    if self._session.user_agent_name == 'Botocore':
        botocore_info = 'Botocore/{0}'.format(
            self._session.user_agent_version)
        if self._session.user_agent_extra:
            self._session.user_agent_extra += ' ' + botocore_info
        else:
            self._session.user_agent_extra = botocore_info
        self._session.user_agent_name = 'Boto3'
        self._session.user_agent_version = boto3.__version__

    if profile_name is not None:
        self._session.set_config_variable('profile', profile_name)

    if aws_access_key_id or aws_secret_access_key or aws_session_token:
        self._session.set_credentials(
            aws_access_key_id, aws_secret_access_key, aws_session_token)

    if region_name is not None:
        self._session.set_config_variable('region', region_name)

    self.resource_factory = boto3.resoureFactory (
        self._session.get_component('event_emitter')
    )
    self._setup_loader()
    self._register_default_handlers()

def get_session(region): 
  accesskey = os.environ.get("AWS_ACCESS_KEY_ID")
  secretkey = os.environ.get("AWS_SECRET_ACCESS_KEY")

  session = Session(aws_access_key_id=accesskey,
  aws_secret_access_key=secretkey,
  region_name=region)

  return session


# Not completed implementation yet
def get_session_2FA(region):
  import boto3

  session = boto3.Session()
  mfa_serial = session._session.full_config['profiles']['quoine-prod-devops']['mfa_serial']
  mfa_token = input('Please enter your 6 digit MFA code:')
  sts = session.client('sts')
  MFA_validated_token = sts.get_session_token(SerialNumber=mfa_serial, TokenCode=mfa_token)
  session = Session(
    aws_session_token=MFA_validated_token['Credentials']['SessionToken'],
    aws_secret_access_key=MFA_validated_token['Credentials']['SecretAccessKey'],
    aws_access_key_id=MFA_validated_token['Credentials']['AccessKeyId']
  )
  return session