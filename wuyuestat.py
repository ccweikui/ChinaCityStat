#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import codecs

class WuyueStat:
	def initWuyueCityList(self):
		totalCount = 0
		wuyueList = []
		for line in open("wuyuelist.txt", "r").readlines():
			cityName = line.split("（")[0].strip()
			pattern = re.compile(r'\d+')
			count = int(pattern.findall(line)[0])
			totalCount += count
			wuyueList.append((cityName, count))
		print totalCount
		return wuyueList

	def initCityInfo(self):
		cityInfoMap = {}
		cityInfoList = []
		for line in open("citystatInfo.txt", "r").readlines():
			infoList = line.split()
			cityName = infoList[0].strip()
			totalPeople = float(infoList[1])
			totalGDP = float(infoList[2])
			averageGDP = float(infoList[3])
			if (totalGDP > 10 and averageGDP > 10):
				cityInfoList.append((cityName, totalPeople, totalGDP, averageGDP))
				cityInfoMap[cityName] = (totalPeople, totalGDP, averageGDP)
		cityInfoList = sorted(cityInfoList, key = lambda city: city[3], reverse = True)
		self.writeToFile("cityinfoordered.txt", cityInfoList)
		print len(cityInfoMap)
		return cityInfoMap
	
	def wuyueStatistics(self, wuyueList, cityInfoMap):
		statistics = []
		existWuyue = {}
		for (cityName, count) in wuyueList:
			visited = False
			for name in cityInfoMap.keys():
				if cityName in name:
					statistics.append((name, count, cityInfoMap[name][0], cityInfoMap[name][2]))
					existWuyue[name] = cityInfoMap[name][0]
					visited = True
			if not visited:
				print cityName
		sortedByPeople = sorted(statistics, key = lambda city: city[2])
		sortedByGDP = sorted(statistics, key = lambda city: city[3])
			
		minPeople = sortedByPeople[0][2]
		minGDP = sortedByGDP[0][3]
		averageGDP = sortedByGDP[len(sortedByGDP) / 2][3]
		averagePeople = sortedByPeople[len(sortedByPeople) / 2][2] 
		"""
		for cityInfo in sortedByPeople:
			averagePeople += cityInfo[2]
			averageGDP += cityInfo[3]
		averageGDP = averageGDP / len(sortedByPeople)
		averagePeople = averagePeople / len(sortedByGDP)	
		"""
		print minPeople, averagePeople, minGDP, averageGDP
		minCityCount = []
		averageCityCount = []
		for name in cityInfoMap.keys():
			if cityInfoMap[name][0] > minPeople and cityInfoMap[name][2] > minGDP:
				minCityCount.append((name, cityInfoMap[name][0], cityInfoMap[name][2]))
			if cityInfoMap[name][0] > averagePeople and cityInfoMap[name][2] > averageGDP:
				averageCityCount.append((name, cityInfoMap[name][0], cityInfoMap[name][2]))
		potentialCount = 0
		for cityInfo in minCityCount:
			if not cityInfo[0] in existWuyue:	
				potentialCount += 1
				print cityInfo[0], cityInfo[1], cityInfo[2]
		print len(minCityCount), len(averageCityCount), potentialCount, len(existWuyue)
		
	def writeToFile(self, fileName, cityInfoList):
		f = codecs.open(fileName, 'a')
		for (name, totalPeople, totalGDP, avergaeGDP) in cityInfoList:
			print name, totalPeople, totalGDP, avergaeGDP
			f.write(name + "\t" + str(totalPeople) + "\t" + str(totalGDP) + "\t" + str(avergaeGDP) + "\n")
		f.close()		
	

if __name__ == '__main__':
	wuyueStat = WuyueStat()
	wuyueList = wuyueStat.initWuyueCityList()
	cityInfoMap = wuyueStat.initCityInfo()
	wuyueStat.wuyueStatistics(wuyueList, cityInfoMap)
	
