function Subscribe(channel)
{
	swampdragon.subscribe('chat-route','local-channel',{servingChannel: channel},null,null);
}

function UnSubscribe(channel)
{
	//swampdragon.unsubscribe('chat-route','local-channel',{servingChannel: channel},null,null);
}

function GetToken(user, otherUser)
{
	tokenValue = '';
	if(user < otherUser)
	{
		tokenValue = user + '||' + otherUser;
	}
	else if(user > otherUser)
	{
		tokenValue = otherUser + '||' + user;
	}
	else if(user === otherUser)
	{
	}
	return tokenValue;
}


function ChatWindowModel(title, tokenValue)
{
	var chatWindowHtml = "<div class='col-sm-3'  id='chatWindow'>"
		chatWindowHtml +=	"<div id='chatWindowHeader'>"
		chatWindowHtml +=		"<button class='close' id='closeCurrentChat'>&times;</button>"
		chatWindowHtml +=		"<label class='label-control' id='chatTitle'>"+title+"</label>"
		chatWindowHtml +=		"<input id='modelToken' name='modelToken' type='hidden' value='"+ tokenValue +"'>"
		chatWindowHtml +=	"</div>"
		chatWindowHtml +=	"<div id='chatDisplay'>"
		chatWindowHtml +=	"</div>"
		chatWindowHtml +=	"<fieldset>"
		chatWindowHtml +=		"<div id='chatComposeArea'>"
		chatWindowHtml +=			"<div>"
		chatWindowHtml +=				"<textarea class='form-control' id='chatComposer'></textarea>"
		chatWindowHtml +=			"</div>"
		chatWindowHtml +=			"<div>"
		chatWindowHtml +=				"<button class='btn' id='sendMessage'>Send</button>"
		chatWindowHtml +=			"</div>"
		chatWindowHtml +=		"</div>"
		chatWindowHtml +=	"</fieldset>"
		chatWindowHtml +="</div>"

	return chatWindowHtml;	
}


function CompareTokens(currentToken)
{
	var duplicatToken = false;
	$('#modelToken').each(function(i)
	{
		if($(this).val()===currentToken)
		{
			duplicatToken = true;
		}
	});
	return duplicatToken;
}

function AppendMessageToChatWindow(messageData)
{
	var chatWindowElement;
	var token = messageData.servingChannel;
	var from = messageData.from;
	var message = messageData.message;
	$('#modelToken').each(function(i)
		{
			if($(this).val() === token)
			{
				chatWindowElement =$(this).parents('#chatWindow');
				return false;
			}
		});
	if(chatWindowElement === 'undefined' || chatWindowElement.length == 0)
	{

	}
	else 
	{
		var chatDisplay = chatWindowElement.find('#chatDisplay');
		var newMsg ;
		if(from === $('#userEmailId').val())
		{
			newMsg +="<br>"
			newMsg = "<div class='right-message'>"
			newMsg +=	"<div class='right-arrow'></div>"
			newMsg +=	"<div class='message-content right-message-content'>"
			newMsg +=		message
			newMsg +=	"</div>"
			newMsg +="</div>"
			newMsg +="<br>"
		}
		else
		{
			newMsg +="<br>"
			newMsg = "<div class='left-message'>"
			newMsg +=	"<div class='left-arrow'></div>"
			newMsg +=	"<div class='message-content left-message-content'>"
			newMsg +=		message;
			newMsg +=	"</div>"
			newMsg +="</div>"
			newMsg +="<br>"
			
		}

		var previousMessages = chatDisplay.html();
		if(previousMessages.length == 0)
		{
			

		}
		newMsg = previousMessages + newMsg;
		chatDisplay.html(newMsg);
	}
}

$(document).ready(function()
	{

		$(document).on('click','#sendMessage',function()
		{
			var button = $(this);
			var chatWindow = $(this).parents('#chatWindow');
			var message = chatWindow.find('#chatComposer').val();
			var servingChannel = chatWindow.find('#modelToken').val();
			var from = $('#userEmailId').val();
			debugger;
			swampdragon.callRouter('chat','chat-route',{servingChannel: servingChannel,message: message,from: from},null,null);
			chatWindow.find('#chatComposer').val('');
			return false;
		});

		$(document).on('click','label',function()
		{

			if(!$(this).hasClass('chatLabel'))
			{
				return;
			}

			var numberOfChats =	$('#chatArea > div').length;
			var title = $(this).text();
			var windowSize = $(window).width();			
			var chatWindowWidth = $('#chatWindow').width();
			var user = $('#userEmailId').val();
			var otherUser = $(this).siblings('#emailId').val();
			var tokenValue, chatWindow;

			if(windowSize<= (numberOfChats*chatWindowWidth))
			{
				alert('chat windows reached max count please close the previous chat(s) to open new chats');
				return;
			}
			tokenValue = GetToken(user,otherUser)
			if(CompareTokens(tokenValue))
			{
				return;
			}
			var previousChats = $('#chatArea').html();
			var newChat = ChatWindowModel(title, tokenValue);
			var newChat = newChat + previousChats;
			$('#chatArea').html(newChat);
			Subscribe(tokenValue);
		});

		$(document).on('click','#closeCurrentChat',function()
		{
			var chatWindow = $(this).parents('#chatWindow');
			var channel = chatWindow.find('#modelToken').val();
			chatWindow.remove();
			UnSubscribe(channel);
		});
	});

swampdragon.onChannelMessage(function(channels, data)
	{
		AppendMessageToChatWindow(data)
	});

