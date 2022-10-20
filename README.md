# PyDepGraph

![Star](https://img.shields.io/github/stars/shangfr/PyDepGraph?style=flat-square) ![fork](https://img.shields.io/github/forks/shangfr/PyDepGraph?style=flat-square) ![watch](https://img.shields.io/github/watchers/shangfr/PyDepGraph?style=flat-square) ![Apache-2.0](https://img.shields.io/github/license/shangfr/PyDepGraph?style=flat-square) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shangfr-pydepgraph-app-gh2ivs.streamlitapp.com/)

#### 介绍

[PyDepGraph-Python项目依赖树可视化工具](https://shangfr-pydepgraph-app-gh2ivs.streamlitapp.com/)

PyDepGraph is a utility for displaying the installed python packages in form of a dependency tree. 

![pic](./picture/pic0.png)

#### 软件架构

软件架构说明

- **Pipdeptree** Python项目依赖数据获取
- **Streamlit** Web应用程序框架
- **Echarts** Graph可视化

#### 安装教程

1. $ git clone https://gitee.com/vencen/py-dep-graph.git

#### 使用说明

1. $ cd py-dep-graph
2. $ streamlit run app.py

##### 上传本地项目依赖json文件

**查看所有包及其依赖**

1. 安装 $ pip install pipdeptree
2. 执行 $ pipdeptree --json > pkg.json

**查看指定包，其需要的依赖** 

3. 执行 $ pipdeptree --json -p xxx包名 > xxxpkg.json

**查看哪些其它包，依赖于此指定包**

4. 执行 $ pipdeptree --json -p xxx包名 -r  > xxxpkg.json



#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

