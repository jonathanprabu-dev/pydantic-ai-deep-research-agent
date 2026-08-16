# Research report: LLMs and AI for medical terminology mapping and normalization

**Request:** LLMs and AI for medical terminology mapping and normalization: SNOMED CT LOINC RxNorm automated code mapping accuracy in peer-reviewed studies, companies selling terminology normalization software including Intelligent Medical Objects, Clinical Architecture, Wolters Kluwer Health Language and Rhapsody, startups and funding in clinical data normalization  
**Context:** SNOMED CT, LOINC, RxNorm, LLM, clinical terminology mapping  
**Generated:** 2026-08-09 16:18 UTC

## Executive summary

LLMs are being applied to map and normalize clinical terminologies such as SNOMED CT, LOINC, and RxNorm, with approaches including fine-tuning, contrastive learning, retrieval-augmented generation, and multilingual embeddings. Reported performance varies widely: some studies show ML-based methods achieving up to 0.99 accuracy for LOINC and 0.95 for SNOMED CT, while direct LLM‑RAG evaluations report modest exact‑code lookup accuracies of 50–60% due to the size and complexity of the terminologies. Challenges include inconsistent SNOMED CT quality, hierarchical limitations, adoption barriers, and the need for quantitative validation, yet the market for clinical terminology normalization software is growing rapidly—projected to reach $2.5 billion by 2027—driven by vendors such as Intelligent Medical Objects, Wolters Kluwer Health Language, Clinical Architecture, and Rhapsody, as well as emerging startups and recent funding rounds.

## LLM-based approaches for medical terminology mapping and normalization

Large language models are increasingly used to map and normalize clinical terminologies such as SNOMED CT, LOINC, ICD, and RxNorm. Approaches include fine-tuning LLMs, contrastive learning, retrieval-augmented generation, and multilingual semantic embeddings to improve cross-lingual and cross-system interoperability, with reported accuracies up to 0.99 for LOINC and substantial gains in SNOMED CT mapping.

**The MAP-CARE framework achieved Acc@5 = 0.90 in translating procedure classification codes across English, German, French, and Italian.**

MAP-CARE uses large language models and multilingual semantic embeddings to encode medical terminologies into a unified space, enabling cross-lingual retrieval and integration of medical procedure data. The framework was published in Scientific Reports in January 2026.

