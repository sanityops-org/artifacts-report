# Expense Audit Report

**Batch**: {filename}
**Policy version**: {policy_version}
**Audited**: {timestamp}
**Records**: {total_records}

---

## Summary

| Verdict | Count |
|---------|-------|
| Pass | {pass_count} |
| Violation | {violation_count} |
| Needs review | {review_count} |

| Severity | Findings |
|----------|----------|
| High | {high_count} |
| Medium | {medium_count} |
| Low | {low_count} |

---

## Violations

### {severity}: {record_id} — {employee_name} — {category} {amount}

- **Rule**: `{rule_id}` — {rule_description}
- **Actual**: {actual_value}
- **Limit**: {limit_value}
- **Overage**: {overage}

---

## Needs Review

### {record_id} — {employee_name}

- **Rule**: `{rule_id}` — {rule_description}
- **Reason**: {why_it_could_not_be_evaluated}

---

## Suspected Duplicates

### {merchant} — {amount}

| Record | Employee | Date |
|--------|----------|------|
| {record_id} | {employee_name} | {expense_date} |

**Matching basis**: {amount_tolerance} / {date_window}

---

## Policy Reference

| Rule | Description | Value |
|------|-------------|-------|
| `{rule_id}` | {description} | {value} |

---

## Parse Failures

| Row | Reason |
|-----|--------|
| {row_number} | {reason} |
