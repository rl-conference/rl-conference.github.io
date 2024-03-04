# RLC Reviewer Guidelines 2024

RLC is introducing a new reviewing process (<a href="https://rl-conference.cc/review_process.html">link</a>) with two types of reviewers: technical and senior. The purpose of this document is to make clear the role of each reviewer type and what goes into each type of review. It is worth stressing that this will be notably different from the typical NeurIPS/ICLR/ICML review process. We are changing things up, because the RLC PC believes the usual process is not working well.

At a high level, let’s distinguish these two types of reviews. A **technical review** is more or less a list of technical errors in the paper. There is no commentary on novelty, significance, or impact. This is not an oversight on our part. It is very intentional. A **senior review** is a typical review, but much closer to what is expected of a TMLR paper review: focus on claims matching evidence.

With terms set, let’s get into the details of technical reviews. It is important that both reviewer types read and understand the following two sections to get the full picture of what we are trying to implement.


## Technical reviews for RLC

Please organize your review into major errors and minor errors. **Major errors** are things that would jeopardize the paper’s ability to support its claims. These include things such as:

* **Math errors:** vacuous theorem statements, flaws in a proof, etc
* **Overclaiming:** like claiming false things about a new method that is not supported by the theory or empirical evidence given
    * **Example:** claiming a new method is significantly better than another based on invalid statistics, such as learning curves averaged over 5 seeds with overlapping shaded regions.
    * **Example:** A new TD learning method is developed with the hopes that it leads to learning richer feature sets with neural networks. It is shown that it achieves higher performance, but there is no measure of what representations are being learned. Any claim regarding the method’s representation learning ability would be unsupported by the experiments.
* Missing literature: that would have impacted the development of the ideas in the paper.
* Related, this **idea has been done before**, and the paper’s treatment is nearly identical to prior work.
* **Collection of minor errors** that, when taken together, make it very difficult to understand the purpose of the paper: poor polish, organization, inconsistent notation, undefined terms, etc. Things that on their own are minor but when co-occurring in mass can make a paper difficult to follow.
* **Unclear problem statement:** we do not know what problem is being solved or the paper did not motivate the problem and it's unclear why it matters. 


Before moving on to minor errors, it is worth discussing flaws in empirical work. Many of these can be seen as minor errors, but do become major errors when combined with overclaiming. However, since the empirical practices in RL are often substandard, we will specifically name a few common errors that should be noted in a technical review:

* **Missing information** like the number of trials (i.e., seeds), the definition of shaded regions / errorbars, not describing how hyperparameters were dealt with
* **Using measures of variance as a measure of confidence:** plotting standard deviation is not the same as a confidence interval
* **Invalid statistical analysis:** using standard error without justification (assumes normality and known variance), using IQM (interquartile mean) without justifying why top and bottom percentiles should be excluded
* **Missing baselines:** relevant baselines that would help us understand the new method (e.g., if claiming a new continuous action method works well, SAC or PPO are likely a useful baseline). Avoid asking for all the baselines, this is not needed and often just makes things less clear
* **Misrepresenting baselines:** using default hyperparameters of agent X, from the literature, on an MDP that agent X has never been applied to. This is appropriate if just to demonstrate X must be tuned for this new MDP, but it is not evidence that X performs poorly on this new MDP.
* **Tuning the hyperparameters of the new method only:** All RL agents are sensitive to hypers. We know this is problem dependent. Showing tuned performance is better than another untuned method is misleading.
* **Claiming SOTA:** This is almost impossible to establish. It requires more seeds than you think, careful tuning of hypers (very expensive), valid confidence intervals (likely studentized bootstrap). Rarely informative. Rarely true.
* **Ranking methods without rigorous statistical support:** Ok to say method A appears better than B in our experiments. Making ranking claims based on too few seeds (3 and 5 are way too few). How many seeds do we need? This is a statistical question based on the underlying performance distributions. **Number of required seeds is not defined by community common practice.**

