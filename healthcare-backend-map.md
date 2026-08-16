# Research report: Unsolved Technical Problems in US Healthcare IT Infrastructure

**Request:** unsolved technical problems in US healthcare IT infrastructure: patient identity matching, provider directory accuracy, TEFCA QHIN adoption, EHR API access and integration costs, health data quality  
**Context:** patient identity matching, provider directory accuracy, TEFCA QHIN adoption, EHR API access and integration costs, health data quality  
**Generated:** 2026-08-09 15:39 UTC

## Executive summary

The US healthcare IT interoperability landscape is structured around TEFCA’s three‑layer framework (Common Agreement, Trusted Exchange Framework, and QHIN Technical Framework), which mandates FHIR R4 standards and a network‑of‑networks model enabling a single IAL2 patient identity verification to unlock data across Qualified Health Information Networks (QHINs). As of mid‑2026, the first QHINs designated in December 2023 are exchanging data, hospital awareness has risen from 51% in 2022 to over 60% in 2023, and the Sequoia Project serves as the Recognized Coordinating Entity under a five‑year contract. However, persistent barriers include inconsistent patient demographic data causing record linkage failures, divergent use of clinical vocabularies (SNOMED CT, LOINC, RxNorm) undermining semantic interoperability, lack of a national patient identification and matching strategy, poor EHR‑FHIR API usability, and insufficient user interfaces or leadership support. Future outlook hinges on expanding TEFCA’s permissible exchange purposes, updating technical standards, and continuing QHIN onboarding, which together promise broader data access and reduced provider costs if the identified challenges are addressed.

## Technical mechanisms and standards

The technical backbone of US healthcare interoperability rests on TEFCA’s three‑layer framework (Common Agreement, Trusted Exchange Framework, and QHIN Technical Framework), which mandates standards for patient identity resolution, authentication, and performance measurement. While FHIR R4 is now required for certified EHRs, achieving true semantic interoperability remains hindered by inconsistent use of clinical vocabularies such as SNOMED CT, LOINC, and RxNorm. TEFCA also introduces a network‑of‑networks model that allows a single patient identity verification (IAL2) to unlock data across multiple QHINs, supported by mandated provider‑directory APIs.

**TEFCA consists of three foundational documents – the Common Agreement, Trusted Exchange Framework, and the QHIN Technical Framework – originally published in January 2022 and updated in November 2023, with the QHIN Technical Framework specifying technical components such as patient identity resolution, authentication, and performance measurement.**

The Trusted Exchange Framework and Common Agreement (TEFCA) was created by the ONC to establish a nationwide floor for health information exchange. The QHIN Technical Framework (QTF) focuses on the technical elements needed for QHIN‑to‑QHIN exchange, including how patient identities are resolved, how authentication is performed, and how performance is measured across the network-of-networks.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

**Becoming a Qualified Health Information Network (QHIN) typically takes about 12 months; the first QHINs were designated in December 2023, and health data began flowing among them within days of designation.**

To join TEFCA’s backbone, a network must complete a rigorous application, onboarding, and designation process and sign the Common Agreement. After the initial QHIN designations in December 2023, the operational network quickly began exchanging electronic health information across the country.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

**ONC’s HTI‑1 Final Rule requires FHIR R4 for all certified EHR systems, yet structural FHIR compliance does not guarantee semantic interoperability; inconsistent mapping of terminologies such as SNOMED CT, LOINC, RxNorm, ICD‑10‑CM, and CPT can lead to clinically inaccurate data exchange.**

While FHIR provides a standardized structure for exchanging health information, it does not define the meaning of the data. Differences in how systems code diagnoses, medications, lab results, and procedures using standard vocabularies can cause the receiving system to misinterpret the information, creating patient‑safety risks even when the exchange is technically successful.

