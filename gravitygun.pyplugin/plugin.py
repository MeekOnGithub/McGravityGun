# /local/bin/python
# -*- coding: utf-8 -*-
"""
File: plugin.py
Version: 0.0.1
Author: YourName
License: TheUnknowLicense (J'en ai juste pas 2)

Dependencies:
	- PyPlugins v0.0.1 / https://github.com/pyplugins/pyplugins
"""
from org.bukkit.entity import Player
from org.bukkit.event.player import PlayerInteractEntityEvent as PIEE
from org.bukkit.inventory import ItemStack
from org.bukkit.util import Vector
from org.bukkit import Sound, Particle


class GravityGunListener(PythonListener):
	listeners = [
		PyEventHandler('onPlayerInteract', PlayerInteractEvent),
		PyEventHandler('onPlayerInteractEntity', PlayerInteractEntityEvent)
	]

	def onPlayerInteract(self, event):
		player = event.getPlayer()
		item = player.getInventory().getItemInMainHand()

		if item is not None and item.hasItemMeta() and item.getItemMeta().hasLore() and 'Gravity Gun' in item.getItemMeta().getLore():
			clicked_block = event.getClickedBlock()

			if clicked_block is not None:
				block_location = clicked_block.getLocation().add(0.5, 0.5, 0.5)
				player_location = player.getLocation().add(0, player.getEyeHeight(), 0)
				direction = player_location.subtract(block_location).toVector().normalize()
				clicked_block.setVelocity(direction.multiply(2))
				player.playSound(player_location, Sound.ENTITY_ENDERMAN_TELEPORT, 1, 1)
				# Afficher une ligne de particules reliant le joueur au bloc cliqué
				for i in range(10):
					loc = player.getLocation().add(0, player.getEyeHeight(), 0).add(clicked_block.getLocation().subtract(player.getLocation()).multiply(i / 10.0))
					player.spawnParticle(Particle.END_ROD, loc, 1)

			# Afficher des messages de debug
			self.logger.debug("Gravity Gun event: player=%s, item=%s, clicked_block=%s" % (player.getName(), item, clicked_block))

	def onPlayerInteractEntity(self, event):
		player = event.getPlayer()
		item = player.getInventory().getItemInMainHand()

		if item is not None and item.hasItemMeta() and item.getItemMeta().hasLore() and 'Gravity Gun' in item.getItemMeta().getLore():
			clicked_entity = event.getRightClicked()

			if isinstance(clicked_entity, Player):
				clicked_entity.setVelocity(Vector(0, 3, 0))
				clicked_entity.playSound(clicked_entity.getLocation(), Sound.ENTITY_PLAYER_HURT, 1, 1)
				# Afficher une ligne de particules reliant le joueur à l'entité cliquée
				for i in range(10):
					loc = player.getLocation().add(0, player.getEyeHeight(), 0).add(clicked_entity.getLocation().subtract(player.getLocation()).multiply(i / 10.0))
					player.spawnParticle(Particle.END_ROD, loc, 1)

			# Afficher des messages de debug
			self.logger.debug("Gravity Gun event: player=%s, item=%s, clicked_entity=%s" % (player.getName(), item, clicked_entity))

	def onCommand(self, event):
		cmd = event.getCommand()
		sender = event.getSender()
		args = event.getArgs()

		if cmd == 'givegravitygun':
			if isinstance(sender, Player):
				item = ItemStack(Material.DIAMOND_HOE)
				item_meta = item.getItemMeta()
				item_meta.setDisplayName("§bGravity Gun")
				item_meta.setLore(["§7A Un objet puisssant pour manipuler les objets."])
				item.setItemMeta(item_meta)
				item.setDurability(0)
				sender.getInventory().addItem(item)
				sender.playSound(sender.getLocation(), Sound.BLOCK_ANVIL_LAND, 1, 1)
			else:
				sender.sendMessage("§cQue les joueurs peuvents utiliser cette commande")
			return True
		
	def onCommand(self, event):
		cmd = event.getCommand()
		sender = event.getSender()
		args = event.getArgs()

		if cmd == 'reloadplugin':
			self.plugin.reload()
			sender.sendMessage("Plugin reloaded!")
			return True	

class GravityGunPlugin(PythonPlugin):
	def onEnable(self):
		pm = self.getServer().getPluginManager()
		pm.registerEvents(GravityGunListener(self), self)
		self.logger.info("§6Plugin activée!")

	def onDisable(self):
		self.logger.info("§6Plugin désactiver :/")
	
	def reload(self):
		self.getServer().getPluginManager().disablePlugin(self)
		self.getServer().getPluginManager().enablePlugin(self)