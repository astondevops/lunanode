from lndynamic import LNDynamic
api_id = 'YOUR API ID'
api_key = 'YOUR API KEY'
api = LNDynamic(api_id, api_key)
print api.request('vm', 'list')
