# PyDepGraph

![Star](https://img.shields.io/github/stars/shangfr/PyDepGraph?style=flat-square) ![fork](https://img.shields.io/github/forks/shangfr/PyDepGraph?style=flat-square) ![watch](https://img.shields.io/github/watchers/shangfr/PyDepGraph?style=flat-square) ![Apache-2.0](https://img.shields.io/github/license/shangfr/PyDepGraph?style=flat-square) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shangfr-pydepgraph-app-gh2ivs.streamlitapp.com/)

**简体中文**🀄 | [English🌎](./README.en.md)

#### 介绍

[PyDepGraph-Python项目依赖树可视化工具](https://shangfr-pydepgraph-app-gh2ivs.streamlitapp.com/)

PyDepGraph is a utility for displaying the installed python packages in form of a dependency tree. 

![pic](./picture/pic0.png)

![pic](./picture/pic1.png)
![pic](./picture/pic2.png)
![pic](./picture/pic3.png)

#### 软件架构

软件架构说明

- **Pipdeptree** Python项目依赖数据获取
- **Streamlit** Web应用程序框架
- **Echarts** Graph可视化

#### 安装教程
```bash
$ git clone https://github.com/shangfr/PyDepGraph.git
```
#### 使用说明
```bash
$ cd py-dep-graph
$ streamlit run app.py
```

##### 上传本地项目依赖json文件

**查看所有包及其依赖**
```bash
$ pip install pipdeptree
$ pipdeptree --json > pkg.json
```

**查看指定包及其需要的依赖** 
```bash
$ pipdeptree --json -p xxx包名 > xxxpkg.json
```

**查看哪些包依赖于此指定包**
```bash
$ pipdeptree --json -p xxx包名 -r  > xxxpkg.json
```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

