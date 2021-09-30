import logging

from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .models import UnikubeUser


logger = logging.getLogger('hurricane.users')


@method_decorator(csrf_exempt, name='dispatch')
class AvatarUploadView(UpdateView):
    model = UnikubeUser
    fields = ["avatar_image"]

    def get_object(self, queryset=None):
        try:
            return super(AvatarUploadView, self).get_object(queryset=queryset)
        except Http404:
            obj, _ = UnikubeUser.objects.get_or_create(id=self.kwargs["pk"])
            return obj

    def form_valid(self, form):
        """
        override this to simply return a status 200 instead of a redirect to success url
        """
        self.object = form.save()
        # todo thumbnail this image right here?
        return JsonResponse(data={"url": self.object.avatar_image.url}, status=200)
