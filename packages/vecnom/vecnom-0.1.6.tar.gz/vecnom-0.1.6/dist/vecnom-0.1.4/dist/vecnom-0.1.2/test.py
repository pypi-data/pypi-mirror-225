from vecnom import VecnomClient

client = VecnomClient("http://127.0.0.1:8000")
# msg = {
#     "selected_table": {
#         "table_name": "your_table_name"
#     },
#     "source_db": {
#         "info": {
#             "sync": False,
#             "db_id": 1
#         }
#     }
# }

# response = client.create_init_sync(msg)

query = {
    "table_name": "your_table_name",
    "text": "your_search_query",
    "top_k": 10
}

response = client.search(query)