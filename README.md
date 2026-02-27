> 在线阅读 | Read Online: https://wenddymacro.github.io/theeffectbook/

# 应用计量经济学讲稿（网页版）

## 书籍概述（中文）
本书围绕“因果识别 + 现代计量工具 + 宏观动态建模”展开，内容从回归与统计基础逐步推进到 IV、DID、RDD、合成控制、事件研究，再扩展到时间序列与 DSGE。全书强调：
- 识别策略与研究设计的匹配
- 实证实现与软件操作（尤其是 Stata 场景）
- 结果解释、稳健性检验与研究叙事

本网页版支持章节导航、公式展示、图表与代码阅读，并提供 PDF 下载。

## Book Overview (English)
This book integrates causal inference, applied econometric practice, and macro-dynamic modeling. It starts from regression/statistics foundations, then moves to IV, DID, RDD, synthetic control, and event-study methods, and extends to time-series and DSGE modeling.

Core focuses include:
- Matching identification strategy to research design
- Practical implementation and software workflows
- Interpretation, robustness checks, and research storytelling

This web edition provides chapter navigation, equations, figures, code blocks, and PDF access.

## 分章节内容概述（中文）
- [特别声明](chapters/chapter-01.html)：课程与讲稿的使用说明与边界。`#说明`
- [第1章 引言](chapters/chapter-02.html)：建立问题意识、数据思维与实证路径。`#ResearchDesign #Data`
- [第2章 概率与统计基础](chapters/chapter-03.html)：抽样、分布、估计与推断基础。`#Probability #Inference`
- [第3章 一元线性回归](chapters/chapter-04.html)：OLS 的直觉、估计和显著性检验。`#OLS #Regression`
- [第4章 多元线性回归](chapters/chapter-05.html)：遗漏变量偏误与控制变量策略。`#OVB #Controls`
- [第5章 识别的评价框架](chapters/chapter-06.html)：内部与外部有效性的系统评估。`#Identification #Validity`
- [第6章 面板数据模型](chapters/chapter-07.html)：固定效应与双向固定效应实务。`#PanelData #FixedEffects`
- [第7章 工具变量法](chapters/chapter-08.html)：IV 识别、弱工具与有效性诊断。`#IV #Endogeneity`
- [第8章 双重差分（DID）](chapters/chapter-09.html)：基准 DID、动态效应与扩展。`#DID #PolicyEvaluation`
- [第9章 断点回归设计（RDD）](chapters/chapter-10.html)：局部因果识别与带宽选择。`#RDD #LocalCausalEffect`
- [第10章 其他因果识别方法](chapters/chapter-11.html)：匹配法等补充策略。`#Matching #CausalInference`
- [第11章 合成控制法](chapters/chapter-12.html)：反事实构造与政策冲击评估。`#SyntheticControl #Counterfactual`
- [第12章 事件研究](chapters/chapter-13.html)：事件时点下的动态处理效应识别。`#EventStudy #DynamicEffects`
- [第13章 时间序列的自回归模型](chapters/chapter-14.html)：AR/VAR 与冲击传导分析。`#TimeSeries #VAR`
- [第14章 动态随机一般均衡模型](chapters/chapter-15.html)：DSGE 结构、求解与政策含义。`#DSGE #MacroModel`
- [第15章 极简 CGE](chapters/chapter-16.html)：教学型一般均衡建模入门。`#CGE #GeneralEquilibrium`
- [第16章 如何讲好经济学故事](chapters/chapter-17.html)：论文结构与叙事逻辑。`#Writing #Storytelling`
- [第17章 基本数学工具](chapters/chapter-18.html)：实证与模型推导所需数学。`#MathTools #Methods`

## Chapter-by-Chapter Highlights (English)
- [Disclaimer](chapters/chapter-01.html): usage notes and scope boundaries. `#Notes`
- [Ch.1 Introduction](chapters/chapter-02.html): framing questions, data thinking, and workflow. `#ResearchDesign #Data`
- [Ch.2 Probability & Statistics](chapters/chapter-03.html): sampling, distributions, estimation, inference. `#Probability #Inference`
- [Ch.3 Simple Regression](chapters/chapter-04.html): OLS intuition, estimation, and testing. `#OLS #Regression`
- [Ch.4 Multiple Regression](chapters/chapter-05.html): omitted variable bias and control strategy. `#OVB #Controls`
- [Ch.5 Identification Framework](chapters/chapter-06.html): internal and external validity checks. `#Identification #Validity`
- [Ch.6 Panel Models](chapters/chapter-07.html): fixed effects and two-way FE practice. `#PanelData #FixedEffects`
- [Ch.7 Instrumental Variables](chapters/chapter-08.html): IV logic, weak-IV risk, and diagnostics. `#IV #Endogeneity`
- [Ch.8 Difference-in-Differences](chapters/chapter-09.html): baseline DID and dynamic extensions. `#DID #PolicyEvaluation`
- [Ch.9 Regression Discontinuity](chapters/chapter-10.html): local causal design and bandwidth. `#RDD #LocalCausalEffect`
- [Ch.10 Other Causal Methods](chapters/chapter-11.html): matching and complementary tools. `#Matching #CausalInference`
- [Ch.11 Synthetic Control](chapters/chapter-12.html): counterfactual construction for policy analysis. `#SyntheticControl #Counterfactual`
- [Ch.12 Event Study](chapters/chapter-13.html): dynamic treatment effects over event time. `#EventStudy #DynamicEffects`
- [Ch.13 Time Series AR Models](chapters/chapter-14.html): AR/VAR and shock transmission. `#TimeSeries #VAR`
- [Ch.14 DSGE](chapters/chapter-15.html): structure, solution logic, and policy interpretation. `#DSGE #MacroModel`
- [Ch.15 Minimal CGE](chapters/chapter-16.html): teaching-oriented general equilibrium entry. `#CGE #GeneralEquilibrium`
- [Ch.16 Economic Storytelling](chapters/chapter-17.html): paper structure and narrative logic. `#Writing #Storytelling`
- [Ch.17 Mathematical Tools](chapters/chapter-18.html): core math support for empirics/modeling. `#MathTools #Methods`

## 网站结构
- `index.html`：首页（A4 封面样式 + 左侧目录导航）
- `chapters/`：章节页面（`chapter-xx.html`）
- `assets/`：样式、图片、PDF 等资源
- `scripts/update_nav.py`：章节目录自动同步脚本

## 发布与更新
### 首次发布到 GitHub Pages
1. 上传当前目录到 GitHub 仓库（分支 `main` 或 `master`）。
2. 在仓库 `Settings -> Pages` 中确认 `Build and deployment` 使用 `GitHub Actions`。
3. 等待 Actions 工作流 `Deploy Book To GitHub Pages` 完成。
4. 访问页面：`https://wenddymacro.github.io/theeffectbook/`

### 后续更新
- 修改内容后提交并推送，Pages 会自动重新部署。
- 若增删章节文件，先运行：

```bash
python3 scripts/update_nav.py
```
