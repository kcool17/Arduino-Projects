#!/usr/bin/env python

#Imports
import discord  
from discord.ext import commands

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from server import DEVS
import os


SCOPES = 'https://www.googleapis.com/auth/classroom.courses.readonly'

class Data(commands.Cog)):
    def __init__(self, bot):
        self.bot = bot

    def check_dev(ctx):
        global DEVS
        return ctx.author.id in DEVS
    
    @commands.command(name = "getcourses")
    @commands.check(check_dev)
    async def get_courses(self, ctx):
        print(0)
        store = file.Storage('data_files' + os.sep + 'token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('data_files' + os.sep + 'credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('classroom', 'v1', http=creds.authorize(Http()))
        
        print(1)
        results = service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])
        print(2)
        if not courses:
            await ctx.send('No courses found.')
        else:
            await ctx.send('Courses:')
            for course in courses:
                await ctx.send(course['name'])
        print(3)


def setup(bot):
    bot.add_cog(Data(bot))
