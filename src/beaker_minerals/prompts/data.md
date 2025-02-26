# USGS Mineral Commodity Data Structure

This document describes the data files included in the beaker_minerals package from the USGS Mineral Commodity Summaries 2025 Data Release.

## Directory Structure

The data is organized into three main categories from the original USGS release:

### 1. Salient Commodity Data
Located in `data/Salient_Commodity_Data_Release_Grouped/`

This is the largest and most detailed dataset containing:
- Individual commodity CSV files with detailed U.S. statistics
- Data for over 90 different mineral commodities
- For each commodity, includes:
  - Production volumes
  - Import/export quantities and values
  - Price data
  - Stock levels
  - Apparent consumption
  - Net import reliance

File naming convention:
- `mcs2025-{commodity}_salient.csv` - Individual commodity data files (e.g., mcs2025-alumi_salient.csv for aluminum)
- `mcs2025-{commodity}_meta.xml` - Corresponding metadata files with field descriptions

### 2. World Production Data  
Located in `data/World_Data_Release_MCS_2025/`

Contains global production statistics including:
- Country-by-country production data
- Global reserves information
- Production capacity by nation
- Historical production trends

Key files:
- `MCS2025_World_Data.csv` - Primary data file
- `MCS2025_World_Data.xml` - Field descriptions and methodology

### 3. Mineral Industry Trends
Located in `data/Mineral_Industry_Trends_And_Statistics_MCS_2025/`

Provides high-level industry analysis including:
- Price growth rates
- Consumption changes
- Critical mineral designations
- End-use applications
- State-by-state production data

Key files:
- `MCS2025_Fig*.csv` - Various trend analysis files
- `MCS2025_T*.csv` - Tables with industry statistics
- `MCS2025_Mineral_Industry_Trends_and_Salient_Statistics.xml` - Data definitions

## Working with the Data

### CSV File Structure
- All CSV files use comma delimiters
- First row contains column headers
- Missing values are typically marked as "-"
- Units are specified in the metadata files

### Metadata Files
The XML metadata files contain:
- Detailed field descriptions
- Unit specifications
- Data collection methodologies
- Quality assurance information
- Source citations

### Common Use Cases

1. Commodity Analysis:
   - Use individual commodity CSVs from the Salient Data directory
   - Cross-reference with world production data for global context

2. Market Research:
   - Combine price data with production/consumption statistics
   - Use trends data for historical patterns

3. Supply Chain Analysis:
   - Reference net import reliance data
   - Analyze country production capabilities
   - Review critical mineral designations

## Data Coverage
- Time Period: 2024 calendar year
- Geographic Scope: U.S. and global statistics
- Update Frequency: Annual
- Publication Date: January 31, 2025

## Complete Directory Structure

