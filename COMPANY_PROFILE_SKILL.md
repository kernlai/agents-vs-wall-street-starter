---
name: company-profile
description: Build lightweight company profiles as structured JSON.
version: 0.3.0
author: Kaylan, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Finance, Company-Research, Forecasting, JSON]
    related_skills: []
---

# Company Profile Skill

## Mission

Build a lightweight, company-specific profile that explains how a company operates, reports, and is economically influenced. The profile is an orientation layer for a later worker that will define metric-specific forecasting signals.

Return one machine-readable JSON object. Make the profile specific enough to distinguish the company and its industry, but stop before detailed evidence extraction, signal selection, modelling, scenarios, or forecasting.

## Core principles

1. **Company-specific, not boilerplate.** Include only information that materially improves understanding of this company.
2. **Structured, not rigid.** Populate a stable common core and use flexible arrays for industry- and company-specific concepts.
3. **Lightweight by default.** Use the smallest authoritative source set that can satisfy the profile contract.
4. **Metric-aware, not metric-led.** Optional target metrics may change emphasis, but they must not turn profile construction into signal research.
5. **Repository first.** Prefer the supplied historical corpus, then use public research only for a material unresolved gap.
6. **Evidence-grounded.** Give every externally verifiable claim claim-level source IDs that resolve to an inspected source-log entry. Never treat a search result or snippet as a reviewed source.
7. **Facts and judgments are distinct.** Mark reported facts, calculations, model judgments, assumptions, and unknowns explicitly. A citation to underlying evidence does not turn a model judgment into a reported fact.
8. **Explicit uncertainty.** Use `null`, empty arrays, and gap records rather than inventing missing facts.
9. **JSON only.** The final response must contain valid JSON with no Markdown fence, preamble, commentary, or trailing text.

## Boundaries

This skill must not:

- select, score, weight, or combine forecasting signals;
- collect detailed evidence for potential signals;
- extract long historical financial series;
- calculate forecasts, scenarios, valuations, or price targets;
- build detailed segment, margin, EPS, or accounting models;
- perform exhaustive competitor, macroeconomic, political, or regulatory research;
- write to a workbook or submission template;
- provide investment recommendations;
- fill fields with generic risk boilerplate merely for completeness;
- present assumptions, interpretations, or unsupported search snippets as reported facts.

The profile should explain **what may matter and where later workers may need to look**. It should not determine **what the final signals are or what they imply for the forecast**.

## Evidence, interpretation, and provenance policy

Every non-null narrative claim, classification, calculation, or assumption must declare one `basis` value:

- `reported_fact`: a faithful quote or paraphrase of an inspected source;
- `calculated`: simple arithmetic derived from reported facts, never a forecast or model output;
- `model_judgment`: an interpretation, synthesis, relative assessment, or materiality classification made by the profile author;
- `assumption`: an explicitly stated premise not established as fact by the inspected sources;
- `unknown`: the value is unresolved and is not being inferred.

Use the sourced-claim shape for narrative fields and string-array items:

```json
{
  "statement": "The company primarily sells through company-operated stores.",
  "basis": "reported_fact",
  "source_ids": ["SRC-001"],
  "source_locators": {
    "SRC-001": "Item 1, Business"
  }
}
```

`source_locators` is optional. Prefer stable headings, filing items, footnotes, tables, or page labels. Use a repository line range only when it refers to the exact fixed file inspected. Never invent a locator, and never use an unstable search-result position.

Apply these invariants:

- `reported_fact` requires one to three `source_ids` that directly support the claim.
- `calculated` requires one to three `source_ids` plus a concise `rationale` containing the inputs and arithmetic method.
- `model_judgment` requires one to three `source_ids` plus a concise `rationale`—or the contract-specific `*_rationale` field—explaining how the cited facts support—but do not themselves state—the conclusion. When a judgment is based solely on caller input, use `source_ids: []` and identify the normalized input path in `input_fields` instead.
- `assumption` requires a concise `rationale`; normally use `source_ids: []`. Add `input_fields` when the premise came from caller input. Do not use an assumption to fill a missing company fact that belongs in `uncertainties_and_gaps`.
- `unknown` requires a null claim value or classification and `source_ids: []`; add a gap record when the unknown is material.
- Every source ID must resolve to exactly one entry in `sources`. Do not put URLs, repository paths, or unregistered IDs directly in claim objects.
- `input_fields` may identify only normalized caller-input paths; it is not a replacement for source IDs on externally verifiable company claims.
- `source_locators`, when present, may contain only keys already listed in that claim's `source_ids`.
- Cite the strongest direct source for the claim; do not attach every reviewed source. Use multiple IDs only for corroboration, synthesis, or a documented conflict.
- Source-log `used_for` is a section inventory, not a substitute for claim-level `source_ids`.

For grouped scalars in `company_identity`, `reporting_context`, and `metric_lenses`, use `field_provenance` to map each non-null externally verifiable field to its `basis`, supporting source IDs, required rationale, and optional locators. Input-derived metadata uses `input_fields` instead of external source IDs.

Before returning, perform this provenance validation pass:

1. Build the set of unique IDs from `sources`.
2. Traverse every claim object, assessment, structured profile item, gap, and `field_provenance` entry.
3. Apply the conditional basis rules and reject missing or disallowed evidence fields.
4. Reject every source ID not present exactly once in the source set.
5. Reject locator keys that are absent from the enclosing `source_ids`.
6. Reject non-null grouped scalar fields without same-named provenance entries and provenance entries for null or nonexistent fields.
7. For each conflict, verify that every distinct reported reading is a separate sourced claim.

## Input contract

### Required inputs

```json
{
  "company": {
    "name": "Example Company",
    "ticker": "EXM"
  },
  "as_of_date": "2026-08-16"
}
```

