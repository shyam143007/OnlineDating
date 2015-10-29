from swampdragon.serializers.model_serializer import ModelSerializer

class ChatMessageSerializer(ModelSerializer):
	class Meta:
		model = 'DatingApp.ChatMessage'
		publish_fields = ['message','from']