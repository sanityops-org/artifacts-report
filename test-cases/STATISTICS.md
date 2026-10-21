# SanityOps Evaluation Test Case Statistics

> Source: auto-aggregated from the `## Metadata` blocks of all 200 case files under `test-cases/`. Generated 2026-10-14.
> **Snapshot note (2026-10-20)**: TC-007 was added after this aggregation. The figures below still describe the 200-case snapshot; they do not include TC-007.
> The "Domain (heuristic)" column is a keyword-based inference from the case file name / source project / artifact type; it is indicative only and should be reviewed manually before formal evaluation.

## 0. At a glance

- Total cases: **200**, 50 per kind (agent-suite / system-prompt / skill / tool-schema).
- Unique source projects: **176**; projects reused across cases are listed in Section 5.
- Mostly permissive licenses (MIT / Apache); **8** cases need special handling, see Section 2.
- Total content: **2,431,092** characters, **12,155** chars/case on average, see Section 4.

---

## 1. Scale and object composition

| Object kind | Directory | Cases | Share | File format |
|---|---|---:|---:|---|
| agent-suite | agent-suite/ | 50 | 25% | .md x 50 |
| system-prompt | single-artifact/system-prompt/ | 50 | 25% | .md x 50 |
| skill | single-artifact/skill/ | 50 | 25% | .md x 50 |
| tool-schema | single-artifact/tool-schema/ | 50 | 25% | .json x 1 + .md x 49 |
| **Total** | test-cases/ | **200** | 100% | md 199 + json 1 |

## 2. License distribution (with quoting constraints)

| License category | Cases | Share | Handling per the README quoting rules |
|---|---:|---:|---|
| MIT | 152 | 76% | Permissive; full quoting/modification allowed |
| Apache-2.0 | 36 | 18% | Permissive; full quoting/modification allowed |
| MIT+Apache-2.0 | 4 | 2% | Permissive; full quoting/modification allowed |
| Apache-2.0(+commercial) | 1 | 0.5% | Permissive parts quotable; commercial/dual-license must be flagged |
| Apache+AGPL(mixed) | 1 | 0.5% | Quote permissive parts only; flag and attribute the AGPL parts |
| AGPL-3.0 | 3 | 1.5% | Non-permissive; keep attribution and assess compliance |
| GPL-3.0 | 1 | 0.5% | Non-permissive; keep attribution and assess compliance |
| Proprietary | 1 | 0.5% | Structure outline + max 10-line short quotes only |
| Undeclared | 1 | 0.5% | No Metadata / no license declaration; must be completed |
| **Total** | **200** | 100% | |

## 3. Collection batches (by collection date)

| Collection date | agent-suite | system-prompt | skill | tool-schema | Total |
|---|---:|---:|---:|---:|---:|
| (none) | 0 | 0 | 0 | 1 | **1** |
| 2026-10-10 | 3 | 1 | 1 | 0 | **5** |
| 2026-10-12 | 12 | 2 | 0 | 0 | **14** |
| 2026-10-13 | 35 | 42 | 27 | 30 | **134** |
| 2026-10-14 | 0 | 5 | 22 | 19 | **46** |

## 4. Content volume

| Object kind | Cases | Total chars | Avg chars | Min | Max |
|---|---:|---:|---:|---:|---:|
| agent-suite | 50 | 679,465 | 13,589 | 4,836 | 29,774 |
| system-prompt | 50 | 464,669 | 9,293 | 3,248 | 35,771 |
| skill | 50 | 849,971 | 16,999 | 5,597 | 67,392 |
| tool-schema | 50 | 436,987 | 8,740 | 5,060 | 20,979 |
| **Total** | **200** | **2,431,092** | **12,155** | 3,248 | 67,392 |

## 5. Source-project reuse and cross-kind overlap

- Unique source projects: **176** (normalized by repo slug, e.g. cinnamon/kotaemon).
- Reused source projects: **12** (see the table below). Projects appearing in both single-artifact and agent-suite are cross-kind overlaps; avoid double-counting them during evaluation.