- Evidence: [How to Maximize Patient Care Through Interoperability](https://omnimd.com/blog/maximizing-patient-care-through-interoperability-in-healthcare-a-how-to-guide/)

**TEFCA enables a single IAL2 identity verification for patients to access records from multiple facilities via QHINs, and the Provider Directory API mandated by CMS‑0057‑F supplies a standardized lookup of participating organizations.**

Through the QHIN network‑of‑networks model, a patient completes one identity assurance level 2 (IAL2) verification and can then retrieve data from any connected participant. The Provider Directory API, required under CMS‑0057‑F, provides a uniform method for payers and providers to discover which organizations are participating in TEFCA exchange.

- Evidence: [Network - Flexpa Docs](https://www.flexpa.com/docs/network)
- Evidence: [Understanding the Provider Directory API: Requirements, ...](https://fire.ly/blog/understanding-the-provider-directory-api/)


## Current state of adoption and progress

As of mid‑2026, the Trusted Exchange Framework and Common Agreement (TEFCA) has moved from initial publication to operational use, with the first Qualified Health Information Networks designated in late 2023 and health data beginning to flow among them shortly thereafter. Hospital awareness and intent to participate rose from just over half in 2022 to more than 60% in 2023, and the Sequoia Project serves as the Recognized Coordinating Entity under a multi‑year contract. The framework’s foundational documents were issued in early 2022 and refreshed in late 2023, defining six permissible exchange purposes that guide current TEFCA‑enabled sharing.

**In December 2023, TEFCA reached a milestone with the first Qualified Health Information Networks (QHINs) designated, and health data began flowing among those QHINs within days.**

This marked the transition from framework development to live nationwide exchange, enabling providers, payers, public health agencies, and patients to share electronic health information across organizational boundaries.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

**Hospital awareness of TEFCA grew from 51% in 2022 to over 60% in 2023, with a majority planning to participate.**

The increase reflects growing recognition of TEFCA’s role in nationwide interoperability among U.S. hospitals surveyed in the study.

- Evidence: [TEFCA Awareness and Planned Participation Among U.S. ...](https://www.ncbi.nlm.nih.gov/books/NBK606030/)

**The Sequoia Project serves as the Recognized Coordinating Entity (RCE) for TEFCA under a five‑year contract awarded by ONC in August 2023.**

As RCE, the Sequoia Project develops, updates, and maintains the Common Agreement, manages the QHIN designation process, and oversees TEFCA operations.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

**TEFCA’s three foundational documents—the Common Agreement, Trusted Exchange Framework, and QHIN Technical Framework—were first published in January 2022 and updated in November 2023, and they define six permissible exchange purposes.**

The exchange purposes are Treatment, Payment, Health care operations, Public Health, Government benefits determination, and Individual access services, which structure how data may be shared under the framework.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)

**The TEFCA policy page on HealthIT.gov was last updated on July 28, 2026, indicating ongoing maintenance and recent activity related to the framework.**

This timestamp shows that the federal government continues to refresh TEFCA guidance and resources as adoption progresses.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)


## Criticisms and barriers

Although TEFCA was designed to remove barriers to nationwide health information exchange, significant criticisms and obstacles remain. These include patient identity and demographic data inconsistencies that cause record linkage failures, the need for organizations to resolve identity issues, normalize terminologies, and implement FHIR APIs before joining, poor user interfaces and lack of leadership support hindering HIE adoption, the absence of a national patient identification and matching strategy that exacerbates privacy and safety risks, and EHR systems that often lack user‑friendly FHIR APIs and app integration, forcing providers into manual workarounds.

**Inconsistent patient demographic data causes record linkage failures during QHIN-to-QHIN exchanges under TEFCA.**

The TEFCA Health Tech Implementation Challenges Guide notes that when QHINs exchange queries, there is a risk that records will not link correctly if patient demographic data is inconsistent. This undermines the goal of seamless nationwide health information exchange.

- Evidence: [TEFCA Health Tech Implementation Challenges Guide](https://www.invene.com/blog/tefca)

**Before joining TEFCA, organizations must address patient identity problems, standardize clinical terminologies, and deploy FHIR APIs.**

The 2026 Healthcare Interoperability Report states that resolving patient identity issues, normalizing clinical terminologies, and implementing FHIR APIs are prerequisites for connecting to TEFCA. These steps represent significant technical and resource burdens for many healthcare entities.

- Evidence: [2026 Healthcare Interoperability Report](https://www.trovehealth.io/insights/?post=trusted-exchange-framework-statistics-2026)

**Poor user interfaces and lack of leadership support hinder adoption of health information exchange networks.**

Researchers analyzing HIE networks have identified poor user interfaces and insufficient leadership support as key barriers to utilization. These factors reduce clinician willingness to engage with exchange platforms.

- Evidence: [Perspectives on Challenges and Opportunities for ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10007006/)

**The absence of a national patient identification and matching strategy worsens privacy and safety risks in health data exchange.**

CHIME’s response to a CMS/ASTP/ONC RFI highlights that without a nationwide patient identification and matching strategy, privacy and safety risks are significantly exacerbated. This gap remains a systemic barrier to trusted exchange.

- Evidence: [CHIME Responds to CMS & ASTP/ONC's RFI on the ...](https://chimecentral.org/chime/resource-post/chime-responds-to-cms-astponc-rfi-on-health-technology-ecosystem)

**Many EHR systems lack user‑friendly FHIR APIs and app integration capabilities, forcing manual workarounds.**

According to the FH‑linked RFI on the Health Technology Ecosystem, EHR systems often do not provide user‑friendly FHIR APIs or easy app integration, compelling providers to rely on external applications that require manual data handling. This inefficiency slows adoption of interoperable workflows.

- Evidence: [Health Technology Ecosystem](https://fah.org/wp-content/uploads/2025/07/RFI-Health-Technology-Ecosystem-61225-FINAL.pdf)


## Future outlook and policy directions

The outlook for resolving US healthcare IT infrastructure challenges centers on the expansion and maturation of TEFCA, which aims to create a nationwide interoperability framework. Upcoming regulations codify TEFCA processes, while ongoing policy efforts expand permissible exchange purposes, update technical standards like FHIR and the QHIN Technical Framework, and rely on the Sequoia Project as the Recognized Coordinating Entity to govern QHIN onboarding and maintenance. These developments promise increased data access, reduced provider costs, and stronger privacy and security safeguards.

**TEFCA plans to expand its permissible exchange purposes beyond the initial six (Treatment, Payment, Health care operations, Public Health, Government benefits determination, Individual access services) based on market needs raised by the QHIN Governing Council.**

ONC and the Recognized Coordinating Entity (RCE) intend to broaden the allowed use cases for TEFCA-mediated exchange over time to address evolving stakeholder demands, thereby increasing the framework's utility for a wider range of healthcare scenarios.

- Evidence: [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)


## Risks and uncertainties

- Patient identity mismatches due to inconsistent demographic data can cause record linkage failures during QHIN‑to‑QHIN exchanges.
- Inconsistent mapping of clinical terminologies (SNOMED CT, LOINC, RxNorm, ICD‑10‑CM, CPT) hinders semantic interoperability despite structural FHIR R4 compliance.
- Absence of a nationwide patient identification and matching strategy exacerbates privacy and safety risks.
- Many EHR systems lack user‑friendly FHIR APIs and easy app integration, forcing providers into manual workarounds.
- Poor user interfaces and insufficient leadership support reduce clinician willingness to adopt HIE platforms.
- Organizations must resolve identity issues, normalize terminologies, and deploy FHIR APIs before joining TEFCA, creating significant technical and resource burdens.
- Uncertainty around the timing and scope of future expansions to TEFCA’s permissible exchange purposes.
- Dependence on the Sequoia Project as the Recognized Coordinating Entity introduces concentration risk if contractual or operational issues arise.

## Conflicting information

- The sources are consistent; no contradictory information was found across the provided sections.

## What to watch next

- Next QHIN designation window: organizations applying now would likely be designated approximately 12 months later (based on the typical 12‑month onboarding timeline).
- Sequoia Project’s five‑year contract as Recognized Coordinating Entity runs through August 2028; watch for contract renewal or performance review signals in mid‑2028.
- ONC updates to TEFCA’s Common Agreement or Trusted Exchange Framework (last updated November 2023); anticipate potential revisions in late 2024 or early 2025.
- Expansion of TEFCA’s permissible exchange purposes beyond the initial six, driven by the QHIN Governing Council; monitor for formal proposals and public comment periods in 2025.
- Release of updated FHIR standards (e.g., FHIR R5) and corresponding adjustments to the QHIN Technical Framework; watch for ONC guidance aligning certified EHRs with newer FHIR versions.
- CMS‑0057‑F Provider Directory API enforcement and adoption metrics; look for quarterly compliance reports starting in early 2025.

## Sources

1. [Healthcare Integration Issues and Their Solutions](https://emorphis.health/blogs/healthcare-integration-issues-solution/)
2. [News - SMART Health IT](https://smarthealthit.org/an-app-platform-for-healthcare/news/)
3. [Interoperability of heterogeneous health information systems](https://pmc.ncbi.nlm.nih.gov/articles/PMC9875417/)
4. [Information Technology Interoperability and Use for Better ...](https://nam.edu/perspectives/information-technology-interoperability-and-use-for-better-care-and-evidence-a-vital-direction-for-health-and-health-care/)
5. [4 Reasons Why EHR Interoperability is a Mess (and How to ...](https://rhapsody.health/blog/reasons-ehr-interoperability-is-a-mess-and-how-to-fix-it/)
6. [Fixing Healthcare's Broken Provider Directory Problem](https://www.linkedin.com/posts/mansourshams_healthcares-provider-directory-problem-is-activity-7484269921254694912-B90S)
7. [Interoperability Isn't a Technology Problem Anymore. It's ...](https://www.primaryrecord.com/healthcare-interoperability-trust-problem/)
8. [Health Information Technology | FAH](https://fah.org/issues-advocacy/health-information-technology/)
9. [10 Healthcare Challenges to Solve in 2026 - Oracle](https://www.oracle.com/health/healthcare-challenges/#:~:text=Among%20the%20biggest%20challenges%20healthcare,people%2C%20and%20protecting%20patient%20data.)
10. [The 4 Levels of Healthcare Interoperability - OpenLoop Health](https://openloophealth.com/blog/the-four-levels-of-healthcare-interoperability-and-why-theyre-important#:~:text=Healthcare%20interoperability%20operates%20on%20four,outcomes%20for%20individuals%20and%20populations.)
11. [Advancing Nationwide Interoperability with TEFCA](https://healthit.gov/policy/tefca/)
12. [Health Data, Technology, and Interoperability: Trusted ...](https://www.federalregister.gov/documents/2024/12/16/2024-29163/health-data-technology-and-interoperability-trusted-exchange-framework-and-common-agreement-tefca)
13. [TEFCA's Limits in Nationwide Healthcare Interoperability](https://www.onhealthcare.tech/p/tefca-and-the-promise-of-nationwide)
14. [Frequently Asked Questions - ONC TEFCA RCE](https://rce.sequoiaproject.org/rce/faqs/)
15. [TEFCA Health Tech Implementation Challenges Guide](https://www.invene.com/blog/tefca)
16. [Updated TEFCA Recognized Coordinating Entity ...](https://www.facebook.com/ahahospitals/posts/the-trusted-exchange-framework-and-common-agreement-recognized-coordinating-enti/1430512612446704/)
17. [Looking Ahead at 2024 - Five Interoperability Predictions ...](https://www.healthgorilla.com/blog/looking-ahead-at-2024-five-interoperability-predictions-from-health-gorilla)
18. [TEFCA: Everything Healthcare Organizations Need to Know](https://rhapsody.health/blog/tefca-everything-healthcare-organizations-need-to-know/)
19. [TEFCA Awareness and Planned Participation Among U.S. ...](https://www.ncbi.nlm.nih.gov/books/NBK606030/)
20. [2026 Healthcare Interoperability Report](https://www.trovehealth.io/insights/?post=trusted-exchange-framework-statistics-2026)
21. [Perspectives on Challenges and Opportunities for ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10007006/)
22. [The Impact of TEFCA & HITRUST on Patient Privacy and ...](https://www.a-lign.com/articles/the-impact-of-tefca-hitrust-on-patient-privacy-and-security)
23. [CHIME Responds to CMS & ASTP/ONC's RFI on the ...](https://chimecentral.org/chime/resource-post/chime-responds-to-cms-astponc-rfi-on-health-technology-ecosystem)
24. [Health Technology Ecosystem](https://fah.org/wp-content/uploads/2025/07/RFI-Health-Technology-Ecosystem-61225-FINAL.pdf)
25. [TEFCA – QHIN Technical Framework Overview](https://www.youtube.com/watch?v=SXFu2KUUbV0)
26. [The State of HIOs & Plans to Participate in TEFCA](https://blog.pocp.com/blog/the-state-of-hios-plans-to-participate-in-tefca)
27. [How to Maximize Patient Care Through Interoperability](https://omnimd.com/blog/maximizing-patient-care-through-interoperability-in-healthcare-a-how-to-guide/)
28. [Qualified Health Information Network (QHIN) Technical ...](https://rce.sequoiaproject.org/wp-content/uploads/2022/01/QTF_0122.pdf)
29. [Approaches to Collect Comprehensive Electronic Patient ...](https://www.sciencedirect.com/org/science/article/pii/S143888712600628X)
30. [Network - Flexpa Docs](https://www.flexpa.com/docs/network)
31. [Understanding the Provider Directory API: Requirements, ...](https://fire.ly/blog/understanding-the-provider-directory-api/)
32. [The Importance of TEFCA/QHIN in the Evolution ...](https://kno2.com/resources/blog/the-importance-of-tefca-qhin-in-the-evolution-of-interoperability/)
33. [Why You Should Pay Attention to TEFCA—Even If You're ...](https://www.centaurihs.com/why-you-should-pay-attention-to-tefca/)
34. [Understanding TEFCA – A National initiative Toward ...](https://contexture.org/understanding-tefca-a-national-step-toward-interoperability/)
35. [TEFCA Healthcare Data Exchange: Guide for CTOs (2026)](https://www.anisolutions.com/2026/04/07/tefca-healthcare-data-exchange/)
36. [Sharing Health Data Update July 2026](https://www.healthitanswers.net/sharing-health-data-update-july-2026/)
37. [TEFCA in Healthcare: Understanding a Vital Concept](https://kodjin.com/blog/trusted-exchange-framework-and-common-agreement/)
38. [TEFCA - ONC - Office of the National Coordinator for Health ...](https://healthit.gov/policy/tefca/#:~:text=In%20practice%2C%20TEFCA%20establishes%20a,where%20the%20information%20is%20stored.)
