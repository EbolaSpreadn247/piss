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
	def __init__(self, member = None, id_slimeoid = None, life_state = None, id_user = None, id_server = None, sltype = "Lab", slimeoid_name = None):
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

		if id_slimeoid != None:
			query_suffix = " WHERE id_slimeoid = '{}'".format(id_slimeoid)
		else:

			if id_user != None and id_server != None:
				query_suffix = " WHERE id_user = '{}' AND id_server = '{}'".format(id_user, id_server)
				if life_state != None:
					query_suffix += " AND life_state = '{}'".format(life_state)
				if sltype != None:
					query_suffix += " AND type = '{}'".format(sltype)
				if slimeoid_name != None:
					query_suffix += " AND name = '{}'".format(slimeoid_name)


		if query_suffix != "":
			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM slimeoids{}".format(
					ewcfg.col_id_slimeoid,
					ewcfg.col_id_user,
					ewcfg.col_id_server,
					ewcfg.col_life_state,
					ewcfg.col_body,
					ewcfg.col_head,
					ewcfg.col_legs,
					ewcfg.col_armor,
					ewcfg.col_weapon,
					ewcfg.col_special,
					ewcfg.col_ai,
					ewcfg.col_type,
					ewcfg.col_name,
					ewcfg.col_atk,
					ewcfg.col_defense,
					ewcfg.col_intel,
					ewcfg.col_level,
					ewcfg.col_time_defeated,
					ewcfg.col_clout,
					ewcfg.col_hue,
					ewcfg.col_coating,
					ewcfg.col_poi,
					query_suffix
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.id_slimeoid = result[0]
					self.id_user = result[1]
					self.id_server = result[2]
					self.life_state = result[3]
					self.body = result[4]
					self.head = result[5]
					self.legs = result[6]
					self.armor = result[7]
					self.weapon = result[8]
					self.special = result[9]
					self.ai= result[10]
					self.sltype = result[11]
					self.name = result[12]
					self.atk = result[13]
					self.defense = result[14]
					self.intel = result[15]
					self.level = result[16]
					self.time_defeated = result[17]
					self.clout = result[18]
					self.hue = result[19]
					self.coating = result[20]
					self.poi = result[21]

			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

