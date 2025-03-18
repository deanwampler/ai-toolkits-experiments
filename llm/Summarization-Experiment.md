# Summarization Experiment

## Using `llm` with Granite 3.2

```shell
cat ~/Downloads/FA5_\ Open\ Trusted\ Data\ Initiative\ -\ 2025\ One-Page\ Overview.md | llm --system 'summarize the input text' --model granite3.2
```
### Result

The Open Dataset Initiative (OTDI) aims to establish a comprehensive, enterprise-ready, and open-access catalog of datasets that meet specific provenance and governance criteria. The initiative is divided into four workstreams:

1. **Workstream 3: Maintain the industry-leading catalog of open datasets**
   - This workstream focuses on creating and managing a catalog that lists all known datasets conforming to OTDI's criteria. It includes outreach for new dataset discovery, recruitment of a review committee, schema definition, metadata management system development, and regular updates to the catalog with validation pipelines.

2. **Workstream 4: Evangelize OTDI**
   - This workstream aims to promote OTDI through various communication channels such as blog posts, conference talks, workshops, and training materials. The goal is to increase awareness and establish OTDI as the go-to resource for enterprise-ready open datasets.

3. **Workstream 2: Maintain the industry-leading catalog of open datasets**
   - This workstream focuses on implementing and enhancing the technical infrastructure required for managing the dataset catalog. It includes the development of pipeline execution stacks, validation pipelines, and data transformation pipelines to ensure the accuracy and consistency of listed datasets.

4. **Workstream 1: Implement the V0.1 pipeline execution stack and the V0.1 validation pipeline**
   - This workstream is responsible for initial implementation of the pipeline infrastructure required for executing validation checks on submitted datasets, identifying potential improvements or additional pipelines needed in later stages.

Staffing requirements for these workstreams include software engineers, DevRel professionals, and background efforts from OTDI participants for outreach and dataset discovery. Contributions may also be sought from the AI Alliance community, marketing teams, and organizations focusing on data aggregation and processing.

Some additional ideas for discussion:

- **Dataset Conformance Rating**: Implement a rating system to differentiate datasets based on their level of conformance to OTDI's criteria. This could help users identify the most reliable sources quickly.

- **Collaboration with Existing Platforms/Initiatives**: Explore partnerships or collaborations with existing data platforms or initiatives (e.g., Kaggle, Google Dataset Search) to enhance OTDI's reach and impact while leveraging their infrastructure and user base.

- **User Feedback Mechanisms**: Develop mechanisms for users to provide feedback on datasets listed in the catalog, helping maintain quality standards and facilitating continuous improvement of OTDI's offerings.

- **Dataset Versioning**: Implement a versioning system for datasets to track changes over time, ensuring transparency and enabling users to revert to previous versions if needed.

- **Privacy Considerations**: Assess privacy implications related to dataset sharing, especially concerning sensitive data, and develop guidelines or tools to help creators anonymize or pseudonymize their datasets where necessary.

## Using `llm` with `gpt-4o-mini`

```shell
cat ~/Downloads/FA5_\ Open\ Trusted\ Data\ Initiative\ -\ 2025\ One-Page\ Overview.md | llm --system 'summarize the input text' --model gpt-4o-mini
```

### Result

The Open Trusted Data Initiative (OTDI) aims to improve the clarity of dataset development, provenance, governance, and licensing, providing a trustworthy catalog for open-access datasets. The initiative seeks to define criteria for dataset quality and create a catalog, increasing user confidence in data usage. Key objectives include establishing OTDI as a leading resource for open-access datasets and demonstrating value through effective governance and provenance guidance. The plan outlines specific key results (KRs) for each objective, focusing on monthly views, dataset additions, and citations.

The execution will involve several workstreams: maintaining dataset governance requirements, developing validation pipelines, managing an industry-leading dataset catalog, and promoting OTDI awareness. Goals for 2025 and 2028 include significant financial investments and vast data collection, with staffing requirements outlined for each workstream.

Key areas for discussion include developing a conformity rating for datasets to differentiate levels of compliance. The initiative encourages feedback and collaboration from AI Alliance members and external organizations.

## Using `llm` with `Meta-Llama-3-8B-Instruct`

```shell
cat ~/Downloads/FA5_\ Open\ Trusted\ Data\ Initiative\ -\ 2025\ One-Page\ Overview.md | llm --system 'summarize the input text' --model Meta-Llama-3-8B-Instruct
```

### Result

ERROR: The prompt size exceeds the context window size and cannot be processed.

More work TODO