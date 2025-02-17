from rest_framework import serializers
from .models import Task, Category, UserProfile
import re


class UserProfileSerializer(serializers.ModelSerializer):
    def validate_first_name(self, value):
        if value and not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z\s]+$', value):
            raise serializers.ValidationError("First name must contain only letters (Arabic or English).")
        return value

    def validate_last_name(self, value):
        if value and not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z\s]+$', value):
            raise serializers.ValidationError("Last name must contain only letters (Arabic or English).")
        return value

    def validate_city(self, value):
        if value and not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z\s]+$', value):
            raise serializers.ValidationError("City must contain only letters (Arabic or English).")
        return value

    def validate_telephone(self, value):
        if value and not re.match(r'^\d+$', value):  # Only digits allowed
            raise serializers.ValidationError("Telephone must contain only numbers.")
        return value

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'telephone', 'city']


class TaskSerializer(serializers.ModelSerializer):
    # category_name = serializers.CharField(source='category.name', read_only=True)
    # category = CategorySerializer(read_only=True)
    # category_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), source='category', write_only=True
    # )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_completed', 'due_date', 
            'created_at', 'updated_at', 'priority', 'category', 'user'
        ]


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many= True, read_only= True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'tasks']

    
    def validate(self, data):
        user = self.context['request'].user
        input_name = data.get('name', '').strip().lower()  # Normalize input
        # Replace multiple spaces with a single space
        normalized_input_name = re.sub(r'\s+', ' ', input_name)

        # Normalize names in the database before checking
        categories = Category.objects.filter(user=user)
        for category in categories:
            db_name_normalized = re.sub(r'\s+', ' ', category.name.strip().lower())
            if normalized_input_name == db_name_normalized:
                raise serializers.ValidationError("You already have a category with this name.")

        # Pass the normalized name forward
        data['name'] = input_name.strip()  # Ensure the name is clean before saving
        return data