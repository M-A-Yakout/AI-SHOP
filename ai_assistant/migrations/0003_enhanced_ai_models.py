# Generated migration for enhanced AI models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ai_assistant', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Create ConversationSession model
        migrations.CreateModel(
            name='ConversationSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('ar', 'Arabic'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German'), ('zh', 'Chinese'), ('ja', 'Japanese'), ('pt', 'Portuguese'), ('ru', 'Russian'), ('hi', 'Hindi')], default='en', max_length=5)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('context', models.JSONField(default=dict, help_text='Conversation context and metadata')),
                ('message_count', models.IntegerField(default=0)),
                ('tokens_used', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_conversations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        
        # Create ConversationMessage model
        migrations.CreateModel(
            name='ConversationMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')], max_length=20)),
                ('content', models.TextField()),
                ('original_language', models.CharField(blank=True, max_length=5)),
                ('translated_content', models.JSONField(default=dict, help_text='Translations in other languages')),
                ('metadata', models.JSONField(default=dict, help_text='Additional message metadata (sources, references, etc.)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='ai_assistant.conversationsession')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        
        # Create AIRecommendation model
        migrations.CreateModel(
            name='AIRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation_type', models.CharField(choices=[('product', 'Product Recommendation'), ('store', 'Store Recommendation'), ('category', 'Category Suggestion'), ('deal', 'Special Deal'), ('trending', 'Trending Item')], max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('language', models.CharField(default='en', max_length=5)),
                ('reason', models.TextField(help_text='Why this recommendation was made')),
                ('data', models.JSONField(default=dict, help_text='Product/store data or link references')),
                ('confidence_score', models.FloatField(default=0.0, help_text='Confidence of recommendation (0-1)')),
                ('clicked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ai_recommendations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        
        # Create WebSearchCache model
        migrations.CreateModel(
            name='WebSearchCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=500, unique=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('results', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(help_text='When this cache expires')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        
        # Add index to WebSearchCache
        migrations.AddIndex(
            model_name='websearchcache',
            index=models.Index(fields=['query', 'language'], name='ai_assistan_query_lang_idx'),
        ),
    ]
