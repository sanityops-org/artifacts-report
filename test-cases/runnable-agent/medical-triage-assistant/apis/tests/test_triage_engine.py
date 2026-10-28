"""Treaging engine test."""

from pathlib import Path

import pytest

from apis.data_store import DataStore
from apis.triage_engine import RedFlagResult, check_red_flags, normalize
from models.enums import RedFlagAction, RedFlagLevel

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


@pytest.fixture(scope="module")
def rules() -> list[dict]:
    return DataStore(data_dir=DATA_DIR).load_red_flag_rules()


# --- Normalization ---

def test_normalize_removes_whitespace():
    """Remove all blanks (including full-width spaces)"""
    assert normalize("Chest pain\u3000, panting\nout of breath!") == "chest pain, panting out of breath!"


def test_normalize_converts_fullwidth_ascii():
    """Full angle ASCII to half angle"""
    assert normalize("ＡＢ１２３！") == "ab123!"


def test_normalize_handles_empty_input():
    """Empty input and None safely return empty strings"""
    assert normalize("") == ""
    assert normalize(None) == ""


# --- Red flag hit: data-driven, keyword by keyword ---

def test_every_keyword_of_every_rule_hits(rules):
    """Each keyword of each rule is called separately, and the action is legal (success standard 1）"""
    # Do not verify result.rule_id == rule["rule_id"]: Specification 5.1 stipulates the order of the rule table file at the same level,
    # And the example keywords of standard 9.2 have a relationship itself (such as "dyspnea" ⊂ "general rash with dyspnea"),
    # The more advanced general rules will be hit first, and each keyword only needs to ensure that "it is hit and the action is legal".
    for rule in rules:
        for keyword in rule["keywords"]:
            result = check_red_flags(keyword, rules)
            assert result.hit is True, f"{rule['rule_id']} The keyword is not hit.: {keyword}"
            assert result.matched_keywords, f"{rule['rule_id']} The keyword is not hit.: {keyword}"
            assert result.action in (
                RedFlagAction.CALL_120_OR_ER,
                RedFlagAction.ER_SOON,
            )


def test_every_rule_has_matching_level_and_action(rules):
    """The severity corresponds to the disposal action one by one."""
    for rule in rules:
        result = check_red_flags(rule["keywords"][0], rules)
        if rule["level"] == "emergency":
            assert result.level == RedFlagLevel.EMERGENCY
            assert result.action == RedFlagAction.CALL_120_OR_ER
        else:
            assert result.level == RedFlagLevel.URGENT
            assert result.action == RedFlagAction.ER_SOON


def test_hit_returns_advice_and_name(rules):
    """Return the suggested copy and rule name when hit"""
    result = check_red_flags("I suddenly had a terrible chest pain.", rules)

    assert result.hit is True
    assert result.rule_id == "RF001"
    assert result.name == "Chest pain / squeezing pain in the anterior region"
    assert "120" in result.advice


# --- Negative example: zero false alarm (success standard 2）---

@pytest.mark.parametrize(
    "text",
    [
        "I have a little insomnia recently.",
        "The tooth is a little sore.",
        "I want to have a routine physical examination.",
        "There are a few small rashes on my arm, which are a little itchy.",
        "The child doesn't like to eat recently.",
        "My blood pressure is a little high. I want to check it again.",
    ],
)
def test_non_red_flag_text_does_not_hit(text, rules):
    """The non-red flag text is not hit."""
    result = check_red_flags(text, rules)

    assert result.hit is False
    assert result.rule_id is None
    assert result.action is None
    assert result.matched_keywords == []


# --- Certainty when hitting more than one ---

def test_emergency_wins_over_urgent(rules):
    """Take it when you hit emergency and urgent at the same time emergency"""
    result = check_red_flags("I vomited after falling on my head, and now I'm unconscious.", rules)

    assert result.hit is True
    assert result.level == RedFlagLevel.EMERGENCY
    assert result.action == RedFlagAction.CALL_120_OR_ER


def test_same_level_uses_file_order(rules):
    """When hit at the same level, take the first one in the order of the rule file."""
    result = check_red_flags("Chest pain and shortness of breath", rules)

    assert result.rule_id == "RF001"


def test_result_is_deterministic(rules):
    """The same input multiple calls have the same result."""
    first = check_red_flags("Chest pain", rules)
    second = check_red_flags("Chest pain", rules)

    assert first.model_dump(mode="json") == second.model_dump(mode="json")


