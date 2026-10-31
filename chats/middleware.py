import time
from django.utils.deprecation import MiddlewareMixin

class CustomRequestLoggerMiddleware:
    """
    A class-based middleware that logs incoming request paths,
    processing duration, and response status codes.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization go here.

    def __call__(self, request):
        # Code executed for each request BEFORE the view is called
        start_time = time.time()
        
        # Example logic: attach custom data to request
        request.custom_attr = "Custom Data"

        # Pass the request to the next middleware/view
        response = self.get_response(request)

        # Code executed for each request AFTER the view is called
        duration = time.time() - start_time
        print(f"[{request.method}] {request.path} - {response.status_code} ({duration:.4f}s) for request")

        return response

    def process_exception(self, request, exception):
        """
        Optional hook: Called when a view raises an exception.
        """
        print(f"Unhandled exception on {request.path}: {exception}")
        return None  # Return HttpResponse to override error handling, or None to let Django handle it