| Source project (slug) | Cases | Case IDs | Kind distribution |
|---|---:|---|---|
| alirezarezvani/claude-skills | 7 | 70, 78, 79, 80, 81, 82, 83 | agent-suite x 1 + skill x 1 + system-prompt x 5 |
| danielmiessler/fabric | 7 | 71, 72, 73, 74, 75, 76, 77 | agent-suite x 1 + system-prompt x 6 |
| modelcontextprotocol/servers-archived | 3 | 183, 184, 190 | tool-schema x 3 |
| modelcontextprotocol/servers | 3 | 185, 186, 187 | tool-schema x 3 |
| zylon-ai/private-gpt | 2 | 106, 130 | agent-suite x 1 + system-prompt x 1 |
| itzcrazykns/vane | 2 | 102, 112 | agent-suite x 1 + system-prompt x 1 |
| assafelovic/gpt-researcher | 2 | 1, 4 | agent-suite x 1 + system-prompt x 1 |
| mintplex-labs/anything-llm | 2 | 38, 109 | agent-suite x 1 + system-prompt x 1 |
| ai4finance-foundation/finrobot | 2 | 66, 90 | agent-suite x 2 |
| onyx-dot-app/onyx | 2 | 68, 108 | agent-suite x 1 + system-prompt x 1 |
| cinnamon/kotaemon | 2 | 101, 137 | agent-suite x 1 + system-prompt x 1 |
| filip-michalsky/salesgpt | 2 | 100, 111 | agent-suite x 1 + system-prompt x 1 |

## 6. Domain coverage (heuristic)

| Domain | agent-suite | system-prompt | skill | tool-schema | Total |
|---|---:|---:|---:|---:|---:|
| General/Other | 9 | 5 | 11 | 5 | **30** |
| Research/Data/Knowledge | 8 | 9 | 3 | 2 | **22** |
| Finance/Investment | 5 | 5 | 4 | 5 | **19** |
| Search/Knowledge | 2 | 2 | 0 | 10 | **14** |
| Productivity/Collaboration | 4 | 2 | 1 | 7 | **14** |
| Media/Writing | 3 | 2 | 2 | 4 | **11** |
| Personal Assistant/General | 6 | 2 | 1 | 0 | **9** |
| Marketing | 2 | 2 | 4 | 0 | **8** |
| Support/Sales | 4 | 3 | 0 | 1 | **8** |
| Multilingual/Translation | 1 | 3 | 1 | 3 | **8** |
| Design/Presentation | 0 | 1 | 6 | 0 | **7** |
| Education/Academic | 0 | 3 | 4 | 0 | **7** |
| Healthcare | 1 | 2 | 1 | 2 | **6** |
| Media/Entertainment | 1 | 0 | 1 | 3 | **5** |
| HR/Recruiting | 0 | 2 | 3 | 0 | **5** |
| Product Management | 0 | 3 | 1 | 0 | **4** |
| Legal | 0 | 1 | 3 | 0 | **4** |
| Sports/Fitness | 1 | 1 | 0 | 2 | **4** |
| Travel | 1 | 1 | 2 | 0 | **4** |
| E-commerce | 1 | 1 | 1 | 1 | **4** |
| Weather | 0 | 0 | 0 | 3 | **3** |
| Music | 0 | 0 | 0 | 2 | **2** |
| Real Estate | 1 | 0 | 1 | 0 | **2** |

## 7. Metadata completeness

| Check | Missing | Detail |
|---|---:|---|
| Missing ## Metadata block | 0 | - |
| Missing Collection Method | 0 | - |
| Missing License | 0 | - |
| Missing Collection Date | 0 | - |

## 8. ID numbering

- ID range **TC-001 - TC-246**: 200 IDs used, 46 numbers unused in the range (from earlier restructuring that merged/removed duplicate projects).
- agent-suite range: TC-004-TC-107; single-artifact range: TC-001-TC-246.

---

## Appendix: case details

### Appendix A. agent-suite (50 cases)

