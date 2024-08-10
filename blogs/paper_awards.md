---
title: "Announcing the RLC 2024 Outstanding Paper Awards"
date: "2024-08-10"
---


# Announcing the RLC 2024 Outstanding Paper Awards

We are honoured to announce the winners of the Outstanding Paper Awards at the First Reinforcement Learning Conference. As we outlined in another blog post, papers are awarded at RLC based on specific aspects of their contribution. We describe the process we used to select the awarded papers after. 

This year’s awards consist of seven papers, one per category. The awarded papers are listed below in alphabetical order by award name. Congratulations to all the authors! 

**Outstanding Paper Award on Applications of RL**
M. Vasco, T. Seno, K. Kawamoto, K. Subramanian, P. R. Wurman, and P. Stone: *A Super-human Vision-based Reinforcement Learning Agent for Autonomous Racing in Gran Turismo*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper213.html).

*This paper demonstrates for the first time that RL agents can achieve super-human performance in a high-fidelity racing simulator using only local features at execution time. Until now, this has only been possible by relying on global features or privileged information, which is unfeasible in practice. Hence, this work constitutes substantial progress in the application of RL for autonomous racing.*

**Outstanding Paper Award on Empirical Methods in RL Research**
K. Javed, A. Sharifnassab, and R. S. Sutton: *SwiftTD: A Fast and Robust Algorithm for Temporal Difference Learning*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper111.html).

*This paper proposes a new online temporal-difference algorithm for the prediction problem in RL with strong empirical performance when using linear function approximation. This paper stood out for its thoroughness, breadth, and depth of experiments that went above and beyond to provide empirical evidence of how the algorithm works. Examples include ablating all the relevant components, visualizing predictions and credit assigned to each pixel, running extensive hyperparameter searches for all baselines, and more.*

**Outstanding Paper Award on Empirical Resourcefulness in RL**
A. Raffin, O. Sigaud, J. Kober, A. Albu-Schaeffer, J. Silvério, and F. Stulp: *An Open-Loop Baseline for Reinforcement Learning Locomotion Tasks*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper18.html).

*This paper challenges common practices in RL by introducing a simple, low-cost method that is competitive with state-of-the-art deep RL algorithms on locomotion tasks. The proposed method generates periodic joint motions using simple oscillators. It performs strongly both in simulation and transfer to a real-world quadruped robot, further highlighting the practicality of this approach. This paper raises an interesting discussion about the trade-offs between cost, complexity, and generality when using deep RL, making it a valuable contribution to Empirical Resourcefulness in RL.*

**Outstanding Paper Award on Pioneering Vision in RL**
C. Cousins, K. Asadi, E. Lobo, and M. Littman. *On Welfare-Centric Fair Reinforcement Learning*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper133.html).

*This paper introduces a new framework for fair reinforcement learning, which allows for different societal ideals of fairness to be encoded through a welfare function rather than optimizing for a specific definition of fairness. The paper stood out for its clear exposition, motivation, and comprehensive theoretical results. This paper’s pioneering vision on fairness in RL opens the door to new research directions where society and other relevant parties agree on the notion of fairness rather than the algorithmic designer.*

**Outstanding Paper Award on Scientific Understanding in RL**
M. Suau, M. T. J. Spaan, and F. A. Oliehoek. Bad Habits: *Policy Confounding and Out-of-Trajectory Generalization in RL*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper216.html).

*This paper furthers our scientific understanding of why RL agents struggle to generalize to new scenarios at test time, paving the way to developing more robust RL algorithms. The paper characterizes the phenomenon of policy confounding through the lens of causality, whereby when following specific trajectories, RL agents can learn behaviours based on spurious correlations (between observations and rewards) because the policy is confounded with the data. The paper shows that on-policy algorithms can learn representations that are sufficient for the trajectory induced by the optimal policy but do not necessarily generalize well to new states, making agents non-robust to changes in the environment’s dynamics.*

**Outstanding Paper Award on Support Tools for RL Research**
D. Corsi, D. Camponogara, and A. Farinelli: *Aquatic Navigation: A Challenging Benchmark for Deep Reinforcement Learning*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper131.html).

*This paper develops a simulator for aquatic navigation using real-world data and proposes it as a new benchmark for RL algorithms. This environment poses a challenge to RL algorithms due to its unpredictable and non-stationary dynamics induced by complex fluid dynamics. Reinforcement learning frequently benefits from the often unpraised work of designing new simulators that capture different facets of the problems we care about, and this environment could very well be another one. Designing RL algorithms for aquatic navigation is a novel application that can have significant practical interest, making this work a valuable contribution to Support Tools for RL Research.*