- Evidence: [LLM-augmented semantic embeddings enable Cross ...](https://www.nature.com/articles/s41598-025-34778-7)

**MAP-CARE's cross-classification mapping yielded exact and near matches exceeding 53.8% at the most granular level when aligning two national procedure classifications.**

This demonstrates the framework's ability to map between different national procedure classification systems (e.g., CHOP and OPS) beyond simple translation, supporting interoperability across heterogeneous healthcare systems.

- Evidence: [LLM-augmented semantic embeddings enable Cross ...](https://www.nature.com/articles/s41598-025-34778-7)

**A systematic review of automatic mapping of clinical terminologies reported that machine learning methods achieve up to 0.99 accuracy for LOINC, 0.954 for SNOMED-CT, and 0.952 for ICD using LightGBM.**

The review highlights the high performance of ML-based approaches, including LLMs, for mapping clinical codes across major terminologies, indicating strong potential for LLM-driven normalization pipelines.

- Evidence: [A systematic review of automatic mapping of clinical ...](https://www.sciencedirect.com/science/article/pii/S2590005626000585)

**A generative modeling study developed four LLM-based text normalization strategies for biomedical text, assessed in a preprint released October 1, 2024.**

The study built and evaluated text normalization pipelines using large language models to map clinical notes to standard terminologies, showcasing an LLM‑centric approach to biomedical text normalization.

- Evidence: [Biomedical Text Normalization through Generative Modeling](https://www.medrxiv.org/content/10.1101/2024.09.30.24314663v1.full-text)

**CDE‑Mapper, introduced May 7, 2025, combines retrieval‑augmented generation with large language models to link clinical concept descriptions to standardized codes.**

This framework leverages LLMs and retrieval‑augmented generation to improve mapping accuracy and adaptability for clinical data element linking across terminologies.

- Evidence: [Using Retrieval-Augmented Language Models for Linking ...](https://arxiv.org/html/2505.04365v1)


## Peer-reviewed evidence on accuracy of LLM-driven clinical code mapping

Empirical studies show that while integrating SNOMED CT with large language models often yields performance improvements, direct comparative evidence is limited. Exact code lookup accuracy for SNOMED CT, LOINC, and ICD codes using LLMs with retrieval-augmented generation remains modest (50–60%), reflecting the challenge of mapping to extensive terminologies such as SNOMED CT’s over 350,000 active concepts. Comparative analyses of RxNorm mapping have contrasted LLM-based approaches with specialized NLP tools, though specific accuracy figures vary across reports.

**In a review of studies integrating SNOMED CT with LLMs, 89% (17 out of 19) reported performance improvements, but only 51% (19 out of 37) provided direct comparisons.**

This indicates that while many studies observe improvements after adding SNOMED CT knowledge to LLMs, fewer than half of the surveyed studies offered head‑to‑head comparisons, limiting the strength of the evidence on accuracy gains.

- Evidence: [Use of SNOMED CT in Large Language Models - PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC11494256/)

**For exact medical code lookup (SNOMED CT, LOINC, or ICD) using LLMs with retrieval‑augmented generation, accuracy drops to 50–60% even when the correct code is present in the retrieval set.**

The modest accuracy highlights a substantial gap in precise code assignment despite access to correct candidates, suggesting that LLMs still struggle with fine‑grained terminology mapping tasks.

- Evidence: [LLMs and RAG for Medical Vocabulary Validation](https://papers.ssrn.com/sol3/Delivery.cfm/2e17a595-0ad3-4bb1-8970-c8ff41b5108f-MECA.pdf?abstractid=6545515&mirid=1)

**SNOMED CT contains more than 350,000 active concepts, illustrating the scale of the terminology that LLMs must map to.**

The large concept count underscores the difficulty of achieving high accuracy in automated mapping, as the model must disambiguate among hundreds of thousands of possible codes.

- Evidence: [ICD-10 has over 70000 codes. SNOMED CT contains more ...](https://www.instagram.com/p/DX1r4ylkbGF/)

**A 2024 blog post compared RxNorm code mapping accuracy among John Snow Labs' NLP tools, GPT‑4, and Amazon Comprehend Medical.**

The comparison aimed to evaluate state‑of‑the‑art performance, though the snippet did not provide specific accuracy numbers for each system.

- Evidence: [State-of-the-art RxNorm Code Mapping with NLP](https://www.johnsnowlabs.com/state-of-the-art-rxnorm-code-mapping-with-nlp-comparative-analysis-between-the-tools-by-john-snow-labs-amazon-and-gpt-4/)


## Challenges and limitations of AI in medical terminology normalization

AI-driven approaches to medical terminology normalization face several persistent challenges, including inconsistencies in SNOMED CT quality, hierarchical limitations of the terminology, adoption barriers due to complexity, reliance on quantitative validation for LLM/RAG methods, and ongoing difficulties in achieving full interoperability across electronic health records despite automation efforts.

**A survey of SNOMED CT implementations reported quality challenges, with only one implementation (n=1) achieving consistency.**

The survey highlighted consistency as a key quality challenge, indicating that most implementations struggled to achieve consistent use of SNOMED CT across settings.

- Evidence: [A survey of SNOMED CT implementations - PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC7185627/#:~:text=SNOMED%20CT%20quality%20challenges,consistency%20(n%20%3D%201).)

**SNOMED CT's hierarchical limitations create challenges for maintaining inter-institutional consistency in clinical term mapping.**

A LOINC article notes that challenges in maintaining inter-institutional consistency and addressing SNOMED CT's hierarchical limitations were only mitigated with a detailed mapping manual, suggesting the hierarchy hinders straightforward mapping.

- Evidence: [Mapping clinical terms to standard terminology for multi- ...](https://loinc.org/articles/mapping-clinical-terms-to-standard-terminology-for-multi-institutional-research-platform-mapping-principles-and-system-deployment)

**The complexity of SNOMED CT and its reimbursement coding system presents a barrier to adoption in healthcare facilities.**

A Chegg Q&A states that the barrier to adopting SNOMED includes its complex use and the need for a numerical coding system for reimbursement, indicating practical adoption hurdles.

- Evidence: [Solved The barrier to adopting SNOMED for healthcare | Chegg.com](https://www.chegg.com/homework-help/questions-and-answers/barrier-adopting-snomed-healthcare-facility-coding--complex-use-reimbursement-coding-syste-q117123863#:~:text=It%20helps%20in%20facilitating%20the%20electronic%20exchange%20of%20health%20data.&text=Therefore%2C%20the%20barrier%20to%20adopting,include%20a%20numerical%20coding%20system.%22)

**LLM- or RAG-based approaches to clinical terminology validation require quantitative reporting, suggesting a lack of standardized qualitative benchmarks.**

The SSRN paper's eligibility criteria mandated that studies examine LLM or RAG systems applied to clinical terminology tasks and report quantitative results, implying that qualitative assessment alone is insufficient for validation.

- Evidence: [LLMs and RAG for Medical Vocabulary Validation](https://papers.ssrn.com/sol3/Delivery.cfm/2e17a595-0ad3-4bb1-8970-c8ff41b5108f-MECA.pdf?abstractid=6545515&mirid=1)

**Automatic mapping of clinical terminologies remains challenging for ensuring interoperability across electronic health records, despite its importance for standardization.**

A 2026 systematic review emphasizes that automated mapping is important for standardizing clinical data and ensuring interoperability, yet acknowledges that significant challenges persist in achieving reliable cross-EHR mapping.

- Evidence: [A systematic review of automatic mapping of clinical ...](https://www.sciencedirect.com/science/article/pii/S2590005626000585)


## Startups, funding, and commercial vendors in clinical terminology normalization software

The clinical terminology normalization software market is experiencing robust growth, with established vendors like Intelligent Medical Objects (IMO) and Wolters Kluwer driving innovation through funding, product launches, and market expansion. IMO secured a $10.0 million growth investment from Warburg Pincus in 2016 and launched IMO Studio in 2023, while the overall market is projected to reach $2.5 billion by 2027. Wolters Kluwer maintains a leading position through its Health Language solutions, reflecting sustained vendor activity in this expanding sector.

**In October 2016, Intelligent Medical Objects (IMO) announced a growth investment from Warburg Pincus to support its expansion, with a co-investment case study specifying the amount as $10.0 million.**

The investment was intended to drive the expansion of IMO and the semantic highway for the health information ecosystem. This funding event highlights ongoing investor interest in established clinical terminology vendors.

- Evidence: [Intelligent Medical Objects (IMO) Announces Growth ...](https://www.prnewswire.com/news-releases/intelligent-medical-objects-imo-announces-growth-investment-from-warburg-pincus-300341240.html)
- Evidence: [Co-investment Case Study: Intelligent Medical Objects (“ ...](https://www.nb.com/handlers/documents.ashx?id=054e693c-9735-475f-83e5-632228a20284&name=IMO+case+study+slide)

**The medical terminology software market was valued at USD 1.18 billion in 2023 and is projected to grow at a rate of 18.42% annually from 2024 to 2030.**

This data point from a competitive analysis underscores the significant and expanding market opportunity for clinical terminology normalization software vendors.

- Evidence: [Medical Terminology Software Companies : Wolters Kluwer](https://www.maximizemarketresearch.com/competitive-analysis/medical-terminology-software-companies/260646/)

**The global medical terminology software market is projected to reach USD 2.5 billion by 2027, up from USD 1.0 billion in 2022, at a CAGR of 19.3%.**

This 2022 market forecast indicates strong growth driven by efforts to minimize medical errors and government healthcare IT adoption initiatives, creating a favorable environment for vendors.

- Evidence: [Intelligent Medical Objects, Inc. (US) and Wolters Kluwer ...](https://www.marketsandmarkets.com/ResearchInsight/medical-terminology-software-market.asp)

**On April 17, 2023, Intelligent Medical Objects launched IMO Studio, a cloud-based platform for clinical terminologies, code sets, and data quality.**

IMO Studio enables a holistic data quality strategy for healthcare organizations, demonstrating the vendor's commitment to innovation in clinical terminology normalization.

- Evidence: [Intelligent Medical Objects Launches Cloud-Based ...](https://www.businesswire.com/news/home/20230417005328/en/Intelligent-Medical-Objects-Launches-Cloud-Based-Platform-for-Clinical-Terminologies-Code-Sets-and-Data-Quality)

**Wolters Kluwer N.V. is a leading player in the global medical terminology software market, offering terminology solutions through its Health Language subsidiary.**

Wolters Kluwer maintains a strong global presence in Europe, North America, Asia, and the Middle East, and has sustained its market position through continuous innovation, such as integrating with practice management systems to standardize terminology.

- Evidence: [Intelligent Medical Objects, Inc. (US) and Wolters Kluwer ...](https://www.marketsandmarkets.com/ResearchInsight/medical-terminology-software-market.asp)
- Evidence: [Health Language Solutions: Simplifying Healthcare Data](https://www.wolterskluwer.com/en/solutions/health-language)


## Risks and uncertainties

- Inconsistent quality and consistency of SNOMED CT implementations across healthcare settings.
- Hierarchical limitations of SNOMED CT hindering inter‑institutional consistency in term mapping.
- Complexity and reimbursement coding demands of SNOMED CT creating adoption barriers for healthcare facilities.
- Lack of standardized qualitative benchmarks; LLM/RAG validation relies heavily on quantitative metrics.
- Persistent difficulties achieving full interoperability across electronic health records despite automated mapping efforts.
- Limited direct comparative evidence in studies integrating LLMs with SNOMED CT, weakening confidence in reported performance gains.
- Modest exact‑code lookup accuracy (50–60%) for LLMs using retrieval‑augmented generation when mapping to large terminologies such as SNOMED CT.

## Conflicting information

- Discrepancy in reported accuracy for LOINC mapping: a systematic review of automatic clinical terminology mapping cites machine‑learning methods achieving up to 0.99 accuracy for LOINC, whereas peer‑reviewed evaluations of LLMs with retrieval‑augmented generation report exact‑code lookup accuracies dropping to 50–60% for LOINC (and similarly for SNOMED CT and ICD).

## What to watch next

- Biannual SNOMED CT releases (July 2025 and January 2026) and their impact on mapping accuracy and consistency.
- Follow‑up validation studies of the MAP‑CAR​E framework after its January 2026 publication, assessing cross‑lingual and cross‑classification performance in additional languages and national procedure classifications.
- Release of CDE‑Mapper updates post its May 7 2025 launch, particularly any version that improves retrieval‑augmented generation linking of clinical concept descriptions to standardized codes.
- Publication of peer‑reviewed comparative studies evaluating LLM‑based RxNorm mapping against specialized NLP tools (e.g., John Snow Labs, Amazon Comprehend Medical) expected in late 2025‑early 2026.
- Market reports tracking the clinical terminology normalization software sector toward the projected $2.5 billion valuation by 2027, including yearly updates on adoption of IMO Studio, Wolters Kluwer Health Language solutions, and emerging startup funding rounds.

## Sources

1. [Recent Developments in Clinical Terminologies — SNOMED ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC6115234/)
2. [Development and Evaluation of SNOMED CT Automated ...](https://medinform.jmir.org/2026/1/e82670)
3. [Data alignment to ICD10, SNOMED, CPT, HCPCS, LOINC, ...](https://marketplace.databricks.com/details/b62bb102-c5f5-4f9a-bd89-38a5a2028e0b/Intelligent-Medical-Objects-IMO_Data-alignment-to-ICD10-SNOMED-CPT-HCPCS-LOINC-CVx-RxNorm-NDC-and-more)
4. [SNOMED CT: Why it matters to you](https://www.wolterskluwer.com/en/expert-insights/snomed-ct-why-it-matters-to-you)
5. [IMO - Intelligent Medical Objects](https://www.snomed.org/snomed-ct-marketplace/imo---intelligent-medical-objects)
6. [LLMs excel in medical coding with terminology, clinical AI](https://www.imohealth.com/resources/can-llms-excel-in-medical-coding-yes-with-rich-semantics-and-clinical-ai/)
7. [State-of-the-art RxNorm Code Mapping with NLP](https://www.johnsnowlabs.com/state-of-the-art-rxnorm-code-mapping-with-nlp-comparative-analysis-between-the-tools-by-john-snow-labs-amazon-and-gpt-4/)
8. [Drugs making a mess of your data? How mapping ...](https://www.wolterskluwer.com/en/expert-insights/drugs-making-a-mess-of-your-data)
9. [LLMs and RAG for Medical Vocabulary Validation](https://papers.ssrn.com/sol3/Delivery.cfm/2e17a595-0ad3-4bb1-8970-c8ff41b5108f-MECA.pdf?abstractid=6545515&mirid=1)
10. [Use of SNOMED CT in Large Language Models - PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC11494256/)
11. [ICD-10 has over 70000 codes. SNOMED CT contains more ...](https://www.instagram.com/p/DX1r4ylkbGF/)
12. [FHIRBench: Benchmarking FHIR Clinical Data ...](https://www.medrxiv.org/content/10.64898/2026.07.14.26358020v1.full)
13. [Use Case Scenarios | Implementation Guides LOINC ...](https://docs.snomed.org/implementation-guides/loinc-implementation-guide/use-case/3.2-use-case-scenarios)
14. [Journal articles referencing LOINC](https://loinc.org/articles)
15. [A systematic review of automatic mapping of clinical ...](https://www.sciencedirect.com/science/article/pii/S2590005626000585)
16. [LLM-augmented semantic embeddings enable Cross ...](https://www.nature.com/articles/s41598-025-34778-7)
17. [Biomedical Text Normalization through Generative Modeling](https://www.medrxiv.org/content/10.1101/2024.09.30.24314663v1.full-text)
18. [Automated LOINC Standardization Using Pre-trained Large ...](https://proceedings.mlr.press/v193/tu22a/tu22a.pdf)
19. [LLMs in Medical Concept Normalization: A Cost-Effective ...](https://www.linkedin.com/posts/briankfung_rxnorm-fhir-activity-7467245884976701440-9kvI)
20. [Using Retrieval-Augmented Language Models for Linking ...](https://arxiv.org/html/2505.04365v1)
21. [Fine-Tuning Methods for Large Language Models in Clinical ...](https://pubmed.ncbi.nlm.nih.gov/40986888/#:~:text=The%202%20common%20fine%2Dtuning,medicine%20or%20health%20care%20operations.)
22. [IMO Health: AI-Native Clinical Data Intelligence](https://www.imohealth.com/)
23. [Intelligent Medical Objects, Inc. (US) and Wolters Kluwer ...](https://www.marketsandmarkets.com/ResearchInsight/medical-terminology-software-market.asp)
24. [Medical Terminology Software Companies : Wolters Kluwer](https://www.maximizemarketresearch.com/competitive-analysis/medical-terminology-software-companies/260646/)
25. [Health Language Solutions: Simplifying Healthcare Data](https://www.wolterskluwer.com/en/solutions/health-language)
26. [Co-investment Case Study: Intelligent Medical Objects (“ ...](https://www.nb.com/handlers/documents.ashx?id=054e693c-9735-475f-83e5-632228a20284&name=IMO+case+study+slide)
27. [Intelligent Medical Objects (IMO) Announces Growth ...](https://www.prnewswire.com/news-releases/intelligent-medical-objects-imo-announces-growth-investment-from-warburg-pincus-300341240.html)
28. [Intelligent Medical Objects: IMO Precision Normalize](https://app.snowflake.com/marketplace/listing/GZT1Z17AWEE?businessNeed=27)
29. [Intelligent Medical Objects Launches Cloud-Based ...](https://www.businesswire.com/news/home/20230417005328/en/Intelligent-Medical-Objects-Launches-Cloud-Based-Platform-for-Clinical-Terminologies-Code-Sets-and-Data-Quality)
30. [IMO - Intelligent Medical Objects - SNOMED International](https://www.snomed.org/snomed-ct-marketplace/imo---intelligent-medical-objects#:~:text=IMO%20%2D%20Intelligent%20Medical%20Objects)
31. [Standardized Vocabularies Boost Interoperability: LOINC & SNOMED ...](https://www.clinisys.com/int/en/resources/standardized-vocabularies-boost-interoperability-loinc-snomed-ct/#:~:text=LOINC%20includes%20codes%20that%20identify,codes%20for%20non%2Dnumeric%20answers.)
32. [A survey of SNOMED CT implementations - PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC7185627/#:~:text=SNOMED%20CT%20quality%20challenges,consistency%20(n%20%3D%201).)
33. [Solved The barrier to adopting SNOMED for healthcare | Chegg.com](https://www.chegg.com/homework-help/questions-and-answers/barrier-adopting-snomed-healthcare-facility-coding--complex-use-reimbursement-coding-syste-q117123863#:~:text=It%20helps%20in%20facilitating%20the%20electronic%20exchange%20of%20health%20data.&text=Therefore%2C%20the%20barrier%20to%20adopting,include%20a%20numerical%20coding%20system.%22)
34. [SNOMED CT to ICD-10-CM Map - National Library of Medicine](https://www.nlm.nih.gov/research/umls/mapping_projects/snomedct_to_icd10cm.html#:~:text=It%20is%20designed%20for%20use,for%20reimbursement%20and%20statistical%20purposes.)
35. [(PDF) A systematic review of automatic mapping of clinical ...](https://www.researchgate.net/publication/401489043_A_systematic_review_of_automatic_mapping_of_clinical_terminologies)
36. [Mapping clinical terms to standard terminology for multi- ...](https://loinc.org/articles/mapping-clinical-terms-to-standard-terminology-for-multi-institutional-research-platform-mapping-principles-and-system-deployment)
