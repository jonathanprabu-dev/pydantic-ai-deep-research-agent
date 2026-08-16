# Research report: US healthcare data infrastructure: gaps and opportunities in claims clearinghouses, EDI, EHR interoperability and prior authorization

**Request:** US healthcare data infrastructure: gaps and opportunities in claims clearinghouses, EDI, EHR interoperability and prior authorization  
**Generated:** 2026-08-09 15:19 UTC

## Executive summary

US healthcare data infrastructure relies on clearinghouses to convert provider claims into standardized EDI 837/835 formats, perform pre‑submission validation, and support prior‑authorization checks. The CMS Interoperability and Prior Authorization Final Rule (CMS‑0057‑F), issued January 17 2024, mandates FHIR‑based APIs for impacted payers (Medicare Advantage, Medicaid, CHIP, QHP issuers) and introduces decision‑timeframes, denial‑transparency, and a MIPS electronic prior‑authorization measure, with staggered compliance dates (operational provisions effective 2026, API requirements generally by Jan 1 2027). Critics note that current clearinghouse/EDI solutions remain costly, fragmented, and have not eliminated prior‑authorization delays, imposing significant administrative burden on providers. Emerging opportunities include AI‑driven prior‑authorization automation, hyper‑automation of EHR workflows, and the integration of FHIR standards with AI to enable real‑time approvals, with the AI‑PA market projected to grow from $1.47 billion in 2025 to $10.31 billion by 2035. Together, regulatory mandates and technological advances aim to reduce administrative costs, improve claim‑submission efficiency, and generate substantial savings across the system.

## Mechanism and standards of claims clearinghouses, EDI, and prior authorization

Healthcare clearinghouses act as intermediaries that convert provider-generated claims into standardized EDI 837 format, validate them against X12 standards and payer-specific rules, and securely transmit them to payers. After adjudication, they receive EDI 835 remittance advice, facilitate payment posting, and offer denial management and analytics. Many clearinghouses also handle eligibility and authorization transactions, performing pre-submission checks for prior authorization requirements to reduce denials.

**Clearinghouses convert provider-generated claims into EDI 837 format and validate the structure against ANSI X12 standards before transmission to payers.**

Providers create claims in EHR or practice management systems; the clearinghouse translates the data into the standard electronic data interchange format (EDI 837 for professional claims, EDI 837I for institutional claims), validates that all required fields are present and correctly formatted, and ensures compliance with X12 standards so that payer systems can process the claim efficiently.

