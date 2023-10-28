from django.contrib import admin

from client.models import Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'comment')


@admin.register(Mailing)
class ClientMailing(admin.ModelAdmin):
    list_display = ('time', 'period', 'status')


@admin.register(Message)
class ClientMessage(admin.ModelAdmin):
    list_display = ('title', 'content')

