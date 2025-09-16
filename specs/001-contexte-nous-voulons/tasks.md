# Tasks: Analyse de Données Foncières DVF pour Investissement Immobilier

**Input**: Design documents from `/specs/001-contexte-nous-voulons/`
**Prerequisites**: spec.md (available), README.md (available), requirements.txt (available)

## Execution Flow (main)
```
1. Load spec.md from feature directory ✓
   → Extract: Python/Jupyter tech stack, DVF data analysis, investor recommendations
2. Load project structure from README.md ✓
   → Extract: notebooks/, assets/, src/, outputs/ structure
3. Load dependencies from requirements.txt ✓
   → Extract: pandas, numpy, matplotlib, ipywidgets, folium/plotly
4. Generate tasks by category:
   → Setup: environment, dependencies, structure
   → Data: preprocessing, validation
   → Analysis: statistical analysis, temporal analysis
   → Visualization: interactive dashboards, widgets
   → Recommendations: rental yield calculations, investor guidance
5. Apply task rules:
   → Different notebooks/files = mark [P] for parallel
   → Sequential notebooks = dependencies (01→02→03→04)
   → Data preparation before analysis
6. Number tasks sequentially (T001, T002...)
7. Generate dependency graph
8. Create parallel execution examples
9. Validate task completeness for DVF analysis project
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Project root**: `c:\Users\vtnde\Documents\Projets\ProjetFoncier`
- **Notebooks**: `notebooks/`
- **Assets**: `assets/`
- **Source**: `src/`
- **Outputs**: `outputs/`

## Phase 1: Environment Setup & Project Structure
- [ ] T001 Create Python 3.11 virtual environment (venv or conda)
- [ ] T002 Install core dependencies: pandas>=2.0.0, numpy>=1.24.0, matplotlib>=3.7.0, jupyter>=1.0.0
- [ ] T003 [P] Install interactive dependencies: ipywidgets>=8.0.0, folium>=0.14.0, plotly>=5.15.0
- [ ] T004 [P] Install development tools: pytest>=7.4.0, black>=23.0.0, flake8>=6.0.0
- [ ] T005 Configure Jupyter Notebook environment and kernel
- [ ] T006 [P] Validate assets/dataset.csv exists and accessible
- [ ] T007 [P] Create outputs/ directory structure for results export

## Phase 2: Data Foundation (MUST COMPLETE BEFORE Phase 3)
**CRITICAL: Data preprocessing must be complete before any analysis**
- [ ] T008 Load and inspect assets/dataset.csv in notebooks/01_preprocessing.ipynb
- [ ] T009 Analyze DVF data structure: columns, data types, missing values in notebooks/01_preprocessing.ipynb
- [ ] T010 Clean data: handle missing values, remove duplicates, normalize postal codes/communes in notebooks/01_preprocessing.ipynb
- [ ] T011 Filter data for 2019-2023 period in notebooks/01_preprocessing.ipynb
- [ ] T012 Create derived variables: prix_m2, rendement_brut calculations in notebooks/01_preprocessing.ipynb
- [ ] T013 Validate cleaned data integrity and export preprocessed dataset in notebooks/01_preprocessing.ipynb
- [ ] T014 [P] Create utility functions in src/dvf_utils.py for data loading and basic calculations

## Phase 3: Statistical Analysis (ONLY after Phase 2 complete)
- [ ] T015 Global descriptive statistics (price, surface, rooms) in notebooks/02_analysis.ipynb
- [ ] T016 Calculate average/median price per m² by commune and department in notebooks/02_analysis.ipynb
- [ ] T017 Analyze by property type (house, apartment, outbuilding) in notebooks/02_analysis.ipynb
- [ ] T018 Temporal evolution analysis: price trends and sales volumes 2019-2023 in notebooks/02_analysis.ipynb
- [ ] T019 Identify market anomalies and outliers in notebooks/02_analysis.ipynb
- [ ] T020 [P] Extend src/dvf_utils.py with statistical analysis functions

## Phase 4: Interactive Visualizations (ONLY after Phase 3 complete)
- [ ] T021 Create matplotlib charts: histograms, boxplots, temporal curves in notebooks/03_visualizations.ipynb
- [ ] T022 Implement interactive widgets for filtering (commune, department, property type, year) in notebooks/03_visualizations.ipynb
- [ ] T023 [P] Develop rental investment simulator widget in notebooks/03_visualizations.ipynb
- [ ] T024 [P] Create department comparison dashboard in notebooks/03_visualizations.ipynb
- [ ] T025 [P] Build advanced opportunity search interface in notebooks/03_visualizations.ipynb
- [ ] T026 Optional: Interactive map of transactions with folium/plotly in notebooks/03_visualizations.ipynb
- [ ] T027 Export key visualizations as PNG/HTML to outputs/ directory

## Phase 5: Investment Recommendations (ONLY after Phase 4 complete)
- [ ] T028 Integrate external rental price data sources in notebooks/04_recommendations.ipynb
- [ ] T029 Calculate gross rental yield by sector using: (annual rent / purchase price) × 100 in notebooks/04_recommendations.ipynb
- [ ] T030 Implement multi-criteria scoring system for investment opportunities in notebooks/04_recommendations.ipynb
- [ ] T031 Identify attractive zones and interesting property types in notebooks/04_recommendations.ipynb
- [ ] T032 Generate personalized investment recommendations with justifications in notebooks/04_recommendations.ipynb
- [ ] T033 Create executive summary for non-technical investors in notebooks/04_recommendations.ipynb
- [ ] T034 [P] Finalize src/dvf_utils.py with recommendation algorithms

## Phase 6: Deliverables & Quality Assurance
- [ ] T035 [P] Export important visualizations (PNG or interactive HTML) to outputs/
- [ ] T036 [P] Create comprehensive analysis report in outputs/
- [ ] T037 [P] Validate all notebooks execute without errors from clean environment
- [ ] T038 [P] Update README.md with execution instructions and results summary
- [ ] T039 Package final deliverable: ZIP with notebooks + outputs for third-party execution
- [ ] T040 [P] Run linting and code quality checks on src/dvf_utils.py

## Dependencies
- Environment setup (T001-T007) before data work (T008-T014)
- Data preprocessing (T008-T013) blocks all analysis (T015-T020)
- Statistical analysis (T015-T020) blocks visualizations (T021-T027)
- Visualizations (T021-T027) block recommendations (T028-T034)
- Core development before deliverables (T035-T040)

## Sequential Notebook Dependencies
```
01_preprocessing.ipynb → 02_analysis.ipynb → 03_visualizations.ipynb → 04_recommendations.ipynb
```

## Parallel Execution Examples

### Phase 1 - Dependencies & Setup
```
Task: "Install interactive dependencies: ipywidgets>=8.0.0, folium>=0.14.0, plotly>=5.15.0"
Task: "Install development tools: pytest>=7.4.0, black>=23.0.0, flake8>=6.0.0"
Task: "Validate assets/dataset.csv exists and accessible"
Task: "Create outputs/ directory structure for results export"
```

### Phase 2 - Utilities Development
```
Task: "Create utility functions in src/dvf_utils.py for data loading and basic calculations"
# Can run in parallel with T013 (data validation)
```

### Phase 4 - Visualization Components
```
Task: "Develop rental investment simulator widget in notebooks/03_visualizations.ipynb"
Task: "Create department comparison dashboard in notebooks/03_visualizations.ipynb"
Task: "Build advanced opportunity search interface in notebooks/03_visualizations.ipynb"
```

### Phase 6 - Final Deliverables
```
Task: "Export important visualizations (PNG or interactive HTML) to outputs/"
Task: "Create comprehensive analysis report in outputs/"
Task: "Validate all notebooks execute without errors from clean environment"
Task: "Update README.md with execution instructions and results summary"
Task: "Run linting and code quality checks on src/dvf_utils.py"
```

## Notes
- [P] tasks = different files/independent components, no dependencies
- Notebooks must execute sequentially: 01→02→03→04
- Verify data quality at each phase before proceeding
- Export results after each major phase for validation
- Focus on investor-friendly outputs and clear recommendations

## Key Functional Requirements Coverage
- **FR-001**: Data cleaning → T008-T013
- **FR-002**: Price per m² analysis → T016
- **FR-003**: Temporal analysis → T018
- **FR-004**: Investment zone ranking → T030-T031
- **FR-005**: Visualizations → T021-T027
- **FR-006**: Interactive widgets → T022-T025
- **FR-007**: Actionable recommendations → T032
- **FR-008**: Non-technical summary → T033
- **FR-009**: Property type analysis → T017
- **FR-010**: Zone avoidance detection → T031
- **FR-011**: Rental yield calculations → T029
- **FR-012**: 2019-2023 period analysis → T011

## Validation Checklist
*GATE: Checked before project completion*

- [ ] All DVF data processing requirements covered (FR-001, FR-011, FR-012)
- [ ] Statistical analyses address investor needs (FR-002, FR-003, FR-009)
- [ ] Interactive visualizations enable exploration (FR-005, FR-006)
- [ ] Investment recommendations are actionable (FR-004, FR-007, FR-010)
- [ ] Non-technical summary suitable for investors (FR-008)
- [ ] Parallel tasks truly independent (different files)
- [ ] Sequential dependencies respected (notebook order)
- [ ] Each task specifies exact file path
- [ ] All required outputs generated in outputs/ directory