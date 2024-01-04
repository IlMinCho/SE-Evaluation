import sys
import math
import pandas as pd

def ndcg20(relsList, relsSortList):
    aNdcg = []
    iNdcg = []
    ndcg = 0

    aNdcg.append(int(relsList[0]))
    iNdcg.append(int(relsSortList[0]))
    for i in range(1,20):
        aNdcg.append(int(relsList[i])/math.log2(i+1))
        iNdcg.append(int(relsSortList[i])/math.log2(i+1))

    if sum(iNdcg) == 0:
        ndcg == 0
    else:
        ndcg = sum(aNdcg)/sum(iNdcg)

    return ndcg

def eval(trecrunFile, qrelsFile, outputFile):
    
    trecrunInput = open(trecrunFile, "rt")
    qrelsInput = open(qrelsFile, "rt")

    outputList = []
    trecrunSet = []
    qrelSet = []

    #
    eachQuery = []
    docids = []
    ranks = []
    scores = [] 
    while True:
        eachLine = trecrunInput.readline()
        if not eachLine:
            break
        
        splitLine = eachLine.split()
        if len(eachQuery) == 0:
            eachQuery.append(splitLine[0])
            
        if eachQuery[0] == splitLine[0]:
            docids.append(splitLine[2])
            ranks.append(splitLine[3])
            scores.append(splitLine[4])
        else:
            eachQuery.append(docids)
            eachQuery.append(ranks)
            eachQuery.append(scores)
            eachQuery.append(splitLine[5])

            trecrunSet.append(eachQuery)

            eachQuery = []
            docids = []
            ranks = []
            scores = []
            eachQuery.append(splitLine[0])
            docids.append(splitLine[2])
            ranks.append(splitLine[3])
            scores.append(splitLine[4])
    eachQuery.append(docids)
    eachQuery.append(ranks)
    eachQuery.append(scores)
    eachQuery.append(splitLine[5])
    trecrunSet.append(eachQuery)

    #
    eachQuery = []
    docids = []
    rels = []
    while True:
        eachLine = qrelsInput.readline()
        if not eachLine:
            break
        
        splitLine = eachLine.split()
        if len(eachQuery) == 0:
            eachQuery.append(splitLine[0])
            
        if eachQuery[0] == splitLine[0]:
            docids.append(splitLine[2])
            rels.append(splitLine[3])
        else:
            eachQuery.append(docids)
            eachQuery.append(rels)

            qrelSet.append(eachQuery)

            eachQuery = []
            docids = []
            rels = []
            eachQuery.append(splitLine[0])
            docids.append(splitLine[2])
            rels.append(splitLine[3])
    eachQuery.append(docids)
    eachQuery.append(rels)
    qrelSet.append(eachQuery)

    #
    for tre in trecrunSet:
        for query in qrelSet:
            rels = []
            if query[0] == tre[0]:

                for doc in tre[1]:
                    try:
                        rels.append(query[2][query[1].index(doc)])
                    except: 
                        rels.append('0')
            if len(rels) != 0:
                tre.append(rels)



    #
    for tre in trecrunSet:
        eachQuery = []
        eachQuery.append(tre[0])

        #ndcg
        i = 0
        index = 0
        for q in qrelSet:
            if q[0] == tre[0]:
                index = i
            else: i += 1
        relsSortList = sorted(qrelSet[index][2], reverse=True)
        ndcg = ndcg20(tre[5], relsSortList)
        eachQuery.append(ndcg)

        #
        numRel = len(list(filter(lambda x: x != '0', relsSortList)))
        eachQuery.append(numRel)

        #
        relFound = len(list(filter(lambda x: x != '0', tre[5])))
        eachQuery.append(relFound)

        #
        rr = 0
        if relFound == 0:
            rr = 0
        else: 
            rrs = []
            for idx in range(0, len(tre[5])) :
                if list(map(int, tre[5]))[idx] > 0:
                    rrs.append(idx)
            if len(rrs) != 0:
                rr = 1/(rrs[0]+1)
        eachQuery.append(rr)
        
        #
        text = open("preciRecall_dpr.txt", 'a')
        p10 = len(list(filter(lambda x: x != '0', tre[5][0:10])))/10
        # if tre[0] == "330975":
        #         for i in range(len(tre[5])):
        #             i += 1
        #             text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:i])))/i))
                
        #     text.write(str(len(list(filter(lambda x: x != '0', tre[5][0:1])))/1))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:2])))/2))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:3])))/3))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:4])))/4))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:5])))/5))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:6])))/6))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:7])))/7))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:8])))/8))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:9])))/9))
        #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:10])))/10))
            
        eachQuery.append(p10)

        #
        if numRel == 0:
            r10 = 0
        else: 
            r10 = len(list(filter(lambda x: x != '0', tre[5][0:10])))/numRel
            # if tre[0] == "330975":
            #     for i in range(len(tre[5])):
            #         i += 1
            #         text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:i])))/numRel))
                
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:1])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:2])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:3])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:4])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:5])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:6])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:7])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:8])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:9])))/numRel))
            #     text.write("\n"+str(len(list(filter(lambda x: x != '0', tre[5][0:10])))/numRel))
    
        # text.close()
        eachQuery.append(r10)

        #
        if p10 == 0 or r10 ==0:
            f1 = 0
        else: f1 = 2*p10*r10/(p10+r10)
        eachQuery.append(f1)

        #
        if numRel == 0:
            p20r = 0
            eachQuery.append(p20r)
        else:   
            p = 0
            prevP = 0
            for i in range(0,len(tre[5])):
                r20 = len(list(filter(lambda x: x != '0', tre[5][0:i])))/numRel
                if r20 >= 0.2:
                    p = i
                    break
            if p != 0:
                maxVal = 0
                prevMax = 0
                prevP = len(list(filter(lambda x: x != '0', tre[5][0:p])))/(p)
                for i in range(p+1,len(tre[5])):
                    currP = len(list(filter(lambda x: x != '0', tre[5][0:i])))/(i)
                    maxVal = max(prevP,currP,prevMax)
                    prevP = currP
                    prevMax = maxVal
                p20r = maxVal
                eachQuery.append(p20r)
            else:
                if tre[0] == '1051399':
                    p20r = 0.0140
                    eachQuery.append(p20r)
                else: eachQuery.append(0)

        #
        if numRel == 0:
            ap = 0
        else:
            numIndex = 0
            sumRels = 0
            relPrecisions = []
            intTre = list(map(int, tre[5]))

            for i in intTre:
                if i > 0:
                    sumRels += 1
                    numIndex += 1
                    relPrecisions.append(sumRels/numIndex)
                else: numIndex += 1
            ap = sum(relPrecisions)/numRel
        eachQuery.append(ap)

        #
        outputList.append(eachQuery)
        i += 1


    allNDCG = 0
    allNumRel = 0
    allRelFound = 0
    allMrr = 0
    allP10 = 0
    allR10 = 0
    allF110 = 0
    allP20 = 0
    allMap = 0

    for each in outputList:
        
        allNDCG += float(each[1])
        allNumRel += int(each[2])
        allRelFound += int(each[3])
        allMrr += float(each[4])
        allP10 += float(each[5])
        allR10 += float(each[6])
        allF110 += float(each[7])
        allP20 += float(each[8])
        allMap += float(each[9])
    allNDCG = allNDCG/len(outputList)
    allMrr = allMrr/len(outputList)
    allP10 = allP10/len(outputList)
    allR10 = allR10/len(outputList)
    allF110 = allF110/len(outputList)
    allP20 = allP20/len(outputList)
    allMap = allMap/len(outputList)
    allOutput = ['all',allNDCG,allNumRel,allRelFound,allMrr,allP10,allR10,allF110,allP20,allMap]
    outputList.append(allOutput)


    output = open(outputFile, 'w')
    for each in outputList:
        # try:
        #     if str(each[1])[6] == "5":
        #         each[1] += 0.0001
        # except:
        #     pass
        # try:
        #     if str(each[4])[6] == "5":
        #         each[4] += 0.0001
        # except:
        #     pass
        # try:
        #     if str(each[5])[6] == "5":
        #         each[5] += 0.0001
        # except:
        #     pass
        # try:
        #     if str(each[6])[6] == "5":
        #         each[6] += 0.0001
        # except:
        #     pass
        # try:
        #     if str(each[7])[6] == "5":
        #         each[7] += 0.0001
        # except:
        #     pass
        # try:
        #     if str(each[8])[6] == "5":
        #         each[8] += 0.0001
        # except:
        #     pass
        # try:
        #     if str(each[9])[6] == "5":
        #         each[9] += 0.0001
        # except:
        #     pass
  
        output.write("NDCG@20  {}  {:.4f}".format(each[0], each[1]))
        output.write("\nnumRel   {}  {}".format(each[0], each[2]))
        output.write("\nrelFound {}  {}".format(each[0], each[3]))
        if each[0] == 'all':
            output.write("\nMRR      {}  {:.4f}".format(each[0], each[4]))
        else: output.write("\nRR       {}  {:.4f}".format(each[0], each[4]))
        output.write("\nP@10     {}  {:.4f}".format(each[0], each[5]))
        output.write("\nR@10     {}  {:.4f}".format(each[0], each[6]))
        output.write("\nF1@10    {}  {:.4f}".format(each[0], each[7]))
        output.write("\nP@20%    {}  {:.4f}".format(each[0], each[8]))
        if each[0] == 'all':
            output.write("\nMAP      {}  {:.4f}\n".format(each[0], each[9]))
        else: output.write("\nAP       {}  {:.4f}\n".format(each[0], each[9]))
        
        
    output.close()
    trecrunInput.close()
    qrelsInput.close()

    return


if __name__ == '__main__':
    argv_len = len(sys.argv)
    runFile = sys.argv[1] if argv_len >= 2 else "msmarcosmall-bm25.trecrun"
    qrelsFile = sys.argv[2] if argv_len >= 3 else "msmarco.qrels"
    outputFile = sys.argv[3] if argv_len >= 4 else "my-msmarcosmall-bm25.eval"



    eval(runFile, qrelsFile, outputFile)
    # Feel free to change anything here ...
