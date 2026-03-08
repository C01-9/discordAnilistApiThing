import requests
import discord
from discord.ext import commands



#client = discord.Client()

intents = discord.Intents.default()
intents.members=True
intents.message_content = True
client=commands.Bot(command_prefix='!', intents=intents)

#stolen from anilist docs
# Here we define our query as a multi-line string
queryId = '''
query ($id: Int) { # Define which variables will be used in the query (id)
  Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    id
    title {
      romaji
      english
      native
    }
    coverImage {
      medium
      color
    }
    episodes
    description
  }
}
'''
querySearch = '''
query ($search: String!) { # Define which variables will be used in the query (id)
  Page {
    media(search: $search, type: ANIME) {
      id
    title {
      romaji
      english
      native
    }
    coverImage {
      medium
      color
    }
    episodes
    description
    }
  }
}
'''
# Define our query variables and values that will be used in the query request
variables = {
    'id': 130003
}
url = 'https://graphql.anilist.co'

""" response = requests.post(url, json={'query': query, 'variables': variables}) """

def splitDataId(response):
    data = response.json()
    media = data['data']['Media']
    title = media['title']['english'] or media['title']['romaji'] or media['title']['native']
    cover_image = media['coverImage']['medium']
    cover_color = media['coverImage']['color'] or discord.Colour.random()
    episodes = media['episodes']
    description = media['description'].replace("<br>", " ").replace("<i>", "*").replace("</i>", "*") if media['description'] else "No description available."
    
    return {
        'title': title,
        'cover_image': cover_image,
        'cover_color': cover_color,
        'episodes': episodes,
        'description': description
    }
def splitDataSearch(response):
    data = response.json()
    results = []
    for i in response.json()['data']['Page']['media']:
        print(str(i['title']['english'])+"|"+str(i['id']))
        results.append("[" + str(i['title']['english']) + "](https://anilist.co/anime/" + str(i['id']) + ")" + " | " + str(i['id']))
    return "\n".join(results)

    """ data = response.json()
    media = data['data']['Page']['media'][index]
    title = media['title']['english'] or media['title']['romaji'] or media['title']['native']
    cover_image = media['coverImage']['medium']
    cover_color = media['coverImage']['color'] or discord.Colour.random()
    episodes = media['episodes']
    description = media['description'].replace("<br>", " ").replace("<i>", "*").replace("</i>", "*") if media['description'] else "No description available."
    
    return {
        'id': media['id'],
        'title': title,
        'cover_image': cover_image,
        'cover_color': cover_color,
        'episodes': episodes,
        'description': description
    } """

    
""" print(response.status_code)
print(response.json())
print("-----------------------------")
print(splitData(response)["title"]) """


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#discord.Embed(colour=Embed.Empty, color=Embed.Empty, title=Embed.Empty, type='rich', url=Embed.Empty, description=Embed.Empty, timestamp=None)

@client.command()
async def getId(ctx, id):
    variables = {
    'id': id
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': queryId, 'variables': variables})
    print(response.status_code)
    print(response.json())

    if response.status_code == 404:
        await ctx.send('Anime not found!')
        return

    embed1=discord.Embed(colour=discord.Colour.from_str(splitDataId(response)['cover_color']), title=splitDataId(response)['title'], description=splitDataId(response)['description'])
    embed1.set_thumbnail(url=splitDataId(response)['cover_image'])
    await ctx.send(embed=embed1)

@client.command()
async def search(ctx, search):
    variables = {
    'search': str(search)
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': querySearch, 'variables': variables})
    print(response.status_code)
    print(response.json())

    if response.status_code == 404:
        await ctx.send('Anime not found!')
        return

    """ embed1=discord.Embed(colour=discord.Colour.from_str(splitDataSearch(response)['cover_color']), title=splitDataSearch(response)['title'], description=splitDataSearch(response)['description'])
    embed1.set_thumbnail(url=splitDataSearch(response)['cover_image'])
    await ctx.send(embed=embed1) """

    embed1=discord.Embed(colour=discord.Colour.random(), title="search results:", description=splitDataSearch(response))
    await ctx.send(embed=embed1)
   
@client.command()
async def meow(ctx):
    response = requests.get("https://cataas.com/cat?json=true")
    await ctx.send(response.json()['url'])

client.run('discord bot token here')
