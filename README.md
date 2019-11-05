# optimization-of-pandas-for-large-CSV
>Pandas 是常用的 Python 软件库，可用于数据操作和分析。在进行数据分析时，导入数据（例如pd.read_csv)几乎是必需的，但对于大的CSV，可能会需要占用大量的内存和读取时间，这对于数据分析时如果需要Reloading原始数据的话会非常低效。
>Dataquest.io 发布了一篇关于如何优化 pandas 内存占用的教程，仅需进行简单的数据类型转换，就能够将一个棒球比赛数据集的内存占用减少了近 90%，而pandas本身集成上的一些压缩数据类型可以帮助我们快速读取数据。


## 1. 方法介绍
[博客](https://blog.csdn.net/wlx19970505/article/details/102920112)

## 2.类的使用

**step1:导入**：from Reduce_fastload import reduce_fastload  
**step2:实例化**：process=reduce_fastload('your path',use_HDF5=True/False,use_feather=True/False)  
**step3:对原始数据作内存优化**：process.reduce_data()  
**step4:加载优化数据**：process_data=process.reload_data()  

## example

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191105195459124.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dseDE5OTcwNTA1,size_16,color_FFFFFF,t_70#pic_center)
&#160; &#160; &#160; &#160;可以看出，原CSV文件占用内存为616.95MB，优化内存后的占用仅为173.9MB，且相对于原来pd.read_csv的7.7s的loading time,读入优化后的预处理数据文件能很大程度上的加速了读取。


### Reference 
[1].https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65
[2].https://zhuanlan.zhihu.com/p/56541628
[3].https://blog.csdn.net/weiyongle1996/article/details/78498603
