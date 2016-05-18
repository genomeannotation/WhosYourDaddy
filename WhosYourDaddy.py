#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
from src.family import Family

def main():
	#usage
	def usage():
		print ("\n-usage: " + sys.argv[0] + " <inputfile> <error percent #>")
		print ("-example: " + sys.argv[0] + " Bdor_big2.lepmap 5\n")
                print ("\nLatest version at:\nhttps://github.com/genomeannotation/WhosYourDaddy\n")
		sys.exit()

	if len(sys.argv) < 3:
		usage()

	errorPercent = sys.argv[-1]

	#read in families
	families = readFamilies()
	
	#process family data
	for family in families:
		family.fillAlleleRatios()
		family.condenseRatios(errorPercent)
		family.predictDad()

	writeOutput(families)

def writeOutput(families):
        # Create output directory
        out_dir = "WYD_output"
        os.system('mkdir -p ' + out_dir)

	fo = open(out_dir + '/output.lepmap', 'w')
	fi = open(sys.argv[1], 'r')
	allLines = fi.readlines()
	for line in allLines:
		splits = line.split("\t")
		if (splits[2] == '0' and splits[3] == '0' and splits[4] != '1'):#this is dad
			for family in families:
				if family.familyNum == splits[0]:
					for thing in splits[:6]:
						fo.write("%s\t"%thing)
					for thing in family.dadAlleles:
						fo.write("%s\t"%thing)
					fo.write("\n")
		else:
			fo.write("%s"%line)

def readFamilies():
	families = []
	familynum = 0
	fi = open(sys.argv[1], 'r')
	allLines = fi.readlines()

	for line in allLines:
		line = line.strip('\n')
		splits = line.split("\t")

		if familynum != splits[0]:
			familynum = splits[0]
			families.append(Family(familynum))

		alleles = splits[6:]
		if (splits[2] == '0' and splits[3] == '0'):
			families[-1].addParent(splits[1], alleles, splits[4])
		else:
			families[-1].addOffspring(alleles)
	return families

if __name__ == '__main__':
    main()


