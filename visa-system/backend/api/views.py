from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Application, ApplicationStatusEvent, Document, Notification
from .permissions import IsSuperUser
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationSerializer,
    DocumentSerializer,
    NotificationSerializer,
    RegisterSerializer,
    StatusEventSerializer,
)


def status_change_notification_message(to_status: str, application: Application) -> str:
    """User-facing notification text when an admin updates application status."""
    who = application.full_name.strip() if application.full_name else 'Your application'
    ref = f'{who} (ref #{application.id})'
    lines = {
        'PENDING': f'{ref}: Your visa application is pending. We will notify you when processing begins.',
        'UNDER_REVIEW': f'{ref}: Your application is now under review.',
        'APPROVED': f'{ref}: Your application has been approved.',
        'REJECTED': f'{ref}: Your application was not approved. Please read the admin comment for next steps.',
    }
    return lines.get(to_status, f'{ref}: Your application status was updated.')


class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user': {'id': user.id, 'username': user.username, 'email': user.email}},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        u = request.user
        return Response(
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'is_superuser': u.is_superuser,
            }
        )

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save(user=request.user, status='PENDING')
        out = ApplicationSerializer(application, context={'request': request})
        return Response(out.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='status-events')
    def status_events(self, request, pk=None):
        application = self.get_object()
        events = application.status_events.all()
        return Response(StatusEventSerializer(events, many=True).data)

    @action(detail=True, methods=['post'], url_path='documents')
    def upload_document(self, request, pk=None):
        application = self.get_object()
        if not (request.user.is_superuser or application.user_id == request.user.id):
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['application'] = application.id
        serializer = DocumentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save()
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='admin-status', permission_classes=[IsSuperUser])
    def admin_status(self, request, pk=None):
        application = self.get_object()
        to_status = request.data.get('status')
        comment = request.data.get('comment', '')

        valid_statuses = {c[0] for c in Application.STATUS_CHOICES}
        if to_status not in valid_statuses:
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        from_status = application.status
        if from_status != to_status:
            application.status = to_status
        if comment != '':
            application.admin_comment = comment
        application.save()

        ApplicationStatusEvent.objects.create(
            application=application,
            changed_by=request.user,
            from_status=from_status,
            to_status=to_status,
            comment=comment,
        )

        if from_status != to_status:
            Notification.objects.create(
                user=application.user,
                application=application,
                message=status_change_notification_message(to_status, application),
            )

        return Response(ApplicationSerializer(application, context={'request': request}).data)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return self.queryset.filter(application__user=user)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).select_related('application')

    @action(detail=True, methods=['patch'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        n = self.get_object()
        n.is_read = True
        n.save(update_fields=['is_read'])
        return Response(NotificationSerializer(n).data)