Required rules:

- `company.name` must be non-empty.
- `company.ticker` should be supplied when available. If name or ticker is ambiguous, require an exchange, jurisdiction, or other reliable identifier.
- `as_of_date` must be an ISO `YYYY-MM-DD` date and acts as the default research cutoff.
- Do not use information published after the effective research cutoff.

### Optional inputs

```json
{
  "company": {
    "name": "Example Company",
    "ticker": "EXM",
    "exchange": "LSE",
    "jurisdiction": "United Kingdom"
  },
  "as_of_date": "2026-08-16",
  "research_cutoff": "2026-08-14",
  "target_period": "FY2026",
  "target_metrics": [
    {
      "label": "Net fees",
      "units": "GBPm"
    }
  ],
  "source_policy": {
    "repository_first": true,
    "public_research_allowed": true
  }
}
```

Defaults:

- `research_cutoff` defaults to `as_of_date`.
- `target_period` defaults to `null`.
- `target_metrics` defaults to `[]`.
- `source_policy.repository_first` defaults to `true`.
- `source_policy.public_research_allowed` defaults to `true`.
- The skill must work when no target metrics are supplied.

### Invocation inputs versus repository metadata

Populate `target_period` and `target_metrics_supplied` only from normalized invocation inputs. A company index, challenge configuration, filename, workbook, or other repository metadata is discovery context—not caller input—unless the caller or invocation wrapper explicitly passes those values through the input contract.

When no target period or metrics are supplied, return `target_period: null`, `target_metrics_supplied: []`, and `metric_lenses: []`. Do not infer challenge metrics merely because they exist elsewhere in the repository.

### Input failure behaviour

Return `status: "error"` rather than guessing when:

- the company cannot be identified unambiguously;
- the required company name or cutoff is missing;
- the cutoff is invalid;
- supplied identifiers refer to conflicting entities.

Use an error such as:

```json
{
  "code": "AMBIGUOUS_COMPANY",
  "message": "The supplied identity matches multiple public companies.",
  "required_information": ["ticker", "exchange"]
}
```

## Metric-specific adaptation

Treat target metrics as relevance hints. First construct the general company profile, then decide whether a metric warrants additional emphasis.

### Generic metrics

Typical characteristics:

- company-wide standard financial-statement measure;
- not restricted to a segment, geography, customer type, or operational definition;
- broadly driven by the entire company.

Examples include total revenue, total net income, and total diluted EPS.

Behaviour:

- do not open an additional source by default;
- do not broaden research;
- rely on the general profile;
- add either no metric lens or a minimal lens explaining why no special treatment is needed.

### Moderately specific metrics

Typical characteristics:

- company-defined or adjusted measure;
- operational KPI;
- measure with a non-obvious definition or accounting basis;
- measure whose meaning depends on the company's business model.

Examples include adjusted gross margin, comparable sales, and net fees.

Behaviour:

- search the selected core sources for the exact term and close variants;
- establish the company definition, scope, basis, units, and reporting frequency where available;
- identify only the business areas required to understand the metric;
- do not automatically open an additional source.

### Highly specific metrics

Typical characteristics:

- limited to a named segment or geography;
- company-defined operating measure with narrow scope;
- dependent on a particular channel, product, customer group, or accounting convention.

Examples include segment operating profit and regional operating KPIs.

Behaviour:

- search the core sources first;
- permit one additional official source if the definition or scope remains materially unresolved;
- add stronger emphasis to relevant segment, geography, reporting, and operating-model context;
- stop before historical extraction, signal selection, or modelling.

### Metric lens constraints

A metric lens may contain only:

- supplied metric label;
- specificity and the reason for that classification;
- company definition where available;
- scope, units, accounting basis, and reporting frequency;
- relevant business areas;
- additional profile emphasis;
- unresolved definition questions.

It must not contain:

- candidate signal scores or weights;
- detailed evidence records;
- historical values;
- forecast assumptions;
- scenarios or forecasts.

## Research policy

### Source hierarchy

Prefer sources in this order:

1. latest annual report or equivalent authoritative filing;
2. latest quarterly, half-year, or full-year results filing;
3. filed earnings release or official trading update;
4. official investor presentation;
5. earnings-call prepared remarks;
6. earnings-call Q&A;
7. other official company, regulator, or exchange material;
8. credible public secondary source.

Never cite or rely on a search snippet as if the underlying source was reviewed.

### Repository-first discovery

When a supplied corpus contains a company index, inspect that index before searching individual documents. Use document metadata—publication date, type, reporting period, and title—to shortlist sources.

Do not select documents merely because they are newest. Exclude by default:

- voting-rights notices;
- routine director or shareholder transaction notices;
- daily buyback logs;
- proxy voting materials;
- AGM voting results;
- duplicate copies of the same disclosure;
- minor administrative announcements;
- conference appearances that add no material company context.

### Default source set

Select no more than three core repository documents:

1. **Latest annual report:** stable business model, products, customers, segments, geographies, fiscal context, accounting, and structural exposures.
2. **One latest results source:** choose the quarterly or half-year filing when accounting, segments, balance sheet, or working capital is material; choose the filed earnings release or official trading update when guidance and current operating conditions are the main need.
3. **Latest useful earnings call or investor presentation:** management framing, operational drivers, cyclicality, seasonality, and company-specific concepts.

Do not use both the periodic filing and earnings release as core sources for the same period. Open the second only under the optional-document rule when a material field remains unresolved. Treat a repository index as source-discovery metadata, not a source-log entry; substantive claims must come from an inspected underlying document.

Permit one optional repository document only when:

- a highly specific metric remains undefined;
- material segment or geographic scope remains unclear;
- a major acquisition, disposal, or reorganization makes the annual report stale;
- an essential reporting convention cannot otherwise be established.

