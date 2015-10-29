from swampdragon.route_handler import ModelPubRouter
from swampdragon import route_handler

from DatingApp.serializers import ChatMessageSerializer
from DatingApp.models import ChatMessage

CHANNEL_DATA_SUBSCRIBE = 'subscribe'

class ChatMessageRouter(ModelPubRouter):
	#verbs = ModelPubRouter.valid_verbs + ['chat']
	valid_verbs = ['subscribe','chat']
	route_name = 'chat-route'

	serializer_class = ChatMessageSerializer
	model = ChatMessage

	def chat(self, *args, **kwargs):
		try:
			channels = self.get_subscription_channels(**kwargs)
			self.publish(channels, kwargs)
		except Exception as e:
			print('error')
			raise e
	

	def subscribe(self, **kwargs):
		client_channel = kwargs.pop('channel')
		server_channels = self.get_subscription_channels(**kwargs)
		self.send(
				data='subscribed',
				channel_setup=self.make_channel_data(client_channel, server_channels, CHANNEL_DATA_SUBSCRIBE),
				**kwargs)
		self.connection.pub_sub.subscribe(server_channels, self.connection)

	def get_subscription_channels(self, **kwargs):
		if('servingChannel' in kwargs):
			self.testServerChannels()
			roomName = kwargs['servingChannel']
			if(roomName not in serviceChannels):
				serviceChannels.append(roomName)
				print(serviceChannels.count(True))
				return serviceChannels
		return ['chatroom']

	def testServerChannels(self):
		try:
			global serviceChannels
			if(serviceChannels.count(True)<=0):
				serviceChannels = []
			else:
				print(serviceChannels.count(True));
		except NameError:
			serviceChannels = []


route_handler.register(ChatMessageRouter)