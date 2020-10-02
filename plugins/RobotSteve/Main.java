package me.Meesum.RobotSteve;

import java.util.Random;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;

public class Main extends JavaPlugin{
	
	@Override
	public void onEnable() {
		
	}
	
	@Override
	public void onDisable() {
		
	}
	
	public boolean onCommand(CommandSender sender, Command cmd, String label, String args[]) {
		if(label.equalsIgnoreCase("fats")) {
			if(sender instanceof Player) {
				Player player = (Player) sender;
				Random random = new Random();
				double m;
				m = random.nextDouble();
				String msg;
				msg = player.getDisplayName() + " Fats \n";
				msg = msg + "Fatness  : ";
				if(m<0.3) {
					msg = msg + "Not ";
				}
				if(m>=0.3 && m < 0.7) {
					msg = msg + "Mildly ";
				}
				if(m>=0.7) {
					msg = msg + "Very ";
				}
				msg = msg + "Fat \n";
				m = random.nextDouble();
				msg = msg + "Loneliness  : ";
				if(m<0.3) {
					msg = msg + "Not Feeling ";
				}
				if(m>=0.3 && m < 0.7) {
					msg = msg + "Mildly ";
				}
				if(m>=0.7) {
					msg = msg + "Really ";
				}
				msg = msg + "Lonely \n";
				m = random.nextDouble();
				msg = msg + "Consumption of Food  : ";
				msg = msg + String.valueOf((int) (m*100));
				msg = msg + " kgs \n";
				m = random.nextDouble();
				msg = msg + "Crappiness at Minecraft  : ";
				int convert = (int) ((m*100)%10);
				msg = msg + String.valueOf(convert);
				msg = msg + "/10 \n";
				
				Bukkit.broadcastMessage(msg);
				return true;
			}
			else {
				sender.sendMessage("Fuck off Raghav");
				return true;
			}
		}
		return false;
	}
}
