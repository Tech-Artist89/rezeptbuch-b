# planner/views.py - Saubere finale Version
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import MealPlan
from .serializers import MealPlanSerializer, MealPlanCreateSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MealPlanCreateSerializer
        return MealPlanSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Override create to return full MealPlan data instead of create data"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Erstelle das MealPlan Objekt
        meal_plan = serializer.save(user=request.user)
        
        # Verwende den MealPlanSerializer für die Response (mit allen Daten)
        response_serializer = MealPlanSerializer(meal_plan)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def current_week(self, request):
        """Gibt die Meal Plans für die aktuelle Woche zurück"""
        today = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        
        meal_plans = self.get_queryset().filter(
            date__range=[start_week, end_week]
        ).order_by('date', 'meal_type')
        
        serializer = self.get_serializer(meal_plans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def week(self, request):
        """Gibt Meal Plans für eine spezifische Woche zurück"""
        start_date = request.query_params.get('start_date')
        if not start_date:
            return Response({'error': 'start_date parameter required'}, status=400)
        
        try:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = start + timedelta(days=6)
            
            meal_plans = self.get_queryset().filter(
                date__range=[start, end]
            ).order_by('date', 'meal_type')
            
            serializer = self.get_serializer(meal_plans, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)