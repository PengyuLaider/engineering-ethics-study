# 题目与评分流程

## 定位材料

先用知识地图选章，再用检索脚本打开相关知识点。书签 `PDF_105` 是原书第 93 页在适配 Word 中的定位名。以下示例从仓库根目录运行。

~~~text
python engineering-ethics-study/scripts/lookup.py --word "原书排版版.docx" --printed 93-95
python engineering-ethics-study/scripts/lookup.py --index "教材页索引.jsonl" 普适性 道义论
python engineering-ethics-study/scripts/lookup.py --review 1.5
python engineering-ethics-study/scripts/lookup.py --stem "主动性责任和被动性责任有何区别？"
python engineering-ethics-study/scripts/lookup.py --section 3.5
python engineering-ethics-study/scripts/lookup.py --topic "能做到就该做吗？"
python engineering-ethics-study/scripts/lookup.py --case 7-末
python engineering-ethics-study/scripts/lookup.py --questions 5.2
python engineering-ethics-study/scripts/lookup.py --item EE-ORIG-05-02
~~~

多关键词按同页匹配的数量排序。普通匹配默认略过卷首目录。章、节、主题和案例使用本版教材的编号。`--case 三鹿` 返回同一事件的两条案例视角，按编号可查叙述和论证路径。`--word` 和 `--index` 分别提供 Word 与索引全文。题库默认使用随包数据，可用 `--bank` 指定自己的文件。

把来题的题干交给 `--stem` 检索，先保留原题和选项。若返回多条同题干记录或相近题，用 `--item` 展开对应候选，对照题源、限定词与原选项。改为问“错误项”、改变关键事实或替换选项的题目需要重新求解。借用评分点前按出处核对适用范围。可用“主动性责任／预防性责任”“源头污染预防／污染预防技术”等词交叉查教材。

## 题型处理

| 题型 | 答案与判断规则 |
| --- | --- |
| 单选与多选 | 逐项对照题干的范围、时间和程度限定，核查正确选项数量。遇到教材口径下并列条件，避免把例子、建议或必要条件误作充分条件。缺项或重复时标出题面问题。 |
| 判断 | 给判定、触发判断的限制词和最小修改。对“所有”“只要”“一定”检查是否存在书中明确的例外。 |
| 简答 | 先给教材术语与并列项，每点补一句与题意相关的解释。若问区别，用同一维度比较，如时间指向、目标和责任主体。 |
| 案例与论述 | 明确谁在何时选择什么，用材料证据支撑原则，比较备选措施及风险和成本，说明责任分配、执行和复核。分值对应实际推理动作，按论证质量接受合理替代结论。 |

## 出题交付

有明确考纲时建立“章节 × 题型 × 难度 × 分值”对照。无特殊要求的单题直接给出题目、参考答案、解析与教材出处。只要求练习题时按用户设定保留答案，便于自测。

每题反向求解一次。选择题检查正确项与干扰项证据，题干中给足必要事实。开放题标出必答点、分值和可接受变体，逐题核算总分。资料不完整的真实事件可改为明确标注的假设案例。

本版每节有一道原创练习。`--questions 5` 查第 5 章题面，`--questions 5.2` 查第 5 章第 2 节，`--item EE-ORIG-05-02` 查答案与评分。出整章或跨章练习时核对章节覆盖和不同题型的实际考查点。

## 题库追加

自建题库使用 JSONL，每行一条对象。沿用包内 `question-bank.jsonl` 的字段与唯一 ID。先匹配来源编号或规范化题干去重，有同题异版时保留版本关系。教材章末题按 `question_location` 记录章、题号和原书／PDF 题页。收到对应课程答案时，补到同一题的 `official_answer`，带上来源和适用范围。

| 字段 | 记录内容 |
| --- | --- |
| `id`、`origin`、`type` | 唯一编号。来源可用用户来题、教师材料、教材思考题或原创试用。题型使用自然中文。 |
| `stem`、`options`、`source` | 保留原题与原选项，同时记出处或批次。 |
| `official_answer`、`proposed_answer` | 记录教师或用户确认答案与助手拟答。尚未收到前者时填 null。 |
| `chapter`、`printed_pages`、`pdf_pages` | 记录该版教材中的题目和可用于解答的页码。 |
| `points`、`rubric`、`status` | 记录分值、分项评分和依据页。状态可用待核、已试答、已核教材或已确认课程口径。 |

教材中引用的法规、标准及案例数据依书中时期理解。涉及现行规定时，查官方文本和施行日期，核对相关旧法的有效状态与题设时间。在 `law_update` 中保留明确的核对日期、条文依据和官方链接。对缺少证据的年份、伤亡数字、命题来源和教师口径保留待查状态。
