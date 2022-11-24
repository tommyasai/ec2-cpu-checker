import functools

class CPUUtilizationGetter:
  def __init__(self, start_time, end_time, period, session):
    self.start_time = start_time
    self.end_time = end_time
    self.period = period
    self.session = session
    self.cloud_watch = session.client("cloudwatch")

  def get_CPUUtilization(self, instance_id):
    def get_metric(instance_id, statistics):
      return self.cloud_watch.get_metric_statistics(
              Namespace='AWS/EC2',
              MetricName='CPUUtilization',
              Dimensions=[
                  {
                      'Name': 'InstanceId',
                      'Value': instance_id
                  },
              ],
              StartTime=self.start_time,
              EndTime=self.end_time,
              Period=self.period,
              Statistics=[
                  statistics
              ]
          )
    average_datapoints = get_metric(instance_id,'Average')['Datapoints']
    maximum_datapoints = get_metric(instance_id, 'Maximum')['Datapoints']
  
    if (len(average_datapoints) == 0):
      raise Exception(f"Failed to get metric for {instance_id}")
    maximum = round(functools.reduce(lambda a, m: a if a > m['Maximum'] else m['Maximum'], maximum_datapoints, 0), 2)
    average = round(functools.reduce(lambda a, m: a + m['Average'], average_datapoints, 0) / len(average_datapoints), 2)
    return {
      'Maximum': maximum, 
      'Average': average,
    }
