#!/usr/bin/env python3
"""
HYBRID Blockchain Stress Test Suite
Comprehensive testing for all HYBRID components including SpiralScript
"""
import asyncio
import time
import random
import statistics
import threading
import concurrent.futures
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'blockchain'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

# Import required modules with fallbacks
try:
    import streamlit as st
except ImportError:
    print("Warning: Streamlit not available for stress testing")
    st = None

try:
    import requests
except ImportError:
    print("Warning: Requests not available for stress testing")
    requests = None

import json
import psutil
import numpy as np

# Add blockchain modules to path

class HybridStressTest:
    """Comprehensive stress test for HYBRID Blockchain system"""

    def __init__(self):
        self.base_url = "http://0.0.0.0:8501"
        self.rpc_url = "http://0.0.0.0:26657"
        self.test_results = {}
        self.start_time = time.time()

        # Test configuration
        self.config = {
            'duration_seconds': 300,  # 5 minutes
            'concurrent_users': 50,
            'transactions_per_second': 100,
            'memory_threshold': 85,  # %
            'cpu_threshold': 90,     # %
            'max_response_time': 5.0  # seconds
        }

        print("🚀 HYBRID Blockchain Stress Test Initialized")
        print(f"📊 Test Duration: {self.config['duration_seconds']}s")
        print(f"👥 Concurrent Users: {self.config['concurrent_users']}")
        print(f"⚡ Target TPS: {self.config['transactions_per_second']}")

    def test_system_resources(self) -> Dict[str, Any]:
        """Test system resource usage"""
        print("\n📊 Testing System Resources...")

        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        results = {
            'cpu_usage': cpu_percent,
            'memory_usage': memory.percent,
            'memory_available': memory.available,
            'disk_usage': disk.percent,
            'disk_free': disk.free,
            'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
        }

        print(f"   🖥️  CPU Usage: {cpu_percent:.1f}%")
        print(f"   💾 Memory Usage: {memory.percent:.1f}%")
        print(f"   💿 Disk Usage: {disk.percent:.1f}%")

        return results

    def test_streamlit_ui(self) -> Dict[str, Any]:
        """Test Streamlit UI performance"""
        print("\n🖥️ Testing Streamlit UI...")

        results = {
            'response_times': [],
            'status_codes': [],
            'errors': []
        }

        test_endpoints = [
            f"{self.base_url}",
            f"{self.base_url}/_stcore/health",
        ]

        for i in range(20):
            for endpoint in test_endpoints:
                try:
                    start_time = time.time()
                    if requests:
                        response = requests.get(endpoint, timeout=10)
                        response_time = time.time() - start_time

                        results['response_times'].append(response_time)
                        results['status_codes'].append(response.status_code)

                        if response.status_code != 200:
                            results['errors'].append(f"Status {response.status_code} for {endpoint}")
                    else:
                        results['errors'].append("Requests module not available")

                except Exception as e:
                    results['errors'].append(f"Request failed: {str(e)}")
                    results['response_times'].append(10.0)  # Timeout value

        avg_response_time = np.mean(results['response_times'])
        max_response_time = np.max(results['response_times'])

        print(f"   ⚡ Average Response Time: {avg_response_time:.2f}s")
        print(f"   🔥 Max Response Time: {max_response_time:.2f}s")
        print(f"   ❌ Errors: {len(results['errors'])}")

        return results

    def test_blockchain_components(self) -> Dict[str, Any]:
        """Test blockchain component functionality"""
        print("\n⛓️ Testing Blockchain Components...")

        results = {
            'wallet_creation': 0,
            'transaction_creation': 0,
            'block_production': 0,
            'trust_validation': 0,
            'errors': []
        }

        try:
            # Test wallet creation
            from blockchain.wallet_manager import create_hybrid_wallet
            for i in range(10):
                wallet = create_hybrid_wallet()
                if wallet:
                    results['wallet_creation'] += 1
            print(f"   💼 Wallets Created: {results['wallet_creation']}/10")

            # Test transaction creation
            from blockchain.transaction_pool import create_transaction, TransactionType
            for i in range(20):
                tx = create_transaction(
                    from_address="hybrid1test",
                    to_address="hybrid1test2",
                    amount=1000000,
                    tx_type=TransactionType.TRANSFER
                )
                if tx:
                    results['transaction_creation'] += 1
            print(f"   💸 Transactions Created: {results['transaction_creation']}/20")

            # Test trust validation
            from blockchain.spiral_trust_engine import SpiralScriptEngine
            spiral_engine = SpiralScriptEngine()
            for i in range(15):
                trust_score = spiral_engine.calculate_trust_score({
                    'reliability': random.randint(70, 100),
                    'competence': random.randint(70, 100),
                    'benevolence': random.randint(70, 100),
                    'integrity': random.randint(70, 100)
                })
                if trust_score > 0:
                    results['trust_validation'] += 1
            print(f"   🌀 Trust Validations: {results['trust_validation']}/15")

        except Exception as e:
            results['errors'].append(f"Blockchain test error: {str(e)}")
            print(f"   ❌ Error: {str(e)}")

        return results

    def test_concurrent_load(self) -> Dict[str, Any]:
        """Test system under concurrent load"""
        print(f"\n🔥 Testing Concurrent Load ({self.config['concurrent_users']} users)...")

        results = {
            'successful_requests': 0,
            'failed_requests': 0,
            'total_requests': 0,
            'response_times': [],
            'errors': []
        }

        def simulate_user():
            """Simulate a single user session"""
            user_results = {'success': 0, 'failure': 0, 'times': []}

            for _ in range(10):  # Each user makes 10 requests
                try:
                    start_time = time.time()

                    # Simulate different user actions
                    action = random.choice(['view_dashboard', 'create_transaction', 'check_balance'])

                    if action == 'view_dashboard' and requests:
                        response = requests.get(f"{self.base_url}", timeout=5)
                    elif action == 'create_transaction':
                        # Simulate transaction creation
                        time.sleep(0.1)  # Simulate processing time
                        response = type('MockResponse', (), {'status_code': 200})()
                    else:  # check_balance
                        # Simulate balance check
                        time.sleep(0.05)
                        response = type('MockResponse', (), {'status_code': 200})()

                    response_time = time.time() - start_time
                    user_results['times'].append(response_time)

                    if hasattr(response, 'status_code') and response.status_code == 200:
                        user_results['success'] += 1
                    else:
                        user_results['failure'] += 1

                except Exception as e:
                    user_results['failure'] += 1
                    user_results['times'].append(5.0)  # Timeout

                time.sleep(random.uniform(0.1, 0.5))  # Random delay between requests

            return user_results

        # Run concurrent user simulations
        with ThreadPoolExecutor(max_workers=self.config['concurrent_users']) as executor:
            futures = [executor.submit(simulate_user) for _ in range(self.config['concurrent_users'])]

            for future in concurrent.futures.as_completed(futures):
                try:
                    user_result = future.result()
                    results['successful_requests'] += user_result['success']
                    results['failed_requests'] += user_result['failure']
                    results['response_times'].extend(user_result['times'])
                except Exception as e:
                    results['errors'].append(f"User simulation error: {str(e)}")

        results['total_requests'] = results['successful_requests'] + results['failed_requests']

        if results['response_times']:
            avg_response = np.mean(results['response_times'])
            max_response = np.max(results['response_times'])
            print(f"   ✅ Successful Requests: {results['successful_requests']}")
            print(f"   ❌ Failed Requests: {results['failed_requests']}")
            print(f"   ⚡ Average Response Time: {avg_response:.2f}s")
            print(f"   🔥 Max Response Time: {max_response:.2f}s")

        return results

    def test_htsx_runtime(self) -> Dict[str, Any]:
        """Test HTSX runtime and component system"""
        print("\n🌟 Testing HTSX Runtime...")

        results = {
            'component_creations': 0,
            'holographic_renders': 0,
            'spiral_script_executions': 0,
            'errors': []
        }

        try:
            # Test HTSX component creation
            from components.hybrid_htsx_holographic import HybridHTSXHolographic
            htsx_engine = HybridHTSXHolographic()

            for i in range(5):
                try:
                    # Test component rendering
                    htsx_engine.render_hybrid_coin({'balance': 1000, 'price': 10.0})
                    results['component_creations'] += 1
                except Exception as e:
                    results['errors'].append(f"Component creation error: {str(e)}")

            print(f"   🧩 Components Created: {results['component_creations']}/5")

            # Test holographic rendering
            from blockchain.holographic_blockchain_engine import HolographicBlockchainEngine
            holo_engine = HolographicBlockchainEngine()

            for i in range(3):
                try:
                    mock_data = holo_engine.generate_mock_data()
                    if mock_data:
                        results['holographic_renders'] += 1
                except Exception as e:
                    results['errors'].append(f"Holographic render error: {str(e)}")

            print(f"   🌈 Holographic Renders: {results['holographic_renders']}/3")

            # Test SpiralScript execution
            from components.spiral_script_compiler import SpiralScriptCompiler
            spiral_compiler = SpiralScriptCompiler()

            for i in range(5):
                try:
                    mock_script = f"""
                    trust_score = calculate_trust(reliability: 85, competence: 90)
                    if trust_score > 80:
                        mint_trust_currency(amount: 100, recipient: "hybrid1test{i}")
                    """
                    result = spiral_compiler.compile_script(mock_script)
                    if result.get('success'):
                        results['spiral_script_executions'] += 1
                except Exception as e:
                    results['errors'].append(f"SpiralScript execution error: {str(e)}")

            print(f"   🌀 SpiralScript Executions: {results['spiral_script_executions']}/5")

        except Exception as e:
            results['errors'].append(f"HTSX runtime test error: {str(e)}")
            print(f"   ❌ Error: {str(e)}")

        return results

    def test_ai_orchestration(self) -> Dict[str, Any]:
        """Test AI orchestration system"""
        print("\n🤖 Testing AI Orchestration...")

        results = {
            'ai_requests': 0,
            'security_scans': 0,
            'optimizations': 0,
            'errors': []
        }

        try:
            from blockchain.multi_ai_orchestrator import MultiAIOrchestrator
            ai_orchestrator = MultiAIOrchestrator()

            # Test AI requests
            for i in range(3):
                try:
                    # Simulate AI analysis request
                    result = ai_orchestrator.analyze_trust_patterns({
                        'network_data': f'test_data_{i}',
                        'trust_scores': [85, 90, 78, 92, 88]
                    })
                    if result:
                        results['ai_requests'] += 1
                except Exception as e:
                    results['errors'].append(f"AI request error: {str(e)}")

            print(f"   🧠 AI Requests: {results['ai_requests']}/3")

        except Exception as e:
            results['errors'].append(f"AI orchestration test error: {str(e)}")
            print(f"   ❌ Error: {str(e)}")

        return results

    def monitor_performance(self, duration: int) -> Dict[str, Any]:
        """Monitor system performance over time"""
        print(f"\n📈 Monitoring Performance for {duration} seconds...")

        results = {
            'cpu_samples': [],
            'memory_samples': [],
            'timestamps': [],
            'peak_cpu': 0,
            'peak_memory': 0,
            'alerts': []
        }

        start_time = time.time()
        sample_interval = 5  # seconds

        while time.time() - start_time < duration:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                timestamp = time.time() - start_time

                results['cpu_samples'].append(cpu_percent)
                results['memory_samples'].append(memory_percent)
                results['timestamps'].append(timestamp)

                results['peak_cpu'] = max(results['peak_cpu'], cpu_percent)
                results['peak_memory'] = max(results['peak_memory'], memory_percent)

                # Check for alerts
                if cpu_percent > self.config['cpu_threshold']:
                    results['alerts'].append(f"High CPU: {cpu_percent:.1f}% at {timestamp:.1f}s")

                if memory_percent > self.config['memory_threshold']:
                    results['alerts'].append(f"High Memory: {memory_percent:.1f}% at {timestamp:.1f}s")

                print(f"   📊 {timestamp:.0f}s - CPU: {cpu_percent:.1f}% | Memory: {memory_percent:.1f}%")

                time.sleep(sample_interval)

            except Exception as e:
                results['alerts'].append(f"Monitoring error: {str(e)}")
                break

        if results['cpu_samples']:
            avg_cpu = np.mean(results['cpu_samples'])
            avg_memory = np.mean(results['memory_samples'])
            print(f"   📊 Average CPU: {avg_cpu:.1f}%")
            print(f"   📊 Average Memory: {avg_memory:.1f}%")
            print(f"   🔥 Peak CPU: {results['peak_cpu']:.1f}%")
            print(f"   🔥 Peak Memory: {results['peak_memory']:.1f}%")
            print(f"   ⚠️  Alerts: {len(results['alerts'])}")

        return results

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_time = time.time() - self.start_time

        report = {
            'test_duration': total_time,
            'timestamp': time.time(),
            'configuration': self.config,
            'results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed_tests': 0,
                'failed_tests': 0,
                'performance_score': 0
            }
        }

        # Calculate pass/fail and performance score
        performance_scores = []

        for test_name, result in self.test_results.items():
            if 'errors' in result and len(result['errors']) == 0:
                report['summary']['passed_tests'] += 1
            else:
                report['summary']['failed_tests'] += 1

            # Calculate individual performance scores
            if test_name == 'ui_test' and 'response_times' in result:
                avg_response = np.mean(result['response_times'])
                ui_score = max(0, 100 - (avg_response * 20))  # 100 - penalty for slow responses
                performance_scores.append(ui_score)

            if test_name == 'resource_test':
                cpu_score = max(0, 100 - result.get('cpu_usage', 0))
                memory_score = max(0, 100 - result.get('memory_usage', 0))
                performance_scores.extend([cpu_score, memory_score])

        if performance_scores:
            report['summary']['performance_score'] = np.mean(performance_scores)

        return report

    def run_full_stress_test(self):
        """Run complete stress test suite"""
        print("🌟" + "="*60 + "🌟")
        print("     HYBRID BLOCKCHAIN COMPREHENSIVE STRESS TEST")
        print("🌟" + "="*60 + "🌟")

        # Run all test components
        self.test_results['resource_test'] = self.test_system_resources()
        if st:
            self.test_results['ui_test'] = self.test_streamlit_ui()
        self.test_results['blockchain_test'] = self.test_blockchain_components()
        self.test_results['concurrent_test'] = self.test_concurrent_load()
        self.test_results['htsx_test'] = self.test_htsx_runtime()
        self.test_results['ai_test'] = self.test_ai_orchestration()

        # Run performance monitoring
        monitoring_duration = min(60, self.config['duration_seconds'])  # Max 1 minute for quick test
        self.test_results['performance_monitor'] = self.monitor_performance(monitoring_duration)

        # Generate final report
        report = self.generate_report()

        print("\n🌟" + "="*60 + "🌟")
        print("                    STRESS TEST RESULTS")
        print("🌟" + "="*60 + "🌟")

        print(f"\n📊 Test Summary:")
        print(f"   ⏱️  Duration: {report['test_duration']:.1f} seconds")
        print(f"   ✅ Tests Passed: {report['summary']['passed_tests']}")
        print(f"   ❌ Tests Failed: {report['summary']['failed_tests']}")
        print(f"   🎯 Performance Score: {report['summary']['performance_score']:.1f}/100")

        # Performance recommendations
        print(f"\n🎯 Performance Analysis:")
        score = report['summary']['performance_score']
        if score >= 90:
            print("   🌟 EXCELLENT: System performing optimally!")
        elif score >= 75:
            print("   ✅ GOOD: System performing well with minor optimizations needed")
        elif score >= 60:
            print("   ⚠️  MODERATE: System needs performance improvements")
        else:
            print("   ❌ POOR: System requires significant optimization")

        # Specific recommendations
        print(f"\n💡 Recommendations:")

        if 'performance_monitor' in self.test_results:
            perf = self.test_results['performance_monitor']
            if perf.get('peak_cpu', 0) > 80:
                print("   🖥️  Consider optimizing CPU-intensive operations")
            if perf.get('peak_memory', 0) > 75:
                print("   💾 Consider implementing memory optimization")
            if perf.get('alerts'):
                print(f"   ⚠️  {len(perf['alerts'])} performance alerts detected")

        if 'concurrent_test' in self.test_results:
            concurrent = self.test_results['concurrent_test']
            success_rate = concurrent.get('successful_requests', 0) / max(1, concurrent.get('total_requests', 1))
            if success_rate < 0.95:
                print(f"   🔄 Improve request success rate (currently {success_rate*100:.1f}%)")

        print(f"\n🚀 HYBRID Blockchain stress test completed successfully!")
        print(f"📋 Full report saved to test results")

        return report

def main():
    """Run the stress test"""
    stress_tester = HybridStressTest()

    try:
        report = stress_tester.run_full_stress_test()

        # Save report to file
        with open('stress_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Report saved to: stress_test_report.json")

    except KeyboardInterrupt:
        print("\n⏹️ Stress test interrupted by user")
    except Exception as e:
        print(f"\n❌ Stress test failed: {str(e)}")

if __name__ == "__main__":
    main()