# --- Review Focus 1：Spoken long sentences / full-width characters / blanks / blank input ---

def test_fullwidth_and_whitespace_input_still_hits(rules):
    """Full-width spaces and full-width punctuation do not affect the hit."""
    result = check_red_flags("Chest pain, shortness of breath! \nIt's been half an hour.", rules)

    assert result.hit is True
    assert result.rule_id in {"RF001", "RF002"}
    assert "Chest pain" in result.matched_keywords


def test_long_colloquial_sentence_hits(rules):
    """Long spoken sentences are not abnormal, and can hit the red flag (the keyword of "pressure panic")"""
    text = (
        "Hello, doctor. My mother is 68 years old. When she got up this morning, she said that her chest had been hurting."
        "I was in a panic and sweated. I didn't have this problem before. I want to ask what to do."
        "My home is a little far from the hospital. Should I take some medicine first or go there directly?"
    )
    result = check_red_flags(text, rules)

    assert isinstance(result, RedFlagResult)
    # This sentence hits RF001 through the keyword "pressure panic": Inserting adverbs in spoken language will disconnect "chest pain",
    # 「"Pressing panic" is a common saying to supplement this. Hit is directed to the emergency room - in line with the safety direction of "I'd rather ask one more question".
    assert result.hit is True
    assert result.rule_id == "RF001"
    assert result.action == RedFlagAction.CALL_120_OR_ER
    assert any("panic" in keyword.lower() for keyword in result.matched_keywords)

    # The same condition is equally hit when expressed in norms, which proves that the rule itself is effective.
    canonical = check_red_flags("Chest pain, squeezing pain", rules)
    assert canonical.hit is True
    assert canonical.rule_id == "RF001"


# --- Review Focus：Real spoken long sentence regression corpus (covering ≥6 rules)---

@pytest.mark.parametrize(
    "text,expected_rule",
    [
        # RF001 Chest pain / anterior region of the heart
        ("When my mother got up this morning, she said that she had a chest pain and was sweating.", "RF001"),
        ("Recently, my chest is always tight, and I'm short of breath when I take two steps.", "RF001"),
        ("His heart ached so much that he was sweating and his face turned pale.", "RF001"),
        ("My chest is stuffy these days, especially when I lie down at night.", "RF001"),
        ("My father's anterior chest pain is the kind of squeezing pain.", "RF001"),
        # RF002 Difficulty in breathing
        ("I can't breathe after climbing two floors. I have to rest for a while.", "RF002"),
        ("I suddenly woke up in the middle of the night and couldn't breathe.", "RF002"),
        ("I always feel that it is hard to breathe, and I feel short of breath when I walk a few steps.", "RF002"),
        # RF003 DISORDER OF CONSCIOUSNESS / FAINTING / CONVULSIONS
        ("The old man suddenly fainted, and he didn't respond.", "RF003"),
        ("He suddenly fainted and his face turned blue.", "RF003"),
        ("Friends are confused and can't answer questions clearly.", "RF003"),
        # RF004 Massive haemorrhage
        ("He has been coughing up blood, and the amount is quite high.", "RF004"),
        ("Spit out a pool of blood, which looks like a lot of bleeding.", "RF004"),
        ("The nose is bleeding non-stop, and I can't stop the cotton stuffing.", "RF004"),
        # RF005 Suspected stroke
        ("My father can't move half of his body and can't speak clearly.", "RF005"),
        ("When I got up in the morning, my mouth was crooked and my eyes were slanted, and one side of my limbs was weak.", "RF005"),
        ("Suddenly paraplegic and slurred speech", "RF005"),
        # RF006 Severe abdominal pain
        ("My stomach hurts so much that I keep vomiting.", "RF006"),
        ("The abdominal pain is severe, and the stomach is hard to touch.", "RF006"),
        # RF007 High fever convulsions in children
        ("The child had a fever and rolled his eyes up.", "RF007"),
        # RF008 Severe allergy
        ("After eating peanuts, my throat was so swollen that I couldn't speak.", "RF008"),
        ("Anaphylactic shock after taking penicillin, and I feel weak all over.", "RF008"),
        # RF009 Pregnancy
        ("I'm bleeding during pregnancy. Do I need to go to the hospital right away?", "RF009"),
        ("Pregnant women have abdominal pain, accompanied by a feeling of falling.", "RF009"),
        # RF010 Head injury（urgent）
        ("I vomited twice after falling on my head, and I was a little confused.", "RF010"),
        ("He vomited after hitting his head and said he had a headache.", "RF010"),
    ],
)
def test_colloquial_sentences_hit_expected_rule(text, expected_rule, rules):
    """Real spoken long sentences must hit and fall into the expected rules (covering 10 rules, 26 sentences)"""
    result = check_red_flags(text, rules)

    assert result.hit is True, f"Not hit: {text}"
    assert result.rule_id == expected_rule, f"{text} Hit {result.rule_id}, expect {expected_rule}"


