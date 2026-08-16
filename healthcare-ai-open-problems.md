# Research report: Documented failures and unsolved problems in healthcare AI

**Request:** documented failures and unsolved problems in healthcare AI: what does not work in clinical deployment, limitations reported in peer-reviewed studies, FDA and ONC requests for information on AI gaps, evaluation and validation shortfalls  
**Context:** clinical deployment, peer-reviewed limitations, FDA ONC AI gaps, evaluation validation shortfalls  
**Generated:** 2026-08-09 16:05 UTC

## Executive summary

Healthcare AI faces persistent challenges when moving from research to clinical deployment, including biased training data, contextual mismatches, privacy and interoperability barriers, and governance shortcomings that can lead to misdiagnoses, limited scalability, and eroded trust. Simultaneously, federal agencies (FDA, ONC/ASTP, CMS/HHS) have issued requests for information in late 2025‑early 2026 to better understand real‑world performance, market adoption, and data gaps, highlighting regulatory concerns about oversight and evidence generation. Despite these problems, peer‑reviewed literature and case studies document measurable benefits of AI in areas such as cancer screening, postpartum care, and clinical decision‑support, showing that AI can improve service quality and patient outcomes when properly implemented. Future progress hinges on regulatory reforms (e.g., the EU AI Act’s risk‑based rules), data infrastructure upgrades (e.g., the European Health Data Space), liability reforms, and collaborative governance frameworks aimed at closing validation and deployment gaps.

## Mechanisms and failure modes of AI in clinical deployment

AI systems often falter when moved from research to clinical practice due to biased training data, contextual mismatches, privacy and interoperability barriers, and governance shortcomings. These failure mechanisms lead to misdiagnoses, limited scalability, and reduced trust in AI-assisted care.

**Biased AI models can lead to misdiagnoses or overlooked conditions, especially in underrepresented patient groups.**

Inaccurate or biased AI models have been shown to produce erroneous clinical predictions when the training data reflects historical inequalities in treatment or access, resulting in disparate diagnostic accuracy across populations.

