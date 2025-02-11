from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Group
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    '''The homepage where all groups are listed'''
    groups = Group.objects.all()
    user = request.user
    context = {
        "groups": groups,
        "user": user
    }
    return render(request, template_name="chat/home.html", context=context)


@login_required
def group_chat_view(request, uuid):
    '''The view for a group where all messages and events are sent to the frontend'''

    group = get_object_or_404(Group, uuid=uuid)
    if request.user not in group.members.all():
        return HttpResponseForbidden("You are not a member of this group.\
                                       Kindly use the join button")

    messages = group.message_set.all()
    '''
    messages are the message the members
    of a group send to the group
    '''

    events = group.event_set.all()
    '''
    events are the messages that indicates
    that a user joined or left the group.
    They will be sent automatically when a user join or leave the group
    '''

    # Combine the events and messages for a group
    message_and_event_list = [*messages, *events]

    # Sort the combination by the timestamp so that they are listed in order
    sorted_message_event_list = sorted(message_and_event_list, key=lambda x: x.timestamp)

    # get the list of all group members
    group_members = group.members.all()

    context = {
        "message_and_event_list": sorted_message_event_list,
        "group_members": group_members,
    }

    return render(request, template_name="chat/groupchat.html", context=context)