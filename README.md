### LATEX-OCR助手
> 基于pytorch、tensorflow与tkinter第三方包创建
> 引用项目[yolov8](https://github.com/ultralytics/ultralytics)与[Latex-OCR](https://github.com/lukas-blecher/LaTeX-OCR)
------
### 包含的基本功能
* 对屏幕进行截图
* 识别图像中的公式位置
* 对公式进行OCR，生成Latex公式代码
* 实时渲染Latex公式，方便修改对照
------
### 必要前置
* 见文件requirement.txt
* 基本前置来自[yolov8](https://github.com/ultralytics/ultralytics/blob/main/setup.py)与[Latex-OCR](https://github.com/lukas-blecher/LaTeX-OCR/blob/main/setup.py)的setup.py文件，可以参照进行配置
* 为达到最好效果最好安装CUDA和Cudnn加速库
* 本项目基于python3.11创建
------
### 功能演示与使用方法
#### 项目功能演示与操作实例
![功能演示](docs/show.gif)
* 【截图】可以以类似QQ截图的方式保存截屏的图片
* 【定位】可以识别在截取的图片中属于公式的部分，并将公式部分切出
* 【识别】可以识别上一步切出的纯公式图片并生成Latex表达式
* 【渲染】可以将生成的Latex表达式的作渲染以预览效果
* 【更新】可以打开与关闭实时渲染模式，打开时可以一边修改一边预览效果；两个指示灯用来显示实时渲染模式是否打开/Latex表达式是否有语法问题
* 【一键】功能等于【截图】+【定位】+【识别】，如果【更新】打开，则可以一键完成所有功能
* **注：本项目渲染由matplotlib库完成，对很多较高级的Latex语法与标签支持性并不高，故渲染效果仅作参考**
#### 模型优化方法
* 此项目的公式截取模型使用Yolov8，在此项目ultralytic-main/tests中保存了公式标注的小型训练集（自己标的），通过增加训练集进行训练可以提升识别公式位置的准确度；
* 在main.py目录下打开命令行，输入
<code>yolo task=detect mode=train model=yolov8n.yaml data=gs.yaml  batch=8 epochs=500</code>
即可进行训练；训练生成的过程数据会保存至run文件夹下，并在主目录下生成pt模型
* 可用的数据集生成与标注文件打包至for_datasets.zip中，使用时修改数据生成路径即可

* **[Latex-OCR](https://github.com/lukas-blecher/LaTeX-OCR)模型的改动已经超出本项目预期，不作优化**
### 项目组件简述
* main文件提供UI界面与组件逻辑联系
* 使用[yolov8](https://github.com/ultralytics/ultralytics)(ultralytics-main)识别出公式位置；如果不截出纯公式图，[Latex-OCR](https://github.com/lukas-blecher/LaTeX-OCR)会把非公式部分强行识别为公式，输出乱码
* 使用[Latex-OCR](https://github.com/lukas-blecher/LaTeX-OCR)(pix2tex)识别出公式的Latex表达式，并使用optimize文件中的规则进行结果优化
* 使用matplotlib库进行公式渲染作为预览

### 调试遇到的问题及解决方式
* matplotlib线程冲突报错：Tcl_AsyncDelete: async handler deleted by the wrong thread
> 在打开实时渲染模式时使用一键模式会出现线程冲突，经排查是一键模式原本需要调用一次matplotlib渲染，随后由于公式发生改变，实时渲染模式的线程立刻也调用渲染函数，两个线程同时调用渲染导致线程冲突；故删去一键模式的渲染步骤，现在在不开启实时渲染模式的情况下一键模型仅处理到生成表达式的步骤，在开启实时渲染情况下正好完成完整流程
* 本项目使用了较多标志位进行线程间逻辑处理，可读性较差
> 目前没有很好的解决方案，也许使用一个文件专门储存逻辑参数或者进行更高程度的对象抽象封装可以提高可读性。~~但是为了大作业做这个有点愚蠢~~

### 附录
> **本项目将被用于提交图像采集课程的大作业** 
#### 可以参考的资料
* [yolov8训练过程及数据集生成方式](https://blog.csdn.net/qq_40716944/article/details/128648001)
* [yolov8模型结构与原理解析](https://blog.csdn.net/xu1129005165/article/details/132582070)