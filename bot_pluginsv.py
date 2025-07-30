## for Paper, Spigot

import discord
from discord import app_commands
import subprocess

TOKEN = "your_token"
client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

mc_process = None

@tree.command(name='start', description=' サーバーを起動します。')
async def start_server(interaction: discord.Interaction):
    global mc_process
    if mc_process is None or mc_process.poll() is not None:
        mc_process = subprocess.Popen(
            ['bash', 'start.sh'],
            stdin=subprocess.PIPE,
            stdout=None,
            stderr=subprocess.STDOUT,
            text=True
        )
        await interaction.response.send_message("サーバーを起動しました。")
    else:
        await interaction.response.send_message("サーバーはすでに起動中です。")

@tree.command(name='stop', description='サーバーを停止します。')
async def stop_server(interaction: discord.Interaction):
    global mc_process
    if mc_process is not None and mc_process.poll() is None:
        mc_process.stdin.write("stop\n")
        mc_process.stdin.flush()
        await interaction.response.send_message("サーバー停止コマンドを送信しました。")
    else:
        await interaction.response.send_message("サーバーは起動していません。")

@tree.command(name='restart', description='サーバーを再起動します。')
async def restart_server(interaction: discord.Interaction):
    global mc_process
    if mc_process is not None and mc_process.poll() is None:
        mc_process.stdin.write("restart\n")
        mc_process.stdin.flush()
        await interaction.response.send_message("サーバー再起動コマンドを送信しました。")
    else:
        await interaction.response.send_message("サーバーは起動していません。")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Minecraft"))
    await tree.sync()
    print("login complete!")

client.run(TOKEN)