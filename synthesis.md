# Research synthesis by topic

Findings from 6 reports, regrouped by theme:

- US healthcare data infrastructure: gaps and opportunities in claims clearinghouses, EDI, EHR interoperability and prior authorization
- Unsolved Technical Problems in US Healthcare IT Infrastructure
- US Healthcare Interoperability Vendors and Funding Landscape
- Documented failures and unsolved problems in healthcare AI
- LLMs and AI for medical terminology mapping and normalization
- FDA real-world performance monitoring and drift detection for AI-enabled medical devices (Sept 2025 Digital Health Center of Excellence RFI, PCCP guidance, postmarket surveillance)

## FHIR-based interoperability and TEFCA implementation

FHIR-based interoperability is being driven by federal rulemaking that requires payers to expose standardized APIs, while TEFCA provides a nationwide trust framework enabling QHINs to exchange clinical data using those same FHIR standards. Together, these initiatives aim to replace fragmented clearinghouse/EDI workflows with real‑time, patient‑centric data access, though adoption remains uneven and many organizations report readiness gaps.

**CMS’s Interoperability and Prior Authorization Final Rule (CMS‑0057‑F) requires impacted payers to implement four FHIR‑based APIs—Patient Access, Provider Access, Payer‑to‑Payer, and Prior Authorization—with compliance mandated by January 1, 2027.**  
This rule moves prior authorization and data sharing from legacy EDI transactions to modern, RESTful FHIR interfaces, aligning with broader interoperability goals.  
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**TEFCA’s foundational documents—the Common Agreement, Trusted Exchange Framework, and QHIN Technical Framework—were first published in January 2022 and updated in November 2023, defining six permissible exchange purposes and specifying technical components such as patient identity resolution, authentication, and performance measurement.**  
These documents establish the legal and technical baseline for QHINs to participate in trusted nationwide exchange.  
- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

