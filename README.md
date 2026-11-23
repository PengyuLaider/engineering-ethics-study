![工程伦理学学习助手。教材复习、案例分析、课堂分享。](assets/cover.png)

# 工程伦理学学习助手

一个中文 Codex Skill，支持**教材复习**与**案例分享**。按《工程伦理学》第二版答题、出题和评分，引用原书页码。也可从课外真实案例出发，核对工程事实，完成伦理分析、讲稿和图文 PPT。

[快速开始](#快速开始) · [使用示例](#使用示例) · [案例分享与汇报](#案例分享与汇报) · [工作原理](#工作原理) · [教材与数据](#教材与数据) · [仓库结构](#仓库结构)

| 课程覆盖 | 知识点 | 教材案例 | 跨章主题 | 题库 |
|:---:|:---:|:---:|:---:|:---:|
| **8 章 39 节** | **91** | **50** | **12** | **74 道** |

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
| 分享课外案例 | 用我给的调查报告准备 7 分钟课堂分享 | 证据时间线、伦理分析、口语讲稿和逐页图解 |

### 查看一条带出处的判断

> **技术可行还需要接受社会评估。** 技术评估考察可行性和设计的完整性。社会评估考察经济、生态与安全。教材在第 219 页还把建成后的管理维修安全和当地居民的认同与满意列入讨论。
>
> 《工程伦理学》第二版，第 216–219 页

~~~bash
python engineering-ethics-study/scripts/lookup.py --topic "实测能运行，项目就应当实施吗"
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

基线为赵莉、姚立根主编的《工程伦理学》第二版，高等教育出版社，2021 年 10 月。ISBN 978-7-04-056942-1。题库收录 33 道章末思考题和 41 道原创练习，附拟答、依据页和自测评分。

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
| [案例分享指南](engineering-ethics-study/references/case-sharing.md) | 事实核验、伦理论证、讲述与交付检查 |
| [检索脚本](engineering-ethics-study/scripts/lookup.py) | 查节、主题、案例、练习和题库答案 |

冒烟测试覆盖章节、案例、问法、题面和答案定位。

~~~bash
python tests/smoke_test.py
~~~
