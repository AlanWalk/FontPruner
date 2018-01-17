"""Usage:
	FontPruner.py --inputPath=<inputPaths>... --inputFont=<inputFont>... [--outputPath=<outputPath>]
"""

from docopt import docopt
import os

SEP					= os.path.sep
SUCCESS_RESULT		= 0
EXEC_JAR			= "java -jar %s %s"

DEFAULT_OUT_FOLDER	= "output"
INTERMEDIATE_FOLDER	= "intermediate"
INPUT_FILE_PATH		= INTERMEDIATE_FOLDER + SEP + "input_file_list.txt"
CHINESE_OUTPUT		= INTERMEDIATE_FOLDER + SEP + "ChineseOutPut.txt"
UNCHINESE_OUTPUT	= INTERMEDIATE_FOLDER + SEP + "unChineseOutPut.txt"

BIN_FOLDER			= "bin"
GEN_FILE_LIST_JAR	= BIN_FOLDER + SEP + "genFileList.jar"
GEN_CHAR_LIST_JAR	= BIN_FOLDER + SEP + "fontExtract.jar"
SFNTTOOL_JAR		= BIN_FOLDER + SEP + "sfnttool.jar"

def genFilePathList(inputPath):
	command = EXEC_JAR % (GEN_FILE_LIST_JAR, " ".join(inputPath)  + " " + INPUT_FILE_PATH)
	print(command)
	if os.system(command) is not SUCCESS_RESULT:
		raise Exception("generate fileList.txt error!")
	print("genFilePathList completed")

def extractFileString():
	command = EXEC_JAR % (GEN_CHAR_LIST_JAR, INPUT_FILE_PATH + " " + INTERMEDIATE_FOLDER)
	print(command)
	if os.system(command) is not SUCCESS_RESULT:
		raise Exception("extract font string  error!")
	print("extractFileString completed")

def bulidNewFont(inputFont, outputPath):
	for fontPath in inputFont:
		fontName = os.path.basename(fontPath)
		fontOutputPath = outputPath + SEP + fontName
		command = EXEC_JAR % (SFNTTOOL_JAR, "-c " + CHINESE_OUTPUT + " " + UNCHINESE_OUTPUT + " " + fontPath + " " + fontOutputPath)
		print(command)

		if os.system(command) is not SUCCESS_RESULT:
			raise Exception("build new font error!" + command)
		print("bulidNewFont completed! "+ fontOutputPath)

if __name__ == "__main__":
	arguments = docopt(__doc__)

	for path in arguments["--inputPath"]:
		if not os.path.exists(path):
			raise Exception("inputPath - bad path: " + path)

	for path in arguments["--inputFont"]:
		if not os.path.exists(path):
			raise Exception("inputFont - bad path: " + path)

	outputPath = arguments["--outputPath"]

	if outputPath == None:
		outputPath = DEFAULT_OUT_FOLDER

	if not os.path.exists(outputPath):
		os.makedirs(outputPath)

	if not os.path.exists(INTERMEDIATE_FOLDER):
		os.makedirs(INTERMEDIATE_FOLDER)

	genFilePathList(arguments["--inputPath"])
	extractFileString()
	bulidNewFont(arguments["--inputFont"], outputPath)




