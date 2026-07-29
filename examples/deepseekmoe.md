---
title: "DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models"
authors:
  - "Damai Dai"
  - "Chengqi Deng"
  - "Chenggang Zhao"
  - "Runxin Xu"
  - "Huazuo Gao"
  - "Deli Chen"
  - "Jiashi Li"
  - "Wangding Zeng"
  - "Xingkai Yu"
  - "Y. Wu"
  - "Zhenda Xie"
  - "Y.K. Li"
  - "Panpan Huang"
  - "Fuli Luo"
  - "Chong Ruan"
  - "Zhifang Sui"
  - "Wenfeng Liang"
paper_url: "https://aclanthology.org/2024.acl-long.70/"
pdf_url: "https://aclanthology.org/2024.acl-long.70.pdf"
arxiv_url: "https://arxiv.org/abs/2401.06066"
doi: "10.18653/v1/2024.acl-long.70"
published: "2024-01-11"
venue: "ACL 2024, Volume 1: Long Papers"
paper_type: "model/method"
topics:
  - "稀疏混合专家语言模型"
  - "专家专门化"
  - "细粒度专家分割"
  - "共享专家隔离"
contributions:
  - "在等专家参数与等计算约束下拆分专家并增加激活专家数"
  - "用始终激活的共享专家承载公共知识并降低路由专家冗余"
  - "以消融和专家屏蔽实验分析专家不可替代性与参数利用率"
  - "扩展到 16.4B 总参数和 2.8B 激活参数并训练 2T tokens"
code_url: "https://github.com/deepseek-ai/DeepSeek-MoE"
status: "analyzed"
sources:
  - "https://aclanthology.org/2024.acl-long.70/"
  - "https://aclanthology.org/2024.acl-long.70.pdf"
  - "https://arxiv.org/abs/2401.06066"
  - "https://arxiv.org/e-print/2401.06066"
  - "https://github.com/deepseek-ai/DeepSeek-MoE"
  - "https://arxiv.org/abs/2405.04434"
  - "https://arxiv.org/abs/2412.19437"
---

# Sources