| ID | Source project | License | Collected | Chars | Domain (heuristic) |
|---|---|---|---|---:|---|
| TC-004 | gpt-researcher | Apache-2.0 | 2026-10-10 | 14,070 | Research/Data/Knowledge |
| TC-005 | OpenClaw | MIT | 2026-10-10 | 10,687 | Productivity/Collaboration |
| TC-006 | agency-agents | MIT | 2026-10-10 | 24,761 | Marketing |
| TC-031 | HKUDS/nanobot | MIT | 2026-10-12 | 21,291 | General/Other |
| TC-032 | NousResearch/hermes-agent | MIT | 2026-10-12 | 17,299 | Research/Data/Knowledge |
| TC-033 | the-open-agent/openagent | Apache-2.0 | 2026-10-12 | 18,222 | General/Other |
| TC-034 | mem0ai/mem0 | Apache-2.0 | 2026-10-12 | 12,886 | Personal Assistant/General |
| TC-035 | AutoGPT Classic | MIT | 2026-10-12 | 8,298 | General/Other |
| TC-036 | OpenManus | MIT | 2026-10-12 | 7,755 | General/Other |
| TC-037 | BabyAGI | MIT | 2026-10-12 | 9,516 | Productivity/Collaboration |
| TC-038 | AnythingLLM Agent | MIT | 2026-10-12 | 10,931 | Research/Data/Knowledge |
| TC-039 | WrenAI | Apache+AGPL(mixed) | 2026-10-12 | 8,889 | Research/Data/Knowledge |
| TC-040 | Leon | MIT | 2026-10-12 | 4,836 | Personal Assistant/General |
| TC-041 | Buzz | Apache-2.0 | 2026-10-12 | 9,164 | General/Other |
| TC-042 | OpenAmer | Apache-2.0(+commercial) | 2026-10-12 | 11,338 | General/Other |
| TC-055 | zubair-trabzada/ai-marketing-claude | MIT | 2026-10-13 | 17,804 | Marketing |
| TC-056 | AgriciDaniel/claude-blog | MIT | 2026-10-13 | 17,550 | Media/Writing |
| TC-057 | jimliu/baoyu-skills | MIT | 2026-10-13 | 12,988 | General/Other |
| TC-058 | i18n-agent/i18nstack | MIT | 2026-10-13 | 13,983 | Multilingual/Translation |
| TC-059 | dongbeixiaohuo/writing-agent | MIT | 2026-10-13 | 12,603 | Media/Writing |
| TC-060 | CowAgent | MIT | 2026-10-13 | 14,818 | Personal Assistant/General |
| TC-061 | homebot | MIT | 2026-10-13 | 13,175 | Personal Assistant/General |
| TC-062 | smartflat-ai | MIT | 2026-10-13 | 11,376 | Real Estate |
| TC-063 | claude-gym-coach | MIT | 2026-10-13 | 16,094 | Sports/Fitness |
| TC-064 | anthropics/anthropic-quickstarts | MIT | 2026-10-13 | 12,756 | Finance/Investment |
| TC-065 | microsoft/UFO | MIT | 2026-10-13 | 16,919 | Productivity/Collaboration |
| TC-066 | AI4Finance-Foundation/FinRobot | Apache-2.0 | 2026-10-13 | 14,912 | Finance/Investment |
| TC-067 | chatwoot/chatwoot | MIT | 2026-10-13 | 15,898 | Support/Sales |
| TC-068 | Onyx | MIT | 2026-10-13 | 9,649 | Research/Data/Knowledge |
| TC-069 | AgentFactory Business Plugins | Apache-2.0 | 2026-10-13 | 18,359 | Productivity/Collaboration |
| TC-070 | claude-skills | MIT | 2026-10-13 | 18,599 | Search/Knowledge |
| TC-071 | Fabric | MIT | 2026-10-13 | 14,853 | Search/Knowledge |
| TC-084 | TauricResearch/TradingAgents | MIT+Apache-2.0 | 2026-10-13 | 29,774 | Finance/Investment |
| TC-090 | AI4Finance-Foundation/FinRobot | Apache-2.0 | 2026-10-13 | 15,230 | Finance/Investment |
| TC-091 | X-PLUG/MobileAgent | MIT | 2026-10-13 | 15,310 | Personal Assistant/General |
| TC-092 | openai/openai-cs-agents-demo | MIT | 2026-10-13 | 20,957 | Support/Sales |
| TC-094 | ai-hedge-fund | MIT | 2026-10-13 | 16,806 | Finance/Investment |
| TC-095 | customer-service-ai-agent | Apache-2.0 | 2026-10-13 | 13,730 | Support/Sales |
| TC-096 | Multi-Agent-Medical-Assistant | Apache-2.0 | 2026-10-13 | 13,918 | Healthcare |
| TC-097 | Lavern | Apache-2.0 | 2026-10-13 | 15,232 | General/Other |
| TC-098 | travel-planner | MIT | 2026-10-13 | 10,995 | Travel |
| TC-099 | e-commerce-agents | MIT | 2026-10-13 | 14,044 | E-commerce |
| TC-100 | SalesGPT | MIT | 2026-10-13 | 10,940 | Support/Sales |
| TC-101 | kotaemon | Apache-2.0 | 2026-10-13 | 8,285 | Research/Data/Knowledge |
| TC-102 | Vane | MIT | 2026-10-13 | 8,646 | Media/Writing |
| TC-103 | Morphic | Apache-2.0 | 2026-10-13 | 7,656 | Research/Data/Knowledge |
| TC-104 | XAgent | Apache-2.0 | 2026-10-13 | 8,703 | General/Other |
| TC-105 | Open Notebook | MIT | 2026-10-13 | 9,792 | Media/Entertainment |
| TC-106 | PrivateGPT | Apache-2.0 | 2026-10-13 | 7,976 | Research/Data/Knowledge |
| TC-107 | Chat UI | Apache-2.0 | 2026-10-13 | 9,192 | Personal Assistant/General |