- Evidence: [How Medical Billing Clearinghouses Work? Best Guide](https://www.medibillrcm.com/blog/how-medical-billing-clearinghouses-work/)

**Clearinghouses perform automated claim scrubbing using rules engines to detect errors such as missing patient/insurance data, mismatched ICD-10 or CPT codes, payer-specific rule violations (e.g., LCD/NCD policies), and NPI mismatches, flagging issues for correction before submission.**

The rules engine validates claims against payer-specific billing rules and CMS guidelines; claims that fail these checks are returned to the provider with real-time notifications, allowing staff to correct and resubmit. This pre-submission validation reduces denials and improves clean claim rates.

- Evidence: [How Medical Billing Clearinghouses Work? Best Guide](https://www.medibillrcm.com/blog/how-medical-billing-clearinghouses-work/)

**After payer adjudication, clearinghouses receive EDI 835 remittance advice containing payment details, adjustment codes, and denial reason codes, which they reconcile with provider records to post payments and trigger follow-up workflows for denials.**

The payer sends an EDI 835 file (ERA) that includes payment amounts, patient responsibility, adjustment codes (e.g., contractual write-offs), and denial reason codes (e.g., CO-16 for missing information). Clearinghouses automate payment posting, update accounts receivable, and provide denial management services such as root-cause tagging and automated resubmission workflows, which can increase clean claim rates by 15–30%.

- Evidence: [How Medical Billing Clearinghouses Work? Best Guide](https://www.medibillrcm.com/blog/how-medical-billing-clearinghouses-work/)

**Clearinghouses support prior authorization by processing eligibility and authorization transactions alongside claims, performing pre-submission checks for missing authorizations to reduce denials due to lack of prior approval.**

Clearinghouses provide national-scale transaction connectivity for eligibility, authorization, claims, and payments; they can verify that services requiring prior approval have the necessary authorization before claim submission. Some clearinghouses use AI-powered scrubbing to detect missing authorizations pre-submission, as demonstrated by a cardiology group that reduced denials from 22% to 7% in four months using such capabilities.

- Evidence: [EDI Clearinghouse | Healthcare Solutions](https://www.availity.com/clearinghouse-and-trading-partner-network/)
- Evidence: [How Medical Billing Clearinghouses Work? Best Guide](https://www.medibillrcm.com/blog/how-medical-billing-clearinghouses-work/)
- Evidence: [Top 10 Clearinghouses in Medical Billing (2026)](https://claimmaxrcm.com/top-10-clearinghouses-in-medical-billing-2026-pricing-pros-cons-compared/)


## Current state: gaps, challenges, and regulatory impact (CMS-0057-F)

The CMS Interoperability and Prior Authorization Final Rule (CMS-0057-F), released January 17, 2024, addresses longstanding gaps in U.S. healthcare data infrastructure—such as fragmented health information exchange, manual prior‑authorization workflows, and administrative burden—by mandating FHIR‑based APIs for payers and imposing new operational requirements on prior authorization. The rule sets staggered compliance dates (operational provisions effective 2026, API requirements generally by 2027), introduces decision‑timeframe and denial‑transparency standards, adds a MIPS electronic prior‑authorization measure, and provides enforcement discretion for FHIR‑only implementations, collectively seeking to streamline data exchange and reduce costs for patients, providers, and payers.

**CMS released the Interoperability and Prior Authorization Final Rule (CMS-0057-F) on January 17, 2024, applying to Medicare Advantage, Medicaid, CHIP, and QHP issuers on the Federally Facilitated Exchanges.**

The rule impacts Medicare Advantage organizations, state Medicaid and CHIP Fee-for-Service programs, Medicaid managed care plans, CHIP managed care entities, and Qualified Health Plan issuers on the Federally Facilitated Exchanges (collectively “impacted payers”). It builds on the 2020 CMS Interoperability and Patient Access final rule (CMS-9115-F) and adds provisions to improve health information exchange and prior authorization processes.

- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**Impacted payers must implement and maintain four FHIR‑based APIs (Patient Access, Provider Access, Payer-to-Payer, Prior Authorization) with API compliance required generally by January 1, 2027.**

The Patient Access API must include prior‑authorization information (excluding drugs) by Jan 1, 2027. The Provider Access API and Payer-to-Payer API must share claims, encounter data, USCDI, and prior‑authorization data by Jan 1, 2027. The Prior Authorization API must support request/response and communicate approval, denial, or status by Jan 1, 2027. Operational provisions such as decision timeframes and denial‑reason disclosure begin January 1, 2026.

- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**Starting in 2026, impacted payers must send prior‑authorization decisions within 72 hours for expedited requests and seven calendar days for standard requests, and must provide a specific reason for denials regardless of transmission method.**

This requirement applies to all impacted payers except QHP issuers on the Federally Facilitated Exchanges. Denial reasons must be communicated via portal, fax, email, mail, or phone. Payers must also publicly report prior‑authorization metrics annually, with the first report due March 31, 2026.

- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**CMS added an Electronic Prior Authorization measure to MIPS and the Medicare Promoting Interoperability Program, requiring attestation beginning with the 2027 performance period for clinicians and the 2027 EHR reporting period for hospitals and critical access hospitals.**

MIPS eligible clinicians must attest “yes” to requesting a prior authorization electronically via a Prior Authorization API using certified EHR technology for at least one medical item or service (excluding drugs) during CY 2027, or claim an exclusion. Eligible hospitals and CAHs must attest similarly for at least one hospital discharge and medical item or service during the 2027 EHR reporting period.

- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**The rule seeks to reduce existing burdens from fragmented data exchange and manual prior‑authorization processes, reflecting current gaps in healthcare data infrastructure.**

The rule’s stated purpose is to improve health information exchange to achieve appropriate access to health records and to reduce overall payer, provider, and patient burden through improved prior‑authorization practices. An enforcement discretion announced February 28, 2024 allows FHIR‑only prior‑authorization APIs without HIPAA Administrative Simplification enforcement for the X12 278 standard, indicating flexibility to ease adoption and address current inefficiencies.

- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)
- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)


## Criticisms and counter‑arguments to current clearinghouse/EDI approaches

Critics argue that existing clearinghouse and EDI solutions for prior authorization remain costly, fall short of true interoperability, and have not eliminated the friction that delays patient care, despite years of investment in electronic data exchange.

**Prior authorization processes impose a significant financial burden on providers, costing $20‑50 per hour and nearly $34,000 annually per provider, highlighting the expense of current clearinghouse/EDI approaches.**

CMS estimates that completing prior authorizations takes providers an average of 13 hours per week, translating to substantial costs that could otherwise be spent on patient care. This expense undermines the economic efficiency promised by electronic clearinghouse systems.

- Evidence: [Moving Prior Authorization into the 21st Century](https://www.cms.gov/newsroom/blog/moving-prior-authorization-21st-century)

**Many payers and providers report being unprepared for interoperability, citing challenges such as determining a cohesive enterprise strategy and digitizing prior authorization policies, indicating that existing EDI clearinghouse solutions have not achieved seamless data exchange.**

A 2025 survey identified the top three interoperability challenges as strategy formulation, digitization of prior auth policies, and related implementation hurdles, showing that EDI alone has not resolved fragmentation in data exchange.

- Evidence: [Many payers, providers unprepared for interoperability and ...](https://www.healthcarefinancenews.com/news/many-payers-providers-unprepared-interoperability-and-prior-authorization-rule-wedi-finds)

**Providers continue to experience prior authorization delays that postpone diagnoses and interrupt treatment, suggesting that clearinghouse/EDI approaches have not fully resolved prior‑authorization friction.**

The American Hospital Association notes providers consistently report such delays, which undermine the promised efficiency of electronic clearinghouse systems and point to lingering workflow and technical gaps.

- Evidence: [AHA Comments on CMS' Interoperability and Prior ...](https://www.aha.org/lettercomment/2026-06-15-aha-comments-cms-interoperability-and-prior-authorization-proposed-rule)


## Future opportunities and emerging technologies

The next wave of US healthcare data infrastructure will be shaped by AI‑driven prior authorization, mandatory FHIR‑based APIs, and hyper‑automation of EHR workflows. Policy timelines (CMS Interoperability and Prior Authorization Final Rule) push payers to enable real‑time electronic prior auth by January 2027, while market data show exploding investment in AI‑PA tools and FHIR‑PA solutions. Together, these advances promise to cut administrative delays, lower denial rates, and unlock billions in savings for providers and payers.

**The CMS Interoperability and Prior Authorization Final Rule (CMS-0057-F) requires impacted payers to implement FHIR-based prior authorization APIs by January 1, 2027, with standard decisions within 7 calendar days and urgent decisions within 72 hours, and CMS estimates the rule will generate at least $16 billion in savings over ten years.**

The rule was released on January 17, 2024. Although the initial compliance date was January 1, 2026, stakeholder feedback extended the API deadline primarily to January 1, 2027 for Medicare Advantage, Medicaid managed care, CHIP, and ACA exchange plans. The decision‑time standards aim to reduce patient‑care delays and administrative burden.

- Evidence: [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)

**The AI prior authorization automation market was valued at USD 1.47 billion in 2025 and is projected to reach USD 10.31 billion by 2035, reflecting a compound annual growth rate (CAGR) of 21.5 %.**

This growth signals strong payer and provider demand for technology that automates submission, documentation, and follow‑up steps in the prior auth workflow. A parallel FHIR‑focused prior auth market was valued at USD 850 million in 2026 and is forecast to grow to USD 3.2 billion by 2036 at a CAGR of 14.2 %.

- Evidence: [AI Prior Authorization Automation Market](https://evolvancemarketresearch.com/reports/ai-prior-authorization-automation-market/)
- Evidence: [Explore the Global FHIR Prior Authorization Market](https://www.futuremarketinsights.com/reports/fhir-prior-authorization-market)

**Healthcare Huddle analysis shows AI prior authorization spending grew ten‑fold from $10 million in 2024 to $100 million in 2025, indicating rapidly accelerating market adoption.**

The surge reflects urgency to reduce the administrative burden documented in AMA surveys, where physicians handle a median of 39 prior auth requests per week consuming roughly 13 hours of staff time, and prior‑auth‑related staffing costs rose 43% between 2019 and 2024.

- Evidence: [AI Prior Authorization: Real-Time Approvals & Automation ...](https://www.develophealth.ai/blog/ai-prior-authorization)

**EHR automation investment strategy for 2026‑2030 predicts a shift toward agentic AI, predictive workflows, and hyper‑automation across clinical and administrative functions, enabling smarter prior authorization and claims processing.**

These technologies aim to reduce manual data entry, improve real‑time decision‑making, and create seamless data exchange between EHRs, clearinghouses, and payer systems.

- Evidence: [EHR Automation Investment Strategy 2026–2030](https://www.anisolutions.com/2026/02/16/future-trends-in-ehr-automation-whats-next-for-digital-healthcare/)

**Integrating FHIR standards with AI technologies automates manual prior authorization workflows, cutting administrative burden and enabling real‑time approvals.**

AI‑driven clinical evidence extraction, LLM‑enriched form filling, and multi‑agent quality assurance allow submissions to be completed in hours or minutes rather than days, while predictive models flag denial risk before submission. Podcast and industry commentary highlight this combination as a key near‑term opportunity.

- Evidence: [Revolutionizing Prior Auth via AI & FHIR](https://ajhcs.org/podcasts/fhir-ai-and-the-future-of-healthcare)
- Evidence: [The Future of Prior Authorization: From Fax Machines to ...](https://easypa.ai/blog/prior-auth-api-future)


## Risks and uncertainties

- Delayed or uneven payer compliance with the CMS‑0057‑F FHIR API requirements could prolong reliance on legacy EDI clearinghouse processes and limit anticipated interoperability gains.
- Providers may face significant implementation costs and technical complexity when upgrading EHRs and clearinghouse connections to support FHIR‑based prior‑authorization APIs.
- AI‑driven prior‑authorization tools raise concerns about algorithmic bias, transparency, and the potential for erroneous denials if not properly validated and overseen.
- Fragmented state Medicaid programs and variability in payer‑specific rules may hinder the uniformity of FHIR API adoption, creating persistent gaps in data exchange.
- Market consolidation among clearinghouses and health‑IT vendors could reduce competition, potentially increasing costs for providers despite efficiency promises.

## Conflicting information

- The sources do not contain contradictory information; they present a consistent view of the current clearinghouse/EDI landscape, the CMS rule, criticisms, and future opportunities.

## What to watch next

- January 1 2026: Operational provisions of CMS‑0057‑F (decision‑timeframes and denial‑reason disclosure) take effect for impacted payers.
- March 31 2026: First annual public reporting of prior‑authorization metrics required by CMS‑0057‑F.
- January 1 2027: General compliance deadline for FHIR‑based APIs (Patient Access, Provider Access, Payer‑to‑Payer, Prior Authorization) under CMS‑0057‑F.
- 2027 MIPS performance period: Clinicians must begin attestation to the Electronic Prior Authorization measure.
- 2027 EHR reporting period: Hospitals and critical access hospitals must begin attestation to the Electronic Prior Authorization measure.
- Ongoing market updates: AI prior‑authorization market size reports (expected 2026‑2027 releases) to gauge adoption trajectory versus projected CAGR of 21.5 %.

## Sources

1. [EDI Archives](https://uhin.org/tag/edi/)
2. [Healthcare EDI Market Report 2026-2031, By Offering ...](https://www.marketsandmarkets.com/Market-Reports/healthcare-edi-market-130571438.html)
3. [Enhancing EHR Interoperability and Security through ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11477175/)
4. [Top 10 Clearinghouses in Medical Billing (2026)](https://claimmaxrcm.com/top-10-clearinghouses-in-medical-billing-2026-pricing-pros-cons-compared/)
5. [EDI Clearinghouse Options | Digital Solutions for health ...](https://www.uhcprovider.com/en/resource-library/edi/edi-clearinghouse-opt.html)
6. [Interoperability as Infrastructure: Policy, Prior Authorization, ...](https://www.linkedin.com/pulse/interoperability-infrastructure-policy-prior-authorization-6irne)
7. [Powering Electronic Prior Authorization with Integrated ...](https://1up.health/blog/powering-electronic-prior-authorization-with-integrated-data-and-ai/)
8. [The 4 Levels of Healthcare Interoperability - OpenLoop Health](https://openloophealth.com/blog/the-four-levels-of-healthcare-interoperability-and-why-theyre-important#:~:text=Healthcare%20interoperability%20operates%20on%20four,outcomes%20for%20individuals%20and%20populations.)
9. [EDI Clearinghouse Options | Digital Solutions for health care ...](https://www.uhcprovider.com/en/resource-library/edi/edi-clearinghouse-opt.html#:~:text=Clearinghouses%20facilitate%20the%20transfer%20of,transactions%20and%20direct%20data%20entry.)
10. [Top 10 Clearinghouses in Medical Billing in 2026](https://www.onemedbilling.com/blog-details/top-10-clearinghouses-in-medical-billing-with-pros-and-cons)
11. [How Medical Billing Clearinghouses Work? Best Guide](https://www.medibillrcm.com/blog/how-medical-billing-clearinghouses-work/)
12. [Medical Billing Clearinghouse: Types, Function, & Process](https://pchhealth.global/glossary/medical-billing-clearinghouse)
13. [Healthcare Clearinghouses: Future Trends & Predictions](https://cms.officeally.com/blog/the-future-of-healthcare-clearinghouses-trends-and-predictions)
14. [What Are Clearinghouses in Healthcare EDI? | EDI Blog](http://ediacademy.com/blog/?p=12232#:~:text=A%20clearinghouse%20is%20an%20intermediary,to%20each%20other%20more%20consistently.)
15. [Medical Billing Clearinghouse: Types, Function, & Process](https://pchhealth.global/glossary/medical-billing-clearinghouse#:~:text=Claim%20submission%20and%20tracking,%2C%20denial%2C%20or%20processing).)
16. [What Is EDI Enrollment? Meaning, Process, and Benefits](https://www.atlassystems.com/blog/edi-enrollment#:~:text=EDI%20(Electronic%20data%20interchange)%20enrollment,advice%2C%20and%20claim%20status%20inquiries.)
17. [What is a claims processing system? - EIS Group](https://www.eisgroup.com/what-is-a-claims-processing-system/#:~:text=So%2C%20what%20is%20claims%20processing,the%20insurer%20and%20the%20customer.)
18. [EDI Clearinghouse | Healthcare Solutions](https://www.availity.com/clearinghouse-and-trading-partner-network/)
19. [What Is a Clearinghouse in Medical Billing?](https://flexbone.ai/blog/what-is-a-clearinghouse-in-medical-billing/)
20. [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/initiatives/burden-reduction/overview/interoperability/policies-regulations/cms-interoperability-prior-authorization-final-rule-cms-0057-f)
21. [CMS Interoperability and Prior Authorization Final Rule ...](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f)
22. [CMS-0057-F: Interoperability and Prior Authorization Final ...](https://fire.ly/regulations/cms-0057-f-interoperability-and-prior-authorization-final-rule/)
23. [Advancing Interoperability and Improving Prior ...](https://www.federalregister.gov/documents/2024/02/08/2024-00895/medicare-and-medicaid-programs-patient-protection-and-affordable-care-act-advancing-interoperability)
24. [CMS-0057-F: Rethink Your Electronic Prior Authorization](https://veradigm.com/veradigm-news/electronic-prior-authorization-cms-0057-f/)
25. [CMS Finalizes Rule to Improve Prior Authorization Process](https://obc.memberclicks.net/cms-finalizes-rule-to-improve-prior-authorization-process)
26. [CMS Interoperability & Prior Authorization Final Rule ...](https://www.linkedin.com/pulse/cms-interoperability-prior-authorization-final-key-impacts-raj-revuru-ovw5e)
27. [Your Guide to CMS-0057-F Compliance](https://www.tegria.com/resources/thought-leadership/your-guide-to-cms-0057-f-compliance/)
28. [CMS Interoperability and Prior Authorization Final Rule (CMS ...](https://hcpf.colorado.gov/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f)
29. [AI Prior Authorization: Real-Time Approvals & Automation ...](https://www.develophealth.ai/blog/ai-prior-authorization)
30. [EHR Automation Investment Strategy 2026–2030](https://www.anisolutions.com/2026/02/16/future-trends-in-ehr-automation-whats-next-for-digital-healthcare/)
31. [Explore the Global FHIR Prior Authorization Market](https://www.futuremarketinsights.com/reports/fhir-prior-authorization-market)
32. [2026 Health IT Trends: What the Industry Is Building ...](https://www.linkedin.com/pulse/2026-health-trends-what-industry-building-toward-uu8ze)
33. [Revolutionizing Prior Auth via AI & FHIR](https://ajhcs.org/podcasts/fhir-ai-and-the-future-of-healthcare)
34. [Top Best Healthcare Interoperability Solutions: Guide for 2026](https://www.bizdata360.com/top-best-healthcare-interoperability-solutions-guide-for-2025/)
35. [The Future of Prior Authorization: From Fax Machines to ...](https://easypa.ai/blog/prior-auth-api-future)
36. [AI Prior Authorization Automation Market](https://evolvancemarketresearch.com/reports/ai-prior-authorization-automation-market/)
37. [Many payers, providers unprepared for interoperability and ...](https://www.healthcarefinancenews.com/news/many-payers-providers-unprepared-interoperability-and-prior-authorization-rule-wedi-finds)
38. [AHA Comments on CMS' Interoperability and Prior ...](https://www.aha.org/lettercomment/2026-06-15-aha-comments-cms-interoperability-and-prior-authorization-proposed-rule)
39. [Moving Prior Authorization into the 21st Century](https://www.cms.gov/newsroom/blog/moving-prior-authorization-21st-century)
40. [Advancing Interoperability and Improving Prior Authorization](https://www.ebglaw.com/insights/publications/advancing-interoperability-and-improving-prior-authorization-no-one-said-it-would-be-easy)
41. [CMS Interoperability and Prior Authorization Final Rule](https://www.careviso.com/news-events/cms-interoperability-and-prior-authorization-final-rule)
42. [CMS Builds Upon Interoperability Rules with Prior ...](https://www.mintz.com/insights-center/viewpoints/52541/2023-04-12-cms-builds-upon-interoperability-rules-prior)
43. [An Overview of the Challenging Process of Prior Authorization](https://pmc.ncbi.nlm.nih.gov/articles/PMC11604005/)
