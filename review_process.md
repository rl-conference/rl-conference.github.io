# Review Process for RLC 2024
## Why this matters 
The quality of a conference depends on the quality of the work published there. One of the most important things we can do is put in place structures that make it more feasible to identify incorrectness in submitted papers and avoid rejecting good work. 

The goal of this proposal is to improve the quality of reviews. This benefits authors, who get better feedback, and also benefits RLC by improving the quality of papers.

One issue is that the community has grown very quickly. This growth has increased the burden on senior researchers, making it less feasible to devote time to reviewing and to training the next generation of reviewers. Junior researchers do not get the same opportunity to develop their reviewing abilities. Further, junior reviewers may have a harder time appreciating the importance of the work, especially if it looks different than the papers they are used to, yet are unfairly tasked with assessing novelty.  
## Proposal for the review process 
A key criteria for the RLC is stated as follows. “The RLC peer review process prioritizes rigorous methodology over perceived importance, aiming to foster scholarly discussions on both well-established and emerging topics in RL.” The below review process reflects this principle. **Note**: It is the opinion of the PC that focusing the review process on correctness will not result in an increased acceptance rate compared with the current review process.

Another fundamental principle is to make the review process as lightweight as possible. Extra work just detracts from spending time reading the paper carefully and writing a good review. The trend for improvements to reviewing has been to **add more work** to improve reviewing; the goal of this proposal is to **reduce workload**. 
### High-level overview

*  We have only two reviewers per paper: a senior reviewer (SR) and a technical reviewer (TR). The TR only checks correctness. The SR writes a regular review covering novelty, significance, and correctness.
* There is one Senior Area Chair (SAC) for each paper, that checks these reviews and is responsible for finding emergency reviews. (Note: We use the term SAC rather than AC to match terminology in OpenReview, explained more below)
* There is no author rebuttal nor author discussion period. However, the SAC and SR can ask authors direct questions (the authors will be able to see the review by this point in the process). There will also still be a reviewer discussion period.
* If the technical review is marked inadequate by the SAC and SR, then it is removed. Note that an SAC can first talk to the TR for improvements, instead of immediately choosing to remove. In the case of removal of a technical review, then the TR is replaced.
    * There is a pool of emergency TRs.
    * If a TR has all their reviews removed, then they are not listed as a reviewer for the RLC.
* The SAC writes a meta-review. It is expected that they will have discussed with the SR to try to get to a consensus. All cases where the SAC recommends rejection when the SR recommends acceptance will be reviewed by the Program Chairs.

### Motivation for two reviews

There may be concerns that two reviews is insufficient, due to noise in the process. This structure for reviewing, however, should already be lower noise. The reasons are as follows. 

* The acceptance principle of the conference (quoted above) allows us to avoid making calls between borderline papers. Noise typically affects these papers the most.
* A key part is to be careful about reviewer selection. This includes separating into the two roles (SR and TR). It also assumes we will more carefully select SACs, SRs and TRs.
* Bad reviews can be removed.
* The SAC and SR can collectively make decisions. It relies more on the SAC to also look at the paper. There may be scaling issues in the future, but for the first RL Conference, this is not a worry.
* A reviewer can actually do a better job when the review burden is lower. Namely, the same set of reviewers will produce less noisy reviews. 

It is important to recognize that adding more reviews does not necessarily decrease variance. Adding more reviews changes the distribution, and this distribution might actually have higher variance (e.g., we add less reliable reviewers). Even worse, this distribution might have high bias—we want to get closer to the distribution of expert reviewers, not a broad distribution over senior researchers, students, bloggers, and others that the current review pools are built from. Also note that for journal papers it is common for an Action Editor to make decisions based only on two reviews. 

### More details about the review process

* The TR only checks correctness. They write a review discussing correctness. They give no scores.
    * Box for Major Errors, Box for Minor Errors 
    * Error types: Academic misconduct/Plagiarism (with link to work that is copied), Missing Literature (minor if it's just a citation, major if it represents missing baselines of ideas that could have been included), Math errors, Empirical errors
    * The TR **will not include** statements about sufficient novelty
    * A short document will be provided outlining typical major and minor errors
* The SR writes a standard review. They have four scores: Reject, Borderline Accept, Weak Accept, Accept. The meanings of these categories are respectively
    * **Reject:** This paper being in the program would actively cause harm (incorrect, misleading, impossible to read).
    * **Borderline Accept:** This paper would not be bad to publish, but there'd be little lost if it was not.
    * **Weak Accept:** There is some value in this paper being published.
    * **Accept:** There is very high value in this paper being published; and not doing so would be harmful (to getting great ideas)
    * **Note:** the plan is to accept all papers that are not marked reject. However, some falling in the borderline category might be rejected pending adjustment of the process due to unforeseen outcomes (e.g., more accepted papers than people we have the capacity for, etc.)
* The SR and SAC can ask the authors questions as needed. Questions can be asked before reviews are submitted, during the reviewer discussion phase and even after the discussion phase. The authors will be informed to expect this and be ready.
* The reviewer discussion phase includes both the SR and TR.
* The SR and SAC can give written feedback to the TR on their review (recommended but not required). There will also be a rating given (Reject review, Acceptable and Excellent).

### Other details about the implementation

* We will use OpenReview. 
* The conference is double-blind. 
* Reviewers and SACs can see each other’s names.
* Everything will be kept hidden from the public: reviews, discussion, rejected papers.
* OpenReview does not yet have the ability to have multiple reviewer roles. We had to map to existing roles, meaning TRs are listed as Reviewers and SRs as Area Chairs. It also means we use the term Senior Area Chair above, for a role that is typically called an Area Chair, again to avoid naming confusion. 

### Timeline

* **Feb 1:** Submission site is opened
* **Mar 1:** Abstract submission deadline
* **Mar 8:** Submission deadline (anywhere on earth)
* **Mar 9 - Mar 15:** Paper bidding
* **Mar 17:** Finalize paper assignment
* **Mar 31:** Reviews due (2 weeks to review)
* **Apr 1 - Apr 14 (2 weeks):** [Review adjustment phase] SAC asks SRs or TRs to adjust their review if needed, SR/SAC read technical reviews and label as accept or reject, SAC assigns emergency reviewers as needed
* **Apr 15 - Apr 26:** Reviewer discussion phase (authors may be contacted with questions)
* **Apr 30:** Meta-reviews from SACs due
* **May 15:** Decision notification
* **Aug 9-12:** Conference