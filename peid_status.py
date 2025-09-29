# import requests

# url = "https://us1.api.matillion.com/dpc/v1/projects/94e19997-6afe-44de-82b2-880389d82996/pipeline-executions/019992d8-54de-76db-b30d-28ab325aa2e7"

# payload = {}
# headers = {
#   'Accept': 'application/json',
#   'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYTzUtTWtvM0hPYWtJRkdIeXNCSFp2RnQ5SElYRzcxWmhudlJjVnc4UEtvIn0.eyJleHAiOjE3NTkxMDY5NjEsImlhdCI6MTc1OTEwNTE2MSwianRpIjoiMDk1ZGVjZjMtYmJmMi00YjFkLTg1MWMtYTVhMDMzNTcxNmZkIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5jb3JlLm1hdGlsbGlvbi5jb20vcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiaHR0cHM6Ly9hcGkubWF0aWxsaW9uLmNvbSIsInN1YiI6Ijc3NTgxZmVlLTQ1MmMtNGNjNi1iOTU4LTE2YjFmMWY5MjUwMCIsInR5cCI6IkJlYXJlciIsImF6cCI6IjJlYTIyZTNhLTI5YTctNDg2Yy1iZjBiLTVkOTRhY2E1MWFjMCIsInNjb3BlIjoicGlwZWxpbmUtZXhlY3V0aW9uIiwiY2xpZW50SG9zdCI6IjQ5LjE1LjI0Ny40NSIsImh0dHBzOi8vbWF0aWxsaW9uLmNvbS9hY2NvdW50SWQiOiI4YTdhZTg3Yi1mMDFiLTQ5ZTctNWI4NC04ZGI2M2Y2Y2QyZDAiLCJjbGllbnRBZGRyZXNzIjoiNDkuMTUuMjQ3LjQ1IiwiY2xpZW50X2lkIjoiMmVhMjJlM2EtMjlhNy00ODZjLWJmMGItNWQ5NGFjYTUxYWMwIn0.kAzZcINnsptZJJspFz737ui-qPvTFkoRM9abU_wZ6qhXJiYRTOglzteve4VgHa-bMTs667Oi2tx9GRnOsEm4aMuWIHlWvbbDBx86ns3gL0PQysTEJ94jIIJiHQX3ks51MjT4WmYhbgX6-KSnlOOJq_Yk7v1Q1Zm5j0606zsiAeRmHGRWEYEqUG5TigcA8h8YWiJyYTyX8q93ilzGfoosVMoUoKqAb6VZ6CIC7zZ2RRDWfwNF1h07_Qp1xCiUEKH6tzgF4ID5jTmu9RUImeW53mD-GaTJN82kVbzlKmoXa3M2R-Bgg7popVTXoPgVlwAZZCdP5ZRSZ1LtBTFHsra0qQ'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


import requests
import json

url = "https://us1.api.matillion.com/dpc/v1/projects/{project_id}/pipeline-executions/019992d8-54de-76db-b30d-28ab325aa2e7"

headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    result = data.get("result", {})

    pipeline_name = result.get("pipelineName")
    status = result.get("status")
    message = result.get("message")

    print("Pipeline Name:", pipeline_name)
    print("Status:", status)
    print("Message:", message)
else:
    print("Error:", response.status_code, response.text)
