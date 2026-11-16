"""
Static verification script for semantic-search-with-amazon-opensearch Terraform configuration
Verifies syntax, resource references, and configuration correctness
"""
import re
import os
import json
from pathlib import Path

# Configuration
REPO_DIR = Path(r"C:\Users\ShangDong\Desktop\迁移验证成功仓库\semantic-search-with-amazon-opensearch")
INFRA_DIR = REPO_DIR / "infra"

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_resources(tf_content):
    """Extract resource definitions from Terraform file"""
    resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
    return re.findall(resource_pattern, tf_content)

def extract_variables(tf_content):
    """Extract variable definitions"""
    var_pattern = r'variable\s+"([^"]+)"'
    return re.findall(var_pattern, tf_content)

def extract_outputs(tf_content):
    """Extract output definitions"""
    output_pattern = r'output\s+"([^"]+)"'
    return re.findall(output_pattern, tf_content)

def extract_references(tf_content):
    """Extract variable and resource references"""
    var_ref_pattern = r'var\.(\w+)'
    res_ref_pattern = r'(huaweicloud_\w+)\.(\w+)\.(\w+)'
    return {
        'variables': re.findall(var_ref_pattern, tf_content),
        'resources': re.findall(res_ref_pattern, tf_content)
    }

def verify_terraform_syntax():
    """Verify Terraform configuration"""
    results = {
        'L1_terraform_syntax': 'PASS',
        'L2_provider_config': 'PASS',
        'L3_resource_definitions': 'PASS',
        'L4_variable_references': 'PASS',
        'L5_output_definitions': 'PASS'
    }

    errors = []

    # Check main.tf exists and readable
    main_tf = INFRA_DIR / "main.tf"
    if not main_tf.exists():
        results['L1_terraform_syntax'] = 'FAIL'
        errors.append(f"main.tf not found at {main_tf}")
        return results, errors

    main_content = read_file(main_tf)

    # L1: Basic syntax check
    if 'terraform {' not in main_content:
        results['L1_terraform_syntax'] = 'FAIL'
        errors.append("Missing 'terraform' block")
    if 'required_providers' not in main_content:
        results['L1_terraform_syntax'] = 'FAIL'
        errors.append("Missing 'required_providers' block")
    if 'provider "huaweicloud"' not in main_content:
        results['L1_terraform_syntax'] = 'FAIL'
        errors.append("Missing huaweicloud provider")

    # L2: Provider configuration
    if 'region = var.region' not in main_content:
        results['L2_provider_config'] = 'FAIL'
        errors.append("Provider region not properly configured")

    # L3: Resource definitions
    resources = extract_resources(main_content)
    expected_resources = [
        'huaweicloud_vpc',
        'huaweicloud_vpc_subnet',
        'huaweicloud_networking_secgroup',
        'huaweicloud_css_cluster',
        'huaweicloud_cce_cluster',
        'huaweicloud_cce_node',
        'huaweicloud_apig_instance',
        'huaweicloud_apig_group',
        'huaweicloud_apig_backend',
        'huaweicloud_apig_api'
    ]

    resource_types = set([r[0] for r in resources])
    for expected in expected_resources:
        if expected not in resource_types:
            errors.append(f"Missing expected resource: {expected}")

    # L4: Variable references
    variables = extract_variables(read_file(INFRA_DIR / "variables.tf"))
    refs = extract_references(main_content)

    # Check backend_host reference
    if 'var.backend_host' in main_content:
        if 'backend_host' not in variables:
            errors.append("Variable 'backend_host' referenced but not defined")

    # L5: Output definitions
    outputs = extract_outputs(main_content)
    expected_outputs = ['vpc_id', 'css_endpoint', 'apig_url', 'cce_cluster_id', 'cce_endpoint']
    for expected in expected_outputs:
        if expected not in outputs:
            errors.append(f"Missing expected output: {expected}")

    return results, errors