### Appendix B. system-prompt (50 cases)

| ID | Source project | License | Collected | Chars | Domain (heuristic) |
|---|---|---|---|---:|---|
| TC-001 | gpt-researcher | Apache-2.0 | 2026-10-10 | 5,846 | Research/Data/Knowledge |
| TC-018 | browser-use/browser-use | MIT | 2026-10-12 | 8,433 | Personal Assistant/General |
| TC-019 | dzhng/deep-research | MIT | 2026-10-12 | 3,248 | Research/Data/Knowledge |
| TC-044 | stanford-oval/storm | MIT | 2026-10-13 | 7,902 | Research/Data/Knowledge |
| TC-045 | presenton/presenton | Apache-2.0 | 2026-10-13 | 14,264 | Design/Presentation |
| TC-046 | mshumer/gpt-author | MIT | 2026-10-13 | 10,156 | Media/Writing |
| TC-048 | chuckmy/agentic-translator | MIT | 2026-10-13 | 17,844 | Multilingual/Translation |
| TC-051 | microsoft/JARVIS | MIT | 2026-10-13 | 9,390 | Personal Assistant/General |
| TC-052 | gymcoach-app/gymcoach | MIT | 2026-10-13 | 15,609 | Sports/Fitness |
| TC-072 | danielmiessler/fabric | MIT | 2026-10-13 | 4,691 | General/Other |
| TC-073 | danielmiessler/fabric | MIT | 2026-10-13 | 4,232 | General/Other |
| TC-074 | danielmiessler/fabric | MIT | 2026-10-13 | 6,549 | General/Other |
| TC-075 | danielmiessler/fabric | MIT | 2026-10-13 | 5,135 | Product Management |
| TC-076 | danielmiessler/fabric | MIT | 2026-10-13 | 3,703 | Media/Writing |
| TC-077 | danielmiessler/fabric | MIT | 2026-10-13 | 9,547 | Education/Academic |
| TC-078 | alirezarezvani/claude-skills | MIT | 2026-10-13 | 8,970 | Finance/Investment |
| TC-079 | alirezarezvani/claude-skills | MIT | 2026-10-13 | 20,098 | General/Other |
| TC-080 | alirezarezvani/claude-skills | MIT | 2026-10-13 | 6,769 | Marketing |
| TC-082 | alirezarezvani/claude-skills | MIT | 2026-10-13 | 35,771 | Product Management |
| TC-083 | alirezarezvani/claude-skills | MIT | 2026-10-13 | 16,844 | Marketing |
| TC-108 | Onyx | MIT | 2026-10-13 | 7,577 | Research/Data/Knowledge |
| TC-109 | AnythingLLM | MIT | 2026-10-13 | 5,675 | Research/Data/Knowledge |
| TC-110 | Paperless-AI | MIT | 2026-10-13 | 6,403 | Education/Academic |
| TC-111 | SalesGPT | MIT | 2026-10-13 | 7,505 | Support/Sales |
| TC-112 | Vane | MIT | 2026-10-13 | 9,309 | Search/Knowledge |
| TC-113 | linq-team/linq-resy-agent | MIT | 2026-10-14 | 10,543 | Productivity/Collaboration |
| TC-114 | vas3k/TaxHacker | MIT | 2026-10-14 | 8,625 | Finance/Investment |
| TC-115 | Nutlope/notesGPT | MIT | 2026-10-14 | 7,438 | General/Other |
| TC-116 | Shubhamsaboo/awesome-llm-apps | Apache-2.0 | 2026-10-14 | 13,875 | Finance/Investment |
| TC-117 | anthropics/financial-services | Apache-2.0 | 2026-10-14 | 11,552 | Finance/Investment |
| TC-118 | interviewstreet/hiring-agent | MIT | 2026-10-13 | 13,991 | HR/Recruiting |
| TC-119 | anthropics/commerce-agents | Apache-2.0 | 2026-10-13 | 12,504 | E-commerce |
| TC-120 | cskwork/ai-law-counsel | MIT | 2026-10-13 | 8,150 | Legal |
| TC-121 | Azure-Samples/azure-ai-travel-agents | MIT | 2026-10-13 | 6,281 | Travel |
| TC-122 | DiogoSoares3/healthcare-report-agent | MIT | 2026-10-13 | 8,304 | Healthcare |
| TC-123 | LosaLosSantos/aurelio-finance | MIT | 2026-10-13 | 7,662 | Finance/Investment |
| TC-124 | Azure-Samples/azure-search-openai-demo | MIT | 2026-10-13 | 6,500 | Search/Knowledge |
| TC-125 | plastic-labs/tutor-gpt | GPL-3.0 | 2026-10-13 | 7,926 | Education/Academic |
| TC-126 | zeyangxu/ai-email-agent | MIT | 2026-10-13 | 6,014 | Product Management |
| TC-127 | vennelchenfoo/slack-it-rag-agent | MIT | 2026-10-13 | 4,622 | Support/Sales |
| TC-128 | vanna-ai/vanna | MIT | 2026-10-13 | 11,274 | Research/Data/Knowledge |
| TC-129 | Dataherald/dataherald | Apache-2.0 | 2026-10-13 | 15,614 | Multilingual/Translation |
| TC-130 | zylon-ai/private-gpt | Apache-2.0 | 2026-10-13 | 8,123 | Research/Data/Knowledge |
| TC-131 | khoj-ai/khoj | AGPL-3.0 | 2026-10-13 | 7,599 | Productivity/Collaboration |
| TC-132 | srbhr/Resume-Matcher | Apache-2.0 | 2026-10-13 | 6,724 | HR/Recruiting |
| TC-133 | hay-kot/mealie | AGPL-3.0 | 2026-10-13 | 6,054 | Healthcare |
| TC-134 | infiniflow/ragflow | Apache-2.0 | 2026-10-13 | 4,620 | Multilingual/Translation |
| TC-135 | leptonai/search_with_lepton | Apache-2.0 | 2026-10-13 | 7,158 | Research/Data/Knowledge |
| TC-136 | twentyhq/twenty | AGPL-3.0 | 2026-10-13 | 6,649 | Support/Sales |
| TC-137 | Cinnamon/kotaemon | Apache-2.0 | 2026-10-13 | 5,397 | Research/Data/Knowledge |

