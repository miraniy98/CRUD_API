from django.db.models import Q
from rest_framework import generics, mixins
from post.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer

#Create Search and List Combined
class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup  = 'pk'
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)
                    ).distinct()
        return BlogPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

#Retrieve Update and Destroy view Combined
class BlogPostRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup              = 'pk'
    serializer_class    = BlogPostSerializer
    permission_classes  = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_queryset(self):
        return BlogPost.objects.all()
