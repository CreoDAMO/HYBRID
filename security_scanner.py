
#!/usr/bin/env python3
"""
HYBRID Blockchain Security Vulnerability Scanner
Comprehensive security analysis for blockchain applications
"""
import os
import re
import json
import ast
import hashlib
import subprocess
import sys
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Vulnerability:
    """Security vulnerability finding"""
    severity: str  # Critical, High, Medium, Low
    category: str
    file_path: str
    line_number: int
    description: str
    recommendation: str
    code_snippet: str

class HybridSecurityScanner:
    def __init__(self):
        self.vulnerabilities = []
        self.scanned_files = 0
        self.critical_count = 0
        self.high_count = 0
        self.medium_count = 0
        self.low_count = 0
        
        # Security patterns to detect
        self.patterns = {
            # Cryptographic vulnerabilities
            'weak_crypto': [
                (r'md5\(', 'MD5 is cryptographically broken'),
                (r'sha1\(', 'SHA1 is vulnerable to collision attacks'),
                (r'random\.random\(', 'Use cryptographically secure random'),
                (r'secrets\.randbelow\(1\)', 'Weak random number generation')
            ],
            
            # Private key exposure
            'private_key_exposure': [
                (r'private_key\s*=\s*["\'][\w\d]{64}["\']', 'Hardcoded private key'),
                (r'mnemonic\s*=\s*["\'].+["\']', 'Hardcoded mnemonic phrase'),
                (r'seed_phrase\s*=\s*["\'].+["\']', 'Hardcoded seed phrase'),
                (r'\.private_key', 'Private key access in code')
            ],
            
            # Network security
            'network_security': [
                (r'http://', 'Unencrypted HTTP connection'),
                (r'localhost', 'Localhost binding in production'),
                (r'0\.0\.0\.0', 'Binding to all interfaces'),
                (r'verify=False', 'SSL verification disabled')
            ],
            
            # Input validation
            'input_validation': [
                (r'eval\(', 'Code injection via eval()'),
                (r'exec\(', 'Code injection via exec()'),
                (r'os\.system\(', 'Command injection vulnerability'),
                (r'subprocess\.call\(.+shell=True', 'Shell injection vulnerability')
            ],
            
            # Authentication/Authorization
            'auth_issues': [
                (r'password\s*=\s*["\'].+["\']', 'Hardcoded password'),
                (r'api_key\s*=\s*["\'].+["\']', 'Hardcoded API key'),
                (r'secret\s*=\s*["\'].+["\']', 'Hardcoded secret'),
                (r'token\s*=\s*["\'].+["\']', 'Hardcoded token')
            ],
            
            # Blockchain specific
            'blockchain_security': [
                (r'balance\s*-=\s*amount\s*(?!.*if)', 'Unchecked balance subtraction'),
                (r'\.transfer\(.+\)\s*(?!.*if)', 'Unchecked transfer'),
                (r'gas_limit\s*=\s*\d{1,4}(?!\d)', 'Low gas limit'),
                (r'nonce\s*=\s*0', 'Hardcoded nonce')
            ]
        }
    
    def scan_file(self, file_path: str) -> List[Vulnerability]:
        """Scan a single file for vulnerabilities"""
        vulnerabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check each pattern category
            for category, patterns in self.patterns.items():
                for pattern, description in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # Get code snippet
                        start_line = max(0, line_num - 2)
                        end_line = min(len(lines), line_num + 1)
                        snippet = '\n'.join(lines[start_line:end_line])
                        
                        # Determine severity
                        severity = self._get_severity(category, pattern)
                        
                        vuln = Vulnerability(
                            severity=severity,
                            category=category,
                            file_path=file_path,
                            line_number=line_num,
                            description=description,
                            recommendation=self._get_recommendation(category),
                            code_snippet=snippet
                        )
                        vulnerabilities.append(vuln)
            
            # Additional checks for Python files
            if file_path.endswith('.py'):
                vulnerabilities.extend(self._check_python_specific(file_path, content))
        
        except Exception as e:
            print(f"⚠️ Error scanning {file_path}: {e}")
        
        return vulnerabilities
    
    def _check_python_specific(self, file_path: str, content: str) -> List[Vulnerability]:
        """Python-specific security checks"""
        vulnerabilities = []
        
        try:
            tree = ast.parse(content)
            
            # Check for dangerous imports
            dangerous_imports = ['pickle', 'marshal', 'shelve', 'dill']
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in dangerous_imports:
                            vuln = Vulnerability(
                                severity="High",
                                category="dangerous_imports",
                                file_path=file_path,
                                line_number=node.lineno,
                                description=f"Dangerous import: {alias.name}",
                                recommendation="Use safer serialization methods like JSON",
                                code_snippet=f"import {alias.name}"
                            )
                            vulnerabilities.append(vuln)
        
        except SyntaxError:
            pass  # Skip files with syntax errors
        
        return vulnerabilities
    
    def _get_severity(self, category: str, pattern: str) -> str:
        """Determine vulnerability severity"""
        critical_patterns = ['private_key', 'mnemonic', 'seed_phrase', 'eval(', 'exec(']
        high_patterns = ['password', 'api_key', 'secret', 'md5', 'os.system']
        
        if any(p in pattern for p in critical_patterns):
            return "Critical"
        elif any(p in pattern for p in high_patterns):
            return "High"
        elif category in ['network_security', 'blockchain_security']:
            return "Medium"
        else:
            return "Low"
    
    def _get_recommendation(self, category: str) -> str:
        """Get security recommendation for category"""
        recommendations = {
            'weak_crypto': 'Use SHA-256 or stronger hashing algorithms',
            'private_key_exposure': 'Store private keys in environment variables or secure storage',
            'network_security': 'Use HTTPS and secure network configurations',
            'input_validation': 'Implement proper input validation and sanitization',
            'auth_issues': 'Use environment variables for sensitive credentials',
            'blockchain_security': 'Implement proper balance checks and transaction validation',
            'dangerous_imports': 'Use safer alternatives for serialization and data handling'
        }
        return recommendations.get(category, 'Review and implement security best practices')
    
    def scan_directory(self, directory: str = ".") -> None:
        """Scan entire directory for vulnerabilities"""
        print("🔍 HYBRID Blockchain Security Scanner")
        print("=" * 50)
        
        # File types to scan
        extensions = ['.py', '.js', '.ts', '.sol', '.rs', '.go', '.json', '.yaml', '.yml']
        
        for root, dirs, files in os.walk(directory):
            # Skip certain directories
            skip_dirs = ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    self.scanned_files += 1
                    
                    vulnerabilities = self.scan_file(file_path)
                    self.vulnerabilities.extend(vulnerabilities)
        
        # Count vulnerabilities by severity
        for vuln in self.vulnerabilities:
            if vuln.severity == "Critical":
                self.critical_count += 1
            elif vuln.severity == "High":
                self.high_count += 1
            elif vuln.severity == "Medium":
                self.medium_count += 1
            else:
                self.low_count += 1
    
    def check_dependencies(self) -> List[Vulnerability]:
        """Check for vulnerable dependencies"""
        vulnerabilities = []
        
        # Check Python dependencies
        if os.path.exists('requirements.txt'):
            try:
                result = subprocess.run(['pip', 'list', '--format=json'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    packages = json.loads(result.stdout)
                    
                    # Known vulnerable packages (example list)
                    vulnerable_packages = {
                        'urllib3': '1.26.5',  # Example vulnerable version
                        'requests': '2.25.0',
                        'cryptography': '3.4.0'
                    }
                    
                    for package in packages:
                        name = package['name'].lower()
                        version = package['version']
                        
                        if name in vulnerable_packages:
                            vuln = Vulnerability(
                                severity="High",
                                category="vulnerable_dependency",
                                file_path="requirements.txt",
                                line_number=0,
                                description=f"Potentially vulnerable package: {name} {version}",
                                recommendation=f"Update {name} to latest version",
                                code_snippet=f"{name}=={version}"
                            )
                            vulnerabilities.append(vuln)
            
            except Exception as e:
                print(f"⚠️ Could not check dependencies: {e}")
        
        return vulnerabilities
    
    def check_configuration_security(self) -> List[Vulnerability]:
        """Check configuration files for security issues"""
        vulnerabilities = []
        
        config_files = ['.env', 'config.json', 'config.yaml', '.replit']
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        content = f.read()
                    
                    # Check for exposed secrets
                    secret_patterns = [
                        (r'password\s*[:=]\s*.+', 'Password in config file'),
                        (r'secret\s*[:=]\s*.+', 'Secret in config file'),
                        (r'api_key\s*[:=]\s*.+', 'API key in config file'),
                        (r'private_key\s*[:=]\s*.+', 'Private key in config file')
                    ]
                    
                    for pattern, description in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            vuln = Vulnerability(
                                severity="Critical",
                                category="config_exposure",
                                file_path=config_file,
                                line_number=0,
                                description=description,
                                recommendation="Use environment variables or secure secret management",
                                code_snippet="[Configuration file contains sensitive data]"
                            )
                            vulnerabilities.append(vuln)
                
                except Exception as e:
                    print(f"⚠️ Error checking {config_file}: {e}")
        
        return vulnerabilities
    
    def generate_report(self) -> None:
        """Generate security report"""
        print(f"\n📊 Security Scan Results")
        print("=" * 50)
        print(f"Files Scanned: {self.scanned_files}")
        print(f"Total Vulnerabilities: {len(self.vulnerabilities)}")
        print(f"🔴 Critical: {self.critical_count}")
        print(f"🟠 High: {self.high_count}")
        print(f"🟡 Medium: {self.medium_count}")
        print(f"🔵 Low: {self.low_count}")
        
        # Group vulnerabilities by severity
        severity_groups = {
            "Critical": [],
            "High": [],
            "Medium": [],
            "Low": []
        }
        
        for vuln in self.vulnerabilities:
            severity_groups[vuln.severity].append(vuln)
        
        # Display vulnerabilities by severity
        for severity in ["Critical", "High", "Medium", "Low"]:
            if severity_groups[severity]:
                print(f"\n{self._get_severity_icon(severity)} {severity} Vulnerabilities:")
                print("-" * 40)
                
                for i, vuln in enumerate(severity_groups[severity], 1):
                    print(f"{i}. {vuln.description}")
                    print(f"   📁 File: {vuln.file_path}:{vuln.line_number}")
                    print(f"   🏷️ Category: {vuln.category}")
                    print(f"   💡 Recommendation: {vuln.recommendation}")
                    if vuln.code_snippet.strip():
                        print(f"   📝 Code snippet:")
                        for line in vuln.code_snippet.split('\n'):
                            if line.strip():
                                print(f"      {line}")
                    print()
    
    def _get_severity_icon(self, severity: str) -> str:
        """Get icon for severity level"""
        icons = {
            "Critical": "🔴",
            "High": "🟠", 
            "Medium": "🟡",
            "Low": "🔵"
        }
        return icons.get(severity, "⚪")
    
    def save_report(self, filename: str = "security_report.json") -> None:
        """Save security report to JSON file"""
        report_data = {
            "scan_summary": {
                "files_scanned": self.scanned_files,
                "total_vulnerabilities": len(self.vulnerabilities),
                "critical": self.critical_count,
                "high": self.high_count,
                "medium": self.medium_count,
                "low": self.low_count
            },
            "vulnerabilities": [
                {
                    "severity": vuln.severity,
                    "category": vuln.category,
                    "file_path": vuln.file_path,
                    "line_number": vuln.line_number,
                    "description": vuln.description,
                    "recommendation": vuln.recommendation,
                    "code_snippet": vuln.code_snippet
                }
                for vuln in self.vulnerabilities
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📄 Detailed report saved to {filename}")

def main():
    """Main scanner function"""
    scanner = HybridSecurityScanner()
    
    # Scan the project
    scanner.scan_directory(".")
    
    # Check dependencies
    dep_vulns = scanner.check_dependencies()
    scanner.vulnerabilities.extend(dep_vulns)
    
    # Check configuration security
    config_vulns = scanner.check_configuration_security()
    scanner.vulnerabilities.extend(config_vulns)
    
    # Update counts
    for vuln in dep_vulns + config_vulns:
        if vuln.severity == "Critical":
            scanner.critical_count += 1
        elif vuln.severity == "High":
            scanner.high_count += 1
        elif vuln.severity == "Medium":
            scanner.medium_count += 1
        else:
            scanner.low_count += 1
    
    # Generate and display report
    scanner.generate_report()
    
    # Save detailed report
    scanner.save_report()
    
    # Security recommendations
    print(f"\n🛡️ Security Recommendations:")
    print("=" * 50)
    print("1. 🔐 Use environment variables for all sensitive data")
    print("2. 🔒 Implement proper input validation")
    print("3. 🌐 Use HTTPS for all network communications")
    print("4. 🔑 Store private keys in secure hardware or HSMs")
    print("5. 📊 Regular security audits and dependency updates")
    print("6. 🧪 Implement comprehensive testing including security tests")
    print("7. 📝 Follow blockchain security best practices")
    print("8. 🔍 Use static analysis tools in CI/CD pipeline")
    
    # Exit code based on findings
    if scanner.critical_count > 0:
        print(f"\n❌ SCAN FAILED: {scanner.critical_count} critical vulnerabilities found!")
        sys.exit(1)
    elif scanner.high_count > 0:
        print(f"\n⚠️ SCAN WARNING: {scanner.high_count} high-severity vulnerabilities found!")
        sys.exit(1)
    else:
        print(f"\n✅ SCAN PASSED: No critical or high-severity vulnerabilities found!")
        sys.exit(0)

if __name__ == "__main__":
    main()
