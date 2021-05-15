# RobotSteve
### A Discord Bot to get Minecraft Stats about your Server
So you want to use this lil hunk of junk, huh? It's not too hard to use it, but know that you *should* know how [discord.py](https://github.com/Rapptz/discord.py) works.
Also know that this bot is supposed to be run on the computer your server is running on because of the commands provided. If you don't want any of this, remove utils.control.control from cogs = \[ ... \] in RobotSteve.py, and disable stats in utils/stats/mcstats->stat - `enabled = False`.

### Modules:
RobotSteve is (primarily) broken into:

RobotSteve.py <br>
|- utils/ (all the [cogs](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html) that RobotSteve uses) <br>
|-- stats/ <br>
|--- mcstats.py (this has `++online`) <br>
|-- other_cogs <br>
|- res/ <br>
|-- TOKEN <br>
|-- config.json <br>

### Setup before running

- Make sure you clone this repository and have a bot ready on Discord's [Developer Portal](https://discord.com/developers/applications).
- Change the contents of `res/TOKEN` to your token.
- In your minecraft server.properties, set `enable-query` to `true` and set `query-port` to any valid port or let it be 25565 (default).
- Change the contents of config.json to something that looks like this:
  - `{"ip": "IP.Address.Goes.Here", "port": "MinecraftPort", "query-port": "QueryPort"}`
  - `"ip"` is your server's IP Address / Domain
  - `"port"` is your server's port. If you haven't changed your `server-port` in server.properties, then set this value of this field to 25565 in the config.json
  - `"query-port"` is your server's `query-port` that you set in server.properties.

- add the path of your server folder as `MINECRAFT_PATH` in your terminal. ex: `export MINECRAFT_PATH=/path/to/minecraft-server/`
- enable / disable the cogs you don't want. The bot currently has:
  - nuts (`++coco -s random-image-to-find`)
  - fats (`++fats` to generate a random set of parameters for lonliness, fatness, consumption of food, and crappiness at minecraft) (we don't fatshame people, it's an internal joke please don't rip me to shreds)
  - blade (`++blade` to give a random ~~Sun-Tzu~~ Technoblade quote (requires a file in `txt/` called `quote.txt`)
  - mcstats
    - `++online` - tells you who's online at the moment
    - `++stats` - server statistics (total time played, longest time played, number of logins/logouts, number of messages sent) (This requires access to the server folder)
  - controls (`++full-stats` to give you information about your files on the server; admins can only invoke this command; do `++help full-stats`, `++full-stats -f=ops`)
  - error_handler (I wouldn't remove this; but eh, to each their own)

### Running
- launch a virtualenv if you want to
- `pip install -r requirements.txt`
- `python3 RobotSteve.py`

### Side Notes
- plugins/RobotSteve has a command that can be installed for spigot servers where you can invoke `/fats` in your minecraft game.
- There's also a backup command that's supposed to call a bash script, disabled by default.
```bash
#!/bin/bash

function minecraftbackup(){
        NOW=$(date +"%Y-%m-%d-%T")

        backupfiles=$HOME/backups/backup*
        old=$HOME/backups/old/
        FILE=$HOME/backups/backup.mc.$NOW.tar.bz2
        minecraft=$HOME/minecraft-server/

        echo "Backing up minecraft. Do not kill this..."

        echo "Making Directory: old..."
        mkdir $old

        echo "Moving old files to old..."
        mv $backupfiles $old

        echo "Start Compressing..."
        tar -cf - $minecraft -P | pv -s $(du -sb $minecraft | awk '{print $1}') | bzip2 -9 > $FILE

        echo "Remove Directory: old..."
        rm -r $old

        echo "Complete!"

        return 1
}
```

