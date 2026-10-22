# Additional paper content review

The additional content comprises Navigation Papers 2, 3 and 4, and Stability & Operations Papers 2 and 3. Each contains 35 original questions. The student library also retains the other three papers, with consistent subject and paper-number labels. Underlying IDs and response keys for those papers are unchanged.

## Reference basis

- [MCA Navigation 034-83, June 2024](https://assets.publishing.service.gov.uk/media/678e2b6eea48a571517acf4f/034-83_OOW_Navigation_Sylabus__Version_-_June_2024___002_.pdf), used from March 2025 exams onwards.
- [MCA Stability & Operations 034-84, June 2024](https://assets.publishing.service.gov.uk/media/679a064d1c041dcc469daeab/034-84_OOW_Stability_and_Operations_Syllabus__Version_-_June_2024_.pdf), used from March 2025 exams onwards.
- MCA MGN 364 Amendment 2 for TSS interpretation, MGN 315 for bridge watchkeeping, MCA enclosed-space guidance, MSN 1877 Amendment 2 for normal UK rest requirements, IMO MARPOL and ISM summaries, and ILO MLC complaint provisions. Exact URLs are in `tools/additional-paper-review.json`.

The author checked the current MCA syllabus listing and public operational references on 22 October 2026. The papers are practice adaptations with one mark per question, not replicas of official written papers or their marking schemes. Tidal curves and hydrostatic data are explicitly training data. No outside tide tables, almanacs or unbundled figures are needed to answer the new questions. Navigation calculations state the assumptions and any required formula or corrected celestial bearing. They do not imply that a corrected azimuth supplied in a question replaces the full almanac-reduction exercise in an official exam.

## Coverage

| Paper | Questions | Main syllabus sections represented |
| --- | ---: | --- |
| Navigation 2 | 35 | All nine: passage-plan stages, following a plan, routeing, course/speed adjustments, sailings, bridge watchkeeping, ice, tide causes/definitions, standard-port tide information |
| Navigation 3 | 35 | All nine; includes fixing geometry, set/drift, Mercator sailing across 180 degrees, operational checks and falling-tide interpolation |
| Navigation 4 | 35 | All nine; includes route changes, radar limitations, TSS manoeuvres, signed compass errors, south-westerly/south-easterly sailings, overhead limits and tides across midnight |
| Stability & Operations 2 | 35 | All six: flotation/buoyancy/loadlines, transverse stability, longitudinal stability, deck watch, pollution prevention and legislation |
| Stability & Operations 3 | 35 | All six; includes large hydrostatic changes, free surface, loll/list, longitudinal centres, loading/discharging draughts, hull stress and complaint procedures |

These are main-section coverage checks, not a claim that every individual sub-outcome is assessed in every paper. The practice collection is an aid alongside instruction and exercises using official publications.

## Marking and review

`tools/build_additional_papers.py` is the authored source. It deterministically distributes choice positions and writes the runtime bank plus a separate review record. Each new question has a syllabus reference and a rationale. The review record contains the key, units, assumptions and public-reference IDs; it is not included in the student bundles. The runtime retains the keys required for offline marking but never renders the rationales or per-question correctness.

Numeric fields accept the stated rounded answer within half a unit of the last requested decimal place. Empty fields never receive credit for zero. Signed values and equivalent decimal formatting are accepted; units belong in the field label. Every required part must be correct. The question banks are fixed: answer order and keys do not change between attempts.

Automated checks cover question counts, section references, all key shapes, figures, duplicate stems, numeric spot checks, blank/partial/extra selections, matching reset, placement regions, and complete-key/blank marking for all eight papers. Browser checks are required for library expansion, each input type, storage, figure controls, submission, locking and restart. Preserve those checks when making changes.

The author has reviewed the arithmetic and wording, but **an independent maritime subject-matter review has not been completed**. Automated checks cannot establish full educational validity. Existing paper content was retained rather than comprehensively re-authored or revalidated.
