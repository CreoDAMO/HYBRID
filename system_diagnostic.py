
#!/usr/bin/env python3
"""
HYBRID Blockchain System-Wide Diagnostic Scanner
Comprehensive error detection and system health analysis
"""

import os
import sys
import ast
import re
import traceback
import importlib
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import time

@dataclass
class DiagnosticIssue:
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str
    file_path: str
    line_number: int
    description: str
    fix_suggestion: str
    code_snippet: str = ""

class SystemDiagnostic:
    """Comprehensive system diagnostic scanner"""
    
    def __init__(self):
        self.issues = []
        self.stats = {
            'files_scanned': 0,
            'total_lines': 0,
            'import_errors': 0,
            'syntax_errors': 0,
            'logic_errors': 0,
            'missing_files': 0,
            'performance_issues': 0
        }
        
    def scan_system(self) -> Dict[str, Any]:
        """Run comprehensive system scan"""
        print("🔍 Starting HYBRID Blockchain System Diagnostic...")
        print("=" * 60)
        
        # 1. Check Python environment
        self._check_python_environment()
        
        # 2. Scan Python files for syntax/import errors
        self._scan_python_files()
        
        # 3. Check file structure integrity
        self._check_file_structure()
        
        # 4. Validate module imports
        self._validate_imports()
        
        # 5. Check for performance issues
        self._check_performance_issues()
        
        # 6. Validate configuration files
        self._validate_configurations()
        
        # 7. Check for security issues
        self._check_security_issues()
        
        # 8. Validate UI components
        self._validate_ui_components()
        
        # 9. Check blockchain components
        self._check_blockchain_components()
        
        # 10. Generate report
        return self._generate_report()
    
    def _check_python_environment(self):
        """Check Python environment health"""
        print("\n🐍 Checking Python Environment...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            self.issues.append(DiagnosticIssue(
                severity="HIGH",
                category="Environment",
                file_path="system",
                line_number=0,
                description=f"Python version {version.major}.{version.minor} may cause compatibility issues",
                fix_suggestion="Upgrade to Python 3.9 or higher"
            ))
        
        # Check required packages
        required_packages = [
            'streamlit', 'plotly', 'pandas', 'numpy', 'requests',
            'cryptography', 'mnemonic', 'aiohttp', 'fastapi', 'uvicorn',
            'web3', 'eth_account', 'bech32', 'ecdsa'
        ]
        
        for package in required_packages:
            try:
                importlib.import_module(package)
            except ImportError:
                self.issues.append(DiagnosticIssue(
                    severity="HIGH",
                    category="Dependencies",
                    file_path="requirements.txt",
                    line_number=0,
                    description=f"Missing required package: {package}",
                    fix_suggestion=f"Install with: pip install {package}"
                ))
                self.stats['import_errors'] += 1
    
    def _scan_python_files(self):
        """Scan all Python files for syntax and logic errors"""
        print("\n📄 Scanning Python Files...")
        
        python_files = list(Path('.').rglob('*.py'))
        
        for file_path in python_files:
            if '.pythonlibs' in str(file_path) or '__pycache__' in str(file_path):
                continue
                
            self.stats['files_scanned'] += 1
            self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path):
        """Scan individual Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                self.stats['total_lines'] += len(lines)
            
            # Check syntax
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.issues.append(DiagnosticIssue(
                    severity="CRITICAL",
                    category="Syntax Error",
                    file_path=str(file_path),
                    line_number=e.lineno or 0,
                    description=f"Syntax error: {e.msg}",
                    fix_suggestion="Fix syntax error according to Python grammar",
                    code_snippet=lines[e.lineno-1] if e.lineno and e.lineno <= len(lines) else ""
                ))
                self.stats['syntax_errors'] += 1
                return
            
            # Check for common issues
            self._check_imports_in_file(file_path, content, lines)
            self._check_logic_issues(file_path, content, lines)
            
        except Exception as e:
            self.issues.append(DiagnosticIssue(
                severity="MEDIUM",
                category="File Access",
                file_path=str(file_path),
                line_number=0,
                description=f"Cannot read file: {str(e)}",
                fix_suggestion="Check file permissions and encoding"
            ))
    
    def _check_imports_in_file(self, file_path: Path, content: str, lines: List[str]):
        """Check import statements in file"""
        import_pattern = re.compile(r'^(?:from\s+\S+\s+)?import\s+(.+)', re.MULTILINE)
        
        for match in import_pattern.finditer(content):
            line_num = content[:match.start()].count('\n') + 1
            import_statement = match.group(0).strip()
            
            # Check for relative imports that might fail
            if 'from .' in import_statement or 'from ..' in import_statement:
                # Check if the relative import is valid
                try:
                    # This is a simplified check - more complex validation could be added
                    if file_path.name == 'main.py' and 'from ui.' in import_statement:
                        # Check if ui module exists
                        if not Path('ui').exists():
                            self.issues.append(DiagnosticIssue(
                                severity="HIGH",
                                category="Import Error",
                                file_path=str(file_path),
                                line_number=line_num,
                                description=f"Relative import may fail: {import_statement}",
                                fix_suggestion="Ensure ui directory exists and has __init__.py",
                                code_snippet=lines[line_num-1]
                            ))
                except Exception:
                    pass
    
    def _check_logic_issues(self, file_path: Path, content: str, lines: List[str]):
        """Check for common logic issues"""
        
        # Check for undefined variables (basic detection)
        undefined_vars = []
        
        # Check for missing return statements in functions
        function_pattern = re.compile(r'^def\s+(\w+)\s*\([^)]*\):', re.MULTILINE)
        for match in function_pattern.finditer(content):
            func_name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            # Simple check for functions that might need return statements
            if func_name.startswith('get_') or func_name.startswith('calculate_'):
                # Look for return statement in the function
                func_end = content.find('\ndef ', match.end())
                if func_end == -1:
                    func_end = len(content)
                func_body = content[match.end():func_end]
                
                if 'return' not in func_body and 'yield' not in func_body:
                    self.issues.append(DiagnosticIssue(
                        severity="MEDIUM",
                        category="Logic Warning",
                        file_path=str(file_path),
                        line_number=line_num,
                        description=f"Function '{func_name}' may be missing return statement",
                        fix_suggestion="Add appropriate return statement if needed",
                        code_snippet=lines[line_num-1]
                    ))
                    self.stats['logic_errors'] += 1
    
    def _check_file_structure(self):
        """Check file structure integrity"""
        print("\n📁 Checking File Structure...")
        
        expected_files = [
            'main.py',
            'start_hybrid.py',
            'requirements.txt',
            'ui/__init__.py',
            'ui/streamlit_ui.py',
            'blockchain/__init__.py',
            'blockchain/hybrid_node.py',
            'blockchain/hybrid_wallet.py',
            '.streamlit/config.toml'
        ]
        
        for file_path in expected_files:
            if not Path(file_path).exists():
                self.issues.append(DiagnosticIssue(
                    severity="HIGH",
                    category="Missing File",
                    file_path=file_path,
                    line_number=0,
                    description=f"Critical file missing: {file_path}",
                    fix_suggestion=f"Create or restore {file_path}"
                ))
                self.stats['missing_files'] += 1
    
    def _validate_imports(self):
        """Validate critical imports"""
        print("\n🔗 Validating Critical Imports...")
        
        critical_modules = [
            ('ui.streamlit_ui', 'create_streamlit_ui'),
            ('blockchain.hybrid_node', 'create_hybrid_node'),
            ('blockchain.hybrid_wallet', 'hybrid_wallet_manager'),
            ('components.convergence_engine', 'convergence_engine')
        ]
        
        for module_name, function_name in critical_modules:
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, function_name):
                    self.issues.append(DiagnosticIssue(
                        severity="HIGH",
                        category="Import Error",
                        file_path=f"{module_name.replace('.', '/')}.py",
                        line_number=0,
                        description=f"Missing function '{function_name}' in {module_name}",
                        fix_suggestion=f"Implement {function_name} function in {module_name}"
                    ))
            except ImportError as e:
                self.issues.append(DiagnosticIssue(
                    severity="CRITICAL",
                    category="Import Error",
                    file_path=f"{module_name.replace('.', '/')}.py",
                    line_number=0,
                    description=f"Cannot import {module_name}: {str(e)}",
                    fix_suggestion=f"Fix import issues in {module_name}"
                ))
                self.stats['import_errors'] += 1
    
    def _check_performance_issues(self):
        """Check for potential performance issues"""
        print("\n⚡ Checking Performance Issues...")
        
        # Check for large files that might cause memory issues
        for file_path in Path('.').rglob('*.py'):
            if file_path.stat().st_size > 1024 * 1024:  # > 1MB
                self.issues.append(DiagnosticIssue(
                    severity="MEDIUM",
                    category="Performance",
                    file_path=str(file_path),
                    line_number=0,
                    description=f"Large file detected ({file_path.stat().st_size // 1024}KB)",
                    fix_suggestion="Consider splitting large files into smaller modules"
                ))
                self.stats['performance_issues'] += 1
    
    def _validate_configurations(self):
        """Validate configuration files"""
        print("\n⚙️ Validating Configurations...")
        
        # Check .streamlit/config.toml
        streamlit_config = Path('.streamlit/config.toml')
        if streamlit_config.exists():
            try:
                with open(streamlit_config, 'r') as f:
                    content = f.read()
                    if 'serverPort' not in content and 'port' not in content:
                        self.issues.append(DiagnosticIssue(
                            severity="LOW",
                            category="Configuration",
                            file_path=str(streamlit_config),
                            line_number=0,
                            description="Streamlit port not explicitly configured",
                            fix_suggestion="Add server port configuration"
                        ))
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    severity="MEDIUM",
                    category="Configuration",
                    file_path=str(streamlit_config),
                    line_number=0,
                    description=f"Error reading config: {str(e)}",
                    fix_suggestion="Fix configuration file format"
                ))
    
    def _check_security_issues(self):
        """Check for potential security issues"""
        print("\n🔒 Checking Security Issues...")
        
        # Check for hardcoded secrets
        for file_path in Path('.').rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Look for potential hardcoded secrets
                secret_patterns = [
                    (r'api_key\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded API key'),
                    (r'password\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded password'),
                    (r'secret\s*=\s*["\'][^"\']+["\']', 'Potential hardcoded secret'),
                ]
                
                for pattern, description in secret_patterns:
                    for match in re.finditer(pattern, content, re.IGNORECASE):
                        line_num = content[:match.start()].count('\n') + 1
                        self.issues.append(DiagnosticIssue(
                            severity="HIGH",
                            category="Security",
                            file_path=str(file_path),
                            line_number=line_num,
                            description=description,
                            fix_suggestion="Use environment variables for secrets",
                            code_snippet=lines[line_num-1]
                        ))
            except Exception:
                pass
    
    def _validate_ui_components(self):
        """Validate UI components"""
        print("\n🖥️ Validating UI Components...")
        
        ui_files = [
            'ui/streamlit_ui.py',
            'ui/hybrid_market_dashboard.py',
            'ui/hybridscan_ui.py',
            'ui/docs_analyzer.py'
        ]
        
        for ui_file in ui_files:
            if Path(ui_file).exists():
                try:
                    with open(ui_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for common UI issues
                    if 'st.' in content and 'import streamlit' not in content:
                        self.issues.append(DiagnosticIssue(
                            severity="HIGH",
                            category="UI Error",
                            file_path=ui_file,
                            line_number=0,
                            description="Using streamlit without proper import",
                            fix_suggestion="Add 'import streamlit as st'"
                        ))
                except Exception as e:
                    self.issues.append(DiagnosticIssue(
                        severity="MEDIUM",
                        category="UI Error",
                        file_path=ui_file,
                        line_number=0,
                        description=f"Error reading UI file: {str(e)}",
                        fix_suggestion="Check file accessibility and encoding"
                    ))
    
    def _check_blockchain_components(self):
        """Check blockchain components"""
        print("\n⛓️ Validating Blockchain Components...")
        
        blockchain_files = [
            'blockchain/hybrid_node.py',
            'blockchain/hybrid_wallet.py',
            'blockchain/consensus.py',
            'blockchain/multi_ai_orchestrator.py'
        ]
        
        for bc_file in blockchain_files:
            if Path(bc_file).exists():
                try:
                    with open(bc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for blockchain-specific issues
                    if 'async def' in content and 'import asyncio' not in content:
                        self.issues.append(DiagnosticIssue(
                            severity="MEDIUM",
                            category="Blockchain",
                            file_path=bc_file,
                            line_number=0,
                            description="Using async without asyncio import",
                            fix_suggestion="Add 'import asyncio'"
                        ))
                except Exception:
                    pass
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive diagnostic report"""
        print("\n📊 Generating Diagnostic Report...")
        
        # Categorize issues by severity
        critical = [i for i in self.issues if i.severity == "CRITICAL"]
        high = [i for i in self.issues if i.severity == "HIGH"]
        medium = [i for i in self.issues if i.severity == "MEDIUM"]
        low = [i for i in self.issues if i.severity == "LOW"]
        
        # Calculate health score
        total_issues = len(self.issues)
        health_score = max(0, 100 - (len(critical) * 25 + len(high) * 10 + len(medium) * 5 + len(low) * 1))
        
        report = {
            'scan_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'health_score': health_score,
            'statistics': self.stats,
            'issues_by_severity': {
                'critical': len(critical),
                'high': len(high),
                'medium': len(medium),
                'low': len(low)
            },
            'issues': self.issues,
            'recommendations': self._generate_recommendations()
        }
        
        self._print_report(report)
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate fix recommendations"""
        recommendations = []
        
        if self.stats['import_errors'] > 0:
            recommendations.append("Install missing Python packages from requirements.txt")
        
        if self.stats['syntax_errors'] > 0:
            recommendations.append("Fix syntax errors before running the application")
        
        if self.stats['missing_files'] > 0:
            recommendations.append("Restore missing critical files")
        
        critical_issues = [i for i in self.issues if i.severity == "CRITICAL"]
        if critical_issues:
            recommendations.append("Address all CRITICAL issues immediately")
        
        return recommendations
    
    def _print_report(self, report: Dict[str, Any]):
        """Print formatted diagnostic report"""
        print("\n" + "="*60)
        print("🎯 HYBRID BLOCKCHAIN SYSTEM DIAGNOSTIC REPORT")
        print("="*60)
        
        print(f"\n📊 System Health Score: {report['health_score']}/100")
        
        if report['health_score'] >= 90:
            print("🟢 EXCELLENT - System is healthy")
        elif report['health_score'] >= 70:
            print("🟡 GOOD - Minor issues detected")
        elif report['health_score'] >= 50:
            print("🟠 FAIR - Several issues need attention")
        else:
            print("🔴 CRITICAL - Immediate action required")
        
        print(f"\n📈 Scan Statistics:")
        for key, value in report['statistics'].items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🚨 Issues by Severity:")
        for severity, count in report['issues_by_severity'].items():
            icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}[severity]
            print(f"   {icon} {severity.upper()}: {count}")
        
        if report['issues']:
            print(f"\n📋 Detailed Issues:")
            for i, issue in enumerate(report['issues'][:10], 1):  # Show first 10
                print(f"\n{i}. [{issue.severity}] {issue.category}")
                print(f"   File: {issue.file_path}:{issue.line_number}")
                print(f"   Issue: {issue.description}")
                print(f"   Fix: {issue.fix_suggestion}")
                if issue.code_snippet:
                    print(f"   Code: {issue.code_snippet}")
            
            if len(report['issues']) > 10:
                print(f"\n... and {len(report['issues']) - 10} more issues")
        
        if report['recommendations']:
            print(f"\n💡 Priority Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print("\n" + "="*60)

def main():
    """Run system diagnostic"""
    diagnostic = SystemDiagnostic()
    report = diagnostic.scan_system()
    
    # Save report to file
    with open('system_diagnostic_report.json', 'w') as f:
        # Convert DiagnosticIssue objects to dicts for JSON serialization
        serializable_report = report.copy()
        serializable_report['issues'] = [
            {
                'severity': issue.severity,
                'category': issue.category,
                'file_path': issue.file_path,
                'line_number': issue.line_number,
                'description': issue.description,
                'fix_suggestion': issue.fix_suggestion,
                'code_snippet': issue.code_snippet
            }
            for issue in report['issues']
        ]
        json.dump(serializable_report, f, indent=2)
    
    print(f"\n📄 Full report saved to: system_diagnostic_report.json")
    return report

if __name__ == "__main__":
    main()
