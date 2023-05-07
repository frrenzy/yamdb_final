from rest_framework import mixins


class ListCreateDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    pass
