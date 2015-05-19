# -*- coding:utf-8 -*-

import os

testCaseFileArr = []
testCassClsArr = []

class caseInfo:
    def __init__(self):
        self.fileName = ""
        self.testCaseName = ""
        self.testCaseList = []
        self.testPassCaseList = []
        self.testFailCaseList = []
        self.testErrorCaseList = []
        self.testUseTime = -1.0
        self.testPassRate = 0.0

    def __repr__(self):
        strReturn = ""
        strReturn += "fileName:" + self.fileName + "\n"
        strReturn += "testCaseName:" + self.testCaseName + "\n"
        strReturn += "testUseTime:" + str(self.testUseTime) + "\n"
        strReturn += "testPassRate:" + str(self.testPassRate) + "\n"
        strReturn += "testCaseList:\n[\n"
        for name in self.testCaseList:
            strReturn += name + "\n"
        strReturn += "]\n"
        strReturn += "testPassCaseList:\n[\n"
        for name in self.testPassCaseList:
            strReturn += name + "\n"
        strReturn += "]\n"
        strReturn += "testFailCaseList:\n[\n"
        for name in self.testFailCaseList:
            strReturn += name + "\n"
        strReturn += "]\n"
        strReturn += "testErrorCaseList:\n[\n"
        for name in self.testErrorCaseList:
            strReturn += name + "\n"
        strReturn += "]\n"
        return strReturn

class ReportItem:
    def __init__(self):
        self.name = "test"
        self.passRate = 0.0
        self.totalCase = 0
        self.passCase = 0
        self.failCase = 0
        self.errorCase = 0
        self.runTime = 0.0

    def __repr__(self):
        strReturn = ""
        strReturn += "name:" + self.name + "\n"
        strReturn += "pass rate:" + str(self.passRate * 100) + "%\n"
        strReturn += "total case:" + str(self.totalCase) + "\n"
        strReturn += "pass case:" + str(self.passCase) + "\n"
        strReturn += "fail case:" + str(self.failCase) + "\n"
        strReturn += "error case:" + str(self.errorCase) + "\n"
        strReturn += "run time:" + str(self.runTime) + "s\n"
        return strReturn

def getAllCaseFile():
    for fileName in os.listdir("./"):
        try:
            if fileName.split('.')[1] == "py" and fileName[0:4] == "test":
                testCaseFileArr.append(fileName)
        except:
            continue

def getAllTestCls():
    for caseFile in testCaseFileArr:
        f = open(caseFile, 'r')
        for line in f:
            if line.split(" ")[0] == "class":
                line = line.strip()
                subClsName = line.split(" ")[1].split("(")[0]
                supClsName = line.split(" ")[1].split("(")[1][:-1]
                if supClsName == "unittest.TestCase":
                    obCase = caseInfo()
                    obCase.fileName = caseFile
                    obCase.testCaseName = subClsName
                    testCassClsArr.append(obCase)
        f.close()

def getTestMethod():
    for ob in testCassClsArr:
        module = __import__(ob.fileName.split(".")[0])
        for methodName in dir(getattr(module, ob.testCaseName)):
            if methodName[0:4] == "test":
                ob.testCaseList.append(methodName)

def getTestResult():
    for ob in testCassClsArr:
        resultFileName = ob.testCaseName + ".txt"
        f = open(resultFileName, 'r')
        for line in f:
            if line.split(' ')[0] == "FAIL:":
                ob.testFailCaseList.append(line.split(' ')[1])
            if line.split(' ')[0] == "ERROR:":
                ob.testErrorCaseList.append(line.split(' ')[1])
            try:
                if line.split(' ')[0] == "Ran" and line.split(' ')[2][0:4] == "test":
                    ob.testUseTime = float(line.split(' ')[4][:-2])
            except:
                continue
        f.close()
    for ob in testCassClsArr:
        for name in ob.testCaseList:
            if name not in ob.testFailCaseList and name not in ob.testErrorCaseList:
                ob.testPassCaseList.append(name)
    for ob in testCassClsArr:
        ob.testPassRate = float(len(ob.testPassCaseList)) / float(len(ob.testCaseList))

