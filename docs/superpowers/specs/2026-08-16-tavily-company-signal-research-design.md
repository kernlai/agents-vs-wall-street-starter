# Tavily Company and Signal Research Design

## Objective

Build a repository-local agent skill and deterministic research pipeline that use Tavily to create source-backed company profiles and resolve metric-specific signal maps at scale. Preserve the existing evidence-to-forecast authority split: models may discover evidence and propose structured claims, while deterministic code owns source freezing, cutoff enforcement, validation, arithmetic, forecast acceptance, and receipts.

Integrate the useful parallel research and company configuration introduced by commit `42901b3` without retaining its unverified model-consensus path as a forecast authority.

## Scope

The implementation will:

- create `.agents/skills/researching-company-signals/` as a discoverable repository skill folder;
- use `TAVILY_API_KEY` from the process environment or the ignored repository `.env` file without logging or persisting the secret;
- research and assemble all required company-profile sections;
- derive three to seven approved signals for every forecast metric;
- search only for evidence required by those approved signals;
- freeze selected Tavily-extracted pages, calculate SHA-256 hashes, and preserve source metadata;
- produce profile and signal-research candidate bundles for deterministic validation;
- add structured model reasoning summaries and an independent look-ahead review to signal metadata;
- reject forecast-driving claims that fail source, cutoff, period, unit, accounting-basis, or look-ahead gates;
- preserve `Decimal` values as decimal strings across JSON boundaries;
- run research for all four companies concurrently with bounded worker counts;
- update `ARCHITECTURE.md`, `architecture/index.html`, commands, and tests to match working behavior;
- commit coherent green slices, push the integration branch regularly, then merge and push `main` after final verification.

The implementation will not expose private model chain of thought, treat model agreement as factual verification, assign numerical weights to qualitative evidence, submit workbooks automatically, or commit API keys and generated research data.

## Repository Integration

The integration branch starts at `origin/niranjan/forecast-inputs`, which is one commit ahead of `origin/main`. This retains its parallel orchestrator, company target configuration, SQLite run memory, normalized forecast-input concept, and tests.

The following branch behavior will change:

- `OpenAIWebResearchProvider` will no longer be the source-discovery authority. Tavily search and extract will supply the web corpus.
- Agent consensus confidence will not promote a fact into the deterministic forecast path.
- Extracted financial values will use decimal strings rather than binary floating point.
- A URL and model-generated evidence sentence will not count as provenance without frozen content, a hash, publication metadata, and an exact verified quotation.
- The pipeline will hand validated company profiles and typed observations to the existing `forecasting` package rather than creating a competing forecast authority.
- Documentation will describe only implemented commands and modules.

## Architecture

```text
company seed + challenge metrics + information cutoff
                         |
                         v
              profile query planner
                         |
                         v
          Tavily search -> Tavily batch extract
                         |
                         v
        freeze content + SHA-256 + source record
                         |
                         v
       agent proposes source-cited profile claims
                         |
                         v
      deterministic profile validation and storage
                         |
                         v
         metric-specific signal-map proposal
                         |
                         v
      deterministic signal-map schema validation
                         |
                         v
       signal query planner (approved signals only)
                         |
                         v
        Tavily search/extract/freeze/verify quote
                         |
                         v
        typed observation + researchAudit metadata
                         |
                         v
      independent no-web look-ahead reviewer
                         |
                         v
     deterministic rejection or forecast compiler
                         |
                         v
            forecast + provenance receipt
```

### Repository skill

`.agents/skills/researching-company-signals/SKILL.md` will tell an agent when and how to:

1. read the challenge metric definitions and company seed;
2. invoke the deterministic profile-research command;
3. inspect source-backed profile candidates and unresolved sections;
4. propose a metric-specific signal map with three to seven signals per metric;
5. invoke signal-specific research only for approved signals;
6. create structured claims and observations using exact quotations from frozen files;
7. run look-ahead review and the deterministic compiler;
8. stop with an explicit rejection when evidence is missing or invalid.

The skill will link to compact schema references and executable repository commands rather than duplicating the implementation. It will be validated with the skill-creator validation tooling and realistic forward tests.

### Tavily client and query planning

A small standard-library client will call Tavily Search and Extract over HTTPS. The client interface will be injectable so tests use fixtures and never consume credits.

Profile query planning will cover the nine required profile sections: business model, products and customers, segments and geographies, fiscal calendar, revenue and cost drivers, accounting definitions, guidance style, cyclicality and seasonality, and external exposures. Queries will include company identity, relevant fiscal periods, information cutoff, and preferred official domains.

