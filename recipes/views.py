from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recipe
from .serializers import RecipeSerializer, RecipeListSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)