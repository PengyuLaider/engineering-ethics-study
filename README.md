![工程伦理学学习助手。教材复习、案例分析、课堂分享。](assets/cover.png)

# 工程伦理学学习助手

一个中文 Codex Skill，支持**教材复习、开卷简答和案例分享**。按《工程伦理学》第二版答题、出题和评分，引用原书页码。也可从课外真实案例出发，核对工程事实，完成伦理分析、讲稿和图文 PPT。

[下载资料](#下载资料) · [快速开始](#快速开始) · [使用示例](#使用示例) · [开卷简答](#开卷简答) · [案例分享与汇报](#案例分享与汇报) · [工作原理](#工作原理) · [教材与数据](#教材与数据) · [仓库结构](#仓库结构)

| 课程覆盖 | 知识点 | 教材案例 | 跨章主题 | 题库 |
|:---:|:---:|:---:|:---:|:---:|
| **8 章 39 节** | **91** | **50** | **12** | **74 道练习 + 59 道简答** |

## 下载资料

2026 年 11 月 23 日版开卷简答资料共 24 页，覆盖 8 章 39 节。前两页有速查目录，第 3–4 页是重点四题，最后一页有两组自测。每题附教材出处和分点参考答案。

| 资料 | 内容 |
| --- | --- |
| [打印 PDF](materials/open-book/short-answer-review.pdf) · [可编辑 Word](materials/open-book/short-answer-review.docx?raw=true) | 开卷简答速查资料 |
| [59 道开卷简答题库](engineering-ethics-study/references/open-book-bank.jsonl) | 题干、分项答案、教材页和自测评分 |
| [章末思考题参考答案](materials/chapter-review-answers.md) | 33 道教材题的拟答、出处和评分点 |
| [教材案例与思考题索引](materials/textbook-cases-and-questions.md) | 按章查案例和复习题的印刷页 |
| [教材 Word 校对报告](materials/word-proofreading-report.md) | 教材底本版本、抽检范围和准确率口径 |

## 快速开始

### 在 Codex 中使用

将仓库里的 [engineering-ethics-study](engineering-ethics-study/) 文件夹复制到已配置的 Codex Skill 目录。保留文件夹名称，并在对话里调用。

~~~text
用 $engineering-ethics-study 解释主动性责任和被动性责任。
先给简答题得分点，再用一个工程情境说明，附教材页码。
~~~

### 用命令行检索

Python 3 使用标准库即可。以下命令从仓库根目录运行。

~~~bash
python engineering-ethics-study/scripts/lookup.py --section 3.5
python engineering-ethics-study/scripts/lookup.py --case "三鹿"
python engineering-ethics-study/scripts/lookup.py --questions 6.5
python engineering-ethics-study/scripts/lookup.py --item EE-ORIG-06-05
~~~

第一条展开知识点，第二条定位两处正式教材案例，第三条呈现练习题面，第四条打开同一道题的拟答和六项评分点。

## 使用示例

| 想做什么 | 怎么问 | 得到什么 |
| --- | --- | --- |
| 查清教材口径 | 实测能运行，工程就应当实施吗？ | 技术评估与社会评估的区别，以及原书第 216–219 页的依据 |
| 比较两个案例 | 三鹿毒奶粉事件和三鹿庭审记录分别怎么分析？ | 第 5 章的人道主义视角，以及第 6 章的组织决策与召回视角 |
| 自测与核分 | 出两道第 6 章的题，先给题目，交卷后再评分 | 题面、可核对的答案和逐项扣分依据 |
| 准备开卷考试 | 结合我提供的教材出简答题，做可打印的速查资料 | 多问式题干、逐页核对的原句、分项答案和册页索引 |
| 分享课外案例 | 用我给的调查报告准备 7 分钟课堂分享 | 证据时间线、伦理分析、口语讲稿和逐页图解 |

### 查看一条带出处的判断

> **技术可行还需要接受社会评估。** 技术评估考察可行性和设计的完整性。社会评估考察经济、生态与安全。教材在第 219 页还把建成后的管理维修安全和当地居民的认同与满意列入讨论。
>
> 《工程伦理学》第二版，第 216–219 页

~~~bash
python engineering-ethics-study/scripts/lookup.py --topic "实测能运行，项目就应当实施吗"
~~~

## 开卷简答

按节覆盖概念、比较和专业应用题。先对照题干确认所问术语和枚举，再查用户提供的同版 Word，用教材原句、原书印刷页和分点答案编排速查资料。

~~~text
用 $engineering-ethics-study 做开卷简答练习。
请解释教材中工程伦理基本准则与道德规范的不同口径，
用我提供的同版 Word 核对原句和印刷页，再写考场可用的分点答案。
~~~

查看从来题拆分、教材取证到打印复核的步骤。[开卷简答与考场资料](engineering-ethics-study/references/open-book-workflow.md)

用命令行查看重点四题中的第一题。其余题沿用资料题号，前缀为 `EE-OPEN-`。

~~~bash
python engineering-ethics-study/scripts/lookup.py --bank engineering-ethics-study/references/open-book-bank.jsonl --item EE-OPEN-Z1
~~~

## 案例分享与汇报

从用户指定的教材案例、书外工程事件或已有课件出发。先核对调查原文与时间线，复原关键决定和当时可选的方案，再用相关伦理原则解释判断。整改写清执行岗位、验证证据和复核时机。

~~~text
用 $engineering-ethics-study 做一段 7 分钟的课外工程案例分享。
请根据我提供的调查报告核对决策过程，写口语讲稿、
逐页图文提纲和资料出处，并说明整改如何验收。
~~~

按需要生成课堂讲稿或课件。已有 PPT 时，可沿用确认过的模板，并核对图源、页序、备注和媒体。[案例分享指南](engineering-ethics-study/references/case-sharing.md)

## 工作原理

1. 用节号、主题或案例名定位知识卡，确认题干要求及教材口径。
2. 回查原书页。概念题核对定义和条件，案例题核对事实、相关方、备选措施及责任。
3. 生成有依据的答案或练习，并把评分点落实到可判分的步骤。

书外案例沿用伦理论证方法。案件事实引用调查材料，教材概念引用教材页码。讲稿和课件依据同一份证据记录。

## 教材与数据

参考教材为赵莉、姚立根主编的《工程伦理学》第二版，高等教育出版社，2021 年 10 月。ISBN 978-7-04-056942-1。两套题库收录 33 道章末思考题、41 道原创练习和 59 道开卷简答，附参考答案、依据页和自测评分。[出版社图书页面](https://www.hep.com.cn/book/show/d0cc3797-e263-4819-8933-4267a2eb5a19)

教材原句按印刷页标注。权利人如需反馈，请提供具体文件、页码和依据。核实后会移除涉及权利问题的内容。[权利问题反馈](https://github.com/PengyuLaider/engineering-ethics-study/issues)

Skill 自带知识卡、案例卡和题库。全文查证可使用你持有的教材。原书排版版 Word 可以通过页级书签检索，例如原书第 95 页的书签为 `PDF_107`。

<details>
<summary>用自己的 Word 或逐页索引查原文</summary>

~~~bash
python engineering-ethics-study/scripts/lookup.py --word "原书排版版.docx" --printed 93-95
python engineering-ethics-study/scripts/lookup.py --index "教材页索引.jsonl" "普适性" "道义论"
~~~

`--word` 适用于带 `PDF_001` 至 `PDF_267` 页级书签的原书排版版。普通 Word 或其他版次可作为对话附件，按实际页码定位。

</details>

## 仓库结构

| 路径 | 用途 |
| --- | --- |
| [SKILL.md](engineering-ethics-study/SKILL.md) | 教材复习和案例分享的统一入口 |
| [教材知识地图](engineering-ethics-study/references/course-map.md) | 全书 39 节的范围和依据页 |
| [题目与评分流程](engineering-ethics-study/references/question-workflows.md) | 检索方式、题库维护与阅卷 |
| [开卷简答与考场资料](engineering-ethics-study/references/open-book-workflow.md) | 分问设计、原句取证、答题及打印核验 |
| [案例分享指南](engineering-ethics-study/references/case-sharing.md) | 事实核验、伦理论证、讲述与交付检查 |
| [检索脚本](engineering-ethics-study/scripts/lookup.py) | 查节、主题、案例、练习和题库答案 |
| [复习资料](materials/) | 下载开卷卷子、章末题答案、案例索引及校对报告 |

冒烟测试覆盖章节、案例、问法、题面和答案定位。

~~~bash
python tests/smoke_test.py
~~~
