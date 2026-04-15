#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="${SCRIPT_DIR}/skills/r-to-py-migration-skill"

usage() {
  cat <<'EOF'
Usage:
  ./skill.sh install codex
  ./skill.sh install claude
  ./skill.sh install copilot
  ./skill.sh install all
  ./skill.sh scaffold <python_package> [project_root]
  ./skill.sh check-contract [contract_csv] [output_json]
  ./skill.sh coverage [contract_csv] [cases_csv] [links_csv] [output_csv] [output_md]
  ./skill.sh notebook <package> <r_version> [contract_csv] [cases_csv] [links_csv] [output_ipynb]
  ./skill.sh full-cycle <package> <r_version> [project_root]

Examples:
  ./skill.sh install codex
  ./skill.sh scaffold demo_pkg
  ./skill.sh notebook demo_pkg 1.2.3
  ./skill.sh full-cycle demo_pkg 1.2.3
EOF
}

ensure_skill_dir() {
  if [[ ! -f "${SKILL_DIR}/SKILL.md" ]]; then
    echo "Skill directory not found: ${SKILL_DIR}" >&2
    exit 1
  fi
}

install_skill() {
  local target="$1"
  local dest_dir

  case "${target}" in
    codex)
      dest_dir="${HOME}/.codex/skills"
      ;;
    claude)
      dest_dir="${HOME}/.claude/skills"
      ;;
    copilot)
      dest_dir="${HOME}/.copilot/skills"
      ;;
    *)
      echo "Unknown install target: ${target}" >&2
      usage
      exit 1
      ;;
  esac

  mkdir -p "${dest_dir}"
  rm -rf "${dest_dir}/r-to-py-migration-skill"
  cp -R "${SKILL_DIR}" "${dest_dir}/"
  echo "Installed to ${dest_dir}/r-to-py-migration-skill"
}

run_scaffold() {
  local python_package="${1:?python package required}"
  local project_root="${2:-.}"
  python3 "${SKILL_DIR}/scripts/scaffold_migration_artifacts.py" \
    --project-root "${project_root}" \
    --python-package "${python_package}"
}

run_check_contract() {
  local contract_csv="${1:-FUNCTION_CONTRACT.csv}"
  local output_json="${2:-migration_artifacts/reference_outputs/function_contract_report.json}"
  python3 "${SKILL_DIR}/scripts/check_function_contracts.py" \
    --contract "${contract_csv}" \
    --output-json "${output_json}"
}

run_coverage() {
  local contract_csv="${1:-FUNCTION_CONTRACT.csv}"
  local cases_csv="${2:-PARITY_CASES.csv}"
  local links_csv="${3:-PARAMETER_CASE_LINKS.csv}"
  local output_csv="${4:-migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.csv}"
  local output_md="${5:-migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.md}"
  python3 "${SKILL_DIR}/scripts/generate_parameter_coverage_report.py" \
    --contract "${contract_csv}" \
    --cases "${cases_csv}" \
    --links "${links_csv}" \
    --output-csv "${output_csv}" \
    --output-md "${output_md}"
}

run_notebook() {
  local package_name="${1:?package required}"
  local r_version="${2:?r version required}"
  local contract_csv="${3:-FUNCTION_CONTRACT.csv}"
  local cases_csv="${4:-PARITY_CASES.csv}"
  local links_csv="${5:-PARAMETER_CASE_LINKS.csv}"
  local output_ipynb="${6:-migration_artifacts/notebooks/manual_validation_${r_version}.ipynb}"
  python3 "${SKILL_DIR}/scripts/generate_manual_validation_notebook.py" \
    --package "${package_name}" \
    --r-version "${r_version}" \
    --contract "${contract_csv}" \
    --cases "${cases_csv}" \
    --links "${links_csv}" \
    --output "${output_ipynb}"
}

run_full_cycle() {
  local package_name="${1:?package required}"
  local r_version="${2:?r version required}"
  local project_root="${3:-.}"

  run_scaffold "${package_name}" "${project_root}"
  python3 "${SKILL_DIR}/scripts/generate_parity_case_templates.py" \
    --contract "${project_root}/FUNCTION_CONTRACT.csv" \
    --output-cases "${project_root}/PARITY_CASES.csv" \
    --output-links "${project_root}/PARAMETER_CASE_LINKS.csv"
  run_check_contract \
    "${project_root}/FUNCTION_CONTRACT.csv" \
    "${project_root}/migration_artifacts/reference_outputs/function_contract_report.json"
  run_coverage \
    "${project_root}/FUNCTION_CONTRACT.csv" \
    "${project_root}/PARITY_CASES.csv" \
    "${project_root}/PARAMETER_CASE_LINKS.csv" \
    "${project_root}/migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.csv" \
    "${project_root}/migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.md"
  run_notebook \
    "${package_name}" \
    "${r_version}" \
    "${project_root}/FUNCTION_CONTRACT.csv" \
    "${project_root}/PARITY_CASES.csv" \
    "${project_root}/PARAMETER_CASE_LINKS.csv" \
    "${project_root}/migration_artifacts/notebooks/manual_validation_${r_version}.ipynb"
}

main() {
  ensure_skill_dir

  local cmd="${1:-}"
  case "${cmd}" in
    install)
      local target="${2:-}"
      case "${target}" in
        codex|claude|copilot)
          install_skill "${target}"
          ;;
        all)
          install_skill codex
          install_skill claude
          install_skill copilot
          ;;
        *)
          usage
          exit 1
          ;;
      esac
      ;;
    scaffold)
      run_scaffold "${2:?python package required}" "${3:-.}"
      ;;
    check-contract)
      run_check_contract "${2:-FUNCTION_CONTRACT.csv}" "${3:-migration_artifacts/reference_outputs/function_contract_report.json}"
      ;;
    coverage)
      run_coverage \
        "${2:-FUNCTION_CONTRACT.csv}" \
        "${3:-PARITY_CASES.csv}" \
        "${4:-PARAMETER_CASE_LINKS.csv}" \
        "${5:-migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.csv}" \
        "${6:-migration_artifacts/reference_outputs/PARAMETER_COVERAGE_REPORT.md}"
      ;;
    notebook)
      run_notebook \
        "${2:?package required}" \
        "${3:?r version required}" \
        "${4:-FUNCTION_CONTRACT.csv}" \
        "${5:-PARITY_CASES.csv}" \
        "${6:-PARAMETER_CASE_LINKS.csv}" \
        "${7:-migration_artifacts/notebooks/manual_validation_${3}.ipynb}"
      ;;
    full-cycle)
      run_full_cycle "${2:?package required}" "${3:?r version required}" "${4:-.}"
      ;;
    ""|-h|--help|help)
      usage
      ;;
    *)
      echo "Unknown command: ${cmd}" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
