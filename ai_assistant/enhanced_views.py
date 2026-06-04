"""
Enhanced AI Assistant Views - Conversations, Recommendations & Web Search
"""
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .services import EnhancedAIService, AIServiceError
from .models import ConversationSession, ConversationMessage, AIRecommendation
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


# ============= Conversation Endpoints =============

@extend_schema(
    parameters=[
        OpenApiParameter(name='language', description='Language code (en, ar, es, fr, etc.)', required=False),
    ],
    request={'type': 'object', 'properties': {'title': {'type': 'string'}}},
    tags=['AI Chat'],
    description='Create a new conversation session'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_conversation(request):
    """Create a new conversation session"""
    try:
        language = request.data.get('language', 'en')
        title = request.data.get('title', 'New Chat')
        
        ai_service = EnhancedAIService()
        session = ai_service.conversation_service.create_session(
            user=request.user,
            language=language,
            title=title
        )
        
        return Response({
            'success': True,
            'session_id': session.id,
            'language': session.language,
            'title': session.title,
            'message_count': session.message_count,
            'created_at': session.created_at
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f"Failed to create conversation: {e}")
        return Response(
            {'error': 'Failed to create conversation', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request={'type': 'object', 'properties': {'message': {'type': 'string'}}},
    tags=['AI Chat'],
    description='Send a message in the conversation'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, session_id):
    """Send a message and get AI response"""
    try:
        message = request.data.get('message', '').strip()
        if not message:
            return Response(
                {'error': 'Message cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get session
        session = get_object_or_404(ConversationSession, id=session_id, user=request.user)
        
        # Generate response
        ai_service = EnhancedAIService()
        result = ai_service.chat(session=session, user_message=message, user=request.user)
        
        if not result.get('success'):
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': True,
            'message': result['content'],
            'language': result['language'],
            'recommendations': result['recommendations'],
            'sources': result['sources'],
            'tokens_used': result['tokens_used'],
            'processing_time': result['processing_time'],
            'session_id': session_id
        }, status=status.HTTP_200_OK)
    
    except ConversationSession.DoesNotExist:
        return Response(
            {'error': 'Conversation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return Response(
            {'error': 'Failed to send message', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    tags=['AI Chat'],
    description='Get conversation history'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request, session_id):
    """Get full conversation history"""
    try:
        session = get_object_or_404(ConversationSession, id=session_id, user=request.user)
        messages = session.messages.all().order_by('created_at')
        
        message_list = [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.created_at,
                'language': msg.original_language
            }
            for msg in messages
        ]
        
        return Response({
            'success': True,
            'session_id': session.id,
            'title': session.title,
            'language': session.language,
            'message_count': session.message_count,
            'tokens_used': session.tokens_used,
            'created_at': session.created_at,
            'messages': message_list
        }, status=status.HTTP_200_OK)
    
    except ConversationSession.DoesNotExist:
        return Response(
            {'error': 'Conversation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        return Response(
            {'error': 'Failed to get conversation', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    tags=['AI Chat'],
    description='List all user conversations'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_conversations(request):
    """List all conversations for the user"""
    try:
        sessions = ConversationSession.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-updated_at')
        
        session_list = [
            {
                'session_id': s.id,
                'title': s.title or f'Chat {s.id}',
                'language': s.language,
                'message_count': s.message_count,
                'tokens_used': s.tokens_used,
                'created_at': s.created_at,
                'updated_at': s.updated_at
            }
            for s in sessions
        ]
        
        return Response({
            'success': True,
            'count': len(session_list),
            'sessions': session_list
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        return Response(
            {'error': 'Failed to list conversations', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============= Recommendations Endpoints =============

@extend_schema(
    parameters=[
        OpenApiParameter(name='language', description='Language code', required=False),
        OpenApiParameter(name='type', description='Recommendation type', required=False),
    ],
    tags=['Recommendations'],
    description='Get personalized recommendations'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """Get personalized product recommendations"""
    try:
        language = request.query_params.get('language', 'en')
        rec_type = request.query_params.get('type', None)
        
        # Get user's recent interactions
        ai_service = EnhancedAIService()
        user_profile = {
            'recent_interests': ['electronics', 'technology', 'gadgets']
        }
        
        recommendations = ai_service.recommendation_service.generate_recommendations(
            user_profile, language
        )
        
        return Response({
            'success': True,
            'language': language,
            'count': len(recommendations),
            'recommendations': recommendations
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return Response(
            {'error': 'Failed to get recommendations', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    tags=['Recommendations'],
    description='Record recommendation click'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_recommendation_click(request, rec_id):
    """Record when a user clicks on a recommendation"""
    try:
        rec = AIRecommendation.objects.get(id=rec_id, user=request.user)
        rec.clicked = True
        rec.save()
        
        return Response({
            'success': True,
            'message': 'Recommendation click recorded'
        }, status=status.HTTP_200_OK)
    
    except AIRecommendation.DoesNotExist:
        return Response(
            {'error': 'Recommendation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error recording click: {e}")
        return Response(
            {'error': 'Failed to record click', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============= Web Search Endpoints =============

@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Search query', required=True),
        OpenApiParameter(name='language', description='Language code', required=False),
    ],
    tags=['Web Search'],
    description='Search the web for information'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def web_search(request):
    """Search the web for information"""
    try:
        query = request.query_params.get('q', '').strip()
        language = request.query_params.get('language', 'en')
        
        if not query:
            return Response(
                {'error': 'Search query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ai_service = EnhancedAIService()
        results = ai_service.web_service.search(query, language=language)
        
        return Response({
            'success': True,
            'query': query,
            'language': language,
            'result_count': len(results),
            'results': results
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return Response(
            {'error': 'Search failed', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============= Language & Translation Endpoints =============

@extend_schema(
    tags=['Language'],
    description='Get supported languages'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supported_languages(request):
    """Get list of supported languages"""
    languages = {
        'en': 'English',
        'ar': 'العربية (Arabic)',
        'es': 'Español (Spanish)',
        'fr': 'Français (French)',
        'de': 'Deutsch (German)',
        'zh': '中文 (Chinese)',
        'ja': '日本語 (Japanese)',
        'pt': 'Português (Portuguese)',
        'ru': 'Русский (Russian)',
        'hi': 'हिन्दी (Hindi)',
    }
    
    return Response({
        'success': True,
        'languages': languages
    }, status=status.HTTP_200_OK)


@extend_schema(
    request={'type': 'object', 'properties': {
        'text': {'type': 'string'},
        'target_language': {'type': 'string'}
    }},
    tags=['Language'],
    description='Detect language and optionally translate'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_and_translate(request):
    """Detect language and translate to target language"""
    try:
        text = request.data.get('text', '').strip()
        target_language = request.data.get('target_language', 'en')
        
        if not text:
            return Response(
                {'error': 'Text is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ai_service = EnhancedAIService()
        detected_lang = ai_service.language_service.detect_language(text)
        
        translated_text = ai_service.language_service.translate_text(text, target_language)
        
        return Response({
            'success': True,
            'original_text': text,
            'detected_language': detected_lang,
            'target_language': target_language,
            'translated_text': translated_text
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return Response(
            {'error': 'Translation failed', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============= Product Assist with Language Support =============

@extend_schema(
    request={'type': 'object', 'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'price': {'type': 'number'},
        'language': {'type': 'string', 'default': 'en'}
    }},
    tags=['AI Assistant'],
    description='AI product enhancement with language support'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_assist_multilingual(request):
    """AI-powered product enhancement with multilingual support"""
    try:
        product_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'category': request.data.get('category'),
            'price': request.data.get('price')
        }
        language = request.data.get('language', 'en')
        
        if not product_data['name']:
            return Response(
                {'error': 'Product name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ai_service = EnhancedAIService()
        result = ai_service.product_assist(
            product_data=product_data,
            user=request.user,
            language=language
        )
        
        result['success'] = True
        return Response(result, status=status.HTTP_200_OK)
    
    except AIServiceError as e:
        logger.error(f"AI Service error: {e}")
        return Response(
            {'error': 'AI service error', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Error in product assist: {e}")
        return Response(
            {'error': 'Internal server error', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