### Appendix C. skill (50 cases)

| ID | Source project | License | Collected | Chars | Domain (heuristic) |
|---|---|---|---|---:|---|
| TC-002 | anthropics/skills | Proprietary | 2026-10-10 | 10,606 | General/Other |
| TC-047 | hikanner/jta | MIT | 2026-10-13 | 12,698 | Multilingual/Translation |
| TC-049 | Akxan/ppt-agent-skill | MIT | 2026-10-13 | 17,603 | Design/Presentation |
| TC-053 | julianStreibel/crib | MIT | 2026-10-13 | 9,820 | Personal Assistant/General |
| TC-054 | Azure-Samples/foundry-hosted-agents-workshop | MIT | 2026-10-13 | 8,258 | Travel |
| TC-081 | alirezarezvani/claude-skills | MIT | 2026-10-13 | 17,821 | Legal |
| TC-138 | coreyhaines31/marketingskills | MIT | 2026-10-13 | 23,355 | Marketing |
| TC-139 | claude-office-skills/skills | MIT | 2026-10-13 | 13,945 | HR/Recruiting |
| TC-140 | coffeefuelbump/csv-data-summarizer-claude-skill | MIT | 2026-10-13 | 9,443 | Research/Data/Knowledge |
| TC-141 | tasteray/skills | MIT | 2026-10-13 | 21,942 | General/Other |
| TC-142 | ZeroPointRepo/youtube-skills | MIT | 2026-10-13 | 16,212 | Media/Entertainment |
| TC-143 | Upload-Post/upload-post-skill | MIT | 2026-10-13 | 11,470 | Productivity/Collaboration |
| TC-144 | shepsci/kaggle-skill | MIT | 2026-10-13 | 14,426 | Education/Academic |
| TC-145 | oil-oil/oiloil-ui-ux-guide | Apache-2.0 | 2026-10-13 | 16,071 | Design/Presentation |
| TC-146 | Ericyoung-183/alpha-insights | MIT | 2026-10-13 | 67,392 | General/Other |
| TC-147 | ryanbbrown/revealjs-skill | MIT | 2026-10-13 | 23,124 | Design/Presentation |
| TC-148 | takechanman1228/claude-persona | MIT | 2026-10-13 | 34,871 | General/Other |
| TC-149 | evolsb/claude-legal-skill | MIT | 2026-10-13 | 18,943 | Legal |
| TC-150 | takechanman1228/claude-ecom | MIT | 2026-10-13 | 12,160 | E-commerce |
| TC-151 | blader/humanizer | MIT | 2026-10-13 | 36,726 | Media/Writing |
| TC-152 | tuanductran/hr-skills | MIT | 2026-10-13 | 7,629 | HR/Recruiting |
| TC-153 | JoelLewis/finance_skills | MIT | 2026-10-13 | 14,552 | Finance/Investment |
| TC-154 | equalang/equalang-skill | Apache-2.0 | 2026-10-13 | 10,230 | General/Other |
| TC-155 | humanpen/humanpen-skill | Apache-2.0 | 2026-10-13 | 9,541 | General/Other |
| TC-156 | superdesigndev/superdesign-skill | MIT | 2026-10-13 | 20,701 | Design/Presentation |
| TC-157 | eddiebelaval/squire | MIT | 2026-10-13 | 27,908 | Education/Academic |
| TC-158 | OpenClaudia/openclaudia-skills | MIT | 2026-10-13 | 11,208 | Finance/Investment |
| TC-159 | Weizhena/Deep-Research-skills | MIT | 2026-10-13 | 8,549 | Research/Data/Knowledge |
| TC-160 | phuryn/pm-skills | MIT | 2026-10-14 | 8,505 | Product Management |
| TC-161 | tradermonty/claude-trading-skills | MIT | 2026-10-14 | 11,140 | Finance/Investment |
| TC-162 | sergebulaev/linkedin-skills | MIT | 2026-10-14 | 18,338 | Marketing |
| TC-163 | kaankiziltug/logo-design-skill | MIT | 2026-10-14 | 21,267 | Design/Presentation |
| TC-164 | YANZHANLIN/ielts-claude-skills | MIT | 2026-10-14 | 8,110 | Education/Academic |
| TC-165 | jamditis/claude-skills-journalism | MIT | 2026-10-14 | 14,787 | Media/Writing |
| TC-166 | w95/awesome-claude-corporate-skills | MIT | 2026-10-14 | 15,752 | General/Other |
| TC-167 | career-ops-hq/career-ops | MIT | 2026-10-14 | 18,149 | HR/Recruiting |
| TC-168 | cathrynlavery/diagram-design | MIT | 2026-10-14 | 34,372 | Design/Presentation |
| TC-169 | K-Dense-AI/scientific-agent-skills | MIT | 2026-10-14 | 31,461 | General/Other |
| TC-170 | OneWave-AI/claude-skills | MIT | 2026-10-14 | 5,597 | General/Other |
| TC-171 | wondelai/skills | MIT | 2026-10-14 | 23,627 | General/Other |
| TC-172 | shawnpang/startup-founder-skills | MIT | 2026-10-14 | 11,313 | Marketing |
| TC-173 | jezweb/claude-skills | MIT | 2026-10-14 | 13,097 | General/Other |
| TC-174 | zubair-trabzada/ai-realestate-claude | MIT | 2026-10-14 | 22,634 | Real Estate |
| TC-175 | apiotrowski-afk/commercial-legal-pl | Apache-2.0 | 2026-10-14 | 21,017 | Legal |
| TC-176 | flysheep-ai/education-skills | MIT | 2026-10-14 | 8,569 | Education/Academic |
| TC-177 | AlpacaLabsLLC/skills-for-architects | MIT | 2026-10-14 | 8,974 | Research/Data/Knowledge |
| TC-178 | mohitagw15856/pm-claude-skills | MIT | 2026-10-14 | 9,292 | Healthcare |
| TC-179 | borski/travel-hacking-toolkit | MIT | 2026-10-14 | 12,567 | Travel |
| TC-180 | agiprolabs/claude-trading-skills | MIT | 2026-10-14 | 14,576 | Finance/Investment |
| TC-181 | appeeky/aso-skills | MIT | 2026-10-14 | 9,623 | Marketing |

