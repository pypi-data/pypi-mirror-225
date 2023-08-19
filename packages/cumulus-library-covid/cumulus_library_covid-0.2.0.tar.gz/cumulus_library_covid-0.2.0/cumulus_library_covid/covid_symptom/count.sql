-- ###########################################################
CREATE TABLE covid_symptom__count_dx_month AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        cond_month,
        enc_class_code,
        age_at_visit,
        ed_note,
        variant_era
    FROM covid_symptom__dx
    GROUP BY cube(cond_month, enc_class_code, age_at_visit, ed_note, variant_era)
)

SELECT
    cnt_encounter AS cnt,
    cond_month,
    enc_class_code,
    age_at_visit,
    ed_note,
    variant_era
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_dx_week AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        cond_week,
        enc_class_code,
        age_at_visit,
        ed_note,
        variant_era
    FROM covid_symptom__dx
    GROUP BY cube(cond_week, enc_class_code, age_at_visit, ed_note, variant_era)
)

SELECT
    cnt_encounter AS cnt,
    cond_week,
    enc_class_code,
    age_at_visit,
    ed_note,
    variant_era
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_pcr_month AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        covid_pcr_month,
        covid_pcr_result_display,
        variant_era,
        ed_note,
        age_at_visit,
        gender,
        race_display
    FROM covid_symptom__pcr
    GROUP BY
        cube(
            covid_pcr_month,
            covid_pcr_result_display,
            variant_era,
            ed_note,
            age_at_visit,
            gender,
            race_display
        )
)

SELECT
    cnt_encounter AS cnt,
    covid_pcr_month,
    covid_pcr_result_display,
    variant_era,
    ed_note,
    age_at_visit,
    gender,
    race_display
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_pcr_week AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        covid_pcr_week,
        covid_pcr_result_display,
        variant_era,
        ed_note,
        age_at_visit,
        gender,
        race_display
    FROM covid_symptom__pcr
    GROUP BY
        cube(
            covid_pcr_week,
            covid_pcr_result_display,
            variant_era,
            ed_note,
            age_at_visit,
            gender,
            race_display
        )
)

SELECT
    cnt_encounter AS cnt,
    covid_pcr_week,
    covid_pcr_result_display,
    variant_era,
    ed_note,
    age_at_visit,
    gender,
    race_display
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_study_period_month AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        start_month,
        variant_era,
        ed_note,
        gender,
        age_group,
        race_display
    FROM covid_symptom__study_period
    GROUP BY cube(start_month, variant_era, ed_note, gender, age_group, race_display)
)

SELECT
    cnt_encounter AS cnt,
    start_month,
    variant_era,
    ed_note,
    gender,
    age_group,
    race_display
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_study_period_week AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        start_week,
        variant_era,
        ed_note,
        gender,
        age_group,
        race_display
    FROM covid_symptom__study_period
    GROUP BY cube(start_week, variant_era, ed_note, gender, age_group, race_display)
)

SELECT
    cnt_encounter AS cnt,
    start_week,
    variant_era,
    ed_note,
    gender,
    age_group,
    race_display
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_symptom_week AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        author_week,
        symptom_display,
        variant_era,
        age_group,
        gender,
        race_display,
        enc_class_code,
        ed_note
    FROM covid_symptom__symptom_nlp
    GROUP BY
        cube(
            author_week,
            symptom_display,
            variant_era,
            age_group,
            gender,
            race_display,
            enc_class_code,
            ed_note
        )
)

SELECT
    cnt_encounter AS cnt,
    author_week,
    symptom_display,
    variant_era,
    age_group,
    gender,
    race_display,
    enc_class_code,
    ed_note
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_symptom_month AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        author_month,
        symptom_display,
        variant_era,
        age_group,
        gender,
        race_display,
        enc_class_code,
        ed_note
    FROM covid_symptom__symptom_nlp
    GROUP BY
        cube(
            author_month,
            symptom_display,
            variant_era,
            age_group,
            gender,
            race_display,
            enc_class_code,
            ed_note
        )
)

SELECT
    cnt_encounter AS cnt,
    author_month,
    symptom_display,
    variant_era,
    age_group,
    gender,
    race_display,
    enc_class_code,
    ed_note
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_prevalence_ed_month AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        author_month,
        covid_dx,
        covid_icd10,
        covid_pcr_result,
        covid_symptom,
        symptom_icd10_display,
        variant_era,
        age_group,
        enc_class_code
    FROM covid_symptom__prevalence_ed
    GROUP BY
        cube(
            author_month,
            covid_dx,
            covid_icd10,
            covid_pcr_result,
            covid_symptom,
            symptom_icd10_display,
            variant_era,
            age_group,
            enc_class_code
        )
)

SELECT
    cnt_encounter AS cnt,
    author_month,
    covid_dx,
    covid_icd10,
    covid_pcr_result,
    covid_symptom,
    symptom_icd10_display,
    variant_era,
    age_group
FROM powerset
WHERE cnt_subject >= 10;

-- ###########################################################
CREATE TABLE covid_symptom__count_prevalence_ed_week AS
WITH powerset AS (
    SELECT
        count(DISTINCT subject_ref) AS cnt_subject,
        count(DISTINCT encounter_ref) AS cnt_encounter,
        author_week,
        covid_dx,
        covid_icd10,
        covid_pcr_result,
        covid_symptom,
        symptom_icd10_display,
        variant_era,
        age_group,
        enc_class_code
    FROM covid_symptom__prevalence_ed
    GROUP BY
        cube(
            author_week,
            covid_dx,
            covid_icd10,
            covid_pcr_result,
            covid_symptom,
            symptom_icd10_display,
            variant_era,
            age_group,
            enc_class_code
        )
)

SELECT
    cnt_encounter AS cnt,
    author_week,
    covid_dx,
    covid_icd10,
    covid_pcr_result,
    covid_symptom,
    symptom_icd10_display,
    variant_era,
    age_group
FROM powerset
WHERE cnt_subject >= 10;
