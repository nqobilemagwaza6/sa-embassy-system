from rest_framework import serializers
from .models import Application, Document, ApplicationStatusEvent, Notification
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=False, allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
        )
        user.is_staff = False
        user.is_superuser = False
        user.set_password(validated_data['password'])
        user.save()
        return user


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'application', 'doc_type', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True, source='document_set')
    class Meta:
        model = Application
        fields = [
            'id',
            'user',
            'documents',
            'full_name',
            'passport_number',
            'nationality',
            'destination_country',
            'travel_date',
            'status',
            'admin_comment',
            'created_at',
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'full_name',
            'passport_number',
            'nationality',
            'destination_country',
            'travel_date',
        ]


class StatusEventSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)

    class Meta:
        model = ApplicationStatusEvent
        fields = ['id', 'from_status', 'to_status', 'comment', 'changed_by', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'application', 'message', 'is_read', 'created_at']