**Outstanding Paper Award on the Theory of RL**
W. Xu, S. Dong, and B. Van Roy. *Posterior Sampling for Continuing Environments*. [Link to paper](https://rlj.cs.umass.edu/2024/papers/Paper277.html).

*This paper develops a new exploration method for the understudied continuing RL problem, showing how one can extend the posterior sampling algorithm originally designed for the episodic setting to the continuing setting. This is achieved by showing how one can reinterpret existing methods to resample a new policy at every time step instead of doing so at the beginning of each episode, an approach which is also effective in high-dimensional state spaces. The resampling probability can be used by the agent to dynamically adjust its planning horizon, thus better handling infinite-horizon problems. This paper stood out through its theoretical rigour in adapting algorithms from the episodic to the continuing setting, being one of the first papers to do so, potentially serving as a catalyst for more research on this topic.*


## Our Process

We selected these papers very carefully after following the process we designed. We decided to award papers for specific aspects of their contribution because we wanted to disentangle awards from aspects such as perceived novelty, impact, high scores, or the topic of the paper. This means that we were okay with an awarded paper having flaws in aspects that were not considered for that specific award; we were much more focused on identifying papers that did one specific thing really well.

Before describing the process we followed, notice we ended up adding a new category from what we had initially announced. As we reviewed the potential papers to be awarded, we realized that we were conflating papers with good empirical design and papers that supported empirical research. Because of that, we split the general “Outstanding Paper Award on Empirical Reinforcement Learning Research” into “Outstanding Paper Award on Empirical Methods in RL Research” and “Outstanding Paper Award on Support Tools for RL Research”.

With that out of the way, let us describe our process. First, we considered papers with conference organizers (at any level) as authors ineligible for the award, even when those papers were explicitly nominated for an award. We paid close attention to all papers explicitly nominated for an outstanding paper award. Still, we considered all other accepted papers for the award, regardless of the recommendation the area chair gave (Borderline accept, Weak accept, Accept). We chose to do so to give all papers a chance of being recognized with an award and increase robustness by considering alternative opinions (outside the review process). In addition, reviewers may not nominate papers they consider borderline, while our goal is to recognize papers that excel in a particular aspect rather than being flawless across the board. This was also needed to select papers for the two subcategories on “Support Tools for RL Research” and “Empirical Methods in RL Research” since reviewers were only provided with a single category on “Empirical RL Research” meant to encompass both of these. 

We selected the awarded papers in a three-stage process where the two of us did the work independently. At every stage, we would independently come up with a list of nominations, and we would then meet to discuss and decide which papers would go to the next stage. In the first stage, we read the abstracts of all the accepted papers and the meta-reviews, and we selected approximately 50 of those papers (out of a total of 113 accepted papers) for a more careful analysis. In the second stage, we additionally read each paper's reviews and looked at key aspects of the paper itself, coming up with a shortlist of 2-3 papers per category. We read each of these remaining 20 papers, specifically considering the category they were being considered for. As a purely hypothetical example, we would be comfortable awarding a paper on the Theory of RL that has very strong theoretical results but has flaws in its empirical evaluation. We wouldn’t award a paper on Empirical Methods in RL with a weak empirical design. Fortunately, at the end of this long process, we had come up, independently, with the exact same paper to be awarded in each category!

Five of the seven awarded papers received an “Accept” recommendation, and two received a “Borderline Accept” from the area chair. Only three had received a nomination from the reviewers.

Our approach allowed us to award a much more diverse set of papers, and we genuinely hope that it will help the community recognize a wider range of papers as valuable contributions. This process allowed us to award fantastic papers that would have a much harder time being recognized in more traditional review processes. Papers with small and large-scale experiments, with and without theoretical results, and with extremely simple and very complex ideas were all awarded here, and we believe this diversity can only strengthen our community.

One more time, congratulations to all the authors!

Below, you can find the updated list of award categories:

**Outstanding Paper Award on Empirical Methods in Reinforcement Learning Research **
*This award recognizes papers that make significant contributions to the empirical methods of reinforcement learning research. Examples include addressing fundamental practical challenges in reinforcement learning or introducing new empirical practices or methodologies. These papers should show a high standard of practical relevance and experimental rigour.*

**Outstanding Paper Award on Support Tools for Reinforcement Learning Research**
*This award recognizes papers that make significant contributions to support tools for reinforcement learning research. Examples include introducing new environments, datasets, benchmarks, evaluation metrics, visualization techniques, or frameworks and tools that will further enable empirical research in reinforcement learning. These papers should show a high standard of practical relevance, accessibility, ease of use and reproducibility.*

**Outstanding Paper Award on Applications of Reinforcement Learning**
*This award aims to acknowledge papers that demonstrate substantial progress in the application of reinforcement learning to complex, real-world problems. This award seeks to highlight groundbreaking work formulating real-world problems using the reinforcement learning framework, introducing a new application domain or challenge to reinforcement learning, or developing reinforcement learning methods that make significant progress on practical scenarios.  The papers should display a notable level of practical utility and uphold a high standard of scientific rigour.*

**Outstanding Paper Award on Empirical Resourcefulness in Reinforcement Learning**
*This award honours papers that demonstrate resourcefulness in empirical research. These are papers that ingeniously overcome the high computational cost of empirical research in reinforcement learning, promoting more frugal empirical research. Examples include showcasing original, cost-effective methodologies and resource-efficient experimental designs. The papers should embody high standards of creativity and practicality without sacrificing experimental rigour.*

**Outstanding Paper Award on Pioneering Vision in Reinforcement Learning**
*This award highlights papers that stand out with their forward-thinking vision and blue-sky ideas in reinforcement learning. The papers awarded in this category will present groundbreaking, visionary ideas, theories, or techniques in reinforcement learning, potentially reshaping current perspectives or paving new avenues for research and applications. The papers must demonstrate originality, creativity, and the potential to inspire transformative advancements in reinforcement learning. *

**Outstanding Paper Award on Scientific Understanding in Reinforcement Learning**
*This award celebrates papers that significantly advance scientific understanding in the domain of reinforcement learning. It encourages the development of a well-founded, clear understanding of the behaviour of existing algorithms or the nuances of different problem formulations or different environments. Awarded papers will fill gaps in our understanding of the field; they will bring clarity to unexplored aspects of existing algorithms, they will provide evidence to dispute common assumptions, or they will better justify common practices in the field. They should also demonstrate excellence in scientific rigour and clarity of exposition with very well-defined claims.*

**Outstanding Paper Award on the Theory of Reinforcement Learning**
*This award acknowledges papers that provide exceptional theoretical contributions to the field of reinforcement learning. Examples include theoretical unifications, new theoretical frameworks or formalisms, mathematical models, results, and theoretical insights into existing RL practices. The papers must exhibit a high level of technical proficiency and innovation.*

RLC 2024 Award Chairs
Marlos C. Machado and Roberta Raileanu
