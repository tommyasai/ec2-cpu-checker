import csv

class WriterInterface:
  def write(self, account_id: str, contents) -> None:
    "Write out the result to somewhere"
    
  def getWriter(writer_type: str):
      match writer_type:
        case 'csv':
            return CsvWriter()
        case _:
            return 0

class CsvWriter(WriterInterface):
  def write(self, account_id: str, contents: list[dict]):
    with open(f'{account_id}.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

      writer.writerow(contents[0].keys())
      writer.writerows(rows.values() for rows in contents)