- Evidence: [Artificial intelligence in healthcare delivery: Prospects and ...](https://www.sciencedirect.com/science/article/pii/S2949916X24000616)

**Contextual errors limit the scalability of medical AI across different healthcare settings.**

A Harvard-led study published in Nature Medicine found that AI systems often fail to account for local workflow nuances, equipment variations, or patient population differences, causing performance drops when deployed outside the original research environment.

- Evidence: [Harvard Study Highlights Contextual Errors and Clinical AI ...](https://www.labmanager.com/harvard-researchers-warn-contextual-errors-may-limit-medical-ai-across-clinical-settings-34997)

**Data privacy and security concerns are a major barrier to AI adoption in clinical settings.**

Stakeholders cite the risk of breaching patient confidentiality and the need for robust cybersecurity measures as key reasons for hesitancy to implement AI tools, slowing their real‑world uptake.

- Evidence: [Overcoming Barriers to Artificial Intelligence Adoption in ...](https://www.preprints.org/manuscript/202603.0316)

**Lack of interoperability between AI systems and existing health IT infrastructure hinders integration.**

AI tools often cannot seamlessly exchange data with electronic health records or other clinical systems due to differing standards and proprietary interfaces, creating operational friction and limiting utility.

- Evidence: [Overcoming Barriers to Artificial Intelligence Adoption in ...](https://www.preprints.org/manuscript/202603.0316)

**Governance failures have allowed biased AI systems to reach clinical deployment.**

Insufficient oversight, inadequate validation protocols, and poor data management practices have enabled models with known biases to be deployed, posing patient safety risks that could have been prevented with stronger governance.

- Evidence: [Edition #3 AI bias: A hidden danger to patient safety](https://www.linkedin.com/pulse/edition-3-ai-bias-hidden-danger-patient-safety-ashraf-alsinglawi-silcf)


## Current regulatory and policy landscape: FDA and ONC requests for information on AI gaps

In late 2025 and early 2026, federal agencies issued multiple requests for information (RFIs) and public comment opportunities that reveal perceived gaps in the evaluation, validation, and oversight of AI-enabled medical devices and health IT. The FDA sought input on real-world performance measurement and drift detection, while ONC/ASTP and CMS/HHS asked for stakeholder views on accelerating AI adoption and market infrastructure. Concurrently, industry groups noted that despite over 1,250 FDA-authorized AI devices by mid‑2025, data limitations hinder visibility into usage and spending, underscoring the regulatory focus on improving evidence generation and transparency.

**On September 30, 2025, the FDA issued a Request for Public Comment seeking input on measuring and evaluating the real‑world performance of AI‑enabled medical devices, including strategies for detecting and managing performance drift, with comments due by December 1, 2025.**

The RFI, released by the FDA’s Digital Health Center of Excellence, asks for information on current practical approaches to assess safety, effectiveness, and reliability of AI devices in clinical use, focusing on metrics, real‑world evaluation methods, data sources, monitoring triggers, human‑AI interaction, and best practices. It explicitly states that the objective is to gather feedback on methods that are deployed at scale, supported by real‑world evidence, and applied in patient‑ or health‑care‑worker‑facing settings.

- Evidence: [Evaluating AI-enabled Medical Device Performance in ...](https://www.fda.gov/medical-devices/digital-health-center-excellence/request-public-comment-measuring-and-evaluating-artificial-intelligence-enabled-medical-device)

**On May 16, 2025, CMS and the HHS Health IT Office issued a Request for Information requesting stakeholder input on the market for digital health products and health technology infrastructure, including AI‑enabled technologies.**

The RFI aimed to collect information on market dynamics, adoption barriers, and infrastructure needs for digital health products, with AI identified as a key area of interest, indicating early 2025 federal attention to gaps in AI market evidence and health‑IT readiness.

- Evidence: [CMS & HHS Health IT Office Issue Request for Information ...](https://www.covingtondigitalhealth.com/2025/05/cms-hhs-health-it-office-issue-request-for-information-on-digital-health-products-and-health-technology-infrastructure/)

**As of July 2025, the FDA had authorized more than 1,250 AI‑enabled medical devices, but data gaps limit visibility into AI use and spending across the healthcare system.**

This figure was cited in a July 2025 letter to HHS from the Bipartisan Policy Center, which warned that while the number of authorized AI devices is growing rapidly, insufficient data collection hampers oversight of utilization and expenditures, highlighting a regulatory blind spot in postmarket surveillance.

- Evidence: [Letter to HHS on Use of Artificial Intelligence as Part ...](https://bipartisanpolicy.org/testimony-letter/letter-to-hhs-on-use-of-ai-as-part-of-clinical-care/)

**On February 24, 2026, AdvaMed submitted a comment letter responding to HHS’s Request for Information on accelerating AI adoption in clinical care, offering industry perspectives on addressing AI gaps.**

AdvaMed’s comment letter, filed in response to the ONC/ASTP RFI (referenced in the HKLaw article), provides recommendations on policies to support AI adoption while addressing validation, oversight, and data‑collection challenges, illustrating stakeholder engagement with the regulatory inquiries.

- Evidence: [accelerating-ai-adoption-in-clinical-care](https://www.advamed.org/member-center/resource-library/ai-adoption-in-clinical-care/)


## Counter‑arguments and reported successes: where AI is working in healthcare

Despite concerns about failures, multiple studies and reports highlight areas where AI delivers measurable benefits in healthcare, including improved service quality, enhanced screening and early detection, support for clinical decision‑making, and demonstrated success in real‑world case studies.

**AI-based technologies have been reported to raise the quality of healthcare services and improve human life quality.**

A systematic literature review concludes that AI can enhance service quality across the healthcare industry and contributes to better overall life quality for patients. This suggests that, when properly implemented, AI tools yield tangible improvements beyond experimental settings.

- Evidence: [A systematic literature review of artificial intelligence in the ...](https://www.sciencedirect.com/science/article/pii/S2444569X2300029X)

**AI is already improving public health through applications such as cancer screenings and postpartum care.**

Researchers note that AI-driven tools are being used to enhance cancer screening programs and support postpartum care, leading to earlier detection and better maternal health outcomes. These real‑world deployments illustrate how AI can address preventive and ongoing care needs.

- Evidence: [The promise and perils of AI in health care](https://www.youtube.com/watch?v=PHCdER8Mekk)

**Evaluation of clinical AI tools is broadly supported in peer‑reviewed literature and is often required for FDA clearance.**

The assessment of AI clinical tools in peer‑reviewed publications shows widespread endorsement, reflecting confidence in their safety and efficacy. Many FDA clearance processes mandate such evaluations, indicating regulatory reliance on evidence of benefit.

- Evidence: [AI, Health, and Health Care Today and Tomorrow](https://jamanetwork.com/journals/jama/fullarticle/2840175)

**Case studies demonstrate successful clinical applications of AI that deliver positive change for patients and organizations.**

Published case studies describe real‑world implementations where AI has improved workflow efficiency, diagnostic accuracy, and patient outcomes, providing concrete examples of AI’s practical value. These examples highlight how limitations can be mitigated through careful deployment and monitoring.

- Evidence: [4 Case Studies of Successful Clinical Applications of AI in ...](https://www.xsolis.com/blog/case-studies-of-successful-implementations-of-ai-in-healthcare/)


## Future directions and proposed solutions to close AI validation and deployment gaps

To address validation and deployment gaps in healthcare AI, stakeholders are advancing regulatory reforms, data infrastructure improvements, liability updates, and collaborative governance frameworks. Key initiatives include the EU AI Act’s risk‑based rules for high‑risk medical AI, the European Health Data Space enabling secure secondary use of health data, revised Product Liability Directive treating AI software as a product, U.S. HIPAA‑2025 and HTI‑1 updates, voluntary AI Pact compliance, and calls for multidisciplinary trustworthy AI frameworks and validation partnerships among developers, clinicians, and regulators.

**The EU AI Act entered into force on 1 August 2024 and will be fully applicable two years later (by 1 August 2026), with high‑risk medical AI systems required to meet risk‑mitigation, data‑quality, transparency and human‑oversight obligations.**

Prohibitions take effect after six months, governance rules and obligations for general‑purpose AI models after 12 months, and rules for AI systems embedded into regulated products after 36 months. The Act also launched the voluntary AI Pact to encourage early compliance.

- Evidence: [Artificial Intelligence in healthcare - Public Health](https://health.ec.europa.eu/ehealth-digital-health-and-care/artificial-intelligence-healthcare_en)


## Risks and uncertainties

- Biased or unrepresentative training data leading to misdiagnoses or overlooked conditions in under‑served patient groups.
- Contextual errors when AI models encounter local workflow nuances, equipment variations, or patient‑population differences, causing performance drops outside the original research setting.
- Data privacy and security risks that discourage adoption due to potential breaches of patient confidentiality and insufficient cybersecurity safeguards.
- Lack of interoperability between AI tools and existing health IT infrastructure (EHRs, clinical systems) stemming from differing standards and proprietary interfaces.
- Governance failures—insufficient oversight, inadequate validation protocols, and poor data management—that allow biased or unsafe models to reach clinical use.
- Performance drift and inadequate real‑world performance measurement, limiting visibility into long‑term safety and effectiveness of AI‑enabled devices.
- Regulatory uncertainty stemming from evolving FDA guidance, ONC/ASTP initiatives, and international frameworks (e.g., EU AI Act) that may change compliance requirements.
- Data gaps hindering oversight of AI utilization, spending, and postmarket surveillance despite over 1,250 FDA‑authorized AI devices by mid‑2025.

## Conflicting information

- The sources do not present direct contradictions; they instead offer complementary perspectives—detailing deployment challenges and limitations while also reporting measurable successes and benefits of AI in clinical settings.

## What to watch next

- FDA’s deadline for public comment on measuring and evaluating the real‑world performance of AI‑enabled medical devices (comments due December 1, 2025).
- Full applicability of the EU AI Act’s requirements for high‑risk medical AI systems (effective August 1, 2026).
- Expected release of FDA guidance or standards on real‑world performance measurement and drift detection for AI devices (anticipated mid‑2026).
- Implementation milestones for the European Health Data Space enabling secure secondary use of health data for AI training and validation (phased rollout 2025‑2026).
- Updates to U.S. HIPAA‑2025 and HTI‑1 regulations concerning AI‑related data privacy and security (expected 2025‑2026).

## Sources

1. [Artificial intelligence in healthcare and medicine - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12455834/)
2. [Risks of Artificial Intelligence (AI) in Medicine](https://www.pneumon.org/Risks-of-Artificial-Intelligence-AI-in-Medicine,191736,0,2.html)
3. [The Challenge of Evaluating AI Products in Healthcare](https://techpolicy.press/the-challenge-of-evaluating-ai-products-in-healthcare)
4. [Keep an Eye on Clinical Validation Gaps in AI-Enabled ...](https://www.aha.org/aha-center-health-innovation-market-scan/2025-09-16-keep-eye-clinical-validation-gaps-ai-enabled-medical-devices)
5. [AI in Drug Discovery: Clinical Failures, Regulatory Reality ...](https://www.mdpi.com/1424-8247/19/6/916)
6. [Challenges in FDA approval of AI medical programs](https://www.facebook.com/groups/909584524258768/posts/938668194683734/)
7. [Healthcare Report.pdf - Center for Sustainable Development](https://csd.columbia.edu/sites/csd.columbia.edu/files/content/Healthcare%20Report.pdf)
8. [6 Common Healthcare AI Mistakes](https://prsglobal.com/blog/6-common-healthcare-ai-mistakes)
9. [5 Major Disadvantages of AI in Healthcare - Keragon](https://www.keragon.com/blog/disadvantages-of-ai-in-healthcare#:~:text=The%20disadvantages%20of%20AI%20in,of%20technology%20replacing%20human%20judgment.)
10. [5 Careers that won't be replaced by AI (and the skills you need to build them)](https://studyonline.uts.edu.au/blog/5-careers-wont-be-replaced-ai-and-skills-you-need-build-them)
11. [Bias in medical AI: Implications for clinical decision-making](https://pmc.ncbi.nlm.nih.gov/articles/PMC11542778/)
12. [Artificial intelligence in healthcare delivery: Prospects and ...](https://www.sciencedirect.com/science/article/pii/S2949916X24000616)
13. [Reflecting on Our Biases Through AI in Health Care](https://learn.hms.harvard.edu/insights/all-insights/confronting-mirror-reflecting-our-biases-through-ai-health-care)
14. [Shaping the Future of Healthcare: Ethical Clinical Challenges ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC11900311/)
15. [Overcoming Barriers to Artificial Intelligence Adoption in ...](https://www.preprints.org/manuscript/202603.0316)
16. [Understanding and Mitigating Unintended Bias in Medical ...](https://hdsr.mitpress.mit.edu/pub/3n0jq4i3)
17. [Edition #3 AI bias: A hidden danger to patient safety](https://www.linkedin.com/pulse/edition-3-ai-bias-hidden-danger-patient-safety-ashraf-alsinglawi-silcf)
18. [Harvard Study Highlights Contextual Errors and Clinical AI ...](https://www.labmanager.com/harvard-researchers-warn-contextual-errors-may-limit-medical-ai-across-clinical-settings-34997)
19. [AI in Healthcare: 5 Integration Barriers & Solutions](https://telehealth.org/news/ai-in-healthcare-5-barriers-and-solutions-for-integration/)
20. [Artificial intelligence in healthcare: transforming the practice of ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC8285156/)
21. [A systematic literature review of artificial intelligence in the ...](https://www.sciencedirect.com/science/article/pii/S2444569X2300029X)
22. [The Pros and Cons of AI in Healthcare](https://hitrustalliance.net/blog/the-pros-and-cons-of-ai-in-healthcare)
23. [AI, Health, and Health Care Today and Tomorrow](https://jamanetwork.com/journals/jama/fullarticle/2840175)
24. [What are the key challenges and success factors ...](https://www.researchgate.net/post/What_are_the_key_challenges_and_success_factors_for_implementing_AI_in_healthcare_systems_especially_in_clinical_decision-making_and_patient_care)
25. [4 Case Studies of Successful Clinical Applications of AI in ...](https://www.xsolis.com/blog/case-studies-of-successful-implementations-of-ai-in-healthcare/)
26. [The promise and perils of AI in health care](https://www.youtube.com/watch?v=PHCdER8Mekk)
27. [Accelerating the Adoption and Use of Artificial Intelligence ...](https://www.federalregister.gov/documents/2025/12/23/2025-23641/request-for-information-accelerating-the-adoption-and-use-of-artificial-intelligence-as-part-of)
28. [Letter to HHS on Use of Artificial Intelligence as Part ...](https://bipartisanpolicy.org/testimony-letter/letter-to-hhs-on-use-of-ai-as-part-of-clinical-care/)
29. [ASTP/ONC's Year-End Moves Mark a Strategic Pivot in ...](https://www.hklaw.com/en/insights/publications/2026/01/astp-oncs-year-end-moves-mark-a-strategic-pivot)
30. [AI in healthcare: the rules, in plain English.](https://livecompliance.com/learn/ai-healthcare-regulations/)
31. [Evaluating AI-enabled Medical Device Performance in ...](https://www.fda.gov/medical-devices/digital-health-center-excellence/request-public-comment-measuring-and-evaluating-artificial-intelligence-enabled-medical-device)
32. [accelerating-ai-adoption-in-clinical-care](https://www.advamed.org/member-center/resource-library/ai-adoption-in-clinical-care/)
33. [CMS & HHS Health IT Office Issue Request for Information ...](https://www.covingtondigitalhealth.com/2025/05/cms-hhs-health-it-office-issue-request-for-information-on-digital-health-products-and-health-technology-infrastructure/)
34. [Healthcare AI Regulations 2025: New Rules, Compliance ...](https://www.accountablehq.com/post/healthcare-ai-regulations-2025-new-rules-compliance-requirements-and-what-providers-need-to-know)
35. [ONC Regulatory Activities](https://healthit.gov/regulations/onc-regulatory-activities/)
36. [Artificial Intelligence in healthcare - Public Health](https://health.ec.europa.eu/ehealth-digital-health-and-care/artificial-intelligence-healthcare_en)
37. [US Regulatory Updates for AI in Healthcare: A 2025 ...](https://www.linkedin.com/pulse/us-regulatory-updates-ai-healthcare-2025-compliance-guide-nirmitee-i5njf)
38. [Ethical Clinical Challenges and Pathways to Trustworthy AI](https://www.mdpi.com/2077-0383/14/5/1605)
39. [Artificial Intelligence in Clinical Decision-Making - Akin Gump](https://www.akingump.com/en/insights/alerts/artificial-intelligence-in-clinical-decision-making-regulatory-roadmap-and-reimbursement-strategies)
40. [Healthcare AI 2025 | Global Practice Guides - Chambers](https://practiceguides.chambers.com/practice-guides/healthcare-ai-2025)
41. [Guide to Healthcare AI 2025: Legal framework, trends & ...](https://gowlingwlg.com/en/insights-resources/guides/2025/guide-to-healthcare-ai-2025)
42. [Artificial intelligence in clinical trials: A comprehensive ...](https://www.sciencedirect.com/science/article/pii/S1386505625003582)
