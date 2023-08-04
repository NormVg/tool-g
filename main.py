import json
import typer
import sys ,os
from typing import List
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt ,Confirm
from rich.markdown import Markdown

Confirm()
theme = Theme({"suc":"green","er":"red","hyl":"cyan"})
data = json.load(open("D:/MyPrograms/toolg/data/command_list.json","r"))

app = typer.Typer()
console = Console(theme=theme)

@app.command("rm")
def remove_command(name:str):
    for i in data:
        if name == i['name']:
            conferm = Prompt.ask(f"Type [green]'remove {i['name']}'[/green] To [red]Delete[/red]")
            if conferm == f"remove {i['name']}":
                data.remove(i)
                json.dump(data,open("D:/MyPrograms/toolg/data/command_list.json","w"),indent=6)
                console.print(f"Deleted [suc]{i['name']}[/suc]",style="er")
            else: console.print("Not matched Process Aborted",style="er")
            return
    console.print(f"[yellow]{name}[/yellow] Not Found, Process Aborted",style="er")
    

@app.command("add")
def add_command(name:str= typer.Argument(default=None),commmand:str= typer.Argument(default=None),disc:str = typer.Argument(default=None)):
    
    if not name or not commmand:
        name = Prompt.ask("[green]Enter Your Command Name[/green]")
        commmand = Prompt.ask("[green]Enter Your Command[green]")
        disc = Prompt.ask("Enter Description", default='None')
        if disc == "None":disc=None

    
    for i in data:
        if name == i['name']:
            console.print(f"{name} already existed, Process Aborted",style="er")
            return
    new = {
            "command": commmand,
            "name": name,
            "disc": disc
      }
    data.append(new)
    json.dump(data,open("D:/MyPrograms/toolg/data/command_list.json","w"),indent=6)
    console.print(f"Command added: \n\t  name - {name} \n\t command - {commmand} \n\t disc - {disc}",style="suc")


@app.command("show")
def show_command(name:str):
    for i in data:
        if name == i['name']:
            console.print(f"Command - [cyan]{i['command']}[/cyan]")
            if i['disc']:
                console.print(f"Disc - {i['disc']}",style="suc")
            return
    console.print(f"[yellow]{name}[/yellow] Not Found, Process Aborted",style="er")

@app.command("update")
def update_command(name:str):
    for i in data:
        if name == i['name']:
            name_new = Prompt.ask("[green]Enter Your Command Name[/green]",default=i['name'])
            command_new = Prompt.ask("[green]Enter Your Command[green]",default=i['command'])
            if None == i['disc']:i['disc']='None'
            disc_new = Prompt.ask("Enter Description",default=i['disc'])
            if disc_new == "None":disc_new=None
            if Confirm.ask("Continue"):
                i['name'] = name_new
                i['command'] = command_new
                i['disc'] = disc_new
                json.dump(data,open("D:/MyPrograms/toolg/data/command_list.json","w"),indent=6)
                console.print(f"Command updated: \n\t name - {name_new} \n\t command - {command_new} \n\t disc - {disc_new}",style="suc")
            return
    console.print(f"[yellow]{name}[/yellow] Not Found, Process Aborted",style="er")

@app.command("exe")
def exe(name:str, args: List[str] = typer.Argument(default=None)):
    for i in data:
        if name == i['name']:
            os.system(i['command']+" ".join(args))
            return
    console.print(f"[yellow]{name}[/yellow] Not Found, Process Aborted",style="er")


def default():
    lst = []
    for i in data:        
        
        lst.append(f"- {i['name']}\n")
    md = """
# ToolG
"""
    md2 = f"""
> All Commands:
{''.join(lst)}
"""
    gmd = Markdown(md)
    gmd2 = Markdown(md2)
    console.print(gmd,style='er')
    console.print(gmd2,style='suc')

    

if __name__ == "__main__":
    if len(sys.argv) >1:
        app()   
    else: typer.run(default)
    
