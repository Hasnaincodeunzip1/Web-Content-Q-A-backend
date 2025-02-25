from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    urls = serializers.ListField(child=serializers.URLField())
    question = serializers.CharField()

    # You could add custom validation logic here if needed.  For example,
    # to limit the number of URLs:
    #
    # def validate_urls(self, value):
    #     if len(value) > 5:  # Example: Limit to 5 URLs
    #         raise serializers.ValidationError("You can only provide a maximum of 5 URLs.")
    #     return value