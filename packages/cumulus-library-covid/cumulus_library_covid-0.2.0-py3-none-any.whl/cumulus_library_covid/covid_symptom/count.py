from typing import List
from cumulus_library.schema import counts


def table(tablename: str, duration=None, study_prefix="covid_symptom") -> str:
    if duration:
        return f"{study_prefix}__{tablename}_{duration}"
    else:
        return f"{study_prefix}__{tablename}"


def count_dx(duration="week"):
    """
    covid_symptom__count_dx_week
    covid_symptom__count_dx_month
    """
    view_name = table("count_dx", duration)
    from_table = table("dx")
    cols = [
        f"cond_{duration}",
        "enc_class_code",
        "age_at_visit",
        "ed_note",
        "variant_era",
    ]
    return counts.count_encounter(view_name, from_table, cols)


def count_pcr(duration="week"):
    """
    covid_symptom__count_pcr_week
    covid_symptom__count_pcr_month
    """
    view_name = table("count_pcr", duration)
    from_table = table("pcr")
    cols = [
        f"covid_pcr_{duration}",
        "covid_pcr_result_display",
        "variant_era",
        "ed_note",
        "age_at_visit",
        "gender",
        "race_display",
    ]
    return counts.count_encounter(view_name, from_table, cols)


def count_study_period(duration="month"):
    """
    covid_symptom__count_study_period_week
    covid_symptom__count_study_period_month
    covid_symptom__count_study_period_year
    """
    view_name = table("count_study_period", duration)
    from_table = table("study_period")
    cols = [
        f"start_{duration}",
        "variant_era",
        "ed_note",
        "gender",
        "age_group",
        "race_display",
    ]
    return counts.count_encounter(view_name, from_table, cols)


def count_prevalence_ed(duration="month"):
    view_name = table("count_prevalence_ed", duration)
    from_table = table("prevalence_ed")
    cols = [
        f"author_{duration}",
        "covid_dx",
        "covid_icd10",
        "covid_pcr_result",
        "covid_symptom",
        "symptom_icd10_display",
        "variant_era",
        "age_group",
        "enc_class_code",
    ]
    return counts.count_encounter(view_name, from_table, cols)


def count_symptom(duration="week"):
    """
    covid_symptom__count_symptom_week
    covid_symptom__count_symptom_month
    """
    view_name = table("count_symptom", duration)
    from_table = table("symptom_nlp")
    cols = [
        f"author_{duration}",
        "symptom_display",
        "variant_era",
        "age_group",
        "gender",
        "race_display",
        "enc_class_code",
        "ed_note",
    ]
    return counts.count_encounter(view_name, from_table, cols)


def concat_view_sql(create_view_list: List[str]) -> str:
    """
    :param create_view_list: SQL prepared statements
    """
    seperator = "-- ###########################################################"
    concat = list()

    for create_view in create_view_list:
        concat.append(seperator + "\n" + create_view + "\n")

    return "\n".join(concat)


def write_view_sql(view_list_sql: List[str], filename="count.sql") -> None:
    """
    :param view_list_sql: SQL prepared statements
    :param filename: path to output file, default 'count.sql' in PWD
    """
    sql_optimizer = concat_view_sql(view_list_sql)
    sql_optimizer = sql_optimizer.replace("ORDER BY cnt desc", "")
    sql_optimizer = sql_optimizer.replace("CREATE or replace VIEW", "CREATE TABLE")
    with open(filename, "w") as fout:
        fout.write(sql_optimizer)


if __name__ == "__main__":
    write_view_sql(
        [
            count_dx("month"),
            count_dx("week"),
            count_pcr("month"),
            count_pcr("week"),
            count_study_period("month"),
            count_study_period("week"),
            count_symptom("week"),
            count_symptom("month"),
            count_prevalence_ed("month"),
            count_prevalence_ed("week"),
        ]
    )
