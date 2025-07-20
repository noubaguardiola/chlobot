import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random
from discord import app_commands
from typing import List
from keepalive import keepalive
load_dotenv()

keepalive=()

print("Lancement du bot...")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) #acces a discord

#reconnaitre un nouvel arrivant sur le serveur
@bot.event 
async def on_member_join(member):
    channel = member.guild.get_channel(1395995406336528444)
    #souhaiter la bienvenue aux nouveaux membres
    emb=discord.Embed(title="NEW MEMBER",description=f"Bienvenue {member.mention} !")
    await channel.send(embed=emb)
    await channel.send("Tape `/help` pour découvrir ce que je peux faire.")

#simple commande help qui liste les intéractions possibles avec le bot
@bot.tree.command(name="help", description="Affiche les commandes et interactions disponibles")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Voici ce que tu peux me demander :**\n"
        "- `bonjour`, `bonsoir`, `ça va?`\n"
        "- `quelle heure est-il`\n"
        "- `la terre est-elle ronde ?`\n"
        "- `/blague` pour que je raconte une blague\n"
        "- `/conseil_inutile` pour que je donne un conseil inutile\n"
    )


@bot.event #decorateur pour enregistrer l'element
async def on_ready():
    print("bot allumé")
    #synchroniser les commandes
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées: {len(synced)}")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message: discord.Message):
    #empecher le bot de se declencher lui meme
    if message.author == bot.user or message.author.bot:
        return
    
    #permettre au bot de reconnaitre un mot avec des capitales ou miniscules
    content = message.content.lower().strip()

    if content == 'bonjour':
        channel = message.channel
        author = message.author
        #dictionnaire pour stocker les différentes réponses
        reponses = [
            "Sur Discord? En pleine journée? Et le travail?",
            "Et moi qui pensais passer une journée tranquille…",
        ]
        await message.channel.send(random.choice(reponses)) #envoie la réponse en message privé + réponse aléatoire

    
    elif content == 'bonsoir':
        channel = message.channel
        author = message.author
        reponses = [
            "Ne serait il pas temps d’aller se coucher? ",
            "Il est tard. Même les bots ont envie de se déconnecter.",
        ]
        await message.channel.send(random.choice(reponses))

         
#ajout de differentes manieres de demander ça va pour ne pas limiter l'utilisateur
    elif content in ['ça va?', 'ca va?', 'ça va', 'ca va']:
        channel = message.channel
        author = message.author
        reponses = [
            "Je suis un script Python avec des émotions simulées. Donc, oui, ça va.",
            "Statistiquement mieux que la moyenne nationale.",
            "Mieux que quelqu’un qui utilise un dark mode."
        ] 
        await message.channel.send(random.choice(reponses))

    elif content in ['quelle heure est-il', 'quelle heure est-il?', 'quelle heure est il', 'quelle heure est il?', 'il est quelle heure', 'il est quelle heure?']:
        channel = message.channel
        author = message.author
        await message.channel.send('La même heure qu’il était hier à la même heure.')


    elif "terre" in content and "ronde" in content: #rendre la compréhension de la question plus facile en reconnaissant 2 mots clés
        channel = message.channel
        author = message.author
        reponses = [
            "Selon la science, oui. Selon ton oncle complotiste, non.",
            "La prochaine question c’est quoi? Le bot est-il vivant?",
    ]
        await message.channel.send(random.choice(reponses))

    #si le message n'est pas compris
    else:
        await message.channel.send("Je n'ai pas compris. Tape `/blague` pour découvrir ce que je peux faire.")

    await bot.process_commands(message)

#création d'une commande
@bot.tree.command(name="blague", description="Raconte moi une blague")
#ajout d'un choix après la sélection de la commande
@app_commands.choices(choices=[
    #définition des différents choix
    app_commands.Choice(name="Informatique", value="informatique"),
    app_commands.Choice(name="Animaux", value="animaux"),
    app_commands.Choice(name="Meilleures blagues", value="meilleures"),
    ])

async def blague(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    if (choices.value == 'informatique'):
        blagues = [
        "Pourquoi les développeurs n’aiment pas la nature ?\n Parce qu’il y a trop de bugs.",
        "Pourquoi Internet est toujours propre ?\n Parce qu’il nettoie ses cookies tous les jours.",
        "Que dit un ordinateur quand il prend sa retraite ?\n « Je vais enfin pouvoir me mettre en veille ! »",
        "Pourquoi les claviers dépriment ?\n Parce qu’ils en ont marre de se faire taper dessus.",
        "Pourquoi Windows n’aime pas les soirées ?\n Parce qu’il finit toujours par crasher.",
    ]
    elif (choices.value == 'animaux'):
        blagues = [
        "Que dit un escargot quand il croise une limace ?\n « T’as oublié ta maison ! »",
        "Que fait une vache quand elle entend une bonne blague ?\n Elle meugle de rire.",
        "Que fait un chien devant un ordinateur ?\n Il cherche la souris.",
        "Pourquoi les mouches ne vont jamais au cinéma ? \n Parce qu’elles détestent les toiles.",
        "Pourquoi les canards sont toujours à l’heure ? \n Parce qu’ils sont dans l’étang.",
    ]

    elif (choices.value == 'meilleures'):
        blagues = [
        "Deux muffins sont dans un four. \n Le premier dit : « Wouah il fait chaud ici ! » \n Le second répond : « AAAAAH ! UN MUFFIN QUI PARLE !!! »",
        "Pourquoi les squelettes ne se battent jamais entre eux ? \n Parce qu’ils n’ont pas les tripes.",
        "Deux oeufs sont dans un frigo.\n L'un dit a l'autre: « Pourquoi tu es tout vert avec des poils? » \n L'autre répond « Parce que je suis un kiwi »",
        "C’est un citron qui traverse la route. Une voiture passe. \n Le citron dit : « Je me suis fait presser ! »",
        "Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? \n Parce que sinon ils tombent dans le bateau.",
    ]

    await interaction.response.send_message(random.choice(blagues))

@bot.tree.command(name="conseil_inutile", description="Donne moi un conseil inutile")
async def conseil_inutile(interaction: discord.Interaction):
    conseils = [
        "Si ton frigo fait du bruit, réponds-lui. Il se sentira écouté.",
        "Pour trouver ton chemin, suis un pigeon. Ils savent où aller.",
        "Si tu as un trou de mémoire, rebouche-le avec du plâtre.",
        "En cas de stress, transforme-toi en cornichon. Les cornichons ne stressent pas.",
        "Pour éviter d’être en retard, pars la veille.",
    ]
    await interaction.response.send_message(random.choice(conseils))

bot.run(os.getenv('DISCORD_TOKEN')) #récupérer le token qui se situe dans .env