@pytest.mark.parametrize("text", ["", "   ", "\n\t", "\u3000\u3000"])
def test_blank_text_does_not_hit_or_raise(text, rules):
    """Empty strings and pure blanks do not hit and do not throw abnormalities."""
    result = check_red_flags(text, rules)

    assert result.hit is False


def test_symptoms_argument_is_also_scanned(rules):
    """Additional incirred symptom words also participate in the matching."""
    result = check_red_flags("Not very comfortable", rules, symptoms=["chest pain"])

    assert result.hit is True
    assert result.rule_id == "RF001"


def test_empty_rules_returns_no_hit():
    """The rule table is safe to return to missed when it is empty."""
    assert check_red_flags("Chest pain", []).hit is False

# --- Candidate departments converge ---

from apis.triage_engine import (  # noqa: E402  （Add paragraphs, and the import is concentrated at the beginning of the paragraph)
    PEDIATRICS_DEPARTMENT_ID,
    ShortlistResult,
    shortlist_departments,
)


@pytest.fixture(scope="module")
def departments(store_departments):
    return store_departments


@pytest.fixture(scope="module")
def store_departments():
    return DataStore(data_dir=DATA_DIR).load_departments()


@pytest.fixture(scope="module")
def mappings():
    return DataStore(data_dir=DATA_DIR).load_symptom_map()


def test_every_mapping_symptom_yields_its_departments(departments, mappings):
    """Each map is called by its symptom, and it is expected that all departments will appear in the candidates (success criteria 3）"""
    for mapping in mappings:
        result = shortlist_departments([mapping["symptom"]], mappings, departments)
        ids = [c.department_id for c in result.candidates]
        assert ids, f"{mapping['symptom']} There are no candidates."
        assert len(ids) <= 3
        for dept_id in mapping["departments"]:
            assert dept_id in ids, f"{mapping['symptom']} Missing {dept_id}, actually {ids}"


def test_aliases_also_match(departments, mappings):
    """The alias is also a hit (patient's spoken alias)"""
    result = shortlist_departments(["I have a terrible headache."], mappings, departments)

    assert result.candidates[0].department_id == "dept_neurology"
    assert result.candidates[0].matched_symptoms == ["Have a headache"]


def test_candidate_names_come_from_departments(departments, mappings):
    """The name of the department in the candidate is taken from the departments table."""
    result = shortlist_departments(["Generate heat"], mappings, departments)

    assert result.candidates[0].name == "General medicine"


def test_score_accumulates_over_symptoms(departments, mappings):
    """Accumulated score when multiple symptoms hit the same department"""
    single = shortlist_departments(["Generate heat"], mappings, departments)
    double = shortlist_departments(["Fever", "Cough"], mappings, departments)

    assert double.candidates[0].department_id == "dept_general_internal"
    assert double.candidates[0].score == single.candidates[0].score + 3


def test_ranking_is_by_score_desc_then_department_id(departments, mappings):
    """Descending order by score; ascending order by department_id with the same score (Standard 5.2 Step 3)"""
    result = shortlist_departments(["Abdominal pain"], mappings, departments)

    ids = [c.department_id for c in result.candidates]
    assert ids == ["dept_general_internal", "dept_surgery"]
    scores = [c.score for c in result.candidates]
    assert scores == sorted(scores, reverse=True)

    # Score in descending order: Neurology with a score of 5 must be ranked before the ENT department with a score of 2.
    # And the latter id is smaller - this order can only be obtained if it is really sorted by score.
    by_score = shortlist_departments(["Headache", "Dizziness"], mappings, departments)
    assert [(c.department_id, c.score) for c in by_score.candidates] == [
        ("dept_neurology", 5),
        ("dept_ent", 2),
    ]

    # When the score is the same, ascending order according to id: the ophthalmology id is larger, but the file order is more forward, and it must be ranked after the ear, nose and throat department.
    tie = shortlist_departments(["Tinnitus", "Red eyes"], mappings, departments)
    assert [c.department_id for c in tie.candidates] == ["dept_ent", "dept_ophthalmology"]


