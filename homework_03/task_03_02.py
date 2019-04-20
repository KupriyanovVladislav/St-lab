import csv
import json


def merge_students_data(csv_file, xlsx_workbook, json_file):
    csv_file = csv.reader(csv_file)
    student_age = {line[0] + " " + line[1]: line[2] for line in csv_file}
    ws = xlsx_workbook["List1"]
    student_mark = dict()
    for row in ws.rows:
        lst_mark = [cell.value for cell in row if isinstance(cell.value, int)]
        student_mark.update({row[0].value: lst_mark})
    data = dict()
    for key in student_mark.keys():
        data.update({key: {"age": int(student_age[key]), "marks": student_mark[key]}})
    json.dump(data, json_file)
