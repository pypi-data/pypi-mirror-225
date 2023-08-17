## 1.文件介绍
evaluator.py  -- 评测demo  
parse_result.py -- 对评测结果文件进行解析、汇总，结构化输出  


## 2.使用方法

### 2.1 评测

1.从http://172.16.59.16:3000/mjchen/ailabsdk_dataset/src/branch/master/evaluation下载数据集  
2.设置evaluator.py文件中的DATASET_DIR变量为实际数据集路径  
3.按下面方法测评:  
比如: 在main中调用下面接口，评测chatglm2_6b模型，对应参数
tasktype: 测试基准(数据集)，此处为mmlu
use_peft: 是否加载权重，此处为False，代表测试的是基座模型
gpu_index：使用哪张GPU卡测试，此处为第5张卡
```
chatglm2_6b_test(tasktype = TaskType.mmlu, use_peft = False, gpu_index = 5)
```

设置好需要评测的参数和模型后，运行下面指令评测即可
```
python evaluator.py
```
### 2.2 结果解析
运行下面指令，默认从当前路径的./result加载解析结果文件
```
python parse_result.py
```
也可指定路径
```
python parse_result.py --dir ./result
```