from core.models import RequestCounter



class RequestCounterMiddleware:
	
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		request_count = RequestCounter.objects.all().first()
		if request_count:
			request_count.requests = int(request_count.requests) + 1
			request_count.save()
		else:
			RequestCounter.objects.create(requests=1)
		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.

		return response