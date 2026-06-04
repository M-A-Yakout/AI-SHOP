"""
AI Assistant serializers with comprehensive validation and documentation
"""
from rest_framework import serializers


class ProductAssistRequestSerializer(serializers.Serializer):
    """
    Serializer for product assistance request
    
    Required fields:
    - name: Product name
    
    Optional fields:
    - description: Product description
    - category: Product category
    - price: Product price
    """
    name = serializers.CharField(
        max_length=300,
        required=True,
        help_text="Product name (required)"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Product description (optional)"
    )
    category = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text="Product category (optional)"
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Product price (optional)"
    )
    
    def validate_name(self, value):
        """Validate product name is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Product name cannot be empty")
        return value.strip()
    
    def validate_price(self, value):
        """Validate price is positive"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Price must be positive")
        return value


class ProductAssistResponseSerializer(serializers.Serializer):
    """
    Serializer for product assistance response
    """
    improved_title = serializers.CharField(
        help_text="AI-generated improved product title"
    )
    seo_description = serializers.CharField(
        help_text="SEO-optimized product description"
    )
    category_suggestions = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of suggested categories"
    )
    tags = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of relevant product tags"
    )
    meta_title = serializers.CharField(
        help_text="SEO meta title"
    )
    meta_description = serializers.CharField(
        help_text="SEO meta description"
    )
    tokens_used = serializers.IntegerField(
        help_text="Number of AI tokens used (0 for mock mode)"
    )
    mode = serializers.CharField(
        help_text="Mode used: 'openai' or 'mock'"
    )
    processing_time = serializers.FloatField(
        help_text="Processing time in seconds"
    )
    success = serializers.BooleanField(
        default=True,
        help_text="Whether the request was successful"
    )
    fallback_used = serializers.BooleanField(
        required=False,
        help_text="Whether fallback mode was used due to API error"
    )
    error_message = serializers.CharField(
        required=False,
        help_text="Error message if fallback was used"
    )


class StoreGeneratorRequestSerializer(serializers.Serializer):
    """
    Serializer for store generation request
    """
    idea = serializers.CharField(
        max_length=500,
        required=True,
        help_text="Store concept or idea (e.g., 'organic skincare', 'sports equipment')"
    )
    
    def validate_idea(self, value):
        """Validate store idea is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Store idea cannot be empty")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Store idea must be at least 3 characters")
        return value.strip()


class StoreInfoSerializer(serializers.Serializer):
    """Store information"""
    name = serializers.CharField()
    description = serializers.CharField()
    tagline = serializers.CharField()


class CategoryInfoSerializer(serializers.Serializer):
    """Category information"""
    name = serializers.CharField()
    description = serializers.CharField()


class ProductInfoSerializer(serializers.Serializer):
    """Product information"""
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    category = serializers.CharField()


class StoreGeneratorResponseSerializer(serializers.Serializer):
    """
    Serializer for store generation response
    """
    store = StoreInfoSerializer(
        help_text="Generated store information"
    )
    categories = CategoryInfoSerializer(
        many=True,
        help_text="List of suggested categories"
    )
    sample_products = ProductInfoSerializer(
        many=True,
        help_text="List of sample products"
    )
    tokens_used = serializers.IntegerField(
        help_text="Number of AI tokens used (0 for mock mode)"
    )
    mode = serializers.CharField(
        help_text="Mode used: 'openai' or 'mock'"
    )
    processing_time = serializers.FloatField(
        help_text="Processing time in seconds"
    )
    success = serializers.BooleanField(
        default=True,
        help_text="Whether the request was successful"
    )
    fallback_used = serializers.BooleanField(
        required=False,
        help_text="Whether fallback mode was used due to API error"
    )
    error_message = serializers.CharField(
        required=False,
        help_text="Error message if fallback was used"
    )


class AIUsageStatsSerializer(serializers.Serializer):
    """
    Serializer for AI usage statistics
    """
    total_requests = serializers.IntegerField(
        help_text="Total number of AI requests"
    )
    product_assist_count = serializers.IntegerField(
        help_text="Number of product assist requests"
    )
    store_generator_count = serializers.IntegerField(
        help_text="Number of store generator requests"
    )
    total_tokens_used = serializers.IntegerField(
        help_text="Total AI tokens consumed"
    )
    avg_processing_time = serializers.FloatField(
        help_text="Average processing time in seconds"
    )
    success = serializers.BooleanField(
        default=True,
        help_text="Whether the request was successful"
    )


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for error responses
    """
    error = serializers.CharField(
        help_text="Error type"
    )
    message = serializers.CharField(
        help_text="Error message"
    )
    details = serializers.DictField(
        required=False,
        help_text="Additional error details"
    )
    success = serializers.BooleanField(
        default=False,
        help_text="Always false for errors"
    )


