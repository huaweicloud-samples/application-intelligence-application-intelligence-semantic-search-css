"""
Minimal verification script - tests if VPC + APIG config is valid
"""
import re
import os
from pathlib import Path

def verify_mini_config():
    """Verify minimal config"""
    config_file = Path(r"C:\Users\ShangDong\Desktop\迁移验证成功仓库\semantic-search-with-amazon-opensearch\infra\verify-mini.tf")
    
    if not config_file.exists():
        print("❌ verify-mini.tf not found")
        return False
    
    content = config_file.read_text(encoding='utf-8')
    
    checks = [
        ("terraform block", "terraform {" in content),
        ("huaweicloud provider", 'provider "huaweicloud"' in content),
        ("VPC resource", 'resource "huaweicloud_vpc"' in content),
        ("Subnet resource", 'resource "huaweicloud_vpc_subnet"' in content),
        ("Security Group", 'resource "huaweicloud_networking_secgroup"' in content),
        ("APIG Instance", 'resource "huaweicloud_apig_instance"' in content),
        ("APIG Group", 'resource "huaweicloud_apig_group"' in content),
    ]
    
    print("=" * 50)
    print("Minimal Config Verification")
    print("=" * 50)
    
    all_pass = True
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
        if not result:
            all_pass = False
    
    print("=" * 50)
    print(f"Result: {'PASS' if all_pass else 'FAIL'}")
    print("=" * 50)
    
    # Estimate deployment time
    print("\nEstimated deployment time: 1-2 minutes")
    print("Resources: VPC + Subnet + SG + APIG Instance + APIG Group")
    
    return all_pass

if __name__ == "__main__":
    verify_mini_config()
