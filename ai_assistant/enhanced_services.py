"""
Enhanced AI Service Layer - Multilingual, Web Search & Recommendations
Integrates Groq API with language detection, translation, web search, and smart recommendations
"""
import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import (
    AIRequest, ConversationSession, ConversationMessage,
    AIRecommendation, WebSearchCache
)

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass


class LanguageService:
    """Handle language detection and translation"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'ar': 'Arabic',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'hi': 'Hindi',
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            from langdetect import detect
            lang = detect(text)
            # Map to our supported languages
            return lang if lang in self.supported_languages else 'en'
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'en'
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        if target_language == 'en':
            return text
        
        try:
            from google.cloud import translate_v2
            client = translate_v2.Client()
            result = client.translate_text(text, target_language=target_language)
            return result['translatedText']
        except Exception as e:
            logger.warning(f"Translation failed: {e}")
            return text


class WebSearchService:
    """Handle web search for product recommendations and information"""
    
    def __init__(self):
        self.cache_duration = 86400  # 24 hours
    
    def search(self, query: str, language: str = 'en', use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Search the web using DuckDuckGo
        Returns cached results if available
        """
        # Check cache
        if use_cache:
            cached = self._get_cached_results(query, language)
            if cached:
                logger.info(f"Using cached search results for: {query}")
                return cached
        
        try:
            from duckduckgo_search import DDGS
            import requests
            from bs4 import BeautifulSoup
            
            ddgs = DDGS()
            results = []
            
            # Search with language parameter
            search_results = ddgs.text(query, region=self._get_region(language), max_results=5)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': 'web'
                })
            
            # Cache the results
            self._cache_results(query, language, results)
            logger.info(f"Web search completed for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return []
    
    def _get_cached_results(self, query: str, language: str) -> Optional[List[Dict]]:
        """Get cached search results if not expired"""
        try:
            cache = WebSearchCache.objects.get(query=query, language=language)
            if cache.expires_at > timezone.now():
                return cache.results
            else:
                cache.delete()
        except WebSearchCache.DoesNotExist:
            pass
        return None
    
    def _cache_results(self, query: str, language: str, results: List[Dict]):
        """Cache search results"""
        try:
            WebSearchCache.objects.update_or_create(
                query=query,
                language=language,
                defaults={
                    'results': results,
                    'expires_at': timezone.now() + timedelta(seconds=self.cache_duration)
                }
            )
        except Exception as e:
            logger.warning(f"Failed to cache search results: {e}")
    
    def _get_region(self, language: str) -> str:
        """Map language to region for search"""
        region_map = {
            'en': 'us',
            'ar': 'sa',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'zh': 'cn',
            'ja': 'jp',
            'pt': 'br',
            'ru': 'ru',
            'hi': 'in',
        }
        return region_map.get(language, 'us')


class RecommendationService:
    """Generate intelligent product and store recommendations"""
    
    def __init__(self, language_service: LanguageService, web_service: WebSearchService):
        self.language_service = language_service
        self.web_service = web_service
    
    def generate_recommendations(self, user_profile: Dict[str, Any], language: str = 'en') -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on user profile"""
        recommendations = []
        
        try:
            # Get recent purchases and preferences
            recent_interests = user_profile.get('recent_interests', [])
            
            if recent_interests:
                for interest in recent_interests:
                    # Search for related products
                    search_results = self.web_service.search(
                        f"best {interest} products 2024",
                        language=language
                    )
                    
                    if search_results:
                        rec = {
                            'title': f"Popular {interest}",
                            'description': search_results[0]['snippet'],
                            'recommendation_type': 'trending',
                            'language': language,
                            'reason': f"Based on your interest in {interest}",
                            'data': search_results[0],
                            'confidence_score': 0.85
                        }
                        recommendations.append(rec)
            
            return recommendations[:5]  # Return top 5
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return []


class ConversationService:
    """Manage multi-turn conversations with context"""
    
    def __init__(self, client, language_service: LanguageService):
        self.client = client
        self.language_service = language_service
    
    def create_session(self, user, language: str = 'en', title: str = '') -> ConversationSession:
        """Create a new conversation session"""
        session = ConversationSession.objects.create(
            user=user,
            language=language,
            title=title or 'New Chat'
        )
        logger.info(f"Created conversation session {session.id} for user {user.username}")
        return session
    
    def add_message(self, session: ConversationSession, role: str, content: str, 
                   original_language: str = '') -> ConversationMessage:
        """Add a message to the conversation"""
        message = ConversationMessage.objects.create(
            session=session,
            role=role,
            content=content,
            original_language=original_language or session.language
        )
        session.message_count += 1
        session.save()
        return message
    
    def get_context(self, session: ConversationSession, max_messages: int = 10) -> List[Dict[str, str]]:
        """Get conversation context for the AI model"""
        messages = session.messages.all().order_by('created_at')[-max_messages:]
        return [
            {
                'role': msg.role,
                'content': msg.content
            }
            for msg in messages
        ]


class EnhancedAIService:
    """
    Enhanced AI Service with multilingual support, web search, and recommendations
    """
    
    def __init__(self):
        self.mock_mode = settings.AI_MOCK_MODE
        self.client = None
        self.language_service = LanguageService()
        self.web_service = WebSearchService()
        self.recommendation_service = RecommendationService(
            self.language_service, self.web_service
        )
        
        # Try to initialize Groq client if not in mock mode
        if not self.mock_mode and settings.GROQ_API_KEY:
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                self.conversation_service = ConversationService(
                    self.client, self.language_service
                )
                logger.info("Enhanced AI Service initialized successfully")
            except ImportError as e:
                logger.warning(f"Groq package not available: {e}. Falling back to mock mode.")
                self.mock_mode = True
            except Exception as e:
                logger.error(f"Failed to initialize AI service: {e}")
                self.mock_mode = True
        else:
            logger.info("Running in mock mode")
            self.mock_mode = True
    
    def chat(self, session: ConversationSession, user_message: str, user=None) -> Dict[str, Any]:
        """
        Multi-turn conversation with language support and web search
        """
        start_time = time.time()
        
        try:
            # Detect language
            detected_language = self.language_service.detect_language(user_message)
            if detected_language != session.language:
                user_message = self._translate_if_needed(user_message, session.language)
            
            # Add user message to conversation
            self.conversation_service.add_message(
                session, 'user', user_message, detected_language
            )
            
            # Get conversation context
            context = self.conversation_service.get_context(session)
            
            # Generate response with web search context
            if self.mock_mode or not self.client:
                response = self._mock_chat_response(user_message, session.language)
            else:
                response = self._groq_chat_response(user_message, context, session.language)
            
            # Add assistant message to conversation
            self.conversation_service.add_message(
                session, 'assistant', response['content'], session.language
            )
            
            # Generate recommendations based on conversation
            recommendations = self.recommendation_service.generate_recommendations(
                {'recent_interests': self._extract_interests(user_message)},
                session.language
            )
            
            processing_time = time.time() - start_time
            
            result = {
                'success': True,
                'content': response['content'],
                'language': session.language,
                'recommendations': recommendations,
                'sources': response.get('sources', []),
                'tokens_used': response.get('tokens_used', 0),
                'processing_time': round(processing_time, 2),
                'session_id': session.id,
                'mode': 'mock' if self.mock_mode else 'groq'
            }
            
            # Log to database
            if user:
                try:
                    session.tokens_used += result['tokens_used']
                    session.save()
                except Exception as e:
                    logger.error(f"Failed to update session: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': round(time.time() - start_time, 2)
            }
    
    def _groq_chat_response(self, message: str, context: List[Dict], language: str) -> Dict[str, Any]:
        """Generate response using Groq API with web search context"""
        try:
            # Search for relevant information
            search_results = self.web_service.search(message, language=language)
            
            system_prompt = f"""You are a helpful multilingual AI assistant that speaks {language}.
You provide detailed, helpful responses and can recommend products and deals.
When relevant, incorporate information from web searches to provide current and accurate information.

Current Language: {language}
Today's Date: {datetime.now().strftime('%Y-%m-%d')}

Web Search Context:
{json.dumps(search_results[:3], ensure_ascii=False)}

Guidelines:
- Always respond in {language}
- Be helpful and friendly
- Provide recommendations when appropriate
- Include sources when using web search information
- Be concise but thorough"""
            
            messages = [
                {"role": "system", "content": system_prompt},
                *context,
                {"role": "user", "content": message}
            ]
            
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            return {
                'content': content,
                'sources': search_results[:3] if search_results else [],
                'tokens_used': response.usage.total_tokens,
            }
            
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            raise AIServiceError(f"AI response generation failed: {e}")
    
    def _mock_chat_response(self, message: str, language: str) -> Dict[str, Any]:
        """Generate mock chat response"""
        language_greetings = {
            'ar': 'مرحباً! كيف يمكنني مساعدتك اليوم؟',
            'es': '¡Hola! ¿Cómo puedo ayudarte hoy?',
            'fr': 'Bonjour! Comment puis-je vous aider aujourd\'hui?',
            'de': 'Hallo! Wie kann ich dir heute helfen?',
            'zh': '你好！我今天能帮你什么？',
            'ja': 'こんにちは！今日はどのようにお手伝いできますか？',
            'pt': 'Olá! Como posso ajudá-lo hoje?',
            'ru': 'Привет! Как я могу вам помочь?',
            'hi': 'नमस्ते! आज मैं आपकी कैसे मदद कर सकता हूँ?',
        }
        
        greeting = language_greetings.get(language, 'Hello! How can I help you today?')
        response = f"{greeting}\n\nYou asked: {message[:100]}...\n\nI'm here to help with product recommendations, store setup, and general questions!"
        
        return {
            'content': response,
            'sources': [],
            'tokens_used': 0,
        }
    
    def _translate_if_needed(self, text: str, target_language: str) -> str:
        """Translate text if language differs"""
        if target_language == 'en':
            return text
        return self.language_service.translate_text(text, target_language)
    
    def _extract_interests(self, message: str) -> List[str]:
        """Extract user interests from message"""
        keywords = ['product', 'store', 'need', 'looking for', 'want', 'recommend']
        interests = []
        words = message.lower().split()
        
        for i, word in enumerate(words):
            if any(kw in word for kw in keywords):
                if i + 1 < len(words):
                    interests.append(words[i + 1])
        
        return interests
    
    def product_assist(self, product_data: Dict[str, Any], user=None, language: str = 'en') -> Dict[str, Any]:
        """Enhance product information with language support"""
        start_time = time.time()
        
        try:
            if self.mock_mode or not self.client:
                result = self._mock_product_assist(product_data, language)
            else:
                result = self._groq_product_assist(product_data, language)
        except Exception as e:
            logger.error(f"Product assist error: {e}")
            result = self._mock_product_assist(product_data, language)
            result['fallback_used'] = True
            result['error_message'] = str(e)
        
        processing_time = time.time() - start_time
        result['processing_time'] = round(processing_time, 2)
        result['language'] = language
        
        if user:
            try:
                AIRequest.objects.create(
                    user=user,
                    request_type='product_assist',
                    input_data=product_data,
                    output_data=result,
                    tokens_used=result.get('tokens_used', 0),
                    processing_time=processing_time
                )
            except Exception as e:
                logger.error(f"Failed to log AI request: {e}")
        
        return result
    
    def _mock_product_assist(self, product_data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Mock product assistance in multiple languages"""
        name = product_data.get('name', 'Product')
        description = product_data.get('description', '')
        
        translations = {
            'ar': f"تحسين {name} - جودة عالية",
            'es': f"Premium {name} - Alta Calidad",
            'fr': f"Premium {name} - Haute Qualité",
            'zh': f"高级{name} - 高品质",
        }
        
        improved_title = translations.get(language, f"Premium {name} - High Quality")
        
        return {
            'improved_title': improved_title,
            'seo_description': description or f"Shop {name} online",
            'category_suggestions': ['Electronics', 'Accessories'],
            'tags': ['premium', 'quality', 'best seller'],
            'meta_title': f"Buy {name}",
            'meta_description': f"Shop {name} online",
            'tokens_used': 0,
            'mode': 'mock'
        }
    
    def _groq_product_assist(self, product_data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Groq-based product assistance"""
        if not self.client:
            raise AIServiceError("AI client not initialized")
        
        name = product_data.get('name', '')
        description = product_data.get('description', '')
        category = product_data.get('category', '')
        price = product_data.get('price', '')
        
        language_names = {
            'ar': 'Arabic', 'es': 'Spanish', 'fr': 'French',
            'zh': 'Chinese', 'ja': 'Japanese'
        }
        lang_name = language_names.get(language, 'English')
        
        prompt = f"""You are an ecommerce expert. Respond in {lang_name}.
Enhance this product information:
- Name: {name}
- Description: {description}
- Category: {category}
- Price: ${price}

Provide JSON with: improved_title, seo_description, category_suggestions, tags, meta_title, meta_description"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": f"You are an expert ecommerce optimizer. Respond in {lang_name}. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            result['tokens_used'] = response.usage.total_tokens
            result['mode'] = 'groq'
            
            return result
            
        except Exception as e:
            logger.error(f"Groq product assist failed: {e}")
            raise AIServiceError(f"Product assistance failed: {e}")


# Backward compatibility
class AIService(EnhancedAIService):
    """Maintain backward compatibility with existing code"""
    pass