A generic metric must not, by itself, trigger an additional source.

### Public research

Public research is a fallback, not the default expansion path.

Use it only when:

- identity cannot otherwise be resolved;
- a material corporate change occurred after the latest useful repository source but before the cutoff;
- a required profile field remains materially unresolved;
- a highly specific metric needs an official definition unavailable in the corpus;
- a central external exposure cannot be understood from company materials.

Limits:

- use no public sources by default;
- use at most two public sources;
- prefer official company, regulator, or exchange sources;
- perform one targeted public-research pass;
- record the reviewed page URL, not a search-results URL;
- do not start broad industry or macroeconomic research.

### Lightweight research budget

Default ceilings:

| Resource | Limit |
|---|---:|
| Core repository documents | 3 |
| Optional repository document | 1 |
| Public sources | 0 by default; maximum 2 |
| Targeted corpus searches | Approximately 6–10 |
| Gap-resolution passes | 1 |
| Initial metadata per selected document | Up to 2,000 characters |
| Context per retained search match | Approximately 1,000–1,500 characters |
| Retained matches per search topic | Usually 1–2 |
| Broad follow-up section reads | Maximum 2 across the profile |
| Unique extracted source text | Target 50,000–65,000 characters; hard stop at 72,000 |
| Extracted-source token guide | Approximately 12,000–18,000 tokens; model-dependent |
| Final JSON | Target 14,000 characters; hard stop 16,000; approximately 2,000–3,500 tokens |
| Source-log entries | Usually 3–6 |
| Target runtime | Approximately 8–12 minutes |

These are ceilings, not targets. Finish earlier when the contract is already satisfied. Character counts are the enforceable extraction control because token counts vary by model and tokenizer.

Count only unique source text returned into the working context, including retained metadata and excerpts. Count overlapping passages once. A search operation may scan a full selected document internally, but it must return only bounded excerpts; never print or load a full document merely to search it.

At 50,000 extracted characters, review the coverage matrix in Step 4 and permit further extraction only for an unresolved material row. At 65,000 characters, stop normal extraction. At the 72,000-character hard stop, record any remaining material issue in `uncertainties_and_gaps` rather than loading more source text.

## Materiality test

Include an item only if it materially helps answer at least one of these questions:

1. How does the company generate revenue or earnings?
2. How is the company operationally organized?
3. How does it define and report financial performance?
4. What causes its business economics to vary?
5. What company-specific concept may matter to later signal discovery?
6. What material external exposure shapes the business?
7. What context is necessary to understand a supplied specific metric?

Exclude:

- generic risk language with no clear company connection;
- exhaustive product, legal-entity, or country lists;
- immaterial subsidiaries or markets;
- detailed executive biographies;
- governance details unrelated to company operation;
- detailed historical figures not needed for orientation;
- generic macroeconomic commentary without a clear transmission mechanism;
- unsupported market-share claims;
- speculative signal ideas.

## Procedure

### Step 1: Validate and normalize the request

- Validate required inputs.
- Normalize obvious company-name and ticker formatting without changing the entity.
- Resolve identity using the supplied exchange or jurisdiction where necessary.
- Set the effective research cutoff.
- Preserve the original target metric labels and units.
- Keep repository-discovered periods and metrics separate from normalized invocation inputs.

Completion criterion: one company and one cutoff are unambiguous, or return `status: "error"`.

### Step 2: Classify target-metric specificity

For each supplied metric, classify it as `generic`, `moderate`, or `high`. Record a concise reason based on scope, company-specific terminology, accounting basis, segment/geographic restriction, and reporting practice.

Do not classify a metric as specific merely because its label is unfamiliar. Verify whether the company defines it specially.

Completion criterion: every supplied metric has a justified classification, even if a generic metric ultimately receives no lens.

### Step 3: Build a source plan from metadata

- Inspect the company index or equivalent source inventory.
- Identify the latest useful annual report before the cutoff.
- Choose one latest periodic filing or results release before the cutoff using the default-source decision rule.
- Identify the latest useful call or presentation before the cutoff.
- Remove duplicate or administratively irrelevant candidates.
- Confirm that an index and a second same-period results document are not being counted as core sources.
- Add an optional fourth document only if permitted by the gap or metric rules.
- Record the exact selected paths and initialize the extracted-character counter before substantive extraction.

Completion criterion: the smallest defensible source set has been selected before substantive extraction begins.

### Step 4: Extract only orientation-level information

Use this mandatory search-first sequence:

1. Read only the frontmatter, title, table of contents where available, and at most 2,000 initial metadata characters from each selected document.
2. Search only the selected documents. Do not search the full company corpus after the source plan has been fixed unless Step 6 authorizes the optional document.
3. Run approximately 6–10 targeted searches covering the topics below. Combine closely related concepts into one search rather than issuing one search per output field.
4. Retain only the best one or two matches per topic, with approximately 1,000–1,500 characters of context per match.
5. Deduplicate overlapping passages before adding them to the extracted-character counter.
6. Open a broader source section only when a retained excerpt cannot be interpreted safely in context. Permit no more than two such section reads across the entire profile.
7. Update an internal coverage matrix and the cumulative unique-character count after each extraction batch.

Search topics:

- business model, products, services, customers, channels, and end markets;
- segments, geographies, and material operating footprint;
- fiscal calendar, reporting currency, accounting basis, adjusted measures, and company terminology;
- broad revenue, cost, margin, earnings, capital-intensity, and working-capital drivers;
- cyclicality, seasonality, and timing factors;
- guidance cadence, metrics, format, and characteristics;
- material industry, macroeconomic, political, geographic, regulatory, currency, commodity, and technology exposures;
- exact supplied metric terms when moderate or highly specific.