class AutomatedStoreRequestSerializer(serializers.Serializer):
    """
    Serializer for automated store creation request
    """
    idea = serializers.CharField(
        max_length=500,
        required=True,
        help_text="Store concept or idea (e.g., 'sports clothing store', 'organic coffee shop')"
    )
    
    def validate_idea(self, value):
        """Validate store idea is not empty and has minimum length"""
        if not value or not value.strip():
            raise serializers.ValidationError("Store idea cannot be empty")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Store idea must be at least 3 characters")
        return value.strip()


class AutomatedStoreInfoSerializer(serializers.Serializer):
    """Store information in automation response"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    url = serializers.CharField()
    api_url = serializers.CharField()
    products_count = serializers.IntegerField()


class AutomatedCategorySerializer(serializers.Serializer):
    """Category information in automation response"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()


class AutomatedBrandSerializer(serializers.Serializer):
    """Brand information in automation response"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()


class AutomatedProductSerializer(serializers.Serializer):
    """Product information in automation response"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    price = serializers.CharField()
    category = serializers.CharField(allow_null=True)
    status = serializers.CharField()
    url = serializers.CharField()


class AutomatedStoreSummarySerializer(serializers.Serializer):
    """Summary information in automation response"""
    total_categories = serializers.IntegerField()
    total_products = serializers.IntegerField()
    ai_mode = serializers.CharField()
    tokens_used = serializers.IntegerField()
    processing_time = serializers.FloatField()


class AutomatedStoreResponseSerializer(serializers.Serializer):
    """
    Serializer for automated store creation response
    """
    success = serializers.BooleanField(
        help_text="Whether the store was created successfully"
    )
    message = serializers.CharField(
        help_text="Success message"
    )
    store = AutomatedStoreInfoSerializer(
        help_text="Created store information"
    )
    categories = AutomatedCategorySerializer(
        many=True,
        help_text="List of created categories"
    )
    brand = AutomatedBrandSerializer(
        help_text="Created brand information"
    )
    products = AutomatedProductSerializer(
        many=True,
        help_text="List of created products"
    )
    summary = AutomatedStoreSummarySerializer(
        help_text="Summary of what was created"
    )
    next_steps = serializers.ListField(
        child=serializers.CharField(),
        help_text="Suggested next steps"
    )


# ============= Conversation Serializers =============

class ConversationMessageSerializer(serializers.Serializer):
    """Serializer for conversation messages"""
    role = serializers.CharField(help_text="Message role: 'user', 'assistant', or 'system'")
    content = serializers.CharField(help_text="Message content")
    timestamp = serializers.DateTimeField(help_text="When the message was sent")
    language = serializers.CharField(help_text="Language of the message")


class ConversationSessionSerializer(serializers.Serializer):
    """Serializer for conversation sessions"""
    session_id = serializers.IntegerField(help_text="Session ID")
    title = serializers.CharField(help_text="Session title")
    language = serializers.CharField(help_text="Primary language")
    message_count = serializers.IntegerField(help_text="Number of messages")
    tokens_used = serializers.IntegerField(help_text="Total tokens used")
    created_at = serializers.DateTimeField(help_text="When session was created")
    updated_at = serializers.DateTimeField(help_text="When session was last updated")


