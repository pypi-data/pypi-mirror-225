import mariadb
import sys

class ReMan(object):
	def __init__(self):
		self.connection = None
		self.cursor = None

	def __del__(self):
		if (self.cursor != None):
			self.cursor.close()
		if (self.connection != None):
			self.connection.close()

	def getDBConnection(self):
		try:
			if (self.connection == None):
				self.connection = mariadb.connect(
					user="reman",
					password="reman",
					host="10.58.3.179",
					database="REMAN")
			return self.connection
		except Exception as e:
			print(f"Failed to connect database, error: {e}")
			sys.exit(1)

	def getDBCursor(self):
		try:
			if (self.cursor == None):
				self.cursor = self.getDBConnection().cursor()
			return self.cursor
		except Exception as e:
			print(f"Failed to get database cursor, error: {e}")
			sys.exit(1)

	def getUserChannels(self, releaseName):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute("SELECT users.name, channels.name "
							 "FROM ReleaseChannel as rc "
							 "INNER JOIN Channels as channels ON rc.channelId = channels.id "
							 "INNER JOIN Users as users ON users.id = channels.userId "
							 "INNER JOIN Releases as releases ON  rc.releaseId = releases.id "
							 f"WHERE releases.name = '{releaseName}'"
							)
			result = self.getDBCursor().fetchall()
		except Exception as e:
			print(f"Failed to get user/channel of {releaseName}, error: {e}")
		return result

	def getChannel(self, releaseName, userName):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute("SELECT channels.name "
							 "FROM ReleaseChannel as rc "
							 "INNER JOIN Channels as channels ON rc.channelId = channels.id "
							 "INNER JOIN Users as users ON users.id = channels.userId "
							 "INNER JOIN Releases as releases ON  rc.releaseId = releases.id "
							 f"WHERE releases.name = '{releaseName}' "
							 f"AND users.name = '{userName}'"
							)
			rows = self.getDBCursor().fetchall()
			if (len(rows) == 1):
				result = rows[0][0]
			else:
				print("None or multiple version! " + len(rows))
		except Exception as e:
			print(f"Failed to get user/channel of {releaseName}, error: {e}")
		return result

	def getReleaseId(self, releaseName):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"SELECT Releases.id FROM Releases WHERE name = '{releaseName}'")
			rows = self.getDBCursor().fetchall()
			if (len(rows) == 1):
				result = rows[0][0]
			elif (len(rows) > 1):
				print("Multiple version! " + len(rows))
		except Exception as e:
			print(f"Failed to get releaseId {releaseName}, error: {e}")
		return result

	def insertRelease(self, releaseName):
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"INSERT INTO Releases (name) VALUES ('{releaseName}');")
			self.getDBConnection().commit()
			return self.getReleaseId(releaseName)
		except Exception as e:
			print(f"Failed to insert {releaseName}, error: {e}")

	def getReleaseChannelIds(self, releaseName):
		result = []
		try:
			cursor = self.getDBCursor()
			cursor.execute("SELECT channels.id "
							"FROM ReleaseChannel as rc "
							"INNER JOIN Channels as channels ON rc.channelId = channels.id "
							"INNER JOIN Releases as releases ON rc.releaseId = releases.id "
							f"WHERE releases.name = '{releaseName}'")
			rows = self.getDBCursor().fetchall()
			print(f"getReleaseChannelIds rows: {rows}")
			for row in rows:
				print(f"row: {row[0]}")
				result.append(row[0])
				print(f"result: {result}")
		except Exception as e:
			print(f"Failed to get releaseChannelIds from {releaseName}, error: {e}")
		return result

	def insertReleaseChannel(self, releaseId, channelId):
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"INSERT INTO ReleaseChannel (releaseId, channelId) VALUES ({releaseId}, {channelId});")
			self.getDBConnection().commit()
		except Exception as e:
			print(f"Failed to insert releaseChannel ({releaseId}, {channelId}), error: {e}")

	def getUserId(self, userName):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"SELECT id FROM Users WHERE name = '{userName}'")
			rows = self.getDBCursor().fetchall()
			if len(rows) == 1:
				result = rows[0][0]
		except Exception as e:
			print(f"Failed to get userId from user: {userName}, error: {e}")
		return result


	def insertChannel(self, channelName, userId):
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"INSERT INTO Channels (name, userId) VALUES ({channelName}, {userId});")
			self.getDBConnection().commit()
		except Exception as e:
			print(f"Failed to insert channel ({channelName}), error: {e}")

	def getChannelId(self, channelName, userId):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"SELECT id FROM Channels WHERE name = '{channelName}' AND userId = {userId}")
			rows = self.getDBCursor().fetchall()
			if len(rows) == 1:
				result = rows[0][0]
		except Exception as e:
			print(f"Failed to get channel id from channel/userId: {channelName}/{userId}, error: {e}")
		return result

	def updateReleaseChannel(self, releaseId, previousChannelId, newChannelId):
		try:
			cursor = self.getDBCursor()
			cursor.execute(f"UPDATE ReleaseChannel SET channelId = {newChannelId} WHERE releaseId = {releaseId} AND channelId = {previousChannelId};")
			self.getDBConnection().commit()
		except Exception as e:
			print(f"Failed to update ReleaseChannel ({releaseId}:{previousChannelId} -> {newChannelId}), error: {e}")


	def createRelease(self, releaseName, fromRelease):
		try:
			# create empty release
			if self.getReleaseId(releaseName) != None:
				raise Exception("Release already exist")
			newReleaseId = self.insertRelease(releaseName)
			# copy channels from previous release
			channelIds = self.getReleaseChannelIds(fromRelease)
			for channelId in channelIds:
				self.insertReleaseChannel(newReleaseId, channelId)
		except Exception as e:
			print(f"Failed to create {releaseName}, error: {e}")

	def createChannel(self, channelName, userName):
		userId = self.getUserId(userName)
		self.insertChannel(channelName, userId)

	def linkReleaseChannel(self, releaseName, userName, channelName):
		releaseId = self.getReleaseId(releaseName)
		userId = self.getUserId(userName)
		previousChannelId = self.getChannelId(self.getChannel(releaseName, userName), userId)
		newChannelId = self.getChannelId(channelName, userId)
		self.updateReleaseChannel(releaseId, previousChannelId, newChannelId)

