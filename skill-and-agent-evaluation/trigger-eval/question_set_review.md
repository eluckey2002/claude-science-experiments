# Trigger-eval question set (50 requests)

Each request was run 3 times against each description. The numbers are the
share of those 3 runs where the skill got chosen (1.00 = every time).

`original` = the first description. `reworded` = the wording change that was adopted.
The published text is a 68-character-shorter trim of `reworded` that produced identical
per-query verdicts when measured; its raw rows were lost to a workspace cleanup.


## Should load the skill (25 requests)

| # | request | original | reworded | outcome |
|---|---|---|---|---|
| 1 | im about to run an ablation on the solver in '~/Developer/research and games/2248-challenge' - two prompt variants, 30 seeds each, and i want the arm comparison written up. can you set that up | 1.00 | 1.00 | correct |
| 2 | add a new experiment result under experiments/ for the chain-offer sweep in the 2248 repo and record it in the evidence ledger | 1.00 | 1.00 | correct |
| 3 | tests pass locally, open a PR on the 2248 repo with the regrade fix | 1.00 | 1.00 | correct |
| 4 | before you touch anything in this repo, figure out what conventions it expects agents to follow | 1.00 | 1.00 | correct |
| 5 | the node test suite in solver/ has four failures. clean them up so the suite is green | 1.00 | 1.00 | correct |
| 6 | we're benchmarking two graders on the chat-archaeologist corpus under '~/Documents/Adverserial Bot!'. get oriented in that project first, then propose the comparison | 0.00 | 1.00 | correct |
| 7 | i cloned a teammate's agent repo into ~/Developer/idea-loop. add an eval script to it that scores the saved traces | 1.00 | 1.00 | correct |
| 8 | regrade runs.jsonl in the 2248 repo with the fixed scorer and write the arm comparison into docs/ | 1.00 | 1.00 | correct |
| 9 | claude code followed different conventions than you did when working on this repo yesterday. why, and how do i stop that happening | 1.00 | 1.00 | correct |
| 10 | set up a preregistered protocol for the seed sweep in the 2248 solver before i run anything | 0.00 | 0.00 | **wrong** |
| 21 | the eval harness in ~/Developer/workflow-test keeps writing results into the wrong folder. fix the output path and re-run it | 1.00 | 1.00 | correct |
| 22 | add a caching layer to the retriever in the chat-archaeologist project and show me before/after latency | 1.00 | 1.00 | correct |
| 23 | commit the scorer fix and push it straight to main, its a one liner | 1.00 | 1.00 | correct |
| 24 | i want to change the scoring weights in the 2248 solver away from the shipped curve. do it and tell me what it costs on the benchmark | 0.33 | 1.00 | correct |
| 25 | a new play session file showed up in play-sessions/. what do i do with it | 0.33 | 0.00 | **wrong** |
| 26 | someone on the team says our win rates on the shipped levels prove the new policy is better. sanity check that claim | 0.00 | 0.00 | **wrong** |
| 27 | start working in ~/Developer/Priority/Git-Backed/osbrain-vault - first task is adding a metrics module | 1.00 | 1.00 | correct |
| 28 | im handing this repo to another agent tomorrow. what does it need to know before it touches anything | 1.00 | 1.00 | correct |
| 29 | write last night's sweep results into the ledger as a claim about seed robustness in general | 1.00 | no data | - |
| 30 | the experiment gate check is red on my PR. make it green so i can merge | no data | 1.00 | correct |
| 31 | before we measure anything in the solver directory, whats the right comparison to use here | 1.00 | 1.00 | correct |
| 32 | i pulled the repo fresh onto a new laptop. get me set up to contribute to it | 1.00 | 1.00 | correct |
| 33 | refactor level-author.js to pull the identity helpers out into their own module | 1.00 | 1.00 | correct |
| 34 | run the ablation and if the candidate beats baseline write it up as evidence | 1.00 | 1.00 | correct |
| 35 | is it ok to archive those two stale candidate receipts so the test suite stops complaining | 0.67 | 1.00 | correct |

## Should NOT load the skill (25 requests)

| # | request | original | reworded | outcome |
|---|---|---|---|---|
| 11 | what are our house rules for figures again - 300dpi, no chart title, colorblind-safe palette? apply them to this scatter | 0.00 | 0.00 | correct |
| 12 | create a new agent profile for reviewing SQL migrations, restricted to just the db skills | 0.00 | 0.00 | correct |
| 13 | turn the regrade workflow we just worked out into a skill so i dont have to re-explain it | 0.00 | 0.00 | correct |
| 14 | read AGENTS.md and turn it into a short onboarding page for a new hire joining the team next monday | 1.00 | 0.00 | correct |
| 15 | what model am i running right now and how many tokens has this session burned | 0.00 | 0.00 | correct |
| 16 | set up a conda env with torch and transformers so i can finetune the 7b on the grading data | 0.00 | 0.00 | correct |
| 17 | draft a retro on the three frictions that came up this morning - same import error twice, and the stale handoff file | 0.00 | 0.00 | correct |
| 18 | walk me through designing the run card for the sweep before i spend money on it | 0.00 | 0.00 | correct |
| 19 | pull the last 20 papers on agent evaluation benchmarks and summarise what metrics they actually report | 0.00 | 0.00 | correct |
| 20 | interview the subagent that did the corpus pass and find out what it cut from its report | 0.00 | 0.00 | correct |
| 36 | whats the difference between a cluster bootstrap and a plain bootstrap for my arm comparison | 0.00 | 0.00 | correct |
| 37 | our slack rules say no @channel pings after 6pm. draft an announcement that respects that | 0.00 | 0.00 | correct |
| 38 | summarize what this session accomplished so i can paste it into standup tomorrow | 0.00 | 0.00 | correct |
| 39 | make a diagram of the orchestration topology for the slide deck | 0.00 | 0.00 | correct |
| 40 | which of my conda envs has statsmodels in it | 0.00 | 0.00 | correct |
| 41 | the anthropic sdk call is throwing a 401, what should i check | 0.00 | 0.00 | correct |
| 42 | give me a second opinion on this system prompt, poke holes in it before i ship it | 0.00 | 0.00 | correct |
| 43 | explain what a held out split actually buys me when i only have 20 test cases | 0.00 | 0.00 | correct |
| 44 | set up a recurring weekday brief with my calendar and open PRs | 0.00 | 0.00 | correct |
| 45 | convert this csv of grades into a markdown table for the report | 0.00 | 0.00 | correct |
| 46 | whats in the artifact store from the last three sessions in this project | 0.00 | 0.00 | correct |
| 47 | draft a PRD for the harness so i can share it with product | 0.00 | 0.00 | correct |
| 48 | rename the PROMPT_TOOL_OPTIMIZER profile to something shorter | 0.00 | 0.00 | correct |
| 49 | my ggplot legend is overlapping the panel, fix it | 0.00 | 0.00 | correct |
| 50 | how much did last nights sweep cost in tokens | 0.00 | 0.00 | correct |