The internal coverage matrix must contain one row for each of these areas: identity and cutoff; business model and revenue model; products and customers; segments and geographies; reporting and accounting context; financial drivers; cyclicality and seasonality; guidance practice; external exposures; current material changes; and supplied metric definitions. Mark each row `supported`, `not_materially_applicable`, or `gap_recorded`, and retain the supporting source ID or gap topic. The matrix is working state and must not be added to the final JSON.

Use `search_files` for bounded content searches when available. Scope each call to the selected document or its exact directory and filter results back to the selected paths. If `search_files` is unavailable or its search backend is missing, use `execute_code` with standard-library `pathlib` and regular expressions to read only the selected paths and print bounded excerpts. The fallback must not import project modules, create indexes or notes, or write files. Do not invoke a repository helper whose write scope is unknown.

Do not extract full documents, hundreds of consecutive lines, or detailed historical series. Do not use `read_file` on a large document before targeted searching except for the bounded metadata read above. Capture only concise facts and relationships sufficient to populate the JSON contract.

Completion criterion: every coverage row is `supported`, `not_materially_applicable`, or `gap_recorded`; selected paths and source IDs are known; overlapping excerpts are deduplicated; and the cumulative unique extracted text remains at or below 72,000 characters.

### Step 5: Apply the materiality and company-specificity filter

For every proposed item:

- confirm it is supported by an inspected source;
- confirm it materially improves company orientation;
- classify it as `reported_fact`, `calculated`, `model_judgment`, `assumption`, or `unknown`;
- attach claim-level `source_ids` under the evidence rules above;
- add a `rationale` when the basis is `calculated`, `model_judgment`, or `assumption`;
- remove generic statements that could describe most companies;
- consolidate duplicates;
- retain only the principal products, customers, segments, geographies, drivers, and exposures;
- move unresolved material questions to `uncertainties_and_gaps`.

Completion criterion: the retained content is recognizably specific to the company; every non-null claim has an explicit basis and valid provenance; and no filler was added solely to populate fields.

### Step 6: Resolve material gaps once

Run one bounded follow-up pass only when a missing item would materially impair the profile or a highly specific metric lens.

- Search the selected corpus more narrowly first.
- Open the optional fourth repository source if justified.
- Use at most two public sources if the repository cannot resolve the gap and public research is allowed.
- Keep the combined total of broad follow-up section reads at two or fewer.
- Apply the same excerpt limits and cumulative character counter to repository and public material.
- If resolving the gap would exceed 72,000 unique extracted characters, record the gap and stop.
- Stop after the single follow-up pass.

Completion criterion: the gap is resolved, or it is explicitly recorded without further research recursion.

### Step 7: Reconcile conflicts and changing definitions

When sources disagree:

1. compare publication dates and reporting periods;
2. distinguish current structure from historical structure;
3. distinguish GAAP from adjusted measures;
4. distinguish different segment, geographic, and customer definitions;
5. prefer formal filings for accounting definitions;
6. prefer newer official materials for current organization and guidance practice;
7. preserve each conflicting reported claim separately with its own source IDs;
8. record unresolved conflicts in `uncertainties_and_gaps`.

Never silently combine inconsistent definitions.

Completion criterion: every material conflict is either resolved transparently or recorded as unresolved.

### Step 8: Construct the JSON profile

Populate the exact top-level contract below. Keep all top-level keys present. Use `null` for an unknown scalar and `[]` for no supported array items. Add a gap record when missing information is material. Replace supported narrative fields and array strings with sourced-claim objects; do not leave bare externally verifiable prose in the output.

Completion criterion: the output conforms to the contract, contains no unsupported facts, distinguishes facts from judgments, and has claim-level source IDs that all resolve to the source log while remaining within the lightweight output budget.

### Step 9: Determine status

Set:

- `complete` when the lightweight contract is materially satisfied;
- `partial` when the profile is useful but a material field or definition remains unresolved after the bounded follow-up pass;
- `error` when required inputs or company identity cannot be resolved.

Completeness does not require every optional array to contain an item. It requires every section to have been considered and handled honestly.

### Step 10: Verify and return

Run the verification checklist at the end of this skill. Mechanically verify unique source IDs, claim-source resolution, conditional basis rules, and locator-key resolution where tooling permits. Then return the JSON object only.

## Output contract

Return all of these top-level keys in this order:

```json
{
  "schema_version": "0.3.0",
  "status": "complete",
  "profile_metadata": {
    "as_of_date": "2026-08-16",
    "research_cutoff": "2026-08-16",
    "profile_depth": "lightweight",
    "target_period": null,
    "target_metrics_supplied": [],
    "source_policy": {
      "repository_first": true,
      "public_research_allowed": true
    }
  },
  "company_identity": {
    "legal_name": null,
    "common_name": null,
    "ticker": null,
    "exchange": null,
    "incorporation_jurisdiction": null,
    "headquarters": null,
    "reporting_currency": null,
    "industry": null,
    "company_description": null,
    "field_provenance": {}
  },
  "business_model": {
    "summary": null,
    "revenue_model": [],
    "products_and_services": [],
    "customer_groups": [],
    "distribution_channels": []
  },
  "operating_structure": {
    "segments": [],
    "geographies": [],
    "operating_footprint": []
  },
  "reporting_context": {
    "fiscal_year_end": {
      "convention": null,
      "latest_reported_date": null,
      "weeks_in_latest_reported_year": null,
      "field_provenance": {}
    },
    "reporting_frequency": null,
    "accounting_standard": null,
    "reporting_currency": null,
    "fiscal_calendar_notes": [],
    "important_accounting_conventions": [],
    "company_defined_terms": [],
    "adjusted_measures_used": [],
    "field_provenance": {}
  },
  "financial_drivers": {
    "revenue_drivers": [],
    "cost_drivers": [],
    "margin_drivers": [],
    "earnings_drivers": [],
    "capital_intensity": {
      "classification": "unknown",
      "basis": "unknown",
      "rationale": null,
      "source_ids": []
    },
    "working_capital_characteristics": []
  },
  "cyclicality_and_seasonality": {
    "cyclicality": null,
    "cycle_sensitivity": {
      "classification": "unknown",
      "basis": "unknown",
      "rationale": null,
      "source_ids": []
    },
    "seasonal_patterns": [],
    "important_timing_factors": []
  },
  "guidance_practices": {
    "provides_guidance": {
      "value": null,
      "basis": "unknown",
      "source_ids": []
    },
    "usual_cadence": null,
    "metrics_commonly_guided": [],
    "guidance_format": [],
    "guidance_characteristics": []
  },
  "external_exposures": [],
  "metric_lenses": [],
  "company_specific_factors": [],
  "sources": [],
  "uncertainties_and_gaps": [],
  "errors": []
}
```

