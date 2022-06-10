'''
Author: feng_chloe
Date: 2022-06-07 13:04:36
Description: sy1 code python3.8+vscode+jupyter notebook
FilePath: \实验一第二次提交c:\Users\20952\Desktop\sy-1.py
'''

# %%
# 导包
# pip install pandas,numpy,matplotlib,seaborn,statsmodels
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections
import matplotlib
import statsmodels.api as sm
from PIL import Image
import io
import pylab

%matplotlib inline
%config InlineBackend.figure_format = 'retina'
# 黑体显示中文
plt.rcParams['font.sans-serif'] = ['Simhei']
# 正常显示符号
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')
sns.set_palette("pastel",8)

# %%
# 1.选择 10 家企业


# 读取数据
d=[]
for i in range(20):
    d.append(pd.read_excel("试验一数据源_沪深300成分股票收益率2006-2015.xlsx",sheet_name=i))

# 获取公司名
company_name=[]
for i in range(20):
    company_name.append(d[i]['证券简称'][:300])
c_code=pd.DataFrame(company_name)

# 合并公司名称为一个Series
conc=[]
conc=pd.Series(conc)
for i in range(20):
    conc=pd.concat([conc,c_code.T.iloc[:,i]])

# 统计公司出现次数 输出出现次数最多的前一百个公司
cter=collections.Counter(conc)
print(cter.most_common(100))

# 选择10个公司为：平安银行，万科A，中国宝安，招商地产(退市)，中集集团，中金岭南'，农产品，中兴通讯，华侨城A，中联重科。 

# %%
# 读取整合选定公司数据
company_select=['平安银行','万科A','中国宝安','招商地产(退市)','中集集团','中金岭南','农产品','中兴通讯','华侨城A','中联重科']
company_dict={}
for i in company_select:
    company_dict[i]=[]
data_select=np.zeros((10,120)).tolist()

# 循环读取
for i in range(20):
    for j in range(299):
        for k in range(10):
            # 只读取指定公司的数据
            if(company_select[k]==d[i]['证券简称'][j]):
                # sheet与sheet之间有一列数据重合
                for x in range(4,10):
                    company_dict[company_select[k]].append(pd.DataFrame(d[i]).iat[j,x])

company_data=[]
company_data=pd.DataFrame(company_data)
for key,value in company_dict.items():
    company_data[key]=value

# %%
# 2.分析整个时间跨度（2006-2015 年）每股收益率的概率分布，判断是否符合正态分布；


# 绘制直方图
for i in company_data.columns:
    plt.hist(company_data[i])
    plt.xlabel('时间')
    plt.ylabel('收益率')
    plt.title(str(i)+'收益率直方图')
    # 图片输出为tiff格式
    png1=io.BytesIO()
    plt.savefig(png1,format="png",dpi=500,pad_inches= .1,bbox_inches='tight')
    png2=Image.open(png1)
   # 需要提前创建好直方图空文件夹
    png2.save('C:/Users/20952/Desktop/课程设计/实验一第一次提交/直方图/matplotlib绘制/'+str(i)+'收益率直方图.tiff')
    png1.close()
    plt.show()

# 绘制直方图
for i in company_data.columns:
    sns.distplot(company_data[i])
    png1=io.BytesIO()
    plt.savefig(png1,format="png",dpi=500,pad_inches= .1,bbox_inches='tight')
    png2=Image.open(png1)
   # 需要提前创建好直方图空文件夹
    png2.save('C:/Users/20952/Desktop/课程设计/实验一第一次提交/直方图/seaborn绘制/'+str(i)+'收益率直方图.tiff')
    png1.close()
    plt.show()

# %%
# 绘制QQ图
for i in company_data.columns:
    sm.qqplot(company_data[i], line='s')
    
    # 保存图片
    png1=io.BytesIO()
    plt.savefig(png1,format="png",dpi=500,pad_inches= .1,bbox_inches='tight')
    png2=Image.open(png1)
    png2.save('C:/Users/20952/Desktop/课程设计/实验一第一次提交/直方图/pylab绘制/'+str(i)+'收益率QQ图.tiff')
    png1.close()
    pylab.show()

# %%
# 进行正态检验 选择K-S检验
from scipy.stats import kstest
# cdf中可以指定要检验的分布，norm表示我们需要检验的是正态分布
# 常见的分布包括norm,logistic,expon,gumbel等
# KS检验最终返回两个结果，分别是检验统计量及P值。若p<0.05,则拒绝原假设，认为“样本数据来自的分布与正态分布有显著差异”。
for i in company_data.columns:
   print(str(i)+'的正态检验结果为：')
   print(kstest(company_data[i],cdf = "norm"))\

# 我们很遗憾地发现：没有一个是符合正态分布的。


# 3.继续分析以上企业的每股收益率，判断 t+1 时期的收益率与上一时期即 t 时期的收益率是否相关。
# 计数
count=0
for i in company_data.columns:
    # 错行读取，以实现t时刻与t+1时刻对应的效果。t时刻列舍弃最后一个数据，t+1时刻舍弃第一个数据
    df=pd.concat([company_data.iloc[0:-1,[count]],company_data.iloc[1:120,[count]].reset_index(drop=True)],ignore_index=True,axis=1)
    count+=1
    print(str(i)+'的相关系数为：\n'+str(df.corr()))

    # 绘制相关性图
    sns.pairplot(df)

    # 绘制热力图
    sns.heatmap(df.corr())
    plt.title(str(i)+'收益率相关性图')

    png1=io.BytesIO()
    plt.savefig(png1,format="png",dpi=500,pad_inches= .1,bbox_inches='tight')
    png2=Image.open(png1)
    # 需要提前创建好相关性图空文件夹
    png2.save('C:/Users/20952/Desktop/课程设计/实验一第一次提交/相关性图/'+str(i)+'收益率直方图.tiff')
    png1.close() 
    
    # 绘制散点矩阵图
    g = sns.PairGrid(df)
    g.map_diag(sns.distplot)
    g.map_upper(plt.scatter)
    g.map_lower(sns.kdeplot)
    plt.title(str(i)+'散点矩阵图')
    png1=io.BytesIO()
    plt.savefig(png1,format="png",dpi=500,pad_inches= .1,bbox_inches='tight')
    png2=Image.open(png1)
    # 需要提前创建好相关性图空文件夹
    png2.save('C:/Users/20952/Desktop/课程设计/实验一第一次提交/相关性图/'+str(i)+'散点矩阵图.tiff')


