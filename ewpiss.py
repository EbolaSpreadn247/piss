import random
import asyncio
import time

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
import ewmap
import ewcasino
import ewquadrants

from ew import EwUser
from ewmarket import EwMarket
from ewdistrict import EwDistrict
from ewplayer import EwPlayer
from ewitem import EwItem

active_pissbattles = {}

""" peeee data model for database persistence """
class EwPissStats:
	#axe id_slimeoid = 0
	id_user = ""
	id_server = -1

	#axe life_state = 0
	#axe body = ""
	#axe head = ""
	#axe legs = ""
	#axe armor = ""
	#axe weapon = ""
	#axe special = ""
	ai = ""
	#axe sltype = "Lab"
	#axe name = ""
	
        #atk = 0
        content = 0
	defense = 0
	#intel = 0
        accuracy = 0
	#level = 0
        volume = 0
	time_defeated = 0
	clout = 0
	#hue = ""
	#coating = ""
	poi = ""

	#slimeoid = EwSlimeoid(member = cmd.message.author, )
	#slimeoid = EwSlimeoid(id_slimeoid = 12

	""" Load the slimeoid data for this user from the database. """
	def __init__(self, member = None, id_user = None, id_server = None):
		query_suffix = ""
		user_data = None
		if member != None:
			id_user = str(member.id)
			id_server = member.guild.id
		elif id_user != None:
			id_user = str(id_user)

		#	user_data = EwUser(member = member)

		#if user_data != None:
		#	if user_data.active_slimeoid > -1:
		#		id_slimeoid = user_data.active_slimeoid

		if id_user != None and id_server != None:
			query_suffix = " WHERE id_user = '{}' AND id_server = '{}'".format(id_user, id_server)
		
		if query_suffix != "":
			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {} FROM pissStats{}".format(
					#ewcfg.col_id_slimeoid,
					ewcfg.col_id_user,
					ewcfg.col_id_server,
					#ewcfg.col_life_state,
					#ewcfg.col_body,
					#ewcfg.col_head,
					#ewcfg.col_legs,
					#ewcfg.col_armor,
					#ewcfg.col_weapon,
					#ewcfg.col_special,
					ewcfg.col_ai,
					#ewcfg.col_type,
					#ewcfg.col_name,
					#ewcfg.col_atk,
                                        ewcfg.col_content,
					ewcfg.col_defense,
					#ewcfg.col_intel,
                                        ewcfg.col.accuracy,
					#ewcfg.col_level,
					ewcfg.col_time_defeated,
					ewcfg.col_clout,
					#ewcfg.col_hue,
					#ewcfg.col_coating,
					ewcfg.col_poi,
					query_suffix
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					#self.id_slimeoid = result[0]
					self.id_user = result[0]
					self.id_server = result[1]
					#self.life_state = result[3]
					#self.body = result[4]
					#self.head = result[5]
					#self.legs = result[6]
					#self.armor = result[7]
					#self.weapon = result[8]
					#self.special = result[9]
					self.ai= result[2]
					#self.sltype = result[11]
					#self.name = result[12]
					#self.atk = result[13]
                                        self.content = result[3]
					self.defense = result[4]
					#self.intel = result[15]
                                        self.accuracy = result[5]
					#self.level = result[16]
					self.time_defeated = result[6]
					self.clout = result[7]
					#self.hue = result[19]
					#self.coating = result[20]
					self.poi = result[8]

			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)


	""" Save urine data object to the database. """
	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save the object.
			cursor.execute("REPLACE INTO pissStats({}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				#ewcfg.col_id_slimeoid,
				ewcfg.col_id_user,
				ewcfg.col_id_server,
				#ewcfg.col_life_state,
				#ewcfg.col_body,
				#ewcfg.col_head,
				#ewcfg.col_legs,
				#ewcfg.col_armor,
				#ewcfg.col_weapon,
				#ewcfg.col_special,
				ewcfg.col_ai,
				#ewcfg.col_type,
				#ewcfg.col_name,
				#ewcfg.col_atk,
                                ewcfg.col_content,
				ewcfg.col_defense,
				#ewcfg.col_intel,
                                ewcfg.col_accuracy,
				#ewcfg.col_level,
				ewcfg.col_time_defeated,
				ewcfg.col_clout,
				#ewcfg.col_hue,
				#ewcfg.col_coating,
				ewcfg.col_poi
			), (
				#self.id_slimeoid,
				self.id_user,
				self.id_server,
				#self.life_state,
				#self.body,
				#self.head,
				#self.legs,
				#self.armor,
				#self.weapon,
				#self.special,
				self.ai,
				#self.sltype,
				#self.name,
				#self.atk,
                                self.content,
				self.defense,
				#self.intel,
                                self.accuracy,
				#self.level,
				self.time_defeated,
				self.clout,
				#self.hue,
				#self.coating,
				self.poi
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

#food would be here but it is eaten by player so the effects should be moved to ewfood and use a property from the food item's class to determin values added to stats

class EwMobility:
	id_mobility = ""
	alias = []
	str_advance = ""
	str_retreat = ""
	str_mobility = ""
	def __init__(
		self,
		id_mobility = "",
		alias = [],
		str_advance = "",
		str_advance_weak = "",
		str_retreat = "",
		str_retreat_weak = "",
		str_mobility = "",
		str_defeat = "",
	):
		self.id_mobility = id_mobility
		self.alias = alias
		self.str_advance = str_advance
		self.str_advance_weak = str_advance_weak
		self.str_retreat = str_retreat
		self.str_retreat_weak = str_retreat_weak
		self.str_mobility = str_mobility
		self.str_defeat = str_defeat

class EwOffense:
	id_offense = ""
	alias = []
	str_attack = ""
	str_offense = ""
	def __init__(
		self,
		id_offense = "",
		alias = [],
		str_attack = "",
		str_attack_weak = "",
		str_attack_coup = "",
		str_offense = "",
	):
		self.id_offense = id_offense
		self.alias = alias
		self.str_attack = str_attack
		self.str_attack_weak = str_attack_weak
		self.str_attack_coup = str_attack_coup
		self.str_offense = str_offense

class EwDefense:
	id_defense = ""
	alias = []
	str_defense = ""
	def __init__(
		self,
		id_defense = "",
		alias = [],
		str_defense = "",

	):
		self.id_defense = id_defense
		self.alias = alias
		self.str_defense = str_defense



class EwSpecial:
	id_special = ""
	alias = []
	str_special = ""
	def __init__(
		self,
		id_special = "",
		alias = [],
		str_special_attack_coup = "",
		str_special = "",
	):
		self.id_special = id_special
		self.alias = alias
		self.str_special_attack_coup = str_special_attack_coup
		self.str_special = str_special

class EwBrain:
	id_brain = ""
	alias = []
	str_brain = ""
	def __init__(
		self,
		id_brain = "",
		alias = [],
		str_brain = "",
		str_victory = "",
		str_battlecry = "",
		str_battlecry_weak = "",
		str_movecry = "",
		str_movecry_weak = "",
		get_strat = None,
	):
		self.id_brain = id_brain
		self.alias = alias
		self.str_brain = str_brain
		self.str_victory = str_victory
		self.str_battlecry = str_battlecry
		self.str_battlecry_weak = str_battlecry_weak
		self.str_movecry = str_movecry
		self.str_movecry_weak = str_movecry_weak
		self.get_strat = get_strat


class EwSlimeoidCombatData:

	# slimeoid brain object
	brain = None

	# slimeoid physical attack stat
	content = 0

	# slimeoid special attack stat
	accuracy = 0
	
	# slimeoid maximum hp
	maxVolume = 0

	# slimeoid current hp
	volume = 0

	# slimeoid shock (reduces effective sap)
	shock = 0

	# slimeoid owner database object (EwPlayer)
	player = None

	def __init__(self,
		#name = "",
		#weapon = None,
		#armor = None,
		#special = None,
		#legs = None,
		brain = None,
		#hue = None,
		#coating = None,
		content = 0,
		#grit = 0,
		accuracy = 0,
		maxVolume = 0,
		volume = 0,
		#sapmax = 0,
		#sap = 0,
		#slimeoid = None,
		player = None
	):
		#self.name = name
		#self.weapon = weapon
		#self.armor = armor
		#self.special = special
		#self.legs = legs
		self.brain = brain
		#self.hue = hue
		#self.coating = coating
		self.content = content
		#self.grit = grit
		self.accuracy = accuracy
		self.maxVolume = maxVolume
		self.volume = volume
		#self.sapmax = sapmax
		#self.sap = sap
		#self.hardened_sap = 0
		self.shock = 0
		#self.slimeoid = slimeoid
		self.player = player

	# roll the dice on whether an action succeeds and by how many degrees of success
	def attempt_action(self, strat, volume_spend, in_range):
		# reduce sap available by shock
		self.volume -= self.shock
		self.volume = max(0, self.volume)
		self.shock = 0
		volume_spend = min(volume_spend, self.volume)
		
		# obtain target number based on the type of action attempted
		target_number = 0
		if strat == ewcfg.pissBattle_strat_attack:
			target_number = self.content * accuracy*volume

		elif strat == ewcfg.pissBattle_strat_evade:
			target_number = 6

		dos = 0
		dice = []
		# roll the dice
		for i in range(volume_spend):
			die_roll = random.randrange(10)
			dice.append(die_roll)
			# a result lower than the target number confers a degree of success. a result of 0 always succeeds and a result of 9 always fails.
			if (die_roll < target_number and die_roll != 9) or die_roll == 0:
				dos += 1

		#ewutils.logMsg("Rolling {} check with {} sap, target number {}: {}, {} successes".format(strat, sap_spend, target_number, dice, dos))
		# spend sap
		self.volume -= volume_spend

		# return degrees of success
		return dos

	# obtain response for attack
	def execute_attack(self, enemy_combat_data, damage, in_range):
		volume = enemy_combat_data.volume
		volume -= damage

		thrownobject = random.choice(ewcfg.thrownobjects_list)

		response = "**"
		if volume <= 0:
			response += self.weapon.str_attack_coup.format(
				active=self.player,
				inactive=enemy_combat_data.player,
			)
		elif (self.maxVolume/self.volume) > 3:
			response += self.weapon.str_attack_weak.format(
				active=self.player,
				inactive=enemy_combat_data.player,
			)
		else:
			response += self.weapon.str_attack.format(
				active=self.player,
				inactive=enemy_combat_data.player,
			)
		
		response += "**"
		response += " :boom:"

		return response

	# apply damage and obtain response
	def take_damage(self, enemy_combat_data, damage, active_dos, in_range):
		
		# apply damage
		self.volume -= damage
		volume = self.volume

		# crush sap on physical attacks only
		volume_crush = 0
		if in_range:
			volume_crush = active_dos / 2
			self.volume -= volume_crush

		# store shock taken for next turn
		self.shock += 2 * active_dos

		# get proper response
		response = ""
		if self.volume > 0:
			if in_range:
				if self.resistance != "":
					response = self.resistance

				if self.analogous != "":
					response += " {}".format(self.analogous)

				if self.splitcomplementary_physical != "":
					response += " {}".format(self.splitcomplementary_physical)

			else:
				if self.weakness != "":
					response = self.weakness

				if self.splitcomplementary_special != "":
					response += " {}".format(self.splitcomplementary_special)


			if hp/damage > 10:
				response += " {} barely notices the damage.".format(self.name)
			elif hp/damage > 6:
				response += " {} is hurt, but shrugs it off.".format(self.name)
			elif hp/damage > 4:
				response += " {} felt that one!".format(self.name)
			elif hp/damage >= 3:
				response += " {} really felt that one!".format(self.name)
			elif hp/damage < 3:
				response += " {} reels from the force of the attack!!".format(self.name)

			if sap_crush > 0:
				response += " (-{} hardened sap)".format(sap_crush)


		return response

	# obtain movement response
	def change_distance(self, enemy_combat_data, in_range):
		response = ""
		if in_range:
			if (self.hpmax/self.hp) > 3:
				response = self.legs.str_retreat_weak.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
			else:
				response = self.legs.str_retreat.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
		else:
			if (self.hpmax/self.hp) > 3:
				response = self.legs.str_advance_weak.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
			else:
				response = self.legs.str_advance.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
		return response

	# harden sap and obtain response
	def harden_sap(self, dos):
		response = ""
		
		sap_hardened = min(dos, self.grit - self.hardened_sap)
		self.hardened_sap += sap_hardened

		if sap_hardened <= 0:
			response = "{} fails to harden any sap!".format(self.name)
		else:
			response = "{} hardens {} sap!".format(self.name, sap_hardened)

		return response
