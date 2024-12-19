class ActivityTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            ActivityLog.objects.create(user=request.user, action=f'Accessed: {request.path}')
        return response