class CreateConversationSerializer(serializers.Serializer):
    """Serializer for creating conversation"""
    title = serializers.CharField(required=False, allow_blank=True, help_text="Conversation title")
    language = serializers.CharField(default='en', help_text="Language code")


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending messages"""
    message = serializers.CharField(help_text="User message")
    language = serializers.CharField(required=False, help_text="Language (auto-detected if not provided)")


# ============= Recommendation Serializers =============

class RecommendationDataSerializer(serializers.Serializer):
    """Serializer for recommendation data"""
    title = serializers.CharField(help_text="Recommendation title")
    description = serializers.CharField(help_text="Recommendation description")
    reason = serializers.CharField(help_text="Why this is recommended")
    confidence_score = serializers.FloatField(help_text="Confidence score 0-1")
    url = serializers.CharField(required=False, help_text="URL to product/deal")


class AIRecommendationSerializer(serializers.Serializer):
    """Serializer for AI recommendations"""
    recommendation_id = serializers.IntegerField(help_text="Recommendation ID")
    type = serializers.CharField(help_text="Type of recommendation")
    title = serializers.CharField(help_text="Recommendation title")
    description = serializers.CharField(help_text="Recommendation description")
    language = serializers.CharField(help_text="Language")
    reason = serializers.CharField(help_text="Why recommended")
    confidence_score = serializers.FloatField(help_text="Confidence 0-1")
    data = serializers.JSONField(help_text="Additional data")
    created_at = serializers.DateTimeField(help_text="When recommended")


# ============= Web Search Serializers =============

class SearchResultSerializer(serializers.Serializer):
    """Serializer for web search results"""
    title = serializers.CharField(help_text="Result title")
    url = serializers.CharField(help_text="Result URL")
    snippet = serializers.CharField(help_text="Search snippet")
    source = serializers.CharField(help_text="Source type")


class WebSearchResponseSerializer(serializers.Serializer):
    """Serializer for web search response"""
    success = serializers.BooleanField(help_text="Whether search succeeded")
    query = serializers.CharField(help_text="Search query")
    language = serializers.CharField(help_text="Search language")
    result_count = serializers.IntegerField(help_text="Number of results")
    results = SearchResultSerializer(many=True, help_text="Search results")


# ============= Language Serializers =============

class LanguageSerializer(serializers.Serializer):
    """Serializer for language code and name"""
    code = serializers.CharField(help_text="Language code")
    name = serializers.CharField(help_text="Language name")


class DetectTranslateSerializer(serializers.Serializer):
    """Serializer for language detection and translation"""
    text = serializers.CharField(help_text="Text to detect/translate")
    target_language = serializers.CharField(default='en', help_text="Target language code")


class DetectTranslateResponseSerializer(serializers.Serializer):
    """Serializer for detect/translate response"""
    success = serializers.BooleanField(help_text="Whether operation succeeded")
    original_text = serializers.CharField(help_text="Original text")
    detected_language = serializers.CharField(help_text="Detected language")
    target_language = serializers.CharField(help_text="Target language")
    translated_text = serializers.CharField(help_text="Translated text")


# ============= Chat Response Serializer =============

class ChatMessageSerializer(serializers.Serializer):
    """Serializer for chat message response"""
    success = serializers.BooleanField(help_text="Whether message succeeded")
    message = serializers.CharField(help_text="AI response message")
    language = serializers.CharField(help_text="Response language")
    recommendations = AIRecommendationSerializer(many=True, help_text="Recommendations")
    sources = SearchResultSerializer(many=True, help_text="Web search sources")
    tokens_used = serializers.IntegerField(help_text="Tokens used")
    processing_time = serializers.FloatField(help_text="Processing time in seconds")
    session_id = serializers.IntegerField(help_text="Conversation session ID")
