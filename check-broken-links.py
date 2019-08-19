import sys
import os.path
import re
import os, fnmatch
import argparse

def getRelativeLinks(filepath):
	"""
	Return a list of all relative links in a markdown file.
	Also return HTML href links.
	"""
	relLinks = []
	if args.verbose:
		print ("Parsing : " + filepath)
	lineCount = 0
	with open(filepath) as f:
		for line in f:
			lineCount +=1
			mdLink = re.match(r"(.*)(\[.*\]\()(.*)(html)(.*)(\))", line)
			if mdLink:
				#print (mdLink.group(0))
				if re.match("^http:", mdLink.group(3)):
					pass
				else:
					relLinks.append([mdLink.group(3)+"md", mdLink.group(5)[1:], lineCount])
			# Sometime HTML is also inserted in markdown
			htmlHrefLink = re.match(r'(.*)(href=")(.*)(html)(.*)(")', line)
			if htmlHrefLink:
				#print (htmlHrefLink.group(0))
				if re.match("^http:", htmlHrefLink.group(3)):
					pass
				else:
					relLinks.append([htmlHrefLink.group(3)+"md", htmlHrefLink.group(5)[1:], lineCount])
	#print (relLinks)
	return tuple(relLinks)

def verifyIfTagExists(filepath, tag):
	"""
	Searches for a HTML tag inside a file.
	Returns True if HTML tag is found, else False.
	"""
	cleanTag = tag.replace("_", " ") #Change "_" to " "
	cleanTag = re.sub("\\\\", "" , cleanTag) #Remove "\\" from Tags
	for line in open(filepath, "r"):
		#print (line + ":::" + cleanTag)
		if line.find(cleanTag) >= 0:
			return True
	else:
		return False

def findBrokenLinks(directory, fileExtension):
	"""
	Search for stray/broken hyper-links in a particular directory
	"""
	print ("\n")
	validLinks = 0
	brokenLinkCount = 0
	totalMdFilesChecked = 0
	for root, dirs, files in os.walk(directory):
		for fname in files:
			if fnmatch.fnmatch(fname, fileExtension):
				totalMdFilesChecked += 1
				mdFilePath = os.path.join(root, fname)
				relLinks = getRelativeLinks(mdFilePath)
				for link in relLinks:
					if os.path.isfile(os.path.dirname(mdFilePath)+"/"+link[0]):
						# MD File Exits
						if link[1]:
							# The link has a TAG (specific part of a page)
							if verifyIfTagExists(os.path.dirname(mdFilePath)+"/"+link[0], link[1]) == False:
								brokenLinkCount += 1
								print str(brokenLinkCount) + "] " + mdFilePath + " (line: " + str(link[2]) + ")" + " points to an invalid tag : " + link[1].replace("_", " ")
							else:
								validLinks += 1
						else:
							# The link has no tag
							validLinks += 1
					else:
						# MD file does not exit as pointed by the link. Stray/broken link.
						brokenLinkCount += 1
						print str(brokenLinkCount) + "] " + mdFilePath + " (line: " + str(link[2]) + ")" + " has a stray/broken link : " + link[0]
	print ("\n")
	print "Total files checked: " + str(totalMdFilesChecked)
	print "Total broken links:  " + str(brokenLinkCount)
	print "Total valid links:   " + str(validLinks)


def checkForBrokenLinksInMarkdownFiles(parentdir):
	"""
	Search for broken links in Markdown files
	"""
	findBrokenLinks(parentdir, '*.md')


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Find out stray/broken links in markdown files")
	parser.add_argument("md_dir", help="Path to Mark Down directory")
	parser.add_argument("-v", "---verbose", action="store_true")
	args = parser.parse_args()

	if os.path.isdir(args.md_dir) == True:
		if args.verbose:
			print ("Looking into directory: " + args.md_dir)
		checkForBrokenLinksInMarkdownFiles(args.md_dir)
	else:
		print "Invalid Input. Given path is not a directory (%s)".format(args.md_dir)
		sys.exit(0)