Schema `0.3.0` supersedes `0.2.0`. It preserves claim-level provenance while normalizing source policy, incorporation jurisdiction, and fiscal-year-end semantics.

### Contract-wide type rules

- Treat the top-level contract and documented nested contracts as closed: do not add undocumented keys.
- Keep every required top-level key present in the specified order.
- Use ISO `YYYY-MM-DD` strings for exact dates and `null` when an exact date is unknown.
- Use JSON booleans for policy and guidance values; never encode them as strings.
- Use arrays only for repeated items and keep every array homogeneous under its documented object contract.
- Use `SRC-001`, `SRC-002`, and so on for source IDs; IDs must be unique and all references must resolve.
- Enforce documented enum values exactly and reject rather than normalize an unsupported output value silently.

## Nested object contracts

### Normalized identity, policy, and fiscal calendar

- Input `company.jurisdiction` is an identity-resolution hint. Output `company_identity.incorporation_jurisdiction` means the company's legal place of incorporation; do not substitute headquarters, listing venue, or principal market.
- `profile_metadata.source_policy` preserves the normalized input object with required boolean keys `repository_first` and `public_research_allowed`.
- `reporting_context.fiscal_year_end.convention` is the recurring convention where disclosed, such as "Sunday nearest January 31".
- `latest_reported_date` is the most recent exact fiscal year-end date established before the cutoff.
- `weeks_in_latest_reported_year` is an integer such as `52` or `53`, or `null` when not established.
- `fiscal_year_end.field_provenance` maps each non-null fiscal-calendar subfield to its basis and evidence. Do not add a parent-level `reporting_context.field_provenance.fiscal_year_end` entry.

### Sourced claim

Use this object for `company_description`, `business_model.summary`, every narrative company-profile array listed below, and any other supported free-text company claim:

```json
{
  "statement": "Revenue is generated primarily through company-operated stores.",
  "basis": "reported_fact",
  "source_ids": ["SRC-001"],
  "source_locators": {
    "SRC-001": "Item 1, Business"
  }
}
```

Add `rationale` only when required by the basis rules. Keep `source_locators` optional and compact. Bare externally verifiable strings are not allowed in claim-bearing fields under schema `0.3.0`.

The following arrays contain sourced-claim objects rather than strings:

- `business_model.revenue_model` and `business_model.distribution_channels`;
- `operating_structure.operating_footprint`;
- `reporting_context.fiscal_calendar_notes`, `important_accounting_conventions`, and `adjusted_measures_used`;
- every array under `financial_drivers` except `capital_intensity`;
- `cyclicality_and_seasonality.seasonal_patterns` and `important_timing_factors`;
- `guidance_practices.metrics_commonly_guided`, `guidance_format`, and `guidance_characteristics`.

`guidance_practices.usual_cadence` is `null` or one sourced-claim object. `cyclicality_and_seasonality.cyclicality` is `null` or one sourced-claim object.

### Sourced assessment

Use this object for `financial_drivers.capital_intensity`, `cyclicality_and_seasonality.cycle_sensitivity`, and `metric_lenses[].specificity`:

```json
{
  "classification": "high",
  "basis": "model_judgment",
  "rationale": "The company operates a large owned physical network and reports recurring capital expenditure requirements.",
  "source_ids": ["SRC-001"],
  "source_locators": {
    "SRC-001": "Item 2, Properties"
  }
}
```

For capital intensity and cycle sensitivity, allowed `classification` is `low`, `moderate`, `high`, or `unknown`. For metric specificity, it is `generic`, `moderate`, or `high`. Classification is normally a `model_judgment`; do not mark it `reported_fact` merely because management discusses the underlying drivers. Use the all-unknown shape in the top-level contract when no supported capital-intensity or cycle-sensitivity assessment can be made.

### Sourced boolean

Use this object for `guidance_practices.provides_guidance`:

```json
{
  "value": true,
  "basis": "reported_fact",
  "source_ids": ["SRC-002"],
  "source_locators": {
    "SRC-002": "Fiscal 2026 Guidance"
  }
}
```

When unresolved, use `value: null`, `basis: "unknown"`, and `source_ids: []`.

### Grouped scalar provenance

`company_identity.field_provenance` and `reporting_context.field_provenance` map each non-null externally verifiable scalar field to its basis and evidence:

```json
{
  "legal_name": {
    "basis": "reported_fact",
    "source_ids": ["SRC-001"],
    "source_locators": {
      "SRC-001": "Cover page"
    }
  },
  "industry": {
    "basis": "model_judgment",
    "rationale": "The company's principal activities align most closely with this industry classification.",
    "source_ids": ["SRC-001"]
  }
}
```

Do not add entries for null fields, input-derived metadata, `company_description`, or array items that carry their own provenance. Every non-null externally verifiable scalar must have exactly one same-named `field_provenance` entry. Apply the normal conditional basis rules inside each entry. Every locator source ID must appear in that entry's `source_ids`.