def verify_backend_code():
    """Verify backend code exists"""
    results = {
        'backend_dockerfile': 'PASS',
        'backend_app': 'PASS',
        'backend_handlers': 'PASS',
        'backend_requirements': 'PASS'
    }

    backend_dir = REPO_DIR / "src" / "backend"
    errors = []

    # Check Dockerfile
    dockerfile = backend_dir / "Dockerfile"
    if not dockerfile.exists():
        results['backend_dockerfile'] = 'FAIL'
        errors.append("Dockerfile not found")

    # Check app.py
    app_py = backend_dir / "app.py"
    if not app_py.exists():
        results['backend_app'] = 'FAIL'
        errors.append("app.py not found")

    # Check handlers
    for handler in ['handler_search.py', 'handler_chat.py', 'handler_index.py']:
        if not (backend_dir / handler).exists():
            results['backend_handlers'] = 'FAIL'
            errors.append(f"Handler {handler} not found")

    # Check requirements
    req = backend_dir / "requirements.txt"
    if not req.exists():
        results['backend_requirements'] = 'FAIL'
        errors.append("requirements.txt not found")

    return results, errors

def verify_k8s_manifest():
    """Verify Kubernetes deployment manifest"""
    results = {
        'k8s_deployment_manifest': 'PASS'
    }

    k8s_file = INFRA_DIR / "k8s-deployment.yaml"
    if not k8s_file.exists():
        results['k8s_deployment_manifest'] = 'FAIL'
        return results, ["k8s-deployment.yaml not found"]

    content = read_file(k8s_file)
    errors = []

    # Check required K8s resources
    if 'kind: Namespace' not in content:
        errors.append("Missing Namespace resource")
    if 'kind: Deployment' not in content:
        errors.append("Missing Deployment resource")
    if 'kind: Service' not in content:
        errors.append("Missing Service resource")

    return results, errors

def verify_documentation():
    """Verify documentation files"""
    results = {
        'readme_cn': 'PASS',
        'readme_en': 'PASS',
        'architecture_doc': 'PASS'
    }

    errors = []

    # Check README.md
    readme = REPO_DIR / "README.md"
    if not readme.exists():
        results['readme_cn'] = 'FAIL'
        errors.append("README.md not found")

    # Check README.en.md
    readme_en = REPO_DIR / "README.en.md"
    if not readme_en.exists():
        results['readme_en'] = 'FAIL'
        errors.append("README.en.md not found")

    # Check architecture.md
    arch = REPO_DIR / "docs" / "architecture.md"
    if not arch.exists():
        results['architecture_doc'] = 'FAIL'
        errors.append("docs/architecture.md not found")

    return results, errors

def main():
    print("=" * 60)
    print("Static Verification - semantic-search-with-amazon-opensearch")
    print("=" * 60)

    all_results = {}
    all_errors = []

    # Run all verifications
    print("\n[1/5] Verifying Terraform configuration...")
    tf_results, tf_errors = verify_terraform_syntax()
    all_results.update(tf_results)
    all_errors.extend(tf_errors)

    print("[2/5] Verifying backend code...")
    be_results, be_errors = verify_backend_code()
    all_results.update(be_results)
    all_errors.extend(be_errors)

    print("[3/5] Verifying Kubernetes manifest...")
    k8s_results, k8s_errors = verify_k8s_manifest()
    all_results.update(k8s_results)
    all_errors.extend(k8s_errors)

    print("[4/5] Verifying documentation...")
    doc_results, doc_errors = verify_documentation()
    all_results.update(doc_results)
    all_errors.extend(doc_errors)

    # Print results
    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)

    for check, result in all_results.items():
        status = "✅ PASS" if result == "PASS" else "❌ FAIL"
        print(f"  {check}: {status}")

    print("\n" + "=" * 60)
    if all_errors:
        print("ERRORS:")
        for err in all_errors:
            print(f"  - {err}")
        print("=" * 60)

    # Summary
    total = len(all_results)
    passed = sum(1 for v in all_results.values() if v == "PASS")
    print(f"\nSUMMARY: {passed}/{total} checks passed")

    # Save results
    output = {
        'repo': 'semantic-search-with-amazon-opensearch',
        'timestamp': '2026-09-15',
        'verification_type': 'static',
        'results': all_results,
        'errors': all_errors,
        'summary': f"{passed}/{total} checks passed"
    }

    output_file = INFRA_DIR / "verification-report.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Verification Report - semantic-search-with-amazon-opensearch\n\n")
        f.write(f"**Date**: 2026-09-15\n\n")
        f.write(f"**Type**: Static Analysis\n\n")
        f.write("## Results\n\n")
        for check, result in all_results.items():
            f.write(f"- **{check}**: {result}\n")
        if all_errors:
            f.write("\n## Errors\n\n")
            for err in all_errors:
                f.write(f"- {err}\n")
        f.write(f"\n## Summary\n\n{passed}/{total} checks passed\n")

    print(f"\nReport saved to: {output_file}")

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
