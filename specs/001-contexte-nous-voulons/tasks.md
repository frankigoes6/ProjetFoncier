# Tasks: Analyse de Données Foncières DVF pour Investissement Immobilier (Simplifié)

**Input**: Design documents from `/specs/001-contexte-nous-voulons/`
**Prerequisites**: spec.md (available), README.md (available), requirements.txt (available)

## Execution Flow (main) - SIMPLIFIED TO 2 NOTEBOOKS
```
1. Load spec.md from feature directory ✓
   → Extract: Python/Jupyter tech stack, DVF data analysis, investor recommendations
2. Load project structure from README.md ✓
   → Extract: notebooks/, assets/, src/, outputs/ structure  
3. Load dependencies from requirements.txt ✓
   → Extract: pandas, matplotlib, ipywidgets (SIMPLIFIED - removed folium/plotly)
4. Generate tasks by category:
   → Setup: environment, dependencies, structure
   → Data: preprocessing, basic derived variables only
   → Application: unified analysis + visualization + recommendations
5. Apply task rules:
   → Different notebooks/files = mark [P] for parallel
   → Sequential notebooks = dependencies (01→02 ONLY)
   → Data preparation before application
6. Number tasks sequentially (T001, T002...)
7. Generate dependency graph
8. Create parallel execution examples
9. Validate task completeness for simplified DVF analysis project
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Project root**: `c:\Users\vtnde\Documents\Projets\ProjetFoncier`
- **Notebooks**: `notebooks/` (SIMPLIFIED: only 2 notebooks)
- **Assets**: `assets/`
- **Source**: `src/`
- **Outputs**: `outputs/`

## Phase 1: Environment Setup & Project Structure
- [ ] T001 Create Python 3.11 virtual environment (venv or conda)
- [ ] T002 Install core dependencies: pandas>=2.0.0, matplotlib>=3.7.0, jupyter>=1.0.0
- [ ] T003 [P] Install interactive dependencies: ipywidgets>=8.0.0 (SIMPLIFIED: removed folium, plotly)
- [ ] T004 [P] Install development tools: pytest>=7.4.0, black>=23.0.0, flake8>=6.0.0
- [ ] T005 Configure Jupyter Notebook environment and kernel
- [ ] T006 [P] Validate assets/dataset.csv exists and accessible
- [ ] T007 [P] Create outputs/ directory structure for results export

## Phase 2: Data Foundation (MUST COMPLETE BEFORE Phase 3)
**CRITICAL: Data preprocessing must be complete before any analysis**
- [ ] T008 Load and inspect assets/dataset.csv in notebooks/01_preprocessing.ipynb
- [ ] T009 Analyze DVF data structure: columns, data types, missing values in notebooks/01_preprocessing.ipynb
- [ ] T010 Clean data: handle missing values, remove duplicates, normalize postal codes/communes in notebooks/01_preprocessing.ipynb
- [ ] T011 Filter data for 2024 period in notebooks/01_preprocessing.ipynb
- [ ] T012 Create essential derived variable: prix_m2 calculation in notebooks/01_preprocessing.ipynb (SIMPLIFIED: removed complex categorizations)
- [ ] T013 Validate cleaned data integrity and export preprocessed dataset in notebooks/01_preprocessing.ipynb
- [ ] T014 [P] Create utility functions in src/dvf_utils.py for data loading and basic calculations

## Phase 3: Unified Application Notebook (ONLY after Phase 2 complete)
**NEW: Single notebook combining analysis, visualization, and recommendations**
- [ ] T015 Load cleaned data and create initial exploration section in notebooks/02_application_investisseur.ipynb
- [ ] T016 Implement descriptive statistics: price, surface, rooms by department/commune in notebooks/02_application_investisseur.ipynb
- [ ] T017 Add property type analysis (apartment, house) with simple widgets in notebooks/02_application_investisseur.ipynb
- [ ] T018 Create temporal evolution analysis: price trends 2024 in notebooks/02_application_investisseur.ipynb
- [ ] T019 Implement main interactive dashboard with ipywidgets: department filter, year slider, price/surface filters in notebooks/02_application_investisseur.ipynb
- [ ] T020 Add matplotlib visualizations: histograms, boxplots, temporal curves that update with dashboard in notebooks/02_application_investisseur.ipynb
- [ ] T021 Create dynamic statistics panel showing top communes, price ranges, volume counts in notebooks/02_application_investisseur.ipynb
- [ ] T022 Add simple investment recommendations section based on DVF data only (no external sources) in notebooks/02_application_investisseur.ipynb
- [ ] T023 Write clear markdown conclusions for non-technical investors in notebooks/02_application_investisseur.ipynb
- [ ] T024 [P] Extend src/dvf_utils.py with dashboard and analysis functions

## Phase 4: Deliverables & Quality Assurance (SIMPLIFIED)
- [ ] T025 [P] Export cleaned dataset to outputs/ directory
- [ ] T026 [P] Validate both notebooks execute without errors from clean environment
- [ ] T027 [P] Update README.md with simplified execution instructions
- [ ] T028 Package final deliverable: simplified notebooks + essential outputs
- [ ] T029 [P] Run linting and code quality checks on src/dvf_utils.py

## Dependencies (SIMPLIFIED)
- Environment setup (T001-T007) before data work (T008-T014)
- Data preprocessing (T008-T013) blocks application development (T015-T024)
- Application notebook development before deliverables (T025-T029)

## Sequential Notebook Dependencies (SIMPLIFIED)
```
01_preprocessing.ipynb → 02_application_investisseur.ipynb
```

## Parallel Execution Examples (SIMPLIFIED)

### Phase 1 - Dependencies & Setup
```
Task: "Install interactive dependencies: ipywidgets>=8.0.0 (SIMPLIFIED: removed folium, plotly)"
Task: "Install development tools: pytest>=7.4.0, black>=23.0.0, flake8>=6.0.0"
Task: "Validate assets/dataset.csv exists and accessible"
Task: "Create outputs/ directory structure for results export"
```

### Phase 2 - Utilities Development
```
Task: "Create utility functions in src/dvf_utils.py for data loading and basic calculations"
# Can run in parallel with T013 (data validation)
```

### Phase 3 - Application Components (All in single notebook)
```
# NOTE: These are sections within the same notebook, so they run sequentially
# No parallel execution possible within the unified application notebook
```

### Phase 4 - Final Deliverables
```
Task: "Export cleaned dataset to outputs/ directory"
Task: "Validate both notebooks execute without errors from clean environment"
Task: "Update README.md with simplified execution instructions"
Task: "Run linting and code quality checks on src/dvf_utils.py"
```

## Notes (UPDATED FOR SIMPLIFICATION)
- [P] tasks = different files/independent components, no dependencies
- **SIMPLIFIED**: Only 2 notebooks: 01→02 (instead of 01→02→03→04)
- **REMOVED**: Complex widgets, external data sources, multiple visualization libraries
- **FOCUSED**: Single interactive dashboard with essential filters and matplotlib charts
- Verify data quality at each phase before proceeding
- Focus on investor-friendly outputs and clear recommendations based on DVF data only

## Key Functional Requirements Coverage (SIMPLIFIED)
- **FR-001**: Data cleaning → T008-T013
- **FR-002**: Price per m² analysis → T016
- **FR-003**: Temporal analysis → T018
- **FR-004**: Investment zone ranking → T021 (via interactive dashboard)
- **FR-005**: Visualizations → T020 (matplotlib only)
- **FR-006**: Interactive widgets → T019 (single unified dashboard)
- **FR-007**: Actionable recommendations → T022
- **FR-008**: Non-technical summary → T023
- **FR-009**: Property type analysis → T017
- **FR-010**: Zone analysis → T021 (integrated in dashboard)
- **FR-011**: Investment insights → T022 (based on DVF data only, no external rental data)
- **FR-012**: 2024 period analysis → T011

## Validation Checklist (SIMPLIFIED)
*GATE: Checked before project completion*

- [ ] All DVF data processing requirements covered (FR-001, FR-011, FR-012)
- [ ] Statistical analyses address investor needs (FR-002, FR-003, FR-009)
- [ ] **SIMPLIFIED**: Single interactive dashboard enables exploration (FR-005, FR-006)
- [ ] Investment recommendations are actionable and based on DVF data only (FR-004, FR-007, FR-010)
- [ ] Non-technical summary suitable for investors (FR-008)
- [ ] **REMOVED**: Complex external data integration, multiple visualization libraries
- [ ] **REMOVED**: Multiple specialized widgets and scoring systems
- [ ] **FOCUSED**: Two-notebook structure with clear dependency flow
- [ ] Parallel tasks truly independent (different files)
- [ ] Sequential dependencies respected (01→02 notebook order)
- [ ] Each task specifies exact file path
- [ ] Essential outputs generated in outputs/ directory
- [ ] Uses only pandas, matplotlib, and ipywidgets (no folium/plotly/seaborn)

## REFACTORING SUMMARY
**FROM**: 4 complex notebooks (40 tasks) with multiple libraries and external data
**TO**: 2 focused notebooks (29 tasks) with essential functionality only

### Key Simplifications Made:
1. **Libraries**: Reduced from 7+ to 3 core libraries (pandas, matplotlib, ipywidgets)
2. **Notebooks**: Merged 02_analysis + 03_visualizations + 04_recommendations → single 02_application_investisseur.ipynb
3. **Widgets**: Removed multiple specialized widgets, kept one unified interactive dashboard
4. **Data Sources**: Removed external rental data integration, focus on DVF data only
5. **Visualizations**: Removed maps and complex charts, focus on matplotlib essentials
6. **Recommendations**: Simplified to actionable insights based on available data only
7. **Dependencies**: Streamlined from complex 4-phase flow to simple 2-notebook sequence