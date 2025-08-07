from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import uuid
import json

from .models import (
    AnalyticsEvent, PageView, UserSession, Metric, Report, 
    Dashboard, Widget, Export, EventType, PageType, SessionType
)
from .serializers import (
    AnalyticsEventSerializer, PageViewSerializer, UserSessionSerializer,
    MetricSerializer, ReportSerializer, DashboardSerializer, WidgetSerializer,
    ExportSerializer, EventTypeSerializer, PageTypeSerializer, SessionTypeSerializer
)

User = get_user_model()


class AnalyticsModelsTest(TestCase):
    """Test cases for Analytics models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.event_type = EventType.objects.create(
            name='click',
            description='User click event',
            category='interaction'
        )
        
        self.page_type = PageType.objects.create(
            name='course',
            description='Course page',
            category='education'
        )
        
        self.session_type = SessionType.objects.create(
            name='web',
            description='Web session',
            category='browser'
        )
    
    def test_event_type_creation(self):
        """Test EventType model creation"""
        event_type = EventType.objects.create(
            name='scroll',
            description='User scroll event',
            category='interaction'
        )
        
        self.assertEqual(event_type.name, 'scroll')
        self.assertEqual(event_type.description, 'User scroll event')
        self.assertEqual(event_type.category, 'interaction')
        self.assertTrue(event_type.is_active)
        self.assertIsNotNone(event_type.id)
    
    def test_page_type_creation(self):
        """Test PageType model creation"""
        page_type = PageType.objects.create(
            name='profile',
            description='User profile page',
            category='user'
        )
        
        self.assertEqual(page_type.name, 'profile')
        self.assertEqual(page_type.description, 'User profile page')
        self.assertEqual(page_type.category, 'user')
        self.assertTrue(page_type.is_active)
        self.assertIsNotNone(page_type.id)
    
    def test_session_type_creation(self):
        """Test SessionType model creation"""
        session_type = SessionType.objects.create(
            name='mobile',
            description='Mobile session',
            category='device'
        )
        
        self.assertEqual(session_type.name, 'mobile')
        self.assertEqual(session_type.description, 'Mobile session')
        self.assertEqual(session_type.category, 'device')
        self.assertTrue(session_type.is_active)
        self.assertIsNotNone(session_type.id)
    
    def test_analytics_event_creation(self):
        """Test AnalyticsEvent model creation"""
        event = AnalyticsEvent.objects.create(
            event_name='button_click',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30),
            metadata={'button_id': 'submit', 'page': '/courses'}
        )
        
        self.assertEqual(event.event_name, 'button_click')
        self.assertEqual(event.event_type, self.event_type)
        self.assertEqual(event.user, self.user)
        self.assertIsNotNone(event.session_id)
        self.assertIsNotNone(event.created_at)
        self.assertIsNotNone(event.updated_at)
    
    def test_page_view_creation(self):
        """Test PageView model creation"""
        page_view = PageView.objects.create(
            page_url='/courses/python-basics',
            page_title='Python Basics Course',
            page_type=self.page_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(minutes=5),
            metadata={'referrer': '/courses', 'scroll_depth': 75}
        )
        
        self.assertEqual(page_view.page_url, '/courses/python-basics')
        self.assertEqual(page_view.page_title, 'Python Basics Course')
        self.assertEqual(page_view.page_type, self.page_type)
        self.assertEqual(page_view.user, self.user)
        self.assertIsNotNone(page_view.session_id)
        self.assertIsNotNone(page_view.created_at)
        self.assertIsNotNone(page_view.updated_at)
    
    def test_user_session_creation(self):
        """Test UserSession model creation"""
        session = UserSession.objects.create(
            user=self.user,
            session_type=self.session_type,
            session_id=str(uuid.uuid4()),
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            device_info={'device': 'desktop', 'browser': 'chrome'}
        )
        
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.session_type, self.session_type)
        self.assertIsNotNone(session.session_id)
        self.assertEqual(session.ip_address, '192.168.1.1')
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(session.updated_at)
    
    def test_metric_creation(self):
        """Test Metric model creation"""
        metric = Metric.objects.create(
            name='Total Page Views',
            description='Total number of page views',
            metric_type='count',
            count_value=1500,
            metadata={'source': 'analytics', 'period': 'monthly'}
        )
        
        self.assertEqual(metric.name, 'Total Page Views')
        self.assertEqual(metric.description, 'Total number of page views')
        self.assertEqual(metric.metric_type, 'count')
        self.assertEqual(metric.count_value, 1500)
        self.assertIsNotNone(metric.created_at)
        self.assertIsNotNone(metric.updated_at)
    
    def test_report_creation(self):
        """Test Report model creation"""
        report = Report.objects.create(
            name='User Engagement Report',
            description='Monthly user engagement metrics',
            report_type='user_engagement',
            created_by=self.user,
            is_public=True,
            filters={'date_range': 'last_30_days', 'user_type': 'all'},
            metadata={'generated_at': timezone.now().isoformat()}
        )
        
        self.assertEqual(report.name, 'User Engagement Report')
        self.assertEqual(report.description, 'Monthly user engagement metrics')
        self.assertEqual(report.report_type, 'user_engagement')
        self.assertEqual(report.created_by, self.user)
        self.assertTrue(report.is_public)
        self.assertIsNotNone(report.created_at)
        self.assertIsNotNone(report.updated_at)
    
    def test_widget_creation(self):
        """Test Widget model creation"""
        report = Report.objects.create(
            name='Test Report',
            report_type='user_engagement',
            created_by=self.user
        )
        
        widget = Widget.objects.create(
            name='Page Views Chart',
            description='Chart showing page views over time',
            widget_type='chart',
            report=report,
            config={'chart_type': 'line', 'data_source': 'page_views'},
            metadata={'refresh_interval': 300}
        )
        
        self.assertEqual(widget.name, 'Page Views Chart')
        self.assertEqual(widget.description, 'Chart showing page views over time')
        self.assertEqual(widget.widget_type, 'chart')
        self.assertEqual(widget.report, report)
        self.assertIsNotNone(widget.created_at)
        self.assertIsNotNone(widget.updated_at)
    
    def test_dashboard_creation(self):
        """Test Dashboard model creation"""
        dashboard = Dashboard.objects.create(
            name='Analytics Dashboard',
            description='Main analytics dashboard',
            created_by=self.user,
            is_public=True,
            layout={'widgets': [{'id': 1, 'position': 'top-left'}]},
            metadata={'theme': 'dark', 'refresh_rate': 60}
        )
        
        self.assertEqual(dashboard.name, 'Analytics Dashboard')
        self.assertEqual(dashboard.description, 'Main analytics dashboard')
        self.assertEqual(dashboard.created_by, self.user)
        self.assertTrue(dashboard.is_public)
        self.assertIsNotNone(dashboard.created_at)
        self.assertIsNotNone(dashboard.updated_at)
    
    def test_export_creation(self):
        """Test Export model creation"""
        report = Report.objects.create(
            name='Test Report',
            report_type='user_engagement',
            created_by=self.user
        )
        
        export = Export.objects.create(
            name='User Engagement Report Export',
            description='Exported user engagement data',
            export_type='pdf',
            report=report,
            created_by=self.user,
            metadata={'export_format': 'pdf', 'include_charts': True}
        )
        
        self.assertEqual(export.name, 'User Engagement Report Export')
        self.assertEqual(export.description, 'Exported user engagement data')
        self.assertEqual(export.export_type, 'pdf')
        self.assertEqual(export.report, report)
        self.assertEqual(export.created_by, self.user)
        self.assertIsNotNone(export.created_at)
        self.assertIsNotNone(export.updated_at)


class AnalyticsSerializersTest(TestCase):
    """Test cases for Analytics serializers"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.event_type = EventType.objects.create(
            name='click',
            description='User click event',
            category='interaction'
        )
        
        self.page_type = PageType.objects.create(
            name='course',
            description='Course page',
            category='education'
        )
        
        self.session_type = SessionType.objects.create(
            name='web',
            description='Web session',
            category='browser'
        )
    
    def test_event_type_serializer(self):
        """Test EventTypeSerializer"""
        data = {
            'name': 'scroll',
            'description': 'User scroll event',
            'category': 'interaction',
            'is_active': True,
            'metadata': {'tracking_enabled': True}
        }
        
        serializer = EventTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        event_type = serializer.save()
        self.assertEqual(event_type.name, 'scroll')
        self.assertEqual(event_type.description, 'User scroll event')
        self.assertEqual(event_type.category, 'interaction')
        self.assertTrue(event_type.is_active)
    
    def test_page_type_serializer(self):
        """Test PageTypeSerializer"""
        data = {
            'name': 'profile',
            'description': 'User profile page',
            'category': 'user',
            'is_active': True,
            'metadata': {'requires_auth': True}
        }
        
        serializer = PageTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        page_type = serializer.save()
        self.assertEqual(page_type.name, 'profile')
        self.assertEqual(page_type.description, 'User profile page')
        self.assertEqual(page_type.category, 'user')
        self.assertTrue(page_type.is_active)
    
    def test_session_type_serializer(self):
        """Test SessionTypeSerializer"""
        data = {
            'name': 'mobile',
            'description': 'Mobile session',
            'category': 'device',
            'is_active': True,
            'metadata': {'device_type': 'mobile'}
        }
        
        serializer = SessionTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        session_type = serializer.save()
        self.assertEqual(session_type.name, 'mobile')
        self.assertEqual(session_type.description, 'Mobile session')
        self.assertEqual(session_type.category, 'device')
        self.assertTrue(session_type.is_active)
    
    def test_analytics_event_serializer(self):
        """Test AnalyticsEventSerializer"""
        data = {
            'event_name': 'button_click',
            'event_type': self.event_type.id,
            'user': self.user.id,
            'session_id': str(uuid.uuid4()),
            'session_start': timezone.now(),
            'session_end': timezone.now() + timedelta(seconds=30),
            'metadata': {'button_id': 'submit', 'page': '/courses'},
            'tags': ['interaction', 'button']
        }
        
        serializer = AnalyticsEventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        event = serializer.save()
        self.assertEqual(event.event_name, 'button_click')
        self.assertEqual(event.event_type, self.event_type)
        self.assertEqual(event.user, self.user)
        self.assertIsNotNone(event.session_id)
    
    def test_page_view_serializer(self):
        """Test PageViewSerializer"""
        data = {
            'page_url': '/courses/python-basics',
            'page_title': 'Python Basics Course',
            'page_type': self.page_type.id,
            'user': self.user.id,
            'session_id': str(uuid.uuid4()),
            'session_start': timezone.now(),
            'session_end': timezone.now() + timedelta(minutes=5),
            'metadata': {'referrer': '/courses', 'scroll_depth': 75},
            'tags': ['course', 'python']
        }
        
        serializer = PageViewSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        page_view = serializer.save()
        self.assertEqual(page_view.page_url, '/courses/python-basics')
        self.assertEqual(page_view.page_title, 'Python Basics Course')
        self.assertEqual(page_view.page_type, self.page_type)
        self.assertEqual(page_view.user, self.user)
    
    def test_user_session_serializer(self):
        """Test UserSessionSerializer"""
        data = {
            'user': self.user.id,
            'session_type': self.session_type.id,
            'session_id': str(uuid.uuid4()),
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=1),
            'ip_address': '192.168.1.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'device_info': {'device': 'desktop', 'browser': 'chrome'},
            'metadata': {'session_quality': 'high'},
            'tags': ['web', 'desktop']
        }
        
        serializer = UserSessionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        session = serializer.save()
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.session_type, self.session_type)
        self.assertIsNotNone(session.session_id)
        self.assertEqual(session.ip_address, '192.168.1.1')
    
    def test_metric_serializer(self):
        """Test MetricSerializer"""
        data = {
            'name': 'Total Page Views',
            'description': 'Total number of page views',
            'metric_type': 'count',
            'count_value': 1500,
            'metadata': {'source': 'analytics', 'period': 'monthly'},
            'tags': ['page_views', 'total']
        }
        
        serializer = MetricSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        metric = serializer.save()
        self.assertEqual(metric.name, 'Total Page Views')
        self.assertEqual(metric.description, 'Total number of page views')
        self.assertEqual(metric.metric_type, 'count')
        self.assertEqual(metric.count_value, 1500)
    
    def test_report_serializer(self):
        """Test ReportSerializer"""
        data = {
            'name': 'User Engagement Report',
            'description': 'Monthly user engagement metrics',
            'report_type': 'user_engagement',
            'is_public': True,
            'filters': {'date_range': 'last_30_days', 'user_type': 'all'},
            'metadata': {'generated_at': timezone.now().isoformat()},
            'tags': ['engagement', 'monthly']
        }
        
        serializer = ReportSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        report = serializer.save(created_by=self.user)
        self.assertEqual(report.name, 'User Engagement Report')
        self.assertEqual(report.description, 'Monthly user engagement metrics')
        self.assertEqual(report.report_type, 'user_engagement')
        self.assertEqual(report.created_by, self.user)
        self.assertTrue(report.is_public)
    
    def test_widget_serializer(self):
        """Test WidgetSerializer"""
        report = Report.objects.create(
            name='Test Report',
            report_type='user_engagement',
            created_by=self.user
        )
        
        data = {
            'name': 'Page Views Chart',
            'description': 'Chart showing page views over time',
            'widget_type': 'chart',
            'report': report.id,
            'config': {'chart_type': 'line', 'data_source': 'page_views'},
            'metadata': {'refresh_interval': 300},
            'tags': ['chart', 'page_views']
        }
        
        serializer = WidgetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        widget = serializer.save()
        self.assertEqual(widget.name, 'Page Views Chart')
        self.assertEqual(widget.description, 'Chart showing page views over time')
        self.assertEqual(widget.widget_type, 'chart')
        self.assertEqual(widget.report, report)
    
    def test_dashboard_serializer(self):
        """Test DashboardSerializer"""
        data = {
            'name': 'Analytics Dashboard',
            'description': 'Main analytics dashboard',
            'is_public': True,
            'layout': {'widgets': [{'id': 1, 'position': 'top-left'}]},
            'metadata': {'theme': 'dark', 'refresh_rate': 60},
            'tags': ['dashboard', 'analytics']
        }
        
        serializer = DashboardSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        dashboard = serializer.save(created_by=self.user)
        self.assertEqual(dashboard.name, 'Analytics Dashboard')
        self.assertEqual(dashboard.description, 'Main analytics dashboard')
        self.assertEqual(dashboard.created_by, self.user)
        self.assertTrue(dashboard.is_public)
    
    def test_export_serializer(self):
        """Test ExportSerializer"""
        report = Report.objects.create(
            name='Test Report',
            report_type='user_engagement',
            created_by=self.user
        )
        
        data = {
            'name': 'User Engagement Report Export',
            'description': 'Exported user engagement data',
            'export_type': 'pdf',
            'report': report.id,
            'metadata': {'export_format': 'pdf', 'include_charts': True},
            'tags': ['export', 'pdf']
        }
        
        serializer = ExportSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        export = serializer.save(created_by=self.user)
        self.assertEqual(export.name, 'User Engagement Report Export')
        self.assertEqual(export.description, 'Exported user engagement data')
        self.assertEqual(export.export_type, 'pdf')
        self.assertEqual(export.report, report)
        self.assertEqual(export.created_by, self.user)


