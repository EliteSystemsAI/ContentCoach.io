import pytest
from unittest.mock import patch
from app import app
from app.models import db, User

@pytest.fixture
def client():
    """Configure Flask test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index_redirect_to_onboarding(client):
    """Test that index redirects to onboarding when no user session"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/onboarding' in response.location

def test_index_redirect_to_chat(client):
    """Test that index redirects to chat when user session exists"""
    with client.session_transaction() as session:
        session['user_id'] = 1
    response = client.get('/')
    assert response.status_code == 302
    assert '/chat' in response.location

def test_onboarding_get(client):
    """Test GET request to onboarding page"""
    response = client.get('/onboarding')
    assert response.status_code == 200
    assert b'onboarding.html' in response.data

def test_onboarding_post_success(client):
    """Test successful user creation through onboarding"""
    test_data = {
        'name': 'Test User',
        'business_niche': 'Digital Marketing',
        'content_goals': 'Grow social media presence'
    }
    
    response = client.post('/onboarding', 
                          json=test_data,
                          content_type='application/json')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    
    with app.app_context():
        user = User.query.filter_by(name='Test User').first()
        assert user is not None
        assert user.business_niche == 'Digital Marketing'
        assert user.content_goals == 'Grow social media presence'

def test_onboarding_post_missing_data(client):
    """Test onboarding with missing required fields"""
    test_data = {
        'name': 'Test User'
        # Missing required fields
    }
    
    response = client.post('/onboarding', 
                          json=test_data,
                          content_type='application/json')
    
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data['success'] is False
    assert 'error' in json_data

def test_chat_page_no_session(client):
    """Test chat page access without session"""
    response = client.get('/chat')
    assert response.status_code == 302
    assert '/onboarding' in response.location

def test_chat_page_with_session(client):
    """Test chat page access with valid session"""
    with app.app_context():
        user = User(name='Test User',
                   business_niche='Digital Marketing',
                   content_goals='Grow social media presence')
        db.session.add(user)
        db.session.commit()
        
        with client.session_transaction() as session:
            session['user_id'] = user.id
            
        response = client.get('/chat')
        assert response.status_code == 200
        assert b'chat.html' in response.data
        assert b'Test User' in response.data

@patch('app.chat_handler.generate_content')
def test_chat_post_success(mock_generate_content, client):
    """Test successful chat message processing"""
    mock_generate_content.return_value = "Here's your content strategy advice..."
    
    with app.app_context():
        user = User(name='Test User',
                   business_niche='Digital Marketing',
                   content_goals='Grow social media presence')
        db.session.add(user)
        db.session.commit()
        
        with client.session_transaction() as session:
            session['user_id'] = user.id
    
        response = client.post('/chat',
                             data={'message': 'How can I improve my content?'})
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'response' in json_data
        assert json_data['response'] == "Here's your content strategy advice..."

def test_chat_post_no_session(client):
    """Test chat endpoint without session"""
    response = client.post('/chat',
                          data={'message': 'Test message'})
    
    assert response.status_code == 401
    json_data = response.get_json()
    assert 'error' in json_data
    assert 'Please complete onboarding first' in json_data['error']

def test_chat_post_no_message(client):
    """Test chat endpoint with missing message"""
    with client.session_transaction() as session:
        session['user_id'] = 1
        
    response = client.post('/chat', data={})
    
    assert response.status_code == 500
    json_data = response.get_json()
    assert 'error' in json_data
    assert 'No message provided' in json_data['error']

@patch('app.chat_handler.generate_content')
def test_chat_post_api_error(mock_generate_content, client):
    """Test chat endpoint handling of API errors"""
    mock_generate_content.return_value = "An error occurred: API Error"
    
    with app.app_context():
        user = User(name='Test User',
                   business_niche='Digital Marketing',
                   content_goals='Grow social media presence')
        db.session.add(user)
        db.session.commit()
        
        with client.session_transaction() as session:
            session['user_id'] = user.id
    
        response = client.post('/chat',
                             data={'message': 'How can I improve my content?'})
        
        assert response.status_code == 500
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'API Error' in json_data['error']