The last point is actually a general principle. The goal of the technical review is to identify errors that would suggest the claims of the paper don’t match the evidence. To determine this you must weigh the evidence provided and determine if it is valid. One run (seed) could be enough to support the right claim. You must evaluate each experiment and the statistical evidence provided, not appeal to what other accepted papers do or do not do!

Let’s move on to minor errors. These are things that can be corrected and do not jeopardize the main message of the paper:

* Grammar, spelling, and general polish
* Plot styles
* Missing citations that are not critical missing baselines or ideas that would change the work
* Undefined notation
* Minor math errors
* Missing details


Finally, it is worth listing a few criticisms that are overused in reviews and are largely invalid—avoid putting these statements in your review!

* **“Not enough environments! The method may not be general”.** True of all current RL algorithms. This request is largely nonsense. Maybe you mean you want to see if the method works with images? Did the authors state that as a goal? Why is that important?
* **“Environments are too simple!”** Is Mountain Car simple? Yes, but so is Atari. This is arbitrary taste-making. The paper should explain why each environment was used and what we learned
* **“New method is not SOTA”.** This is nearly impossible to show, and only relevant if the paper states this as a goal
* **“New method is too simple”. “New method only combines existing ideas”.** Complexity != contribution
* **“No theoretical justification”.** Theory is but one form of evidence and is not required in every paper.

The guidelines above are not strict rules, and it is possible that some accepted papers may violate these guidelines with good reason. As such, the primary requirement for a paper to be accepted is that it clearly synthesizes new knowledge and that knowledge is of sufficient interest to the RL community. 


## Senior Reviewer Guidelines
The principles of the RLC should be reflected in the review process:

**The RLC peer review process prioritizes rigorous methodology over perceived importance, aiming to foster scholarly discussions on both well-established and emerging topics in RL.**

As such, the overall advice to senior reviewers is to **focus on three things:** (1) does the work provide evidence supporting the main contributions proposed by the authors—claims matched by evidence? (2) Is there an audience for the work? (3) What knowledge gap did the paper address?  

To make this concise, we provide three main guidelines to remember when reviewing. 
* **Answer three key questions for yourself**, to make a decision to Accept or Reject:
    * What is the specific question/problem tackled by the paper?
    * Is the approach well motivated, including being well-placed in the literature?
    * Does the paper support the claims? This includes determining if results, whether theoretical or empirical, are correct and if they are scientifically rigorous.
* **Organize your review as follows (inspired by [Sutton’s guide for writing good reviews](https://www.dropbox.com/scl/fi/4sfm8x3qlm3xp05xs0cdg/review-advice.rtf?rlkey=t2dvidfscp87w83us8tk0gn57&e=1&dl=0)):** 
    * Summarize what the paper claims to do/contribute. Be positive and generous.
    * Clearly state your decision (accept or reject) with one or two key reasons for this choice.
    * Provide supporting arguments for the reasons for the decision.
    * Provide additional feedback with the aim to improve the paper. Make it clear that these points are here to help, and not necessarily part of your decision assessment.

----

## Additional Resources
For great in-depth resources on reviewing, see these resources:

* Daniel Dennet: [Criticising with Kindness](https://www.brainpickings.org/2014/03/28/daniel-dennett-rapoport-rules-criticism/).
* Comprehensive advice: [Mistakes Reviewers Make](https://niklaselmqvist.medium.com/mistakes-reviewers-make-ce3a4c595aa2).
* Views from multiple reviewers: [Last minute reviewing advice](https://acl2017.wordpress.com/2017/02/23/last-minute-reviewing-advice/).
* [Sample excellent reviews](https://iclr.cc/Conferences/2020/ReviewerGuide) from ICLR 2020 reviewer instructions.
* [Rich Sutton’s guide for writing good reviews](https://www.dropbox.com/scl/fi/4sfm8x3qlm3xp05xs0cdg/review-advice.rtf?rlkey=t2dvidfscp87w83us8tk0gn57&dl=0).
