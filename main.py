import datetime
import pprint
import csv
import aws_session
import instances
import cpu_utilization
from write import CsvWriter, WriterInterface

pp = pprint.PrettyPrinter(indent=1)

period=3600
start_time=datetime.datetime(2022, 10, 1)
end_time=datetime.datetime(2022, 10, 30)



session = aws_session.get_session("ap-northeast-1")
all_regions = instances.get_regions(session)
output_array = []
for region in all_regions:
  session = aws_session.get_session(region)
  ig = instances.InstancesGetter(session)
  instances_info = ig.get_instances_info()
  if len(instances_info) == 0:
    continue
  account_id = instances_info[0][0]

  print(f"=== account: {account_id}, region: {region} ===")
  cpg = cpu_utilization.CPUUtilizationGetter(start_time, end_time, period, session)
  for i in instances_info:
    instance_id = i[1]
    instance_type = i[2]
    instance_key_name = i[4]
    print(f"InstanceKeyName: {instance_key_name}, InstanceId: {instance_id}")
    try:
      result = cpg.get_CPUUtilization(instance_id)
    except Exception as e:
      print(e)
      continue

    output_array.append({
      "InstanceName": instance_key_name,
      "InstanceId": instance_id,
      "InstanceType": instance_type,
      "MaximumCPUUtilization": result["Maximum"],
      "AverageCPUUtilization": result["Average"],
      "Region": region,
      "AccountId": account_id,
      "From": start_time,
      "To": end_time,
    })


if len(output_array) == 0:
  print("There are no target instances.")
  quit()

writer_type = "csv"
writer = WriterInterface.getWriter(writer_type)
if writer == 0:
  print("""The type of writer is not proper: {writer_type}""")
  quit()
writer.write(account_id, output_array)
