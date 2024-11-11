from rest_framework import serializers
from .models import Task, Category


class TaskSerializer(serializers.ModelSerializer):
    # category_name = serializers.CharField(source='category.name', read_only=True)
    # category = CategorySerializer(read_only=True)
    # category_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), source='category', write_only=True
    # )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_completed', 'due_date', 
            'created_at', 'updated_at', 'priority', 'category'
        ]


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many= True, read_only= True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'tasks']