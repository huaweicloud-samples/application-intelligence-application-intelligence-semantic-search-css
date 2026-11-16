"""
Run terraform via Python subprocess
"""
import subprocess
import os
import sys

os.environ['HW_ACCESS_KEY'] = 'HPUAXMXXILTOMVUTE8YE'
os.environ['HW_SECRET_KEY'] = '1CBRMTugWByixQK1D33ZdsIFQerfeo39L1wI61Ko'

infra_dir = r"C:\Users\ShangDong\Desktop\迁移验证成功仓库\semantic-search-with-amazon-opensearch\infra"
tf_exe = r"C:\Users\ShangDong\Desktop\terraform.exe"

print("=" * 50)
print("Running terraform init...")
print("=" * 50)

result = subprocess.run(
    [tf_exe, "init"],
    cwd=infra_dir,
    capture_output=True,
    text=True,
    env=os.environ.copy()
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode != 0:
    print("\n❌ Terraform init failed")
    sys.exit(1)

print("\n✅ Terraform init successful")
print("\n" + "=" * 50)
print("Running terraform plan...")
print("=" * 50)

result = subprocess.run(
    [tf_exe, "plan", "-var-file=verify-mini.tfvars"],
    cwd=infra_dir,
    capture_output=True,
    text=True,
    env=os.environ.copy()
)

print("STDOUT:", result.stdout[:2000])
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode != 0:
    print("\n❌ Terraform plan failed")
    sys.exit(1)

print("\n✅ Terraform plan successful")
print("\n" + "=" * 50)
print("Running terraform apply...")
print("=" * 50)

result = subprocess.run(
    [tf_exe, "apply", "-var-file=verify-mini.tfvars", "-auto-approve"],
    cwd=infra_dir,
    capture_output=True,
    text=True,
    env=os.environ.copy()
)

print("STDOUT:", result.stdout[:3000])
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode != 0:
    print("\n❌ Terraform apply failed")
    sys.exit(1)

print("\n✅ Terraform apply successful!")