def writeReportFile():
    ob = ReportItem()
    for testCase in testCassClsArr:
        ob.totalCase += len(testCase.testCaseList)
        ob.passCase += len(testCase.testPassCaseList)
        ob.failCase += len(testCase.testFailCaseList)
        ob.errorCase += len(testCase.testErrorCaseList)
        ob.runTime += testCase.testUseTime
    ob.passRate = float(ob.passCase) / float(ob.totalCase)
    moduleFile = open("reportTotal.html", 'w')
    moduleFile.write("<html>\n")
    moduleFile.write("  <head><title>Report</title></head>\n")
    moduleFile.write("  <body>\n")
    moduleFile.write("      <hr width=\"720\" align=\"left\"/>\n")
    moduleFile.write("      <table width=\"720\" border=\"1\" bordercolor=\"#E6E6E6\" rules=\"none\" style=\"table-layout:fixed\">\n")
    moduleFile.write("          <tr bgcolor=\"#2894FF\" align=\"center\">\n")
    moduleFile.write("              <td width=\"100\"><b>Name</b></td>\n")
    moduleFile.write("              <td width=\"100\"><b>PassRate</b></td>\n")
    moduleFile.write("              <td width=\"100\"><b>TotalCase</b></td>\n")
    moduleFile.write("              <td width=\"100\"><b>PassCase</b></td>\n")
    moduleFile.write("              <td width=\"100\"><b><font color=\"#0000FF\">FailCase</font></b></td>\n")
    moduleFile.write("              <td width=\"100\"><b>ErrorCase</b></td>\n")
    moduleFile.write("              <td width=\"100\"><b>RunTime</b></td>\n")
    moduleFile.write("          </tr>\n")
    moduleFile.write("          <tr bgcolor=\"#E0E0E0\" align=\"center\">\n")
    moduleFile.write("              <td width=\"100\" bgcolor=\"#E0E0E0\"><b>%s</b></td>\n" % ob.name)
    fRate = ob.passRate * 100.0
    strRate = "%.2f" % fRate
    moduleFile.write("              <td width=\"100\"><font color=\"red\"><b>%s</b></font></td>\n" % (strRate + "%"))
    moduleFile.write("              <td width=\"100\"><font color=\"green\"><b>%s</b></font></td>\n" % ob.totalCase)
    moduleFile.write("              <td width=\"100\"><font color=\"green\"><b>%s</b></font></td>\n" % ob.passCase)
    moduleFile.write("              <td width=\"100\"><b><font color=\"red\">%s</font></b></td>\n" % ob.failCase)
    moduleFile.write("              <td width=\"100\"><font color=\"red\"><b>%s</b></font></td>\n" % ob.errorCase)
    moduleFile.write("              <td width=\"100\"><font color=\"green\"><b>%ss</b></font></td>\n" % ob.runTime)
    moduleFile.write("          </tr>\n")
    moduleFile.write("      </table>\n")
    moduleFile.write("      <hr width=\"720\" align=\"left\"/>\n")
    moduleFile.write("  </body>\n")
    moduleFile.write("</html>\n")
    moduleFile.close()
    f = open("reportDetail.html", 'w')
    f.write("<html>\n")
    f.write("  <body>\n")
    f.write("    <table width=\"720\" border=\"1\" bordercolor=\"#E6E6E6\" rules=\"none\" style=\"table-layout:fixed\">\n")
    f.write("      <tr bgcolor=\"#2894FF\" align=\"center\">\n")
    f.write("        <td width=\"200\"><b></b></td>\n")
    f.write("        <td width=\"130\"><b>PassRate</b></td>\n")
    f.write("        <td width=\"130\"><b>TotalCase</b></td>\n")
    f.write("        <td width=\"130\"><b>PassCase</b></td>\n")
    f.write("        <td width=\"130\"><b>FailCase</b></td>\n")
    f.write("        <td width=\"130\"><b>ErrorCase</b></td>\n")
    f.write("        <td width=\"130\"><b>RunTime</b></td>\n")
    for testCase in testCassClsArr:
        f.write("      <tr bgcolor=\"#E0E0E0\" align=\"center\">\n")
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%s</b></small></font></td>\n" % \
            testCase.testCaseName)
        fRate = float(testCase.testPassRate) * 100.0
        strRate = "%.2f" % fRate
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%s</b></small></font></td>\n" % (strRate + "%"))
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%d</b></small></font></td>\n" % len(testCase.testCaseList))
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%d</b></small></font></td>\n" % len(testCase.testPassCaseList))
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%d</b></small></font></td>\n" % len(testCase.testFailCaseList))
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%d</b></small></font></td>\n" % len(testCase.testErrorCaseList))
        f.write("        <td width=\"100\"><font color=\"green\"><small><b>%s</b></small></font></td>\n" % (str(testCase.testUseTime) + "s"))
        f.write("      </tr>\n")
    f.write("    </table>\n  </body>\n</html>")
    f.close()

def main():
    getAllCaseFile()
    getAllTestCls()
    getTestMethod()
    getTestResult()
    writeReportFile()
    
if __name__ == "__main__":
    main()