### Appendix D. tool-schema (50 cases)

| ID | Source project | License | Collected | Chars | Domain (heuristic) |
|---|---|---|---|---:|---|
| TC-003 | - | Undeclared | - | 7,117 | General/Other |
| TC-050 | danny-avila/LibreChat | MIT | 2026-10-13 | 17,579 | General/Other |
| TC-182 | brave/brave-search-mcp-server | MIT | 2026-10-13 | 11,885 | Search/Knowledge |
| TC-183 | modelcontextprotocol/servers-archived | MIT | 2026-10-13 | 8,364 | Search/Knowledge |
| TC-184 | modelcontextprotocol/servers-archived | MIT | 2026-10-13 | 8,859 | Productivity/Collaboration |
| TC-185 | modelcontextprotocol/servers | MIT+Apache-2.0 | 2026-10-13 | 12,112 | Research/Data/Knowledge |
| TC-186 | modelcontextprotocol/servers | MIT+Apache-2.0 | 2026-10-13 | 7,043 | Productivity/Collaboration |
| TC-187 | modelcontextprotocol/servers | MIT+Apache-2.0 | 2026-10-13 | 6,050 | General/Other |
| TC-188 | financial-datasets/mcp-server | MIT | 2026-10-13 | 9,086 | Finance/Investment |
| TC-189 | mschneider82/mcp-openweather | MIT | 2026-10-13 | 5,060 | Weather |
| TC-190 | modelcontextprotocol/servers-archived | MIT | 2026-10-13 | 5,548 | Search/Knowledge |
| TC-191 | GeLi2001/shopify-mcp | MIT | 2026-10-13 | 6,482 | E-commerce |
| TC-192 | varunneal/spotify-mcp | MIT | 2026-10-13 | 6,310 | Music |
| TC-193 | nickclyde/duckduckgo-mcp-server | MIT | 2026-10-13 | 6,652 | Search/Knowledge |
| TC-194 | openbnb-org/mcp-server-airbnb | MIT | 2026-10-13 | 7,004 | Search/Knowledge |
| TC-195 | kimtaeyoon83/mcp-server-youtube-transcript | MIT | 2026-10-13 | 6,428 | Media/Entertainment |
| TC-196 | Rudra-ravi/wikipedia-mcp | MIT | 2026-10-13 | 7,913 | Media/Writing |
| TC-197 | abhiz123/todoist-mcp-server | MIT | 2026-10-13 | 5,713 | Multilingual/Translation |
| TC-198 | r-huijts/strava-mcp | MIT | 2026-10-13 | 6,045 | Sports/Fitness |
| TC-199 | KyrieTangSheng/mcp-server-nationalparks | MIT | 2026-10-13 | 5,485 | Support/Sales |
| TC-200 | truss44/mcp-crypto-price | MIT | 2026-10-13 | 5,876 | Finance/Investment |
| TC-201 | traves-theberge/mealdb-mcp | MIT | 2026-10-13 | 5,566 | Healthcare |
| TC-202 | exa-labs/exa-mcp-server | MIT | 2026-10-14 | 10,648 | Search/Knowledge |
| TC-205 | domdomegg/airtable-mcp-server | MIT | 2026-10-14 | 7,156 | Productivity/Collaboration |
| TC-206 | cmer81/open-meteo-mcp | MIT | 2026-10-14 | 9,432 | Weather |
| TC-207 | yuna0x0/hackmd-mcp | MIT | 2026-10-14 | 10,359 | Productivity/Collaboration |
| TC-208 | QuantGeekDev/coincap-mcp | MIT | 2026-10-14 | 7,856 | Finance/Investment |
| TC-209 | nspady/google-calendar-mcp | MIT | 2026-10-14 | 10,111 | Productivity/Collaboration |
| TC-210 | GongRzhe/Office-Word-MCP-Server | MIT | 2026-10-14 | 7,814 | Productivity/Collaboration |
| TC-213 | firecrawl/firecrawl-mcp-server | MIT | 2026-10-14 | 13,326 | Search/Knowledge |
| TC-214 | elevenlabs/elevenlabs-mcp | MIT | 2026-10-14 | 10,076 | General/Other |
| TC-223 | DeepL/deepl-mcp-server | MIT | 2026-10-14 | 8,033 | Multilingual/Translation |
| TC-228 | tavily-ai/tavily-mcp | MIT | 2026-10-14 | 10,238 | Search/Knowledge |
| TC-229 | MarkusPfundstein/mcp-obsidian | MIT | 2026-10-14 | 7,823 | Productivity/Collaboration |
| TC-230 | 8enSmith/mcp-open-library | MIT | 2026-10-13 | 7,688 | Search/Knowledge |
| TC-231 | isdaniel/mcp_weather_server | Apache-2.0 | 2026-10-13 | 7,896 | Weather |
| TC-232 | ChanMeng666/server-google-news | MIT | 2026-10-13 | 6,214 | Media/Writing |
| TC-233 | r-huijts/rijksmuseum-mcp | MIT | 2026-10-13 | 12,245 | General/Other |
| TC-234 | berlinbra/alpha-vantage-mcp | MIT | 2026-10-13 | 11,735 | Finance/Investment |
| TC-235 | rianvdm/lastfm-mcp | MIT | 2026-10-13 | 9,263 | Music |
| TC-236 | damoqiongqiu/mcp-local-translate | MIT | 2026-10-13 | 7,518 | Multilingual/Translation |
| TC-237 | Grinv/tmdb-mcp | MIT | 2026-10-13 | 10,145 | Media/Entertainment |
| TC-238 | guangxiangdebizi/news-mcp | Apache-2.0 | 2026-10-14 | 5,912 | Media/Writing |
| TC-239 | veithly/rss-mcp | Apache-2.0 | 2026-10-14 | 6,192 | Media/Writing |
| TC-241 | drakonkat/wizzy-mcp-tmdb | MIT | 2026-10-14 | 8,799 | Media/Entertainment |
| TC-242 | anirbanbasu/frankfurtermcp | MIT | 2026-10-14 | 8,924 | Finance/Investment |
| TC-243 | cyanheads/sports-mcp-server | Apache-2.0 | 2026-10-14 | 10,276 | Sports/Fitness |
| TC-244 | jdamcd/gtfs-mcp | MIT | 2026-10-14 | 6,688 | Research/Data/Knowledge |
| TC-245 | cyanheads/nominatim-mcp-server | Apache-2.0 | 2026-10-14 | 15,464 | Search/Knowledge |
| TC-246 | cyanheads/cdc-health-mcp-server | Apache-2.0 | 2026-10-13 | 20,979 | Healthcare |

*SanityOps Evaluation Test Case Statistics - auto-generated*
