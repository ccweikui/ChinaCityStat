#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import codecs

class CityStat: 
	# Get the city list in China.
	def getCityList(self):
		url = "https://zh.wikipedia.org/zh-cn/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%9F%8E%E5%B8%82%E5%88%97%E8%A1%A8"
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "lxml")
		divs = soup.findAll("li")
		result = []
		for l in divs:
			if u'地级市' in l.text.strip() or u'县级市' in l.text.strip() or u'副省级市' in l.text.strip():
				lists = l.findAll('a')
				for value in lists:
					result.append([value["href"], value.text.strip()])
		result = result[:-4]
		print len(result)
		return result

	def getCityInfo(self):
		cityList = self.getCityList()
		prefixURL = "https://zh.wikipedia.org"
		cityInfoList = []
		for index, (url, name) in enumerate(cityList):
			try :
				cityInfoList.append(self.processEachCity(prefixURL + url, name))
			except:
				print "Error:" + url
		return cityInfoList

	def processEachCity(self, url, name):
		print url
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "lxml")
		#table = soup.findAll("table", {"class":"infobox vcard"})
		table = soup.findAll(name = "table", attrs={"class":re.compile(r'infobox.*vcard')})
		trs = table[0].findAll("tr")
		totalPeople = 0
		totalGDP = 0
		averageGDP = 0
		pattern = re.compile(r'\d+\d')
		for tr in trs:
			th = tr.find("th")
			td = tr.find("td")
			if th != None and u'总人口' in th.text.strip():
				text = td.text.strip().split(u'万')
				text = text[0].replace(",","")
				totalPeople = float(pattern.findall(text)[0])
				# 部分总人口未使用万作单位
				if totalPeople > 10000:
					totalPeople = totalPeople / 10000
			if th != None and th.text.strip().startswith(u'GDP') and u'亿' in td.text.strip():
				text = td.text.strip().split(u'亿')[0].replace(",","").strip()
				totalGDP = float(pattern.findall(text)[0])
			if totalPeople > 0 and totalGDP > 0:
				print totalGDP, totalPeople
				break
		if totalGDP == 0:
			for tr in trs:
				th = tr.find("th")
				td = tr.find("td")
				if th != None and th.text.strip().startswith(u'人均GDP'):
					print totalGDP
					print td.text.strip()
					text = td.text.strip().split(u'元')[0].replace(",","").strip()
					totalGDP = totalPeople * float(pattern.findall(text)[0]) / 10000
					break
		return (name, totalPeople, totalGDP, totalGDP / totalPeople * 10000)


	def writeToFile(self, cityInfoList):
		f = codecs.open('citystatInfo.txt', 'a', 'utf-8')
		for (name, totalPeople, totalGDP, avergaeGDP) in cityInfoList:
			print name, totalPeople, totalGDP, avergaeGDP
			f.write(name + "\t" + str(totalPeople) + "\t" + str(totalGDP) + "\t" + str(avergaeGDP) + "\n")
		f.close()		
	

if __name__ == '__main__':
	cityStat = CityStat()
	cityInfoList = cityStat.getCityInfo()
	cityStat.writeToFile(cityInfoList)