### Target metric input

```json
{
  "label": "Revenue",
  "units": "USDm"
}
```

### Product or service

```json
{
  "name": "Product or service category",
  "description": "Concise description",
  "basis": "reported_fact",
  "importance": "primary",
  "importance_basis": "model_judgment",
  "importance_rationale": "This category is central to the company's stated offering and revenue model.",
  "source_ids": ["SRC-001"]
}
```

Allowed `importance`: `primary`, `secondary`, `emerging`, `unknown`.

`basis` applies to the name and description. `importance_basis` applies only to the relative importance classification and normally is `model_judgment`; include `importance_rationale` for that judgment.

### Customer group

```json
{
  "name": "Customer group",
  "description": "Who buys and why",
  "basis": "reported_fact",
  "source_ids": ["SRC-001"]
}
```

### Segment

```json
{
  "name": "Reported segment",
  "description": "What the segment contains",
  "basis": "reported_fact",
  "materiality": "primary",
  "materiality_basis": "model_judgment",
  "materiality_rationale": "The segment is a principal reported component of the company.",
  "source_ids": ["SRC-001"]
}
```

### Geography

```json
{
  "name": "Region",
  "role": "Major market or operating region",
  "basis": "reported_fact",
  "materiality": "primary",
  "materiality_basis": "model_judgment",
  "materiality_rationale": "The region is a principal market or operating area in the reviewed disclosures.",
  "source_ids": ["SRC-001"]
}
```

Allowed `materiality`: `high`, `moderate`, `low`, `primary`, `secondary`, `unknown` as appropriate to the object. Use one consistent vocabulary within each array. `basis` applies to the reported name and description or role; `materiality_basis` and `materiality_rationale` identify the separate model judgment.

### Company-defined term

```json
{
  "term": "Comparable sales",
  "definition": "Company definition where available",
  "basis": "reported_fact",
  "source_ids": ["SRC-001"],
  "source_locators": {
    "SRC-001": "Defined terms"
  }
}
```

### External exposure

```json
{
  "category": "macroeconomic",
  "exposure": "Housing-market activity",
  "description": "How and why the company is exposed",
  "basis": "model_judgment",
  "rationale": "The cited sources identify housing activity as a demand influence for the company's principal offerings.",
  "materiality": "high",
  "materiality_basis": "model_judgment",
  "materiality_rationale": "The exposure affects a broad portion of company demand.",
  "source_ids": ["SRC-001", "SRC-003"]
}
```

Preferred `category`: `industry`, `macroeconomic`, `political`, `geographic`, `regulatory`, `currency`, `commodity`, `technology`, or `other`.

Allowed `materiality`: `high`, `moderate`, `low`, `unknown`.

`basis` applies to the stated exposure relationship. Use `reported_fact` only when the source directly makes that relationship; use `model_judgment` with `rationale` when the profile synthesizes it. Materiality is a separate assessment and requires `materiality_basis` and a concise `materiality_rationale`.

### Metric lens

```json
{
  "input_metric": "Segment operating profit",
  "specificity": {
    "classification": "high",
    "basis": "model_judgment",
    "rationale": "The metric is restricted to a named operating segment.",
    "source_ids": [],
    "input_fields": ["target_metrics[0].label"]
  },
  "company_definition": null,
  "scope": "Named operating segment",
  "accounting_basis": null,
  "units": "USDm",
  "reporting_frequency": "quarterly",
  "relevant_business_areas": [],
  "additional_profile_emphasis": [],
  "unresolved_questions": [],
  "field_provenance": {
    "scope": {
      "basis": "reported_fact",
      "source_ids": ["SRC-001"]
    },
    "reporting_frequency": {
      "basis": "reported_fact",
      "source_ids": ["SRC-001"]
    }
  }
}
```

Allowed `specificity.classification`: `generic`, `moderate`, `high`.

Metric specificity is a sourced-assessment object. When its classification follows solely from the caller's label, use `source_ids: []` and identify the label in `input_fields`; when company-specific scope or definitions influence the classification, add those source IDs. Use `field_provenance` for each non-null company-defined or externally verified scalar. Do not cite `input_metric` or `units` when they merely reproduce caller input. `relevant_business_areas`, `additional_profile_emphasis`, and `unresolved_questions` contain sourced-claim objects with basis and provenance when non-empty.

A generic supplied metric may be omitted from `metric_lenses` when no additional company-specific context is necessary; it must still appear in `profile_metadata.target_metrics_supplied`.

### Company-specific factor

```json
{
  "name": "Company-specific concept",
  "category": "operating_model",
  "description": "What makes the concept distinctive",
  "potential_relevance": "Why a later signal worker may need to understand it",
  "materiality": "high",
  "basis": "model_judgment",
  "rationale": "The cited operating facts support treating this concept as distinctive and potentially relevant.",
  "source_ids": ["SRC-001", "SRC-003"]
}
```

Keep `category` flexible. Allowed `materiality`: `high`, `moderate`, `low`, `unknown`. The description, potential relevance, and materiality are normally a combined `model_judgment`; `rationale` must explain the inference from the cited sources.

`potential_relevance` must remain a broad explanatory relationship. It must not nominate, score, or quantify a forecast signal.

### Source log entry

```json
{
  "source_id": "SRC-001",
  "title": "Annual Report 2025",
  "source_type": "annual_report",
  "publisher": "Example Company",
  "publication_date": "2026-03-01",
  "reporting_period": "FY2025",
  "location": "repository path or reviewed public URL",
  "used_for": [
    "business_model",
    "operating_structure",
    "reporting_context"
  ]
}
```

Requirements:

