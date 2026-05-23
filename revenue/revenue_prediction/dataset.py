from openpyxl import Workbook
from openpyxl.styles import Font
import random

wb=Workbook()

ws=wb.active

ws.title="Growth_Data"

headers=[
"Infrastructure_Development",
"Teaching_Quality_Improvement",
"Digital_Learning_Adoption",
"Student_Satisfaction",
"New_Programs_Introduced",
"Marketing_Reach",
"Retention_Rate",
"Future_Growth_Trend"
]

ws.append(headers)

for i in range(2000):

    infrastructure=random.randint(1,10)

    teaching=random.randint(1,10)

    digital=random.randint(1,10)

    satisfaction=random.randint(1,10)

    programs=random.randint(1,10)

    marketing=random.randint(1,10)

    retention=random.randint(50,100)

    score=(
        infrastructure+
        teaching+
        digital+
        satisfaction+
        programs+
        marketing+
        retention/10
    )

    if score>=55:
        growth="High Growth"

    elif score>=38:
        growth="Moderate Growth"

    else:
        growth="Low Growth"

    ws.append([
        infrastructure,
        teaching,
        digital,
        satisfaction,
        programs,
        marketing,
        retention,
        growth
    ])

for cell in ws[1]:
    cell.font=Font(bold=True)

wb.save(
    "growth_dataset.xlsx"
)

print("Dataset Generated")