Signal query planning will consume only validated signal definitions. Each query will include the signal hypothesis, target metric, target period, required evidence, units, freshness requirement, and preferred official domains. This prevents broad generic research from silently becoming a forecast driver.

Search will use explicit result and concurrency limits. Extract will batch selected URLs. Primary sources such as company investor relations, regulators, exchanges, and government statistics will be preferred. Third-party sources may provide discovery or corroboration but cannot override an available primary source without a recorded reason.

### Source freezing and provenance

Every selected web result will become an immutable run source record containing:

- canonical URL;
- publisher and title;
- document type;
- publication date or timestamp, with uncertainty recorded explicitly;
- Tavily request ID and query ID;
- local frozen-content path;
- SHA-256 of the exact frozen bytes;
- retrieval timestamp;
- information-cutoff decision;
- extraction status and failure reason.

Generated source files and run bundles will be ignored by Git. Receipts will retain relative paths and hashes so the run can be audited while the source snapshot is present. A source without an admissible publication time, or one published after the cutoff, cannot drive a profile claim or forecast observation.

Exact quotations will be verified byte-for-text against normalized frozen content before acceptance. The validator will reject source URL, hash, quote, period, unit, currency, or accounting-basis mismatches.

## Company Profile Workflow

The seed configuration will contain stable identifiers and challenge-owned values only: company name, ticker, exchange, regulator and investor-relations domains, target metrics, target periods, units, accounting bases, and information cutoff.

Tavily research will generate a candidate bundle, not an authoritative profile. An agent will propose section claims using source IDs and exact quotes from that bundle. Deterministic code will require every profile section to contain at least one accepted source-backed claim before emitting a usable `CompanyProfile`.

Profile enrichment will not copy numerical facts directly into forecasts. It exists to shape the signal map and evidence queries. Missing profile evidence remains visible and fails the profile stage instead of being filled from model memory.

## Signal Map and Observation Workflow

For each challenge metric, the agent will propose three to seven material signals with declared roles, hypotheses, directions, periods, units, importance, resolvers, evidence requirements, combination methods, freshness rules, correlation groups, and status.

Deterministic validation will require exactly one anchor for a compilable metric, supported role/resolver/combination triples, compatible units and accounting bases, unique IDs, and three to seven signals. Constraints will have explicit deterministic evaluators. Driver formulas will use `Decimal`; modifiers remain qualitative; scenario triggers remain conditional.

Only approved signals enter the signal-research planner. Tavily results that do not satisfy a declared evidence requirement may be retained as rejected research leads but cannot become observations.

## Model Audit Metadata

Every model-produced profile proposal, signal-map proposal, and signal observation will include a `researchAudit` object. This is an inspectable decision summary, not private chain of thought.

```json
{
  "schemaVersion": "research_audit.v1",
  "provider": "openai",
  "model": "configured-model-id",
  "modelKnowledgeCutoff": "declared-date-or-unknown",
  "requestId": "provider-request-id",
  "promptSha256": "sha256-of-exact-prompt",
  "inputManifestSha256": "sha256-of-canonical-source-manifest",
  "suppliedSourceIds": ["source-id"],
  "claims": [
    {
      "claimId": "claim-id",
      "summary": "Concise factual or causal claim",
      "sourceIds": ["source-id"],
      "exactQuotes": ["verbatim quotation"],
      "assumptions": [],
      "decision": "accepted"
    }
  ],
  "rejectedEvidence": [],
  "reasoningSummary": "Concise explanation of evidence selection and uncertainty",
  "createdAt": "ISO-8601 timestamp"
}
```

The pipeline will not request, store, or claim to expose hidden reasoning tokens. Persisted or encrypted provider reasoning items may be retained only for API continuation when supported; they are not audit evidence and will not be written into public receipts.

## Look-Ahead Review

An independent reviewer model will receive only:

- the canonical frozen-source manifest;
- the exact source excerpts supplied to the proposing model;
- the information cutoff;
- the prompt hash and research audit;
- the proposed profile claims, signal definitions, or observations.

The reviewer will use a provider interface so its request construction and response validation are testable without network access. The first live implementation will use the OpenAI Responses API when `OPENAI_API_KEY` is available, with model and reasoning effort recorded in the review metadata. The current repository `.env` does not contain that credential, so live reviewer execution requires the operator to add it; no fallback model may silently approve a payload.

The reviewer will have no web-search tool. It will return `lookahead_review.v1` with a verdict, issue list, claim IDs, cited source IDs, severity, and explanation. Supported issue codes are:

- `UNSUPPORTED_CLAIM`;
- `SOURCE_NOT_SUPPLIED`;
- `QUOTE_NOT_IN_SOURCE`;
- `POST_CUTOFF_FACT`;
- `ACTUAL_PRESENTED_AS_FORECAST`;
- `UNDECLARED_ASSUMPTION`;
- `SUSPICIOUS_PRECISION`;
- `PERIOD_LEAKAGE`;
- `MODEL_CUTOFF_UNDISCLOSED`.

The reviewer cannot prove that a claim came from model training data. Its purpose is to detect output that cannot be reconstructed from the supplied admissible evidence. Documentation and receipts will call such findings "suspected look-ahead" or "unsupported knowledge," not proven training-data use.

Deterministic code will independently verify source IDs, quotes, hashes, publication times, periods, and values. Any deterministic provenance failure blocks the item regardless of reviewer output. An error-level reviewer finding sets `lookaheadStatus` to `blocked_for_lookahead`; the forecast compiler will reject that item until a new, grounded proposal and review pass are produced. Warnings remain visible but cannot by themselves alter forecast arithmetic.

## Signal Payload Handoff

The forecast handoff will carry validated facts and observations plus audit metadata:

```json
{
  "schemaVersion": "forecast_input.v2",
  "companyId": "ADI",
  "profileReceipt": {},
  "signalMapReceipt": {},
  "observations": [],
  "researchAudit": {},
  "lookaheadReview": {
    "status": "passed",
    "issues": []
  },
  "provenanceManifestSha256": "..."
}
```

The forecast engine will accept only payloads whose schema is valid, provenance manifest matches, deterministic evidence checks pass, and look-ahead status is not blocked. Model confidence scores may be retained as descriptive metadata but will not determine factual acceptance or numerical weighting.

## Failure Handling

- Missing `TAVILY_API_KEY`: stop before network calls with a secret-safe setup message.
- Search or extraction timeout: retry transient failures with a bounded count; record unresolved URLs.
- Partial profile coverage: emit a candidate bundle and fail profile completion with missing-section codes.
- Missing publication date: reject as forecast-driving evidence unless an authoritative source record supplies an admissible date.
- Post-cutoff source: freeze for audit if returned, mark rejected, and exclude from model context used for proposals.
- Hash or quotation mismatch: reject the claim or observation.
- Reviewer unavailable: mark review incomplete and block forecast handoff rather than silently bypassing it.
- Missing reviewer API credential: run deterministic look-ahead checks, mark model review incomplete, and block live forecast handoff.
- Reviewer disagreement: preserve the report and require a new grounded proposal or explicit human review; never manufacture a forecast adjustment.
- One company lane fails: preserve other completed lanes, report the failed lane, and allow a targeted rerun.

## Testing

Implementation will follow failing-test-first vertical slices. Tests will cover:

- secret-safe `.env` loading;
- Tavily request serialization, response validation, batching, retry, and failure handling using fixtures;
- profile query coverage for all nine required sections;
- signal-specific query construction and prohibition of unapproved signals;
- source freezing, canonical manifests, SHA-256 stability, publication cutoff, and quote verification;
- profile completeness and three-to-seven-signals-per-metric validation;
- `Decimal` serialization and accounting-basis compatibility;
- audit-schema validation and prompt/input-manifest hashing;
- reviewer isolation from web tools and supported issue codes;
- deterministic blocking for provenance and error-level look-ahead findings;
- parallel company execution and targeted failure behavior;
- compatibility with the existing ADI compiler receipt;
- skill folder validation and realistic forward-use scenarios;
- a manually authorized live Tavily smoke run that creates a real frozen source bundle without exposing the key.

Final verification will run the complete Python test suite, signal tests, starter tests, profile/compiler example, skill validator, JSON validation, and a Git diff/status audit. The final push to `main` occurs only after these checks pass.

## Documentation

`ARCHITECTURE.md` will gain the Tavily discovery/freeze stage, audit metadata, independent look-ahead reviewer, deterministic blocking policy, and explicit limits on detecting training-data use. `architecture/index.html` will be revised to match the actual implemented commands and modules. The README will document setup and runnable commands without exposing secrets.

## Delivery and Git Strategy

Work will proceed on `integrate/tavily-company-research`, based on commit `42901b3`. Each coherent green vertical slice will be committed and pushed. After final verification, current remote `main` will be merged or fast-forwarded as appropriate, the integration branch will be merged into `main`, and `main` will be pushed. No force push will be used.
