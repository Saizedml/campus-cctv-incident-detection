# Data, licences and access

**No datasets, annotations or model weights are redistributed.** Public media in this repository consist of original diagrams, aggregate plots and synthetic interface examples. Dataset names describe the research sources, not files included in the release. Download from the authors, check their current terms, and obtain any required acknowledgement yourself. The code's MIT licence does not relicense datasets or external models.

The table records the project roles and documented terms. Author/source links also identify the requested citation. Non-commercial, share-alike, stock-image and privacy conditions remain attached to their sources. Licence metadata can conflict with accompanying terms; the stricter unresolved restriction is retained below. Some source pages could not be re-read during release preparation; those are explicitly marked rather than presented as newly verified permission.

## Weapon sources

| Dataset / citation | Research role | Recorded licence or terms | Access / citation source |
|---|---|---|---|
| Sohas / ODeBiC, Pérez-Hernández and colleagues | Training, including held-object look-alikes | CC BY-SA 4.0 | [OD-WeaponDetection release](https://github.com/ari-dasci/OD-WeaponDetection) |
| OD-WeaponDetection, Castillo and colleagues | Knife detector and verifier training | CC BY-SA 4.0 | [Author repository and licence](https://github.com/ari-dasci/OD-WeaponDetection/blob/master/License.md) |
| Dangerous Items, Zbigniew Omiotek | Grouped training/validation; original full-frame reference test | CC BY 4.0 in the research inventory; mixed-source provenance requires care | [Author Zenodo release and paper citation](https://zenodo.org/records/16422779) |
| HOD, Ha, Kim and Na | Knife training subset | Research only; no redistribution; source stock-image rights also apply | [Author repository](https://github.com/poori-nuna/HOD-Benchmark-Dataset) |
| Open Images, Kuznetsova and colleagues | Knife positives, look-alikes and hard negatives | Annotations CC BY 4.0; images listed as CC BY 2.0, with per-image source attribution | [Official licence statement](https://storage.googleapis.com/openimages/web/factsfigures_v7.html) |
| LVIS, Gupta, Dollár and Girshick; COCO images | Training look-alikes and object context | Annotations CC BY 4.0; image-specific COCO/Flickr terms. LVIS page was unavailable for the release recheck | [LVIS source](https://www.lvisdataset.org/dataset), [COCO terms](https://cocodataset.org/#termsofuse) |
| USRT Mock Attack, Salazar González and colleagues | Camera-separated validation and locked weapon evaluation; no training | CC BY-NC 4.0 | [Author project and citation](https://deepknowledge-us.github.io/US-Real-time-gun-detection-in-CCTV-An-open-problem-dataset/) |
| CCTV-Gun, Yellapragada and colleagues | Proposed recency comparison only; not run | Component and repository terms must be checked before reuse; no release permission assumed | [Author repository](https://github.com/srikarym/CCTV-Gun) |

Keep source/video groups together and deduplicate before splitting. USRT cameras share actors and scenery; the locked camera is not a new-actor evaluation. Positive sequences are not continuous negative exposure. The frozen grouped Dangerous Items membership was retained, with held-out images removed from training by hash.

## Negative footage

| Dataset / citation | Research role | Recorded licence or terms | Access / citation source |
|---|---|---|---|
| MEVA, team and dataset authors | Separate validation sites and unseen school-site test; bus-site hard-negative mining | CC BY 4.0 | [Official project](https://mevadata.org/), [data description](https://mevadata.org/resources/README-meva-kf1-data.html) |
| NWPU Campus, Cao, Lu, Wang and Zhang | Independent negative test exposure from its normal training split | Academic, non-commercial research only; no redistribution or derived datasets without permission; privacy and indemnity terms | [Official project and CVPR citation](https://campusvad.github.io/) |

Fixed RGB MEVA footage is used; IR and PTZ sources are excluded. Absence of weapon/fall labels is not proof that every interval is incident-free. NWPU's normal training split is held out by this project; its abnormal test videos are not used for the reported negative rates.

## Falls sources

| Dataset / citation | Research role | Recorded licence or terms | Access / citation source |
|---|---|---|---|
| OmniFall, benchmark authors | Unified labels, splits and synthetic training | Dataset-card metadata says CC BY-NC 4.0, while accompanying text has stated CC BY-NC-SA 4.0; resolve this inconsistency before redistribution | [Author dataset card, paper and package](https://huggingface.co/datasets/simplexsigil2/omnifall) |
| OF-Synthetic, OmniFall authors | Synthetic falls/posture training | OmniFall terms above | [Author dataset card](https://huggingface.co/datasets/simplexsigil2/omnifall) |
| OF-In-the-Wild, derived from Oops!, Epstein and colleagues / OmniFall authors | Locked falls evaluation | CC BY-NC-SA 4.0; non-commercial research or education; source and annotation terms both apply | [Oops! author data terms](https://oops.cs.columbia.edu/data/), [OmniFall citation](https://huggingface.co/datasets/simplexsigil2/omnifall) |
| Le2i, Dubois and Miteran | Staged training and held-out event tuning | CC BY-NC-SA 3.0 in the research inventory; source recheck was access-blocked | [Institutional source and DOI](https://search-data.ubfc.fr/imvia/FR-13002091000019-2024-04-09_Fall-Detection-Dataset.html) |
| GMDCSA24, Alam and colleagues | Staged training and subject-separated validation | MIT in the author repository | [Author release](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos) |
| CAUCAFall, Eraso and colleagues | Staged RGB training and subject-separated validation; IR excluded | CC BY 4.0 | [Mendeley source and citation](https://data.mendeley.com/datasets/7w7fccy7ky/4) |
| EDF, Zhang, Conly and Athitsos | Staged training and continuous event tuning; RGB only | CC BY 4.0 | [Author archive and citation](https://zenodo.org/records/15494102) |
| OCCU, Zhang, Conly and Athitsos | Occlusion-rich staged training and event tuning; RGB only | CC BY 4.0 | [Author archive and citation](https://zenodo.org/records/15494102) |

## Violence options, future work only

No violence model or result is included. The planned pose/change-detection/ConvLSTM reproduction uses RWF-2000's official split; a frozen V-JEPA 2 feature arm would test transfer. Bus Violence is reserved as a distinct source. Continuous fight intervals remain an access/licensing gap.

| Dataset / citation | Proposed role | Recorded licence or terms | Access / citation source |
|---|---|---|---|
| RWF-2000, Cheng, Cai and Li | Reproduction training/validation | Zenodo records CC BY 4.0, but the author repository forbids modification, redistribution and commercial use without approval. Retain those stricter terms; Zenodo recheck was rate-limited | [Author terms](https://github.com/mchengny/RWF2000-Video-Database-for-Violence-Detection), [author Zenodo record](https://zenodo.org/records/15687512) |
| SCVD, Aremu and colleagues | Additional clip-level training/validation | CC BY-NC-SA 4.0 in the research inventory; account access required; page text unavailable in release recheck | [Author Kaggle release](https://www.kaggle.com/datasets/toluwaniaremu/smartcity-cctv-violence-detection-dataset-scvd) |
| SCFD, Aktı and colleagues | Additional surveillance fight clips | MIT in the author repository | [Author release](https://github.com/seymanurakti/fight-detection-surv-dataset) |
| AIRTLab, Bianculli and colleagues | Staged violence and hugging/clapping hard negatives | Research and educational use; do not infer unrestricted redistribution | [Author release](https://github.com/airtlab/A-Dataset-for-Automatic-Violence-Detection-in-Videos) |
| Bus Violence, Ciampi, Foszner and colleagues | Cross-dataset test | CC BY-NC 4.0 | [Author project and citation](https://ciampluca.github.io/bus_violence_dataset/), [archive](https://zenodo.org/records/7044203) |
| UBI-Fights, Degardin and Proença | Conditional continuous event evaluation | Licence unclear; clearance required before use | [Author project](http://socia-lab.di.ubi.pt/EventDetection/) |

Sources excluded or deferred for unavailable access, unclear terms or weak suitability include CMDFall, UP-Fall, MCFD, UCF-Crime, Armed CCTV Footage, ADOC, VIRAT, MSAD, IITB-Corridor, Street Scene, NTU CCTV-Fights and commercial/gated violence collections. Unofficial mirrors are not a substitute for permission. None is redistributed or used to imply extra benchmark coverage here.

## Reproducing training or building a demo bundle

Acquire data from the sources above under their terms. Establish source-, subject- and site-separated splits before fitting anything; remove duplicate held-out images by content hash. Train the task heads on authorised training data, select thresholds on validation, then freeze a new version before a fresh held-out assessment. This curated release does not include the private experiment orchestration or pretend that new weights will reproduce the published outcome automatically.

For a local replay bundle, use footage you may process, export evidence through the pipeline interfaces, and point the dashboard at your local output directory. Do not put a bundle in Git. A downloadable release asset requires explicit redistribution rights for every clip, validation/demo-only membership and per-file attribution. The present release ships synthetic interface examples instead.
