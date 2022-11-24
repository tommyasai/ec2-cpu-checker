import jmespath

class InstancesGetter:
  def __init__(self, session):
    self.ec2 = session.client("ec2")

  def get_instances_info(self):
    response = self.ec2.describe_instances(
        Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
        ],
    )
    output = jmespath.search("Reservations[].Instances[].[NetworkInterfaces[0].OwnerId, InstanceId, InstanceType, \
        KeyName, [Tags[?Key=='Name'].Value] [0][0]]", response)
    return output


def get_regions(session):
  ec2 = session.client("ec2")
  return [region['RegionName']
    for region in ec2.describe_regions()['Regions']]