- [ACL Anthology 正式出版页](https://aclanthology.org/2024.acl-long.70/)
- [ACL 2024 正式论文 PDF](https://aclanthology.org/2024.acl-long.70.pdf)
- [arXiv 摘要页（2401.06066）](https://arxiv.org/abs/2401.06066)
- [arXiv v1 TeX 源码包](https://arxiv.org/e-print/2401.06066)
- [DeepSeek-AI 官方代码与模型仓库](https://github.com/deepseek-ai/DeepSeek-MoE)
- [DeepSeek-V2 官方技术报告](https://arxiv.org/abs/2405.04434)
- [DeepSeek-V3 官方技术报告](https://arxiv.org/abs/2412.19437)

# 0 一句话判断

DeepSeekMoE 的关键价值不是简单地“把 MoE 做得更大”，而是重新分配同一份专家参数和计算预算：把少量大专家切成更多小专家，让每个 token 组合更多细粒度专家；再把公共能力固定交给始终激活的共享专家，使路由专家更有机会聚焦差异性知识。这个设计很简洁，也能自然解释论文中 2B 规模等预算比较的稳定收益。

最有说服力的证据是受控的 2B 实验：相同数据、训练设置、总参数、激活参数和 FLOPs 下，DeepSeekMoE 在 Table 1 列出的 11 项指标上全部优于 GShard；把最高路由分数的专家屏蔽后，DeepSeekMoE 的损失上升更快，且移除共享专家会把 Pile loss 从 1.808 推高到 2.414。后两项结果支持“专家更不可替代、冗余更低”，但它们仍是功能性代理指标，不能单独证明每个专家已经形成可解释且互不重叠的语义分工。

论文的主要边界同样清楚：训练语料未公开，缺少多随机种子、置信区间和真实端到端延迟数据；细粒度路由增加的跨设备通信也没有在主要实验中被量化。因此，这是一篇架构假设与受控证据都很强的工作，但“ultimate expert specialization”仍应理解为研究方向，而不是已被完全验证的终局结论。

# 1 论文概览

## 1.1 研究问题

稀疏 MoE 通过只激活少数专家，在扩大总参数量的同时控制单 token 计算量。论文认为，常见 top-1/top-2 MoE 仍受到两个结构性问题限制：

1. **知识混杂（knowledge hybridity）**：专家数量少、单个专家过大时，一个专家会接收覆盖多类知识的 token，难以形成聚焦分工。
2. **知识冗余（knowledge redundancy）**：不同 token 都需要的公共知识会被重复写入多个专家，浪费专家参数。

论文把目标定义为提高 **expert specialization**，即让专家掌握更聚焦、重叠更少的知识。其直接研究范围是 Transformer 中替代 FFN 的稀疏 MoE 层，不涉及注意力稀疏化、检索增强或动态改变每个 token 的计算预算。

## 1.2 核心产物与贡献

论文贡献的是一种 MoE 层设计，而不是新的路由学习范式或新的预训练目标。DeepSeekMoE 包含两个相互配合的结构：

- **Fine-Grained Expert Segmentation**：把每个原专家沿 FFN 中间维切成 \(m\) 个小专家，总专家数从 \(N\) 增至 \(mN\)，每个 token 的激活数从 \(K\) 增至 \(mK\)，从而保持专家总参数与激活计算基本不变。
- **Shared Expert Isolation**：从专家池中隔离 \(K_s\) 个共享专家，对每个 token 始终激活；剩余计算预算用于 top-\((mK-K_s)\) 路由专家。

论文先在约 2B 总参数、100B tokens 的受控实验中比较 Dense、Hash Layer、Switch Transformer、GShard 和 DeepSeekMoE，再把架构扩展到 16.4B 总参数、2.8B 激活参数，并在 2T tokens 上预训练。

## 1.3 主要结论

- 2B 设置中，DeepSeekMoE 与 GShard 都是约 2.0B 总参数、0.3B 激活参数、每 2K tokens 约 4.3T FLOPs；DeepSeekMoE 在 Table 1 的 1 项语言建模 loss 和 10 个下游指标上全部更优。
- DeepSeekMoE 2B 的整体表现接近一个使用全部 16 份 FFN 参数的 Dense\(\times16\) 对照，并与专家参数和专家计算均放大 1.5 倍的 GShard\(\times1.5\) 接近。
- 16B 设置中，DeepSeekMoE 每 4K tokens 为 74.4T FLOPs，约为 LLaMA2 7B 的 39.6%、同语料 DeepSeek 7B 的 40.5%；其总体基准表现与两者相当，但在 MMLU、CEval、CMMLU 等多项选择任务上落后于 DeepSeek 7B。
- 正式 ACL 版本只以 base model 的 2B 和 16B 证据作为主结论。arXiv v1 还包含 Chat SFT 与 145B 初步实验，二者不应混同为 ACL 正式版本的同行评审结论。

# 2 背景与定位

## 2.1 从稀疏计算到专家分工

标准 Transformer block 的 FFN 对每个 token 使用同一组参数。典型 MoE 则把 FFN 替换为 \(N\) 个专家，并由门控网络计算 token 隐状态 \(\mathbf u_t^l\) 与专家中心 \(\mathbf e_i^l\) 的亲和度：

\[
s_{i,t}=\operatorname{Softmax}_i\left((\mathbf u_t^l)^\top \mathbf e_i^l\right).
\]

只有 top-\(K\) 专家的门值 \(g_{i,t}\) 非零，因此总参数可以远高于单 token 的激活参数。GShard 代表可学习 top-2 路由，Switch Transformer 使用 top-1 路由；Hash Layer 则以固定哈希完成 token 到专家的分配。它们主要解决“如何在稀疏激活下扩展容量”，DeepSeekMoE 进一步追问“固定容量与计算下，专家颗粒度和公共知识应该如何组织”。

## 2.2 与直接替代方案的区别

DeepSeekMoE 没有改变“token 经路由器选择 FFN 专家”的基本框架，也仍需辅助均衡损失。其差异主要来自专家池内部的结构重参数化：

- 相对 top-1/top-2 路由，它用更多、更小的专家提供更丰富的组合空间。
- 相对单一同质专家池，它把公共路径与条件路径显式分开。
- 相对 Expert Choice 等改变分配方向或容量约束的方法，它仍然是 token-choice top-\(K\) 路由，更容易嵌入已有 MoE 训练系统。

论文也承认，共享专家并非完全没有先例；其新意在于把共享专家与细粒度分割共同解释为“降低公共知识冗余、提高路由专家专门化”的统一架构。

## 2.3 “上界”应如何理解

论文把 Dense\(\times16\) 称为相同专家容量下 MoE 的严格上界，因为该对照对每个 token 都使用 16 份标准 FFN 参数，不再因稀疏路由舍弃任何专家容量。这个上界只对论文构造的 FFN 容量与训练设置成立：它不是所有同 FLOPs 模型的理论最优值，也不覆盖注意力容量、优化方法、数据质量或更一般的稠密架构。

# 3 DeepSeekMoE 的专家重组机制

## 3.1 输入、输出与两阶段重参数化

输入是第 \(l\) 层注意力后的 token 表示 \(\mathbf u_t^l\)，输出是 MoE-FFN 结果与残差之和。论文先把原来的 \(N\) 个专家各切成 \(m\) 份，再固定保留 \(K_s\) 个共享专家。完整层可写成：

\[
\mathbf h_t^l =
\sum_{i=1}^{K_s}\operatorname{FFN}_i(\mathbf u_t^l)
+\sum_{i=K_s+1}^{mN} g_{i,t}\operatorname{FFN}_i(\mathbf u_t^l)
+\mathbf u_t^l.
\]

共享专家不经过 top-\(K\) 竞争；路由器只从剩余 \(mN-K_s\) 个专家中选择 \(mK-K_s\) 个。由此，单 token 实际使用 \(K_s\) 个共享专家和 \(mK-K_s\) 个路由专家，总激活数仍是 \(mK\)。

> [Figure 1]

Figure 1 用三幅结构图固定了公平比较的核心：传统 top-2、细粒度分割、再加入共享专家的完整 DeepSeekMoE，在专家总参数与激活计算上保持不变。它说明收益假设来自“参数如何分组、专家如何组合”，而不是暗中增加每 token 计算；但图本身并不处理更高专家数可能引入的通信和 kernel 效率损失。

## 3.2 细粒度专家分割

若原始每个专家的 FFN 中间维为 \(d_{\mathrm{ff}}\)，切分后单个专家使用约 \(d_{\mathrm{ff}}/m\)。专家总数由 \(N\) 变为 \(mN\)，激活数由 \(K\) 变为 \(mK\)，因此理想化的专家参数量和矩阵乘计算量保持不变。

设计动机有两层。第一，单个小专家容纳的知识范围更窄，有利于减少知识混杂。第二，同一 token 可以组合更多小专家，组合自由度显著增加。论文给出的例子是：\(N=16\) 时 top-2 只有
\(\binom{16}{2}=120\) 种组合；切成 64 个小专家并激活 8 个后，组合数变为
\(\binom{64}{8}=4{,}426{,}165{,}368\)。组合数不是性能保证，但它说明该重参数化扩大了条件计算路径的表达空间。

## 3.3 共享专家隔离

共享专家对所有 token 始终可见，目标是集中存放不同上下文都会使用的通用变换。若公共知识被共享路径吸收，路由专家便无需重复学习同一内容，可以把容量留给更具条件性的特征。为了维持计算预算，加入 \(K_s\) 个共享专家后，路由激活数相应减少 \(K_s\)。

这一机制隐含了一个可检验假设：共享专家应该比任意新增路由专家更难替代，同时路由专家之间应减少功能冗余。论文没有直接标注各专家的语义主题，而是通过禁用共享专家、屏蔽高分路由专家及减少激活专家数来测试这种功能不可替代性。

## 3.4 路由与均衡损失

更多专家会放大 routing collapse 风险，即少数专家长期吸收大部分 token、其余专家训练不足。ACL 正式版本使用 expert-level balance loss：

\[
\mathcal L_{\mathrm{Bal}}=\alpha\sum_{i=1}^{N'}f_iP_i,
\]

\[
f_i=\frac{N'}{K'T}\sum_{t=1}^{T}\mathbf 1(\text{token }t\text{ 选择专家 }i),
\qquad
P_i=\frac{1}{T}\sum_{t=1}^{T}s_{i,t},
\]

其中 \(N'=mN-K_s\)，\(K'=mK-K_s\)。\(f_i\) 描述实际分配频率，\(P_i\) 描述平均路由概率。该正则项鼓励负载均衡，但论文同时观察到更强的均衡约束会损害模型质量，因此在 16B 训练中只取 \(\alpha=0.001\)。

## 3.5 16B 实例与训练实现

DeepSeekMoE 16B 使用 28 层、隐藏维 2048、16 个注意力头，每头 128 维。第一层保留稠密 FFN，因为作者观察到第一层负载均衡收敛尤其慢；其余 FFN 均替换为 MoE。每个 MoE 层含 2 个共享专家和 64 个路由专家，每个专家为标准 FFN 的 \(1/4\)，每个 token 固定使用 2 个共享专家和 top-6 路由专家。最终模型约 16.4B 总参数、2.8B 激活参数。

预训练语料为 DeepSeek-AI 构建、以英语和中文为主的多语语料，训练量 2T tokens；BPE 词表 100K，上下文长度 4096。训练采用 AdamW（\(\beta_1=0.9,\beta_2=0.95\)，weight decay 0.1），峰值学习率 \(4.2\times10^{-4}\)，前 2K steps warmup，在 80% 和 90% 进度处各乘 0.316；batch 为 4608 条序列、约 18M tokens，共 106,449 steps，不使用 dropout。

实验基于 HAI-LLM，使用 tensor、data、pipeline 与 expert parallelism，并为路由和跨专家线性层融合编写 CUDA/Triton kernel。论文报告使用 A100 或 H800 集群及 InfiniBand，但没有给出完整训练所需 GPU 数、GPU-hours、墙钟时间或能耗。

# 4 从 2B 受控实验到 16B 扩展的证据

## 4.1 2B 等预算架构比较

验证实验统一使用从同一内部语料抽取的 100B tokens、8K BPE 词表、9 层 Transformer、隐藏维 1280、最大长度 2048。DeepSeekMoE 2B 含 1 个共享专家和 63 个路由专家，每个专家为标准 FFN 的 \(1/4\)，每个 token 激活 1 个共享专家与 7 个路由专家。对比模型共享训练语料与超参数；GShard 与 DeepSeekMoE 还对齐到约 2.0B 总参数、0.3B 激活参数和每 2K tokens 4.3T FLOPs。

> [Table 1]

Table 1 是最干净的主结果：DeepSeekMoE 在列出的 11 项指标（Pile loss 与 10 个下游指标）上都优于 GShard，例如 Pile loss 由 1.867 降到 1.808，HellaSwag 从 50.5 升到 54.8，ARC-challenge 从 31.6 升到 34.3，TriviaQA EM 从 10.2 升到 16.6。该表强力支持“在这一规模和训练预算下，结构重组优于传统 top-2”，但 HumanEval、MBPP 等绝对分数很低，不能据此推断现代代码模型场景中的收益幅度。

论文还比较了 Hash Layer、Switch Transformer 与 0.2B dense baseline。稀疏模型普遍优于同激活参数的 0.2B dense 模型，说明更大总容量本身有效；DeepSeekMoE 对 GShard 的等预算优势则进一步隔离了本文架构的贡献。

## 4.2 更大 GShard 与稠密容量对照

> [Table 3]

Table 3 显示 DeepSeekMoE 用 1.89B 总专家参数、0.24B 激活专家参数和 4.3T FLOPs，取得与 GShard\(\times1.5\) 接近的整体结果；后者使用 2.83B 总专家参数、0.35B 激活专家参数和 5.8T FLOPs。它也接近每 token 使用全部 1.89B 专家参数、计算达 24.6T FLOPs 的 Dense\(\times16\)：Pile loss 分别为 1.808 与 1.806。不过 RACE 两项和 NaturalQuestions 上仍有差距，所以“接近上界”是跨任务总体判断，而非每个任务都已达到上界。

这组比较比只看总参数更有解释力，因为它同时列出总专家参数、激活专家参数与 FLOPs。不过 Dense\(\times16\) 是作者特制的 FFN 容量对照，不是常规参数比例的 dense Transformer；把它外推成普遍理论上界会过度强化结论。

## 4.3 组件消融

> [Figure 2]

Figure 2 在相同总参数与激活参数下依次比较 GShard、加入 1 个共享专家、进一步切为 32 个专家、再切为 64 个专家。多数任务随共享专家引入和粒度变细而改善，支持两个组件都在发挥作用；但图中性能按各任务最佳值归一化，未报告随机种子、方差或显著性，因此更适合判断一致趋势，不适合估计精确效应量。

arXiv v1 还报告，在 64 个总专家且激活数固定时，使用 1、2、4 个共享专家的 Pile loss 分别为 1.808、1.806、1.811，差异很小。作者据此在扩展模型中采用共享专家与激活路由专家约 1:3 的比例。这个比例是经验选择，不是由正式 scaling law 推导。

## 4.4 专家专门化的功能性代理

> [Figure 3]

Figure 3 对每个 token 屏蔽不同比例的最高路由概率专家，再从剩余专家中选择 top-\(K\)。在无屏蔽时与 GShard\(\times1.5\) 的 Pile loss 同为 1.808，随后 DeepSeekMoE 的损失上升更快。作者将这种敏感性解释为路由专家更难相互替代、参数冗余更低；更谨慎地说，该实验测到的是局部替代性，不直接揭示专家学习了哪些语义知识。

共享专家的干预结果更强：禁用共享专家、同时多激活一个路由专家以保持计算量后，Pile loss 从 1.808 上升到 2.414。这说明共享路径承担了路由专家不能即时替代的重要功能，与“公共知识被隔离”相容；但也可能部分来自共享专家始终参与训练造成的分布依赖，论文没有用重新训练后的替代结构排除这一解释。

> [Figure 4]

Figure 4 把 DeepSeekMoE 的激活路由专家数从 7 逐步减至 3；只激活 4 个路由专家时，Pile loss 已与完整 top-2 GShard 接近。该结果表明细粒度组合能以更少激活专家保留较多能力，但这是对已按 7 个路由专家训练好的模型做推理期干预，不能完全代表低激活配置从头训练后的最优结果。

> [Figure 5]

Figure 5 补上了从头训练证据：新模型仍有 1 个共享专家和 63 个路由专家，但每 token 只激活 3 个路由专家，即激活专家参数约为 GShard 的一半；在图示的 HellaSwag、PIQA、ARC-easy、ARC-challenge、TriviaQA 和 NaturalQuestions 上仍全部超过 GShard。这比纯推理期裁剪更能支持参数利用率提升，但任务范围缩小到 6 项，且仍未给出多次训练的不确定性。

## 4.5 16B 规模的能力与计算比较

> [Table 2]

Table 2 把 DeepSeekMoE 16B 与 LLaMA2 7B、同语料 DeepSeek 7B 放在一起：三者每 4K tokens 的 FLOPs 分别为 74.4T、187.9T、183.5T。DeepSeekMoE 在 Pile BPB（0.74 对 0.76/0.75）、HellaSwag（77.1 对 75.6/75.4）、HumanEval（26.8 对 14.6/26.2）和 TriviaQA（64.8 对 63.8/59.7）等指标上有优势，但在 DROP（32.9 对 34.0/34.9）、MMLU（45.0 对 45.8/48.2）、CEval（40.6 对 33.9/45.0）和 CMMLU（42.5 对 32.6/47.2）上并不占优。因此，“约 40% 计算达到相当表现”适合作为整体概括，而不是逐任务支配。

DeepSeek 7B 是更关键的架构对照，因为它与 DeepSeekMoE 16B 使用相同 2T 语料；LLaMA2 7B 虽训练 token 数同为 2T，但语料组成不同，代码、数学和中文差异不能归因于 MoE 架构。作者还指出 DeepSeekMoE 16B 的注意力参数约 0.5B，而 DeepSeek 7B 约 2.5B，并把多项选择任务的落后与较小注意力容量联系起来；这是合理假设，但论文没有给出单独扩展注意力容量的消融。

附录 Figure 6 展示了 2T tokens 训练过程中的多任务曲线，说明上述差异并非只在最终 checkpoint 突然出现；Figure 7 则按激活参数比较当时 Open LLM Leaderboard 的平均成绩。二者提供趋势与外部榜单背景，但都没有误差带，且榜单模型的数据和训练配方不可控。

# 5 局限、适用边界与复现条件

## 5.1 作者明确承认的限制

- **粒度与硬件效率冲突**：更细专家在消融中持续改善模型质量，但过小矩阵会降低 GPU kernel 效率，所以 16B 只采用 \(1/4\) 标准 FFN 的专家。
- **跨设备通信开销**：每个 token 选择更多专家时，expert parallelism 的 dispatch/combine 通信可能增加；论文没有在多节点部署中量化这一额外成本。
- **容量比例尚未搜索**：主要实验固定总专家参数为标准 FFN 的 16 倍、激活专家参数为 2 倍，最优总容量、激活容量与专家粒度缺少 scaling law。

## 5.2 数据与评测边界

训练语料只被描述为 DeepSeek-AI 构建、以英语和中文为主并包含网页、数学、代码与出版物的多语语料。论文没有公布来源清单、各域比例、去重与质量过滤规则、版权许可、隐私处理或基准污染检查，也没有发布语料。因此外部研究者无法在同数据条件下复现 100B 或 2T 训练。

主要结果来自自动基准，缺少开放式生成、人类偏好、安全性、事实可靠性和长上下文评测。模型上下文长度为 4096；“中英双语”表现不能外推到更广泛的多语覆盖。论文未报告多随机种子、置信区间或统计显著性，2B 消融中数值较小的差异尤其需要谨慎。

## 5.3 因果解释边界

等预算 2B 对照较好地支持“该架构提高下游表现”，但“提高表现是因为语义上的专家专门化”只得到间接支持。屏蔽敏感性说明专家较难替代，不能区分语义分工、路由分布更尖锐、优化耦合或容量利用率等机制。若要直接验证，需要展示专家激活与可解释语义簇、跨域迁移、专家互信息或可控替换之间的系统关系。

16B 对 DeepSeek 7B 的比较同时改变了总参数、激活参数、FFN/attention 参数比例和稀疏执行方式。它证明了一个有吸引力的质量-FLOPs 工作点，却不能单独估计每项设计选择的因果贡献。

## 5.4 系统效率与发布边界

论文以理论 FLOPs 为主，未报告预训练吞吐、端到端生成 tokens/s、首 token 延迟、并发、显存带宽占用或跨节点通信比例。ACL 正式版报告“单张 40GB GPU 可部署”，arXiv v1 另称经算子优化可接近 7B dense 模型 2.5 倍推理速度；二者都缺少正式延迟表，不能直接等同于任意框架和硬件上的真实加速。

官方仓库发布了 16B Base/Chat checkpoint 的入口、推理说明、微调脚本和 DeepSpeed 配置；代码采用 MIT License，模型使用带用途限制的 DeepSeek License Agreement。仓库没有提供完整预训练流水线、训练数据、2B 验证模型 checkpoint 或论文所述 HAI-LLM/CUDA/Triton 训练实现，因此可做推理与下游微调，但无法完整复现论文预训练。

# 6 结论与未决问题

## 6.1 可以确认的贡献

1. DeepSeekMoE 把“专家粒度”和“公共/条件知识分工”变成两个明确、可独立消融的 MoE 设计变量。
2. 在 2B、100B tokens 的同数据同预算设置中，它对 GShard 的优势覆盖论文列出的全部主指标，且更大 GShard 与 Dense\(\times16\) 对照强化了参数效率证据。
3. 专家屏蔽、共享专家替换和半激活从头训练共同表明，DeepSeekMoE 的有效专家参数比例高于所比较的 GShard 配置。
4. 16.4B 模型证明该架构能在 2T tokens 训练中稳定扩展，并以 2.8B 激活参数达到与 7B dense 模型大体相当的基准表现。

## 6.2 尚未解决的问题

- 专家颗粒度、共享专家数、激活专家数与模型规模之间是否存在可预测的 scaling law？
- 如何在保留细粒度组合优势的同时，降低小矩阵计算和 all-to-all 通信开销？
- 专家不可替代性是否对应稳定、可解释、可迁移的语义专门化？
- 注意力容量与专家容量应如何联合分配，才能修复 MMLU、CEval、CMMLU 等任务的弱项？
- 在公开数据、公开训练代码和多次独立训练下，等预算优势能否复现？
- 架构在长上下文、后训练、量化、在线 serving 和安全评测中的收益是否保持？

# 7 我的研究判断

我认为这篇论文最值得复用的不是“shared experts”或“更多小专家”中的单一组件，而是它对 MoE 参数预算的拆解方式：总参数、激活参数、专家颗粒度和组合自由度是四个不同变量，不应只用“总参数/激活参数”两个数字描述稀疏模型。Figure 1 与 Table 1 共同把这个观点讲得非常清楚。

证据强度上，2B 的等预算比较优于 16B 的跨模型榜单比较。前者较好控制了语料、训练设置、总参数、激活参数与 FLOPs，后者更接近实际模型价值，但混入了语料和注意力容量差异。若后续工作只能复现一部分，我会优先复现 2B 对照、Figure 2 消融和 Figure 3 的屏蔽曲线。

我不会把屏蔽后损失上升更快直接命名为“语义专门化更强”。它首先证明的是冗余更低或功能更不可替代。要完成论文标题中更强的主张，下一步应把路由行为与可解释数据属性连接起来，并验证这种分工能否跨 checkpoint、随机种子、语料域和模型规模保持稳定。

工程上，这个方向的关键不再只是模型 FLOPs，而是细粒度 GEMM 的利用率与专家通信。论文已经准确预见了这一矛盾；后续 DeepSeek 系列继续保留 DeepSeekMoE，同时改进负载均衡和训练系统，也说明架构价值与系统共设计必须一起评估。

# 8 版本、发布与后续工作

## 8.1 arXiv v1 与 ACL 正式版本

arXiv v1 于 2024-01-11 提交；ACL 正式版本发表于 2024 年 8 月的 ACL 2024 长文集，页码 1280--1297。两版核心架构、2B 验证与 16B base 结论一致，但范围不同：

- arXiv v1 还报告了 16B Chat 的 1.4M 样本 SFT，以及训练到 245B tokens 的 145B 初步模型。
- ACL 正式版本删除了 Chat 与 145B 章节，增加了明确的 “Limitations and Future Work”，并把正式主张集中在架构、2B 验证与 16B base model。

因此，本笔记的图表编号与核心结论均以 ACL 正式 PDF 为准；arXiv v1 的额外结果只用于说明版本演进，不作为 ACL 正式版本的决定性证据。

## 8.2 官方模型与代码发布

[DeepSeek-MoE 官方仓库](https://github.com/deepseek-ai/DeepSeek-MoE)提供 DeepSeekMoE 16B Base 和 Chat 的公开 checkpoint 入口，标注序列长度为 4096，并给出 Transformers 推理及全量/QLoRA 微调示例。仓库的公开内容支持模型使用和下游适配，但不等于论文训练流程的完整复现包；模型许可证也不同于代码的 MIT License，使用与再分发需要分别核对。

## 8.3 架构后续

- [DeepSeek-V2](https://arxiv.org/abs/2405.04434) 将 DeepSeekMoE 与 Multi-head Latent Attention 结合，扩展到 236B 总参数、21B 激活参数和 8.1T 预训练 tokens。它是官方模型线对本文架构的直接延续，而不是独立复现。
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437) 继续采用经 DeepSeek-V2 验证的 DeepSeekMoE，扩展到 671B 总参数、37B 激活参数，并引入 auxiliary-loss-free load balancing 与 multi-token prediction。无辅助损失均衡直接回应了本文中“均衡正则可能损害性能”的问题。

在本笔记采用的一手来源范围内，没有独立团队对论文全部受控实验的公开复现。后续官方模型证明该架构路线可以继续扩展，但不能替代公开数据、公开预训练代码和多随机种子复现。
