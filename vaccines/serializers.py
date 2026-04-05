from rest_framework import serializers
from vaccines.models import Vaccine, Species

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['code', 'name']

class VaccineSerializer(serializers.ModelSerializer):
    applicable_species = SpeciesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Vaccine
        fields = ['id', 'name', 'category', 'description', 'applicable_species']
