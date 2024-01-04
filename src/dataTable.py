from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    ql = open("ql.eval", "r")
    bm25 = open("bm25.eval", "r")
    dpr = open("dpr.eval", "r")

    query = []
    qlAp = []
    bmAp = []
    ql_bm = []
    dprAp = []
    ql_dpr = []
    while True:
        eachQl = ql.readline()
        eachBm = bm25.readline()
        eachDpr = dpr.readline()
        if not eachQl:
            break

        if eachQl.startswith('AP') or eachQl.startswith('MAP'):
            eachQl = eachQl.split()
            eachBm = eachBm.split()
            eachDpr = eachDpr.split()

            eachQl[2] = '{:6.4f}'.format(float(eachQl[2]))
            eachBm[2] = '{:6.4f}'.format(float(eachBm[2]))
            eachDpr[2] = '{:6.4f}'.format(float(eachDpr[2]))
            

            query.append(eachQl[1])
            qlAp.append(eachQl[2])
            bmAp.append(eachBm[2])
            if float(eachQl[2]) == 0:
                eachQlBm = '{:5.1f}%'.format(0)
                ql_bm.append(eachQlBm)
            else :
                eachQlBm = '{:5.1f}%'.format(100*(float(eachBm[2])-float(eachQl[2]))/float(eachQl[2])) 
                ql_bm.append(eachQlBm)
            dprAp.append(eachDpr[2])
            if float(eachQl[2]) == 0:
                eachQlDpr = '{:5.1f}%'.format(0)
                ql_dpr.append(eachQlDpr)
            else :
                eachQlDpr = '{:5.1f}%'.format(100*(float(eachDpr[2])-float(eachQl[2]))/float(eachQl[2])) 
                ql_dpr.append(eachQlDpr)

           


    eval_data = {'Query': query,
            'QL': qlAp,
            'BM25': bmAp,
            'QL~BM %': ql_bm,
            'DPR': dprAp, 
            'QL~DPR %': ql_dpr}

    data = DataFrame(eval_data)
    pd.set_option('display.max_row',None)
    print(data)

    ql.close()
    bm25.close()
    dpr.close()



    preciRecall_ql = open("preciRecall_ql.txt", "r")
    preciRecall_bm25 = open("preciRecall_bm25.txt", "r")
    preciRecall_dpr = open("preciRecall_dpr.txt", "r")

    ql_precision = []
    ql_recall = []

    bm25_precision = []
    bm25_recall = []

    dpr_precision = []
    dpr_recall = []

    for i in range(0,2000):
        if i < 1000:
            ql_precision.append(float(preciRecall_ql.readline()))
            bm25_precision.append(float(preciRecall_bm25.readline()))
            dpr_precision.append(float(preciRecall_dpr.readline()))
        elif i >= 1000 and i <2000:
            ql_recall.append(float(preciRecall_ql.readline()))
            bm25_recall.append(float(preciRecall_bm25.readline()))
            dpr_recall.append(float(preciRecall_dpr.readline()))



    plt.plot(ql_recall, ql_precision, label='QL')
    plt.plot(bm25_recall, bm25_precision, label='BM25')
    plt.plot(dpr_recall, dpr_precision, label='DPR')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve for Query 330975')

    plt.legend()
    plt.show()