def test_max_candidates_truncates(departments, mappings):
    """max_candidates Effective: Cut off when hitting multiple departments"""
    two = shortlist_departments(["Abdominal pain"], mappings, departments, max_candidates=2)
    assert [c.department_id for c in two.candidates] == [
        "dept_general_internal",
        "dept_surgery",
    ]

    one = shortlist_departments(["Abdominal pain"], mappings, departments, max_candidates=1)
    assert [c.department_id for c in one.candidates] == ["dept_general_internal"]


def test_deterministic_for_same_input(departments, mappings):
    """The same input multiple calls have the same result."""
    first = shortlist_departments(["Fever", "Abdominal pain"], mappings, departments)
    second = shortlist_departments(["Fever", "Abdominal pain"], mappings, departments)

    assert first.model_dump(mode="json") == second.model_dump(mode="json")


# --- Pediatric population rules (success criteria 4）---

def test_under_fourteen_forces_pediatrics(departments, mappings):
    """When under the age of 14, choose compulsory convergence for pediatrics."""
    result = shortlist_departments(["Generate heat"], mappings, departments, age=8)

    assert [c.department_id for c in result.candidates] == [PEDIATRICS_DEPARTMENT_ID]
    assert result.age_rule_applied is True
    assert "pediatrics" in result.note.lower()


def test_thirteen_forces_pediatrics(departments, mappings):
    """13 The age is still within the pediatric rules."""
    result = shortlist_departments(["Generate heat"], mappings, departments, age=13)

    assert result.age_rule_applied is True


def test_fourteen_does_not_trigger_pediatrics(departments, mappings):
    """14 The year does not trigger the pediatric rules."""
    result = shortlist_departments(["Generate heat"], mappings, departments, age=14)

    assert result.age_rule_applied is False
    assert "dept_pediatrics" not in [c.department_id for c in result.candidates]


def test_age_unknown_does_not_trigger_pediatrics(departments, mappings):
    """Pediatric rules are not triggered when the age is unknown."""
    result = shortlist_departments(["Generate heat"], mappings, departments)

    assert result.age_rule_applied is False


def test_pediatrics_rule_keeps_original_score(departments, mappings):
    """Pediatric rules retain the original hit score of pediatrics."""
    result = shortlist_departments(["Children vomit"], mappings, departments, age=5)

    assert result.candidates[0].score == 3
    assert result.candidates[0].matched_symptoms == ["Children vomit"]


# --- The bottom branch ---

def test_unmatched_symptoms_return_empty_candidates_with_fallback(departments, mappings):
    """When there is no hit, it is selected as empty, and the bottom department is given."""
    result = shortlist_departments(["I can't say what's wrong."], mappings, departments)

    assert result.candidates == []
    assert result.fallback_department == "dept_general_internal"
    assert result.age_rule_applied is False
    assert "internal medicine" in result.note.lower()


def test_empty_symptoms_return_fallback(departments, mappings):
    """When the list of symptoms is empty, it is also the bottom of the pocket."""
    result = shortlist_departments([], mappings, departments)

    assert result.candidates == []
    assert result.fallback_department == "dept_general_internal"


def test_blank_symptoms_are_ignored(departments, mappings):
    """Pure blank symptom words are ignored."""
    result = shortlist_departments(["   "], mappings, departments)

    assert result.candidates == []
    assert result.fallback_department == "dept_general_internal"


def test_matched_candidates_have_no_fallback(departments, mappings):
    """When there is a candidate, fallback_department is None"""
    result = shortlist_departments(["Generate heat"], mappings, departments)

    assert result.fallback_department is None
    assert "Please select 1 department from the candidates" in result.note


def test_unknown_department_id_in_mapping_is_skipped(departments):
    """Skipping when the mapping points to an unknown department, which does not affect other hits."""
    broken = [
        {"symptom": "Generate heat", "aliases": [], "departments": ["dept_not_exist"], "weight": 3},
        {"symptom": "Cough", "aliases": [], "departments": ["dept_general_internal"], "weight": 1},
    ]
    result = shortlist_departments(["Fever", "Cough"], broken, departments)

    assert [c.department_id for c in result.candidates] == ["dept_general_internal"]


def test_no_hit_returns_shortlist_result_instance(departments, mappings):
    """The return value type is correct, which is convenient for the tool layer. dump"""
    assert isinstance(shortlist_departments(["It has nothing to do with the main complaint."], mappings, departments), ShortlistResult)