- assign unique IDs in order: `SRC-001`, `SRC-002`, and so on;
- include only inspected sources;
- use a repository-relative path for corpus sources;
- use the reviewed page URL for public sources;
- use `used_for` to name the top-level sections supported, while treating it only as a coarse source inventory;
- require every claim-level and field-level source ID to resolve to exactly one source-log entry;
- omit inspected sources that support no retained claim, field, conflict, or material gap;
- do not list duplicate copies of the same disclosure unless they materially differ.

### Uncertainty or gap

```json
{
  "topic": "Geographic revenue definition",
  "issue": "The reviewed sources do not establish whether geography is based on billing location or end demand.",
  "importance": "moderate",
  "source_ids": ["SRC-001"],
  "conflicting_claims": [],
  "suggested_follow_up": "Check geographic footnotes if this becomes relevant to a selected signal."
}
```

Allowed `importance`: `high`, `moderate`, `low`.

For a missing disclosure, `source_ids` identifies the most relevant inspected sources whose coverage was insufficient; it does not claim that a source explicitly states the absence. For a conflict, populate `conflicting_claims` with separate sourced-claim objects so each reading retains its own source IDs and optional locators. Never merge conflicting counts, dates, definitions, scopes, or reporting bases into one unsupported value.

Conflict example:

```json
{
  "topic": "Current location count",
  "issue": "The reviewed current sources use different scopes or dates that cannot be reconciled precisely.",
  "importance": "moderate",
  "source_ids": ["SRC-002", "SRC-003"],
  "conflicting_claims": [
    {
      "statement": "The company reported more than 1,280 locations at quarter-end.",
      "basis": "reported_fact",
      "source_ids": ["SRC-002"]
    },
    {
      "statement": "Management later described more than 1,300 branches following a recent acquisition.",
      "basis": "reported_fact",
      "source_ids": ["SRC-003"]
    }
  ],
  "suggested_follow_up": "Reconcile the count only if a later task requires a same-date operating footprint."
}
```

When sources identify operating lines or concepts but do not disclose their standalone economics, record the disclosure limitation as a gap. Do not convert the absence of line-level financial visibility into a model-derived factual description.

### Error

```json
{
  "code": "INVALID_INPUT",
  "message": "Required input is missing or invalid.",
  "required_information": []
}
```

## Writing and compression rules

Default output caps:

| Field or item | Maximum |
|---|---:|
| Products and services | 4 |
| Customer groups | 4 |
| Distribution channels | 5 |
| Segments | 4 |
| Geographies | 4 |
| Accounting conventions | 5 |
| Company-defined terms | 5 |
| Each financial-driver array | 4 |
| External exposures | 7 |
| Company-specific factors | 5 |
| Uncertainties and gaps | 5 |
| Sources | 6 |
| Metric lenses | One per supplied moderate/high metric; omit generic lenses unless needed |

Default string caps:

| String | Maximum characters |
|---|---:|
| Company description | 300 |
| Claim statement | 220 |
| Judgment or calculation rationale | 240 |
| Gap issue | 350 |
| Source locator | 120 |

Target at most 14,000 serialized JSON characters and enforce a 16,000-character hard stop. If the draft exceeds either threshold, remove lower-materiality claims and duplication; never remove required keys, basis labels, provenance, or material gaps. Exceed a per-array cap only when omission would materially misrepresent the company, and retain only the minimum necessary overage.

- Prefer compact arrays of distinct items over long narrative paragraphs.
- Keep the company description to one or two sentences.
- Keep each driver or exposure concise and causal: state how it relates to the company.
- Include principal products, customers, segments, and geographies, not exhaustive lists.
- Avoid repeating the same concept in several sections. Put it in the most natural section and reference it indirectly elsewhere only when necessary.
- Do not include detailed percentages or historical figures unless one is indispensable to understanding company structure or terminology.
- Preserve company-defined terminology rather than replacing it with generic financial language.
- Distinguish geography by customer location, billing location, destination, or operations when the source does so.
- Distinguish reported and adjusted measures.
- Keep provenance compact: use source IDs in claims and retain titles, paths, URLs, dates, and publication metadata only in `sources`.
- Add locators to precise figures, definitions, calculations, disputed claims, and long sources when a stable locator materially improves verification; do not add decorative locators to every claim.
- Do not repeat a reported fact inside a model-judgment rationale. Explain only the inference needed to distinguish the judgment from its cited evidence.
- Provenance overhead does not justify exceeding the lightweight output budget. Retain fewer material claims rather than deleting basis labels or claim-level source IDs.
- Do not infer the absence of an exposure merely because selected sources do not discuss it.

## Stop conditions

Stop normal research when all applicable conditions below are satisfied:

- identity and cutoff are resolved;
- business model and revenue model are understandable;
- principal products/services and customer groups are captured;
- material segments and geographies are captured or explicitly unavailable;
- fiscal and reporting context is established;
- broad financial drivers are captured;
- material cyclicality and seasonality are described;
- guidance practice is described or marked unknown;
- material external exposures are captured;
- supplied metrics have received proportional treatment;
- sources are logged;
- material unresolved questions are recorded;
- every Step 4 coverage row is `supported`, `not_materially_applicable`, or `gap_recorded`;
- further research would mainly add detail rather than alter the profile's usefulness.

Stop as soon as these conditions are satisfied; do not continue merely because research budget remains. Independently, the 72,000-character limit is a mandatory stop even when a coverage row remains unresolved; record the unresolved material issue in `uncertainties_and_gaps` and proceed to profile construction.

## Production and evaluation modes

**Production mode is the default.** Return exactly one schema `0.3.0` profile object and nothing else. Do not add runtime, search counts, token estimates, test results, or evaluator commentary to the profile.

