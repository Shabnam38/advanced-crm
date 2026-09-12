from django.test import TestCase
from leads.models import Lead
from .models import Interaction

class InteractionModelTests(TestCase):
    def test_create_interaction(self):
        lead = Lead.objects.create(full_name="Test Lead")
        interaction = Interaction.objects.create(
            lead=lead,
            interaction_type='call',
            summary="Discussed pricing",
        )
        self.assertEqual(interaction.interaction_type, 'call')