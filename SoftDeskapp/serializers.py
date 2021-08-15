from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Projects, Contributors, Issues, Comments


class CreateUserSerializer(serializers.ModelSerializer):
    """
    serializer
    use to create a new user
    didn't return the password 'cause of the write_of parameters
    method create, add and save a new user in db
    """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ("title", "description", "type")

    def create(self, validated_data):
        project = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
        )
        project.save()
        return project


class ProjectUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ("title", "description", "type")
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'type': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', "first_name", "last_name")


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ('user_id', 'role')

    @staticmethod
    def validate_user_id(value):
        user = User.objects.filter(id=value)
        if not user:
            raise serializers.ValidationError("this user doens't exist")
        return value


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class IssuesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ("title", "desc", "tag", "priority", "status", "assignee_user_id")

        @staticmethod
        def validate_assignee_user_id(value):
            user = User.objects.filter(id=value)
            if not user:
                raise serializers.ValidationError("This user doesn't exist")
            return value


class IssuesupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ("title", "desc", "tag", "priority", "status")
        extra_kwargs = {
            'title': {'required': False},
            'desc': {'required': False},
            'tag': {'required': False},
            'priority': {'required': False},
            'status': {'required': False},
        }


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('description',)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
