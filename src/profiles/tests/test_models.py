import os
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from src.profiles.models import RelationshipType, Interests, PersonalityType, Education, \
    ZodiacSign, QueUser

import pytest


class TestProfileModel(TestCase):
    @pytest.mark.django_db
    def test_relationship_type_model(self):
        relationship_type = RelationshipType.objects.create(relation_goals='S')
        assert str(relationship_type) == 'S'

    @pytest.mark.django_db
    def test_interests_model(self):
        interests = Interests.objects.create(interests='sports')
        assert interests.interests == 'sports'

    @pytest.mark.django_db
    def test_personality_type_model(self):
        personality_type = PersonalityType.objects.create(personality_type='ISTJ')
        assert str(personality_type) == 'ISTJ'

    @pytest.mark.django_db
    def test_education_model(self):
        education = Education.objects.create(name='HS')
        assert str(education) == 'HS'

    @pytest.mark.django_db
    def test_zodiac_sign_model(self):
        zodiac_sign = ZodiacSign.objects.create(zodiac_sign='leo')
        assert str(zodiac_sign) == 'leo'

    @pytest.mark.django_db
    def test_que_user_model(self):
        user = QueUser.objects.create(
            username='test_users',
            phone='1234567890',
            birthday='2000-01-01',
        )
        assert user.id is not None
        assert user.telegram_id == 1
        assert user.username == 'test_users'
        assert user.phone == '1234567890'
        assert user.birthday == '2000-01-01'
