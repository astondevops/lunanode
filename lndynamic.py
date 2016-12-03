class LNDynamic:
	LNDYNAMIC_URL = 'https://dynamic.lunanode.com/api/{CATEGORY}/{ACTION}/'

	def __init__(self, api_id, api_key):
		if len(api_id) != 16:
			raise LNDAPIException('supplied api_id incorrect length, must be 16')
		if len(api_key) != 128:
			raise LNDAPIException('supplied api_key incorrect length, must be 128')

		self.api_id = api_id
		self.api_key = api_key
		self.partial_api_key = api_key[:64]

	def request(self, category, action, params = {}):
		import json
		import time
		import hmac
		import hashlib
		import urllib
		import urllib2

		url = self.LNDYNAMIC_URL.replace('{CATEGORY}', category).replace('{ACTION}', action)
		request_array = dict(params)
		request_array['api_id'] = self.api_id
		request_array['api_partialkey'] = self.partial_api_key
		request_raw = json.dumps(request_array)
		nonce = str(int(time.time()))
		handler = "%s/%s/" % (category, action)
		hasher = hmac.new(self.api_key, '%s|%s|%s' % (handler, request_raw, nonce), hashlib.sha512)
		signature = hasher.hexdigest()

		data = urllib.urlencode({'req': request_raw, 'signature': signature, 'nonce': nonce})
		content = urllib2.urlopen(urllib2.Request(url, data)).read()
		return json.loads(content)

class LNDAPIException(Exception):
	pass