**Evaluation mode belongs to an external tester or invocation wrapper.** Build the same production-valid profile without changing its schema, then report test telemetry separately. Useful telemetry includes runtime seconds, selected-document count, public-source count, targeted-search count, unique extracted characters, serialized profile characters, schema validity, unsupported-claim count, and repository changes. Evaluation telemetry must never appear as a top-level profile key or source-log entry.

## Maintenance benchmark gate

For future material changes to this skill, exercise Home Depot, Analog Devices, Hays, and Deere when their repository corpora are available; together they cover retailer, semiconductor, staffing, industrial, and financing structures. At minimum cover: no supplied metrics; a generic metric; a company-defined metric; a narrow segment metric; public research disabled; a cutoff before the newest document; ambiguous identity; and a material unresolved conflict.

Use these acceptance gates:

| Check | Required result |
|---|---:|
| Valid JSON and exact top-level contract | 100% |
| Post-cutoff sources | 0 |
| Unsupported sampled claims | 0 |
| Duplicate or unresolved source IDs | 0 |
| Core repository documents | No more than 3 |
| Optional repository documents | No more than 1 |
| Public sources | No more than 2 |
| Unique extracted source text | No more than 72,000 characters |
| Serialized profile | No more than 16,000 characters |
| Repository files changed by profile execution | 0 |
| Forecasts, signal selections, or recommendations | 0 |

Run the no-metric case first because it verifies that repository metadata is not silently promoted into invocation inputs. A benchmark failure blocks a schema-version release until fixed or explicitly documented as a known limitation.

## Final verification checklist

Before returning the output, verify:

### Input and identity

- [ ] Company identity is unambiguous.
- [ ] The effective cutoff is explicit.
- [ ] Every source was published on or before the cutoff.
- [ ] Original target metric labels and units are preserved.
- [ ] Target period and metrics came from normalized invocation inputs, not repository metadata.

### Research discipline

- [ ] Repository materials were considered first.
- [ ] The source set is authoritative, relevant, and non-duplicative.
- [ ] Exactly one same-period periodic filing or results release was treated as the core latest-results source.
- [ ] Repository indexes were used for discovery only and were not logged as substantive sources.
- [ ] No more than three core and one optional repository document were used without an explicit exception.
- [ ] Public research was used only for a material gap and stayed within the two-source limit.
- [ ] Every source-log entry was actually inspected and used.
- [ ] Exact source paths were selected before substantive extraction.
- [ ] Large documents were searched before any broader section was opened.
- [ ] Search results were bounded to one or two retained matches of approximately 1,000–1,500 characters per topic.
- [ ] Overlapping excerpts were deduplicated and cumulative unique extracted characters were tracked.
- [ ] No more than two broad follow-up section reads were used.
- [ ] Unique extracted source text stayed within the 72,000-character hard stop.
- [ ] No extraction command created repository notes, indexes, caches, or bytecode artifacts.
- [ ] Every coverage-matrix row was resolved or recorded as a gap before drafting.

### Profile quality

- [ ] Content is recognizably specific to the company and industry.
- [ ] Generic boilerplate and immaterial detail were removed.
- [ ] Stable facts and current context were not confused.
- [ ] Reporting periods, currencies, scopes, and accounting bases are not mixed.
- [ ] Company-defined terms are preserved.
- [ ] Unknown or conflicting information is explicit.
- [ ] No unsupported precise claim, figure, or market-share statement was added.

### Basis and claim-level provenance

- [ ] Every non-null narrative claim and classification declares an allowed `basis`.
- [ ] Every `reported_fact` has one to three direct source IDs.
- [ ] Every `calculated` claim has source IDs and a rationale with inputs and arithmetic.
- [ ] Every `model_judgment` has a rationale and either source IDs or, when based solely on caller input, explicit `input_fields`; no judgment is attributed to management unless management stated it.
- [ ] Every `assumption` is explicit, has a rationale, and is not filling a missing company fact.
- [ ] Every material `unknown` is null and recorded as a gap rather than inferred.
- [ ] Every non-null externally verifiable identity, reporting, and metric-lens scalar has a same-named `field_provenance` entry with an allowed basis and valid evidence.
- [ ] Every claim-level and field-level source ID resolves to exactly one unique `sources` entry.
- [ ] Every locator key is present in its claim's or field's source-ID list.
- [ ] Every material conflict preserves each reported reading with its own source IDs.
- [ ] Source-log `used_for` was not treated as a substitute for claim-level provenance.

### Metric proportionality

- [ ] Each metric was classified using definition and scope, not unfamiliarity alone.
- [ ] Generic metrics did not trigger unnecessary research.
- [ ] Specific metrics received only the additional context needed to understand them.
- [ ] No metric lens contains signals, weights, historical extraction, assumptions, or forecasts.

### Output integrity

- [ ] Output is valid JSON.
- [ ] All required top-level keys are present in the required order.
- [ ] No undocumented top-level or nested keys were added.
- [ ] `schema_version` is `0.3.0`.
- [ ] `status` is `complete`, `partial`, or `error`.
- [ ] `source_policy` is an object containing the two required booleans.
- [ ] Incorporation jurisdiction is not confused with headquarters or listing venue.
- [ ] Fiscal-year-end convention, exact date, and week count use their normalized nested fields.
- [ ] Unknown scalar values are `null`, not fabricated text.
- [ ] Unsupported arrays are empty rather than padded.
- [ ] Source IDs are unique.
- [ ] Default array and string caps were respected with only minimum necessary overage.
- [ ] Serialized JSON does not exceed 16,000 characters.
- [ ] Production output contains no evaluation telemetry.
- [ ] There is no Markdown fence, preamble, explanation, or text after the JSON.

If any check fails, correct the profile before returning it. If the failure cannot be corrected within the bounded research policy, return `partial` with a gap or `error` with a structured error record.