├── data
│   ├── Mineral_Industry_Trends_And_Statistics_MCS_2025
│   │   ├── MCS2025_Fig10_Price_Growth_Rates.csv
│   │   ├── MCS2025_Fig11_Pch_Consump_2023_2024.csv
│   │   ├── MCS2025_Fig12_Pch_Consump_2020_2024.csv
│   │   ├── MCS2025_Fig13_Scrap.csv
│   │   ├── MCS2025_Fig1_Minerals_in_Economy.csv
│   │   ├── MCS2025_Fig2_Net_Import_Reliance.csv
│   │   ├── MCS2025_Fig3_Major_Import_Sources.csv
│   │   ├── MCS2025_Fig4_Value_by_Type.csv
│   │   ├── MCS2025_Mineral_Industry_Trends_and_Salient_Statistics.xml
│   │   ├── MCS2025_T1_Mineral_Industry_Trends.csv
│   │   ├── MCS2025_T2_Mineral_Economic_Trends.csv
│   │   ├── MCS2025_T3_State_Value_Rank.csv
│   │   ├── MCS2025_T4_Critical_Minerals_End_Use.csv
│   │   └── MCS2025_T5_Critical_Minerals_Salient.csv
│   ├── Salient_Commodity_Data_Release_Grouped
│   │   ├── mcs2025-abras_meta.xml
│   │   ├── mcs2025-abras_salient.csv
│   │   ├── mcs2025-alumi_meta.xml
│   │   ├── mcs2025-alumi_salient.csv
│   │   ├── mcs2025-antim_meta.xml
│   │   ├── mcs2025-antim_salient.csv
│   │   ├── mcs2025-arsen_meta.xml
│   │   ├── mcs2025-arsen_salient.csv
│   │   ├── mcs2025-asbes_meta.xml
│   │   ├── mcs2025-asbes_salient.csv
│   │   ├── mcs2025-barit_meta.xml
│   │   ├── mcs2025-barit_salient.csv
│   │   ├── mcs2025-bauxi_meta.xml
│   │   ├── mcs2025-bauxi_salient.csv
│   │   ├── mcs2025-beryl_meta.xml
│   │   ├── mcs2025-beryl_salient.csv
│   │   ├── mcs2025-bismu_meta.xml
│   │   ├── mcs2025-bismu_salient.csv
│   │   ├── mcs2025-boron_meta.xml
│   │   ├── mcs2025-boron_salient.csv
│   │   ├── mcs2025-bromi_meta.xml
│   │   ├── mcs2025-bromi_salient.csv
│   │   ├── mcs2025-cadmi_meta.xml
│   │   ├── mcs2025-cadmi_salient.csv
│   │   ├── mcs2025-cemen_meta.xml
│   │   ├── mcs2025-cemen_salient.csv
│   │   ├── mcs2025-chrom_meta.xml
│   │   ├── mcs2025-chrom_salient.csv
│   │   ├── mcs2025-clays_meta.xml
│   │   ├── mcs2025-clays_salient.csv
│   │   ├── mcs2025-cobal_meta.xml
│   │   ├── mcs2025-cobal_salient.csv
│   │   ├── mcs2025-coppe_meta.xml
│   │   ├── mcs2025-coppe_salient.csv
│   │   ├── mcs2025-diamo_meta.xml
│   │   ├── mcs2025-diamo_salient.csv
│   │   ├── mcs2025-diato_meta.xml
│   │   ├── mcs2025-diato_salient.csv
│   │   ├── mcs2025-felds_meta.xml
│   │   ├── mcs2025-felds_salient.csv
│   │   ├── mcs2025-feore_meta.xml
│   │   ├── mcs2025-feore_salient.csv
│   │   ├── mcs2025-fepig_meta.xml
│   │   ├── mcs2025-fepig_salient.csv
│   │   ├── mcs2025-fescr_meta.xml
│   │   ├── mcs2025-fescr_salient.csv
│   │   ├── mcs2025-fesla_meta.xml
│   │   ├── mcs2025-fesla_salient.csv
│   │   ├── mcs2025-feste_meta.xml
│   │   ├── mcs2025-feste_salient.csv
│   │   ├── mcs2025-fluor_meta.xml
│   │   ├── mcs2025-fluor_salient.csv
│   │   ├── mcs2025-galli_meta.xml
│   │   ├── mcs2025-galli_salient.csv
│   │   ├── mcs2025-garne_meta.xml
│   │   ├── mcs2025-garne_salient.csv
│   │   ├── mcs2025-gemst_meta.xml
│   │   ├── mcs2025-gemst_salient.csv
│   │   ├── mcs2025-germa_meta.xml
│   │   ├── mcs2025-germa_salient.csv
│   │   ├── mcs2025-gold_meta.xml
│   │   ├── mcs2025-gold_salient.csv
│   │   ├── mcs2025-graph_meta.xml
│   │   ├── mcs2025-graph_salient.csv
│   │   ├── mcs2025-gypsu_meta.xml
│   │   ├── mcs2025-gypsu_salient.csv
│   │   ├── mcs2025-heliu_meta.xml
│   │   ├── mcs2025-heliu_salient.csv
│   │   ├── mcs2025-indiu_meta.xml
│   │   ├── mcs2025-indiu_salient.csv
│   │   ├── mcs2025-iodin_meta.xml
│   │   ├── mcs2025-iodin_salient.csv
│   │   ├── mcs2025-kyani_meta.xml
│   │   ├── mcs2025-kyani_salient.csv
│   │   ├── mcs2025-lead_meta.xml
│   │   ├── mcs2025-lead_salient.csv
│   │   ├── mcs2025-lime_meta.xml
│   │   ├── mcs2025-lime_salient.csv
│   │   ├── mcs2025-lithi_meta.xml
│   │   ├── mcs2025-lithium_salient.csv
│   │   ├── mcs2025-manga_meta.xml
│   │   ├── mcs2025-manga_salient.csv
│   │   ├── mcs2025-mercu_meta.xml
│   │   ├── mcs2025-mercu_salient.csv
│   │   ├── mcs2025-mgcomp_meta.xml
│   │   ├── mcs2025-mgcomp_salient.csv
│   │   ├── mcs2025-mgmet_meta.xml
│   │   ├── mcs2025-mgmet_salient.csv
│   │   ├── mcs2025-mica_meta.xml
│   │   ├── mcs2025-mica_salient.csv
│   │   ├── mcs2025-molyb_meta.xml
│   │   ├── mcs2025-molyb_salient.csv
│   │   ├── mcs2025-nicke_meta.xml
│   │   ├── mcs2025-nicke_salient.csv
│   │   ├── mcs2025-niobi_meta.xml
│   │   ├── mcs2025-niobi_salient.csv
│   │   ├── mcs2025-nitro_meta.xml
│   │   ├── mcs2025-nitro_salient.csv
│   │   ├── mcs2025-peat_meta.xml
│   │   ├── mcs2025-peat_salient.csv
│   │   ├── mcs2025-perli_meta.xml
│   │   ├── mcs2025-perli_salient.csv
│   │   ├── mcs2025-phosp_meta.xml
│   │   ├── mcs2025-phosp_salient.csv
│   │   ├── mcs2025-plati_meta.xml
│   │   ├── mcs2025-plati_salient.csv
│   │   ├── mcs2025-potas_meta.xml
│   │   ├── mcs2025-potas_salient.csv
│   │   ├── mcs2025-pumic_meta.xml
│   │   ├── mcs2025-pumic_salient.csv
│   │   ├── mcs2025-quart_meta.xml
│   │   ├── mcs2025-quart_salient.csv
│   │   ├── mcs2025-rareee_meta.xml
│   │   ├── mcs2025-rareee_salient.csv
│   │   ├── mcs2025-rheni_meta.xml
│   │   ├── mcs2025-rheni_salient.csv
│   │   ├── mcs2025-salt_meta.xml
│   │   ├── mcs2025-salt_salient.csv
│   │   ├── mcs2025-sandc_meta.xml
│   │   ├── mcs2025-sandc_salient.csv
│   │   ├── mcs2025-sandi_meta.xml
│   │   ├── mcs2025-sandi_salient.csv
│   │   ├── mcs2025-scand_meta.xml
│   │   ├── mcs2025-scand_salient.csv
│   │   ├── mcs2025-selen_meta.xml
│   │   ├── mcs2025-selen_salient.csv
│   │   ├── mcs2025-silve_meta.xml
│   │   ├── mcs2025-silve_salient.csv
│   │   ├── mcs2025-simet_meta.xml
│   │   ├── mcs2025-simet_salient.csv
│   │   ├── mcs2025-sodaa_meta.xml
│   │   ├── mcs2025-sodaa_salient.csv
│   │   ├── mcs2025-stonc_meta.xml
│   │   ├── mcs2025-stonc_salient.csv
│   │   ├── mcs2025-stond_meta.xml
│   │   ├── mcs2025-stond_salient.csv
│   │   ├── mcs2025-stron_meta.xml
│   │   ├── mcs2025-stron_salient.csv
│   │   ├── mcs2025-sulfu_meta.xml
│   │   ├── mcs2025-sulfu_salient.csv
│   │   ├── mcs2025-talc_meta.xml
│   │   ├── mcs2025-talc_salient.csv
│   │   ├── mcs2025-tanta_meta.xml
│   │   ├── mcs2025-tanta_salient.csv
│   │   ├── mcs2025-tellu_meta.xml
│   │   ├── mcs2025-tellu_salient.csv
│   │   ├── mcs2025-thall_meta.xml
│   │   ├── mcs2025-thall_salient.csv
│   │   ├── mcs2025-thori_meta.xml
│   │   ├── mcs2025-thori_salient.csv
│   │   ├── mcs2025-timin_meta.xml
│   │   ├── mcs2025-timin_salient.csv
│   │   ├── mcs2025-tin_meta.xml
│   │   ├── mcs2025-tin_salient.csv
│   │   ├── mcs2025-titan_meta.xml
│   │   ├── mcs2025-titan_salient.csv
│   │   ├── mcs2025-tungs_meta.xml
│   │   ├── mcs2025-tungs_salient.csv
│   │   ├── mcs2025-vanad_meta.xml
│   │   ├── mcs2025-vanad_salient.csv
│   │   ├── mcs2025-vermi_meta.xml
│   │   ├── mcs2025-vermi_salient.csv
│   │   ├── mcs2025-yttri_meta.xml
│   │   ├── mcs2025-yttri_salient.csv
│   │   ├── mcs2025-zeoli_meta.xml
│   │   ├── mcs2025-zeoli_salient.csv
│   │   ├── mcs2025-zinc_meta.xml
│   │   ├── mcs2025-zinc_salient.csv
│   │   ├── mcs2025-zirco_meta.xml
│   │   └── mcs2025-zirco_salient.csv
│   └── World_Data_Release_MCS_2025
│       ├── MCS2025_World_Data.csv
│       └── MCS2025_World_Data.xml