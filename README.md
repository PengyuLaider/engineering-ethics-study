![工程伦理学学习助手。教材依据、伦理判断、答题与评分。](assets/cover.png)

# 工程伦理学学习助手

围绕《工程伦理学》第二版做中文**答题、原创命题、案例分析和分项评分**。知识点和答案附原书页码，使用带页书签的 Word 版时可定位到对应页。

[快速开始](#快速开始) · [使用示例](#使用示例) · [工作原理](#工作原理) · [教材与数据](#教材与数据) · [仓库结构](#仓库结构)

| 课程覆盖 | 知识点 | 案例 | 跨章主题 | 题库 |
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

### 查看一条带出处的判断

> **技术可行还需要接受社会评估。** 技术评估考察可行性和设计的完整性。社会评估考察经济、生态与安全。教材在第 219 页还把建成后的管理维修安全和当地居民的认同与满意列入讨论。
>
> 《工程伦理学》第二版，第 216–219 页

~~~bash
python engineering-ethics-study/scripts/lookup.py --topic "实测能运行，项目就应当实施吗"
~~~

## 工作原理

1. 用节号、主题或案例名定位知识卡，确认题干要求及教材口径。
2. 回查原书页。概念题核对定义和条件，案例题核对事实、相关方、备选措施及责任。
3. 生成有依据的答案或练习，并把评分点落实到可判分的步骤。

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
| [SKILL.md](engineering-ethics-study/SKILL.md) | 答题、出题、评分和案例分析规则 |
| [教材知识地图](engineering-ethics-study/references/course-map.md) | 全书 39 节的范围和依据页 |
| [题目与评分流程](engineering-ethics-study/references/question-workflows.md) | 检索方式、题库维护与阅卷 |
| [检索脚本](engineering-ethics-study/scripts/lookup.py) | 查节、主题、案例、练习和题库答案 |

冒烟测试覆盖章节、案例、问法、题面和答案定位。

~~~bash
python tests/smoke_test.py
~~~
