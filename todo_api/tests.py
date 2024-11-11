from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task, Category, CustomUser
from .serializers import TaskSerializer, CategorySerializer


class TodoAPITestCase(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = CustomUser.objects.create_user(username="user1", email="user1@example.com", password="password1")
        self.user2 = CustomUser.objects.create_user(username="user2", email="user2@example.com", password="password2")
        
        # Log in user1 for testing
        self.client.force_authenticate(user=self.user1)

        # Create a category for user1
        self.category1 = Category.objects.create(name="Category 1", description="User1's category", user=self.user1)
        
        # Create tasks for user1
        self.task1 = Task.objects.create(
            title="Task 1",
            description="User1's task",
            is_completed=False,
            priority='M',
            category=self.category1
        )

    def test_create_category(self):
        """Test user can create a category."""
        data = {
            "name": "New Category",
            "description": "A new category for user1",
        }
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(user=self.user1).count(), 2)

    def test_create_task(self):
        """Test user can create a task."""
        data = {
            "title": "New Task",
            "description": "A new task for user1",
            "is_completed": False,
            "priority": "H",
            "category": self.category1.id
        }
        response = self.client.post(reverse('task-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(category__user=self.user1).count(), 2)

    def test_list_categories(self):
        """Test user can only list their own categories."""
        response = self.client.get(reverse('category-list-create'))
        categories = Category.objects.filter(user=self.user1)
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_list_tasks(self):
        """Test user can only list their own tasks."""
        response = self.client.get(reverse('task-list-create'))
        tasks = Task.objects.filter(category__user=self.user1)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_task_detail_access(self):
        """Test user can access their own task details."""
        response = self.client.get(reverse('task-detail', args=[self.task1.id]))
        serializer = TaskSerializer(self.task1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_task_detail_no_access(self):
        """Test user cannot access another user's task details."""
        # Create a task for user2
        category_user2 = Category.objects.create(name="Category 2", description="User2's category", user=self.user2)
        task_user2 = Task.objects.create(title="Task User2", description="User2's task", priority='L', category=category_user2)
        
        response = self.client.get(reverse('task-detail', args=[task_user2.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task(self):
        """Test user can update their own task."""
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "is_completed": True,
            "priority": "L",
            "category": self.category1.id
        }
        response = self.client.put(reverse('task-detail', args=[self.task1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, data["title"])
        self.assertTrue(self.task1.is_completed)

    def test_delete_task(self):
        """Test user can delete their own task."""
        response = self.client.delete(reverse('task-detail', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_category_detail_no_access(self):
        """Test user cannot access another user's category details."""
        # Create a category for user2
        category_user2 = Category.objects.create(name="Category 2", description="User2's category", user=self.user2)
        
        response = self.client.get(reverse('category-detail', args=[category_user2.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_categories_different_user(self):
        """Test a user cannot see categories belonging to another user."""
        # Log in as user2 and list categories
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # User2 should see no categories since theirs haven't been created