**The first Qualified Health Information Networks (QHINs) were designated in December 2023, with health data flowing among them within days; by November 2025 eleven QHINs were active, supporting over 71,000 participating sites or organizations.**  
Rapid designation and growth illustrate TEFCA’s scaling capacity, yet the sheer number of participants highlights the challenge of ensuring uniform FHIR implementation across diverse entities.  
- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)
- Evidence: [Oracle Health designated QHIN under TEFCA data sharing ...](https://www.healthcaredive.com/news/oracle-health-qhin-designation-tefca/806217/)
- Evidence: [The History & Growth of TEFCA® - ONC](https://healthit.gov/resources/data-liquidity-affordability-and-access-the-history-growth-of-tefca/)

**TEFCA enables a single IAL2 identity verification for patients to access records from multiple facilities via QHINs, and the Provider Directory API mandated by CMS‑0057‑F supplies a standardized lookup of participating organizations.**  
This combination reduces identity‑matching friction and gives providers a reliable directory to discover exchange partners, reinforcing the FHIR‑based data flow envisioned by both initiatives.  
- Evidence: [Network - Flexpa Docs](https://www.flexpa.com/docs/network)
- Evidence: [Understanding the Provider Directory API: Requirements, ...](https://fire.ly/blog/understanding-the-provider-directory-api/)

**Hospital awareness of TEFCA rose from 51% in 2022 to over 60% in 2023, with a majority planning to participate, yet many payers and providers report being unprepared for interoperability, citing challenges such as determining a cohesive enterprise strategy and digitizing prior authorization policies.**  
While awareness is growing, the persistence of readiness gaps suggests that simply having APIs or QHIN designations is insufficient without organizational investment in workflow integration and change management.  
- Evidence: [TEFCA Awareness and Planned Participation Among U.S. ...](https://www.ncbi.nlm.nih.gov/books/NBK606030/)
- Evidence: [Many payers, providers unprepared for interoperability and ...](https://www.healthcarefinancenews.com/news/many-payers-providers-unprepared-interoperability-and-prior-authorization-rule-wedi-finds)

**The TEFCA policy page on HealthIT.gov was last updated on July 28, 2026, indicating ongoing maintenance and recent activity related to the framework.**  
Regular updates reflect continuous refinement of the Common Agreement and technical guidance as more QHINs join and exchange volumes increase.  
- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

## Prior authorization automation and clearinghouse functions

Clearinghouses play a central role in U.S. healthcare data infrastructure by converting provider claims into standardized EDI formats, validating them against ANSI X12 standards, and performing automated claim scrubbing to catch errors before submission. They also support prior authorization by processing eligibility and authorization transactions alongside claims, flagging missing authorizations to reduce denials. Recent federal policy, market growth, and AI innovation are reshaping these functions, pushing payers toward FHIR‑based APIs and intelligent automation to cut administrative burden, accelerate decisions, and realize significant cost savings.

**Clearinghouses convert provider‑generated claims into EDI 837 format, validate against ANSI X12 standards, and perform automated claim scrubbing to detect errors before submission.**  
This includes checking for missing patient/insurance data, mismatched ICD‑10 or CPT codes, payer‑specific rule violations, and NPI mismatches, flagging issues for correction. By performing these functions, clearinghouses reduce claim denials and improve transmission efficiency.  
- Evidence: [How Medical Billing Clearinghouses Work? Best Guide](https://www.medibillrcm.com/blog/how-medical-billing-clearinghouses-work/)

**Clearinghouses also support prior authorization by processing eligibility and authorization transactions alongside claims and performing pre‑submission checks for missing authorizations to reduce denials due to lack of prior approval.**  
This integration allows providers to verify that required authorizations are present before claim submission, decreasing the likelihood of payer denials and associated rework. It demonstrates how clearinghouse functions extend beyond basic claims processing to prior auth workflows.  
- Evidence: [EDI Clearinghouse | Healthcare Solutions](https://www.availity.com/clearinghouse-and-trading-partner-network/)

**The CMS Interoperability and Prior Authorization Final Rule (CMS‑0057‑F), issued January 17, 2024, requires impacted payers to implement and maintain four FHIR‑based APIs (Patient Access, Provider Access, Payer‑to‑Payer, Prior Authorization) with compliance generally required by January 1, 2027.**  
The rule applies to Medicare Advantage, Medicaid, CHIP, and QHP issuers on the Federally Facilitated Exchanges, aiming to standardize data exchange and reduce administrative burden associated with prior authorization. Compliance timelines give payers several years to upgrade their systems.  
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**Starting in 2026, impacted payers must send prior‑authorization decisions within 72 hours for expedited requests and within seven calendar days for standard requests, and must provide a specific reason for denials regardless of transmission method.**  
These timelines are designed to reduce delays that can postpone diagnoses and interrupt treatment, addressing a key pain point reported by providers. The requirement for a specific denial reason improves transparency and enables providers to address issues more effectively.  
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**CMS estimates that the Interoperability and Prior Authorization Final Rule will generate at least $16 billion in savings over ten years by reducing manual prior‑authorization processes and associated provider burden.**  
The projected savings stem from decreased administrative costs, faster decision‑making, and reduced need for costly manual follow‑up on denials. This economic incentive underscores the policy’s potential to drive widespread adoption of electronic prior auth solutions.  
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**The AI prior authorization automation market was valued at USD 1.47 billion in 2025 and is projected to reach USD 10.31 billion by 2035, reflecting a compound annual growth rate (CAGR) of 21.5 %.**  
This rapid growth reflects increasing investment in AI‑driven solutions that automate manual prior auth workflows, integrate with FHIR standards, and aim to deliver real‑time approvals. The market expansion signals a shift away from legacy EDI‑centric approaches toward intelligent automation.  
- Evidence: [AI Prior Authorization Automation Market](https://evolvancemarketresearch.com/reports/ai-prior-authorization-automation-market/)

## Patient identity matching and EMPI solutions

Reports show that patient identity matching and enterprise master patient index (EMPI) solutions are critical for enabling nationwide data exchange, with vendors like Verato recognized as market leaders and the EMPI software market poised for strong growth, while TEFCA readiness requires resolving identity inconsistencies before organizations can participate.

**Verato has been named the #1 vendor in Enterprise Patient Identity, EMPI, and Patient Matching for Revenue Cycle Management in Black Book Research’s 2026 report.**  
The ranking reflects health‑industry assessments of Verato’s ability to solve duplicate record problems and improve revenue‑cycle efficiency. It underscores the growing reliance on specialized EMPI tools to support accurate patient identification across disparate systems.  

**Health system clients rated Verato #1 in Enterprise Patient Identity, EMPI, and Patient Matching in a June 2026 survey.**  
The survey feedback comes directly from provider organizations that use Verato’s platform for record linkage and deduplication. High ratings indicate strong satisfaction with the vendor’s matching accuracy and workflow integration.  
- Evidence: [Health System Clients Rate Verato #1 in Enterprise Patient ...](https://www.newswire.com/news/health-system-clients-rate-verato-1-in-enterprise-patient-identity-empi-and)

**In a case study, Verato resolved more than 3 million backlog tasks, automatically cleared 41% of same‑source duplicates and supplied supporting data for another 36%, delivering value to 77% of high‑priority identity tasks and cutting determination time by 80% for nearly half of duplicate tasks.**  
These metrics demonstrate the scalability and efficiency of Verato’s EMPI capabilities when applied to large legacy datasets. The reduction in manual review time translates into faster patient‑record availability for clinical and billing operations.  
- Evidence: [Moving beyond NextGate®: Unifying patient identity with ...](https://verato.com/resources/moving-beyond-nextgate/)

**The master patient index software market is expected to grow from US$1.54 billion in 2025 to US$3.90 billion by 2034.**  
This near‑tripling of market size reflects rising demand for robust patient‑matching infrastructure as health systems pursue interoperability and value‑based care. Vendors are investing in AI‑enhanced matching algorithms to capture this expansion.  
- Evidence: [Master Patient Index Software Market Size, Share and ...](https://www.theinsightpartners.com/reports/master-patient-index-software-market)

**Before joining TEFCA, organizations must address patient identity problems, standardize clinical terminologies, and deploy FHIR APIs.**  
The prerequisite ensures that record linkage across QHINs is reliable and that exchanged data can be interpreted correctly. Failure to resolve identity mismatches leads to record linkage failures and compromises the safety and privacy of health information exchange.  
- Evidence: [2026 Healthcare Interoperability Report](https://www.trovehealth.io/insights/?post=trusted-exchange-framework-statistics-2026)

## AI challenges: bias, governance, and real-world performance monitoring

The reports collectively show that AI in healthcare faces persistent bias risks, governance gaps that let flawed models reach patients, and significant obstacles to monitoring real‑world performance due to interoperability shortcomings and incomplete evidence reporting.

**Biased AI models can lead to misdiagnoses or overlooked conditions, particularly in underrepresented patient groups.**  
Peer‑reviewed studies note that when training data lack diversity, algorithms produce skewed outcomes that compromise diagnostic accuracy for minority populations. This risk is amplified when models are deployed without adequate bias testing.  
- Evidence: [Artificial intelligence in healthcare delivery: Prospects and ...](https://www.sciencedirect.com/science/article/pii/S2949916X24000616)

**Governance failures have allowed biased AI systems to reach clinical deployment.**  
Analyses of AI bias incidents point to insufficient oversight, missing validation protocols, and inadequate regulatory checks that let problematic models enter use. Such gaps undermine patient safety and trust in AI tools.  
- Evidence: [Edition #3 AI bias: A hidden danger to patient safety](https://www.linkedin.com/pulse/edition-3-ai-bias-hidden-danger-patient-safety-ashraf-alsinglawi-silcf)

**Lack of interoperability between AI systems and existing health IT infrastructure hinders integration and complicates real‑world performance monitoring.**  
When AI tools cannot exchange data seamlessly with EHRs or other clinical systems, developers struggle to collect the real‑world data needed for drift detection and outcome assessment. This barrier also forces reliance on manual workarounds that increase error risk.  
- Evidence: [Overcoming Barriers to Artificial Intelligence Adoption in ...](https://www.preprints.org/manuscript/202603.0316)
- Evidence: [Evaluating AI-enabled Medical Device Performance in ...](https://www.fda.gov/medical-devices/digital-health-center-excellence/request-public-comment-measuring-and-evaluating-artificial-intelligence-enabled-medical-device)

**The FDA’s September 30 2025 Request for Information seeks stakeholder input on measuring and evaluating AI‑enabled medical device performance in real‑world settings, with comments due by December 1 2025; as of the request date no public comments had been posted to the docket.**  
The RFI is part of the FDA’s effort to define standardized metrics for performance monitoring and drift detection, reflecting concerns that current postmarket surveillance lacks consistency. The absence of early comments indicates that stakeholder engagement is still underway.  
- Evidence: [Evaluating AI-enabled Medical Device Performance in ...](https://www.fda.gov/medical-devices/digital-health-center-excellence/request-public-comment-measuring-and-evaluating-artificial-intelligence-enabled-medical-device)
- Evidence: [Document (FDA-2025-N-4203-0001)](https://www.regulations.gov/document/FDA-2025-N-4203-0001)

**Nearly half of FDA‑approved AI/ML medical devices lacked a reported clinical study and over half omitted any performance metric, while demographic and socioeconomic data are consistently underreported, increasing algorithmic bias risk.**  
Incomplete evidence reporting makes it difficult to assess whether AI tools perform equitably across diverse populations. The gap in demographic data further obscures bias detection and hampers efforts to enforce fairness in AI‑enabled devices.  
- Evidence: [Evaluating transparency in AI/ML model characteristics for ...](https://www.nature.com/articles/s41746-025-02052-9)
- Evidence: [A scoping review of reporting gaps in FDA-approved AI ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11450195/)

## Medical terminology mapping and normalization (including LLM approaches)

Reports collectively show that medical terminology mapping and normalization remain pivotal for achieving semantic interoperability, with a growing market driven by the need for standardized coding, while LLM‑based methods demonstrate strong cross‑language performance but still struggle with exact code retrieval, highlighting the necessity of complementary strategies and ongoing standardization initiatives.

**The medical terminology software market was valued at USD 1.18 billion in 2023 and is projected to grow at a compound annual growth rate of 18.42% from 2024 to 2030.**  
This growth reflects increasing investment in tools that standardize clinical concepts across EHRs, billing systems, and research platforms, underscoring the economic incentive to solve terminology mapping challenges.  
- Evidence: [Medical Terminology Software Companies : Wolters Kluwer](https://www.maximizemarketresearch.com/competitive-analysis/medical-terminology-software-companies/260646/)

**The MAP‑CAR​E framework achieved an Acc@5 of 0.90 when translating procedure classification codes across English, German, French, and Italian.**  
Such high top‑5 accuracy indicates that LLMs can effectively capture semantic similarities between disparate terminologies, supporting multilingual mapping efforts that are essential for global data exchange.  
- Evidence: [LLM-augmented semantic embeddings enable Cross ...](https://www.nature.com/articles/s41598-025-34778-7)

**For exact medical code lookup (SNOMED CT, LOINC, or ICD) using LLMs with retrieval‑augmented generation, accuracy falls to 50–60% even when the correct code is present in the retrieval set.**  
This limitation reveals that while LLMs excel at semantic similarity, they still require robust validation or hybrid approaches to guarantee precise code assignment, a critical requirement for billing and clinical decision‑support.  
- Evidence: [LLMs and RAG for Medical Vocabulary Validation](https://papers.ssrn.com/sol3/Delivery.cfm/2e17a595-0ad3-4bb1-8970-c8ff41b5108f-MECA.pdf?abstractid=6545515&mirid=1)

**The Regenstrief Institute maintains LOINC and signed a collaboration agreement with SNOMED International on October 27 2022 to promote standardized terminology adoption.**  
This partnership aims to align two of the most widely used clinical terminologies, facilitating better mapping consistency and reducing the manual effort required for cross‑walks between systems.  
- Evidence: [New collaboration agreement between ...](https://www.snomed.org/news/new-collaboration-agreement-between-snomed-international-and-loinc%C2%AE-from-regenstrief)

**The ONC HTI‑1 Final Rule mandates FHIR R4 for all certified EHR systems, yet structural compliance does not ensure semantic interoperability because inconsistent mapping of SNOMED CT, LOINC, RxNorm, ICD‑10‑CM, and CPT can lead to clinically inaccurate data exchange.**  
Despite adherence to technical standards, divergent terminology mappings continue to cause clinically significant errors, indicating that further work on normalization and validation is essential to realize the full promise of FHIR‑based exchange.  
- Evidence: [How to Maximize Patient Care Through Interoperability](https://omnimd.com/blog/maximizing-patient-care-through-interoperability-in-healthcare-a-how-to-guide/)

## Contradictions and corrections
- The reports disagree on the number of Qualified Health Information Networks (QHINs) under TEFCA as of 2025: one source states that eleven data exchanges had received QHIN status by November 2025 (more than double the five initial QHINs designated in December 2023), while another source claims that only eight organizations had completed onboarding as inaugural QHINs by 2025 (listing eHealth Exchange, Epic Nexus, Health Gorilla, KONZA, MedAllies, CommonWell, Kno2, and eClinicalWorks). This discrepancy leaves unclear the actual count of QHINs operational during that period.

## Open questions
- What is the real‑world impact of TEFCA‑enabled QHIN exchanges on patient care outcomes, such as reductions in duplicate testing or improvements in care coordination?
- How effective are current patient identity matching solutions (e.g., Verato, NextGate) at reducing record linkage failures across QHIN‑to‑QHIN exchanges under varying data quality conditions?
- What are the actual implementation costs and resource burdens for small and rural providers to adopt FHIR‑based prior‑authorization APIs by the 2027 deadline, and how do these compare to projected savings?
- To what extent does the expansion of TEFCA’s permissible exchange purposes beyond the initial six address emerging use cases like social determinants of health data sharing or public health emergency reporting?
- What are the long‑term sustainability and funding models for QHINs after the initial federal support phases, and how might this affect continued participation?
- How do AI‑driven prior‑authorization tools perform in real‑world clinical settings regarding accuracy, bias, and provider satisfaction beyond market‑size projections?
- What specific gaps remain in semantic interoperability (e.g., consistent mapping of SNOMED CT, LOINC, RxNorm) despite structural FHIR R4 compliance, and how are they being measured or addressed?
