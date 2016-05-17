#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

class Family:

	def __init__(self, famnum):
		self.familyNum = famnum
		self.allelePairs = []
		self.alleleRatios = []
		self.dadAlleles = []
		self.momAlleles = []
		self.momID = 0;
		self.dadID = 0;

	def addParent(self, pid, pairs, sex):
		if (sex == '1'):
			self.momID = pid
			self.momAlleles = pairs
		else:
			self.dadID = pid
			self.dadAlleles = pairs

	def addOffspring(self, pairs):
		self.allelePairs.append([])
		for pair in pairs:
			self.allelePairs[-1].append(pair)

	def fillAlleleRatios(self):
		for i in xrange(0,len(self.allelePairs[-1])): #iterate through allele site positions
			self.alleleRatios.append([])
			for individual in self.allelePairs:
				if (individual[i] != '0 0'): #throw out "0 0"
					self.alleleRatios[-1].append(individual[i]) #add site 'i' to ratios list				

	def condenseRatios(self, errorPercent):
		i = 0
		for alleleSite in self.alleleRatios:
			alleleTypes = []
			for eachAllele in alleleSite:
				try:
					location = alleleTypes.index(eachAllele)
				except ValueError:
					location = -1
				#unique allele type and #weed out low error percent
				if location < 0 and ((float(alleleSite.count(eachAllele)) / float(len(alleleSite)))*100 > float(errorPercent)):
					alleleTypes.append(eachAllele)
					alleleTypes.append(alleleSite.count(eachAllele))
			#print alleleTypes
			self.alleleRatios[i] = alleleTypes
			i += 1

	def predictDad(self):
		i = 0
		sites = ["1 1", "1 2", "2 2"]
		for momAlleleSite in self.momAlleles:
			dadSite = "0 0"
			if momAlleleSite == "1 1":
				percents = self.checkRatio(i,sites[:2])
				if 0.9 <= percents[0]: # case 1
					dadSite = sites[0]
				elif 0.9 <= percents[1]: # case 2
					dadSite = sites[2]
				elif 0.25 <= percents[0] <= 0.75 and 0.25 <= percents[1] <= 0.75: # case 3
					dadSite = sites[1]
			elif momAlleleSite == "1 2":
				percents = self.checkRatio(i,sites[:])
				if 0.25 <= percents[0] <= 0.75 and 0.25 <= percents[1] <= 0.75: # case 4
					dadSite = sites[0]
				elif 0.10 <= percents[0] <= 0.40 and 0.35 <= percents[1] <= 0.65 and 0.10 <= percents[2] <= 0.40: # case 5
					dadSite = sites[1]
				elif 0.25 <= percents[1] <= 0.75 and 0.25 <= percents[2] <= 0.75: # case 6
					dadSite = sites[2]
			elif momAlleleSite == "2 2":
				percents = self.checkRatio(i,sites[1:])
				if 0.9 <= percents[0]: # case 7
					dadSite = sites[0]
				elif 0.25 <= percents[0] <= 0.75 and 0.25 <= percents[1] <= 0.75: # case 8
					dadSite = sites[1]
				elif 0.9 <= percents[1]: # case 9
					dadSite = sites[2]
			self.dadAlleles[i] = dadSite
			i += 1

	def checkRatio(self, i, sites):
		returnSites = []
		total = 0
		for checkSite in sites:
			site = self.alleleRatios[i]
			j = 0
			d = 0
			for nothing in range(len(site)/2):
				if checkSite == site[j]:
					d = 1
					returnSites.append(site[j+1])
					total += int(site[j+1])
				j += 2
			if d == 0:
				returnSites.append("0")
		for j in range(len(returnSites)):
			if total != 0:
				returnSites[j] = float(returnSites[j]) / float(total)
		return returnSites
		