class AnalyticsAPITest(APITestCase):
    """Test cases for Analytics API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.event_type = EventType.objects.create(
            name='click',
            description='User click event',
            category='interaction'
        )
        
        self.page_type = PageType.objects.create(
            name='course',
            description='Course page',
            category='education'
        )
        
        self.session_type = SessionType.objects.create(
            name='web',
            description='Web session',
            category='browser'
        )
        
        # Authenticate user
        self.client.force_authenticate(user=self.user)
    
    def test_event_type_list(self):
        """Test EventType list endpoint"""
        url = reverse('event-type-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'click')
    
    def test_event_type_create(self):
        """Test EventType create endpoint"""
        url = reverse('event-type-list')
        data = {
            'name': 'scroll',
            'description': 'User scroll event',
            'category': 'interaction',
            'is_active': True,
            'metadata': {'tracking_enabled': True}
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'scroll')
        self.assertEqual(response.data['description'], 'User scroll event')
    
    def test_analytics_event_create(self):
        """Test AnalyticsEvent create endpoint"""
        url = reverse('analytics-event-list')
        data = {
            'event_name': 'button_click',
            'event_type': self.event_type.id,
            'session_id': str(uuid.uuid4()),
            'session_start': timezone.now(),
            'session_end': timezone.now() + timedelta(seconds=30),
            'metadata': {'button_id': 'submit', 'page': '/courses'},
            'tags': ['interaction', 'button']
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['event_name'], 'button_click')
        self.assertEqual(response.data['event_type'], self.event_type.id)
    
    def test_analytics_event_stats(self):
        """Test AnalyticsEvent stats endpoint"""
        # Create some test events
        AnalyticsEvent.objects.create(
            event_name='button_click',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30)
        )
        
        url = reverse('event-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_events', response.data)
        self.assertIn('unique_users', response.data)
    
    def test_page_view_create(self):
        """Test PageView create endpoint"""
        url = reverse('page-view-list')
        data = {
            'page_url': '/courses/python-basics',
            'page_title': 'Python Basics Course',
            'page_type': self.page_type.id,
            'session_id': str(uuid.uuid4()),
            'session_start': timezone.now(),
            'session_end': timezone.now() + timedelta(minutes=5),
            'metadata': {'referrer': '/courses', 'scroll_depth': 75},
            'tags': ['course', 'python']
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['page_url'], '/courses/python-basics')
        self.assertEqual(response.data['page_title'], 'Python Basics Course')
    
    def test_page_view_stats(self):
        """Test PageView stats endpoint"""
        # Create some test page views
        PageView.objects.create(
            page_url='/courses/python-basics',
            page_title='Python Basics Course',
            page_type=self.page_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(minutes=5)
        )
        
        url = reverse('page-view-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_views', response.data)
        self.assertIn('unique_views', response.data)
    
    def test_user_session_create(self):
        """Test UserSession create endpoint"""
        url = reverse('user-session-list')
        data = {
            'session_type': self.session_type.id,
            'session_id': str(uuid.uuid4()),
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=1),
            'ip_address': '192.168.1.1',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'device_info': {'device': 'desktop', 'browser': 'chrome'},
            'metadata': {'session_quality': 'high'},
            'tags': ['web', 'desktop']
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['session_type'], self.session_type.id)
        self.assertEqual(response.data['ip_address'], '192.168.1.1')
    
    def test_user_session_stats(self):
        """Test UserSession stats endpoint"""
        # Create some test sessions
        UserSession.objects.create(
            user=self.user,
            session_type=self.session_type,
            session_id=str(uuid.uuid4()),
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            ip_address='192.168.1.1'
        )
        
        url = reverse('session-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_sessions', response.data)
        self.assertIn('unique_users', response.data)
    
    def test_report_create(self):
        """Test Report create endpoint"""
        url = reverse('report-list')
        data = {
            'name': 'User Engagement Report',
            'description': 'Monthly user engagement metrics',
            'report_type': 'user_engagement',
            'is_public': True,
            'filters': {'date_range': 'last_30_days', 'user_type': 'all'},
            'metadata': {'generated_at': timezone.now().isoformat()},
            'tags': ['engagement', 'monthly']
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'User Engagement Report')
        self.assertEqual(response.data['report_type'], 'user_engagement')
    
    def test_dashboard_create(self):
        """Test Dashboard create endpoint"""
        url = reverse('dashboard-list')
        data = {
            'name': 'Analytics Dashboard',
            'description': 'Main analytics dashboard',
            'is_public': True,
            'layout': {'widgets': [{'id': 1, 'position': 'top-left'}]},
            'metadata': {'theme': 'dark', 'refresh_rate': 60},
            'tags': ['dashboard', 'analytics']
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Analytics Dashboard')
        self.assertEqual(response.data['description'], 'Main analytics dashboard')
    
    def test_analytics_overview(self):
        """Test analytics overview endpoint"""
        # Create some test data
        AnalyticsEvent.objects.create(
            event_name='button_click',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30)
        )
        
        PageView.objects.create(
            page_url='/courses/python-basics',
            page_title='Python Basics Course',
            page_type=self.page_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(minutes=5)
        )
        
        UserSession.objects.create(
            user=self.user,
            session_type=self.session_type,
            session_id=str(uuid.uuid4()),
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            ip_address='192.168.1.1'
        )
        
        url = reverse('analytics-overview')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_events', response.data)
        self.assertIn('total_page_views', response.data)
        self.assertIn('total_sessions', response.data)
        self.assertIn('total_users', response.data)
    
    def test_analytics_real_time(self):
        """Test analytics real-time endpoint"""
        url = reverse('analytics-real-time')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('active_users', response.data)
        self.assertIn('active_sessions', response.data)
        self.assertIn('events_last_hour', response.data)
        self.assertIn('page_views_last_hour', response.data)
    
    def test_analytics_user_engagement(self):
        """Test analytics user engagement endpoint"""
        # Create some test data
        UserSession.objects.create(
            user=self.user,
            session_type=self.session_type,
            session_id=str(uuid.uuid4()),
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            ip_address='192.168.1.1'
        )
        
        url = reverse('analytics-user-engagement')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_analytics_conversion_funnel(self):
        """Test analytics conversion funnel endpoint"""
        url = reverse('analytics-conversion-funnel')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_unauthorized_access(self):
        """Test unauthorized access to analytics endpoints"""
        # Create a non-staff user
        regular_user = User.objects.create_user(
            email='regular@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=regular_user)
        
        # Try to access analytics data
        url = reverse('analytics-event-list')
        response = self.client.get(url)
        
        # Should only see their own data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No events for this user
    
    def test_filtering_and_search(self):
        """Test filtering and search functionality"""
        # Create test events
        AnalyticsEvent.objects.create(
            event_name='button_click',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30)
        )
        
        AnalyticsEvent.objects.create(
            event_name='form_submit',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30)
        )
        
        # Test filtering
        url = reverse('analytics-event-list')
        response = self.client.get(url, {'event_type': self.event_type.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test search
        response = self.client.get(url, {'search': 'button'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event_name'], 'button_click')
    
    def test_ordering(self):
        """Test ordering functionality"""
        # Create test events with different timestamps
        event1 = AnalyticsEvent.objects.create(
            event_name='first_event',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30)
        )
        
        event2 = AnalyticsEvent.objects.create(
            event_name='second_event',
            event_type=self.event_type,
            user=self.user,
            session_id=str(uuid.uuid4()),
            session_start=timezone.now(),
            session_end=timezone.now() + timedelta(seconds=30)
        )
        
        # Test ordering by created_at descending
        url = reverse('analytics-event-list')
        response = self.client.get(url, {'ordering': '-created_at'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Second event should come first (newer)
        self.assertEqual(response.data[0]['event_name'], 'second_event')
