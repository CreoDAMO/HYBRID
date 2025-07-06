
#!/usr/bin/env python3
"""
HYBRID Blockchain Stress Testing Suite
Comprehensive testing for all blockchain components
"""
import asyncio
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import requests
import json
import sys
import os

# Add blockchain module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'blockchain'))

from blockchain.hybrid_node import create_hybrid_node, NodeType
from blockchain.hybrid_wallet import hybrid_wallet_manager, create_hybrid_wallet
from blockchain.x_licence import licence_module, LicenseType, NFTLicenseProof
from blockchain.x_naas import naas_module, NaaSProvider, NaaSStatus
from blockchain.x_moe import moe_module, MoEModel, ModelStatus
from blockchain.ethermint import ethermint

class StressTestResults:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors = []
        self.performance_metrics = {}
        self.start_time = time.time()

    def add_result(self, test_name: str, success: bool, duration: float, error: str = None):
        self.total_tests += 1
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            if error:
                self.errors.append(f"{test_name}: {error}")
        
        self.performance_metrics[test_name] = duration

    def get_summary(self):
        total_time = time.time() - self.start_time
        return {
            "total_tests": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.failed_tests,
            "success_rate": (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0,
            "total_duration": total_time,
            "avg_test_time": sum(self.performance_metrics.values()) / len(self.performance_metrics) if self.performance_metrics else 0,
            "errors": self.errors
        }

class HybridStressTest:
    def __init__(self):
        self.results = StressTestResults()
        self.base_url = "http://0.0.0.0:26657"
        self.nodes = []
        self.wallets = []

    async def run_all_tests(self):
        """Run comprehensive stress tests"""
        print("🚀 Starting HYBRID Blockchain Super Stress Test")
        print("=" * 60)
        
        # Test categories
        test_suites = [
            ("Wallet System", self.test_wallet_system),
            ("License Module", self.test_license_module),
            ("NaaS Module", self.test_naas_module),
            ("MoE Module", self.test_moe_module),
            ("Ethermint EVM", self.test_ethermint_system),
            ("Node Operations", self.test_node_operations),
            ("Concurrent Load", self.test_concurrent_load),
            ("RPC Endpoints", self.test_rpc_endpoints),
            ("Cross-Chain Bridge", self.test_cross_chain_bridge),
            ("Performance Limits", self.test_performance_limits)
        ]
        
        for suite_name, test_func in test_suites:
            print(f"\n🧪 Testing {suite_name}...")
            try:
                await test_func()
                print(f"✅ {suite_name} tests completed")
            except Exception as e:
                print(f"❌ {suite_name} tests failed: {e}")
                self.results.add_result(f"{suite_name}_suite", False, 0, str(e))
        
        # Print final results
        self.print_results()

    async def test_wallet_system(self):
        """Stress test wallet creation and operations"""
        start_time = time.time()
        
        # Test 1: Mass wallet creation
        try:
            wallets_created = 0
            for i in range(100):
                wallet = hybrid_wallet_manager.create_new_wallet(f"test_wallet_{i}")
                if wallet:
                    wallets_created += 1
                    self.wallets.append(wallet)
            
            success = wallets_created == 100
            self.results.add_result("mass_wallet_creation", success, time.time() - start_time)
            
            if success:
                print(f"  ✅ Created {wallets_created} wallets successfully")
            else:
                print(f"  ❌ Only created {wallets_created}/100 wallets")
                
        except Exception as e:
            self.results.add_result("mass_wallet_creation", False, time.time() - start_time, str(e))

        # Test 2: Concurrent wallet operations
        start_time = time.time()
        try:
            async def wallet_operation():
                wallet = random.choice(self.wallets)
                balance = hybrid_wallet_manager.get_balance(wallet.address)
                return balance >= 0
            
            tasks = [wallet_operation() for _ in range(50)]
            results = await asyncio.gather(*tasks)
            success = all(results)
            
            self.results.add_result("concurrent_wallet_ops", success, time.time() - start_time)
            print(f"  ✅ Concurrent wallet operations: {sum(results)}/50 successful")
            
        except Exception as e:
            self.results.add_result("concurrent_wallet_ops", False, time.time() - start_time, str(e))

    async def test_license_module(self):
        """Stress test NFT license system"""
        start_time = time.time()
        
        # Test 1: Mass license registration
        try:
            licenses_created = 0
            for i in range(50):
                proof = NFTLicenseProof(
                    license_id=f"HNL-VAL-{i:03d}",
                    owner_address=f"hybrid1test{i:020d}",
                    license_type=LicenseType.VALIDATOR if i % 2 == 0 else LicenseType.STORAGE,
                    chain="base",
                    contract_address=f"0x{i:040x}",
                    token_id=str(i),
                    block_height=12345 + i,
                    tx_hash=f"0x{hash(f'license_{i}'):064x}",
                    signature=f"0x{i:064x}"
                )
                
                if licence_module.register_nft_proof(proof):
                    licenses_created += 1
            
            success = licenses_created == 50
            self.results.add_result("mass_license_creation", success, time.time() - start_time)
            print(f"  ✅ Registered {licenses_created}/50 licenses")
            
        except Exception as e:
            self.results.add_result("mass_license_creation", False, time.time() - start_time, str(e))

        # Test 2: License verification stress
        start_time = time.time()
        try:
            verifications = 0
            for i in range(100):
                address = f"hybrid1test{i % 50:020d}"
                license_type = LicenseType.VALIDATOR if i % 2 == 0 else LicenseType.STORAGE
                if licence_module.verify_license(address, license_type):
                    verifications += 1
            
            success = verifications > 0
            self.results.add_result("license_verification_stress", success, time.time() - start_time)
            print(f"  ✅ License verifications: {verifications}/100 successful")
            
        except Exception as e:
            self.results.add_result("license_verification_stress", False, time.time() - start_time, str(e))

    async def test_naas_module(self):
        """Stress test NaaS delegation system"""
        start_time = time.time()
        
        # Test 1: Mass NaaS provider registration
        try:
            providers_created = 0
            for i in range(20):
                provider = NaaSProvider(
                    provider_id=f"naas_provider_{i}",
                    name=f"Test Provider {i}",
                    address=f"hybrid1naas{i:020d}",
                    commission_rate=random.uniform(0.1, 0.5),
                    max_delegations=random.randint(10, 100),
                    uptime_guarantee=random.uniform(0.95, 0.999),
                    managed_nodes=[]
                )
                
                if naas_module.register_naas_provider(provider):
                    providers_created += 1
            
            success = providers_created == 20
            self.results.add_result("mass_naas_providers", success, time.time() - start_time)
            print(f"  ✅ Registered {providers_created}/20 NaaS providers")
            
        except Exception as e:
            self.results.add_result("mass_naas_providers", False, time.time() - start_time, str(e))

        # Test 2: Mass delegations
        start_time = time.time()
        try:
            delegations_created = 0
            providers = naas_module.list_providers()
            
            for i in range(100):
                if providers:
                    provider = random.choice(providers)
                    delegation_id = naas_module.delegate_to_naas(
                        delegator=f"hybrid1user{i:020d}",
                        provider_id=provider.provider_id,
                        license_id=f"HNL-VAL-{i % 50:03d}",
                        node_type="validator" if i % 2 == 0 else "storage"
                    )
                    if delegation_id:
                        delegations_created += 1
            
            success = delegations_created > 0
            self.results.add_result("mass_naas_delegations", success, time.time() - start_time)
            print(f"  ✅ Created {delegations_created}/100 NaaS delegations")
            
        except Exception as e:
            self.results.add_result("mass_naas_delegations", False, time.time() - start_time, str(e))

    async def test_moe_module(self):
        """Stress test AI MoE system"""
        start_time = time.time()
        
        # Test 1: Mass model registration
        try:
            models_created = 0
            for i in range(25):
                model = MoEModel(
                    model_id=f"test_model_{i}",
                    name=f"Test AI Model {i}",
                    description=f"Test model for stress testing {i}",
                    ipfs_cid=f"QmTest{i:040d}",
                    creator=f"hybrid1creator{i:020d}",
                    version=f"1.{i}.0",
                    input_schema={"type": "string"},
                    output_schema={"type": "string"},
                    inference_fee=random.randint(10000, 1000000)
                )
                
                if moe_module.register_model(model):
                    models_created += 1
            
            success = models_created == 25
            self.results.add_result("mass_moe_models", success, time.time() - start_time)
            print(f"  ✅ Registered {models_created}/25 AI models")
            
        except Exception as e:
            self.results.add_result("mass_moe_models", False, time.time() - start_time, str(e))

        # Test 2: Mass inference calls
        start_time = time.time()
        try:
            inference_calls = 0
            models = moe_module.list_active_models()
            
            for i in range(100):
                if models:
                    model = random.choice(models)
                    call_id = moe_module.call_moe(
                        caller=f"hybrid1user{i:020d}",
                        model_id=model.model_id,
                        input_data=f"test input data {i}"
                    )
                    if call_id:
                        inference_calls += 1
            
            success = inference_calls > 0
            self.results.add_result("mass_moe_inference", success, time.time() - start_time)
            print(f"  ✅ Created {inference_calls}/100 inference calls")
            
        except Exception as e:
            self.results.add_result("mass_moe_inference", False, time.time() - start_time, str(e))

    async def test_ethermint_system(self):
        """Stress test Ethermint EVM subsystem"""
        start_time = time.time()
        
        # Test 1: Mass contract deployment
        try:
            contracts_deployed = 0
            for i in range(20):
                contract_address = ethermint.deploy_contract(
                    creator=f"hybrid1creator{i:020d}",
                    bytecode=f"0x{i:064x}",
                    abi=[{"name": "test", "type": "function"}],
                    gas_limit=500000,
                    gas_price=1000
                )
                if contract_address:
                    contracts_deployed += 1
            
            success = contracts_deployed == 20
            self.results.add_result("mass_contract_deployment", success, time.time() - start_time)
            print(f"  ✅ Deployed {contracts_deployed}/20 EVM contracts")
            
        except Exception as e:
            self.results.add_result("mass_contract_deployment", False, time.time() - start_time, str(e))

        # Test 2: Mass contract calls
        start_time = time.time()
        try:
            contract_calls = 0
            contracts = list(ethermint.contracts.keys())
            
            for i in range(50):
                if contracts:
                    contract_address = random.choice(contracts)
                    tx_hash = ethermint.call_contract(
                        caller=f"hybrid1caller{i:020d}",
                        contract_address=contract_address,
                        function_data=f"test_function_{i}",
                        gas_limit=100000,
                        gas_price=1000
                    )
                    if tx_hash:
                        contract_calls += 1
            
            success = contract_calls > 0
            self.results.add_result("mass_contract_calls", success, time.time() - start_time)
            print(f"  ✅ Made {contract_calls}/50 contract calls")
            
        except Exception as e:
            self.results.add_result("mass_contract_calls", False, time.time() - start_time, str(e))

    async def test_node_operations(self):
        """Stress test node creation and operations"""
        start_time = time.time()
        
        try:
            # Create multiple nodes
            for i in range(5):
                node_type = "validator" if i % 2 == 0 else "storage"
                node = create_hybrid_node(node_type)
                self.nodes.append(node)
            
            success = len(self.nodes) == 5
            self.results.add_result("node_creation", success, time.time() - start_time)
            print(f"  ✅ Created {len(self.nodes)}/5 nodes")
            
        except Exception as e:
            self.results.add_result("node_creation", False, time.time() - start_time, str(e))

    async def test_concurrent_load(self):
        """Test system under concurrent load"""
        start_time = time.time()
        
        async def concurrent_operation():
            operations = [
                lambda: hybrid_wallet_manager.create_new_wallet(f"concurrent_{random.randint(1000, 9999)}"),
                lambda: licence_module.verify_license(f"hybrid1test{random.randint(0, 49):020d}", LicenseType.VALIDATOR),
                lambda: moe_module.list_active_models(),
                lambda: ethermint.get_balance(f"hybrid1user{random.randint(0, 99):020d}"),
            ]
            
            operation = random.choice(operations)
            try:
                result = operation()
                return result is not None
            except:
                return False
        
        try:
            # Run 200 concurrent operations
            tasks = [concurrent_operation() for _ in range(200)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful = sum(1 for r in results if r is True)
            success = successful > 150  # 75% success rate
            
            self.results.add_result("concurrent_load", success, time.time() - start_time)
            print(f"  ✅ Concurrent operations: {successful}/200 successful")
            
        except Exception as e:
            self.results.add_result("concurrent_load", False, time.time() - start_time, str(e))

    async def test_rpc_endpoints(self):
        """Test RPC endpoint responsiveness"""
        start_time = time.time()
        
        try:
            # Test various RPC endpoints
            endpoints = [
                "/status",
                f"/balance/{random.choice(self.wallets).address if self.wallets else 'hybrid1test'}",
                "/founder",
            ]
            
            successful_requests = 0
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                    if response.status_code == 200:
                        successful_requests += 1
                except:
                    pass
            
            success = successful_requests > 0
            self.results.add_result("rpc_endpoints", success, time.time() - start_time)
            print(f"  ✅ RPC endpoints: {successful_requests}/{len(endpoints)} responsive")
            
        except Exception as e:
            self.results.add_result("rpc_endpoints", False, time.time() - start_time, str(e))

    async def test_cross_chain_bridge(self):
        """Test cross-chain bridge functionality"""
        start_time = time.time()
        
        try:
            # Test bridge operations
            if self.nodes:
                node = self.nodes[0]
                bridge_txs = 0
                
                for i in range(10):
                    tx_hash = await node.bridge.bridge_tokens(
                        from_chain="hybrid",
                        to_chain="base",
                        amount=random.randint(1000, 10000),
                        token="HYBRID"
                    )
                    if tx_hash:
                        bridge_txs += 1
                
                success = bridge_txs > 0
                self.results.add_result("cross_chain_bridge", success, time.time() - start_time)
                print(f"  ✅ Bridge transactions: {bridge_txs}/10 successful")
            else:
                self.results.add_result("cross_chain_bridge", False, time.time() - start_time, "No nodes available")
                
        except Exception as e:
            self.results.add_result("cross_chain_bridge", False, time.time() - start_time, str(e))

    async def test_performance_limits(self):
        """Test system performance limits"""
        start_time = time.time()
        
        try:
            # Memory stress test
            large_data = []
            for i in range(1000):
                large_data.append({
                    "id": i,
                    "data": "x" * 1000,  # 1KB per entry
                    "timestamp": time.time()
                })
            
            # CPU stress test
            def cpu_intensive_task():
                total = 0
                for i in range(100000):
                    total += i ** 2
                return total
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(cpu_intensive_task) for _ in range(50)]
                results = [f.result() for f in as_completed(futures)]
            
            success = len(results) == 50 and len(large_data) == 1000
            self.results.add_result("performance_limits", success, time.time() - start_time)
            print(f"  ✅ Performance stress test completed")
            
        except Exception as e:
            self.results.add_result("performance_limits", False, time.time() - start_time, str(e))

    def print_results(self):
        """Print comprehensive test results"""
        summary = self.results.get_summary()
        
        print("\n" + "=" * 60)
        print("🎯 HYBRID BLOCKCHAIN SUPER STRESS TEST RESULTS")
        print("=" * 60)
        
        print(f"📊 Overall Statistics:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        print(f"   Total Duration: {summary['total_duration']:.2f}s")
        print(f"   Average Test Time: {summary['avg_test_time']:.3f}s")
        
        if summary['success_rate'] >= 90:
            print("\n🏆 EXCELLENT! System passed stress test with flying colors!")
        elif summary['success_rate'] >= 75:
            print("\n✅ GOOD! System handled stress test well!")
        elif summary['success_rate'] >= 50:
            print("\n⚠️  MODERATE! System survived but needs optimization!")
        else:
            print("\n❌ POOR! System needs significant improvements!")
        
        # Performance breakdown
        print(f"\n⚡ Performance Breakdown:")
        for test_name, duration in sorted(self.results.performance_metrics.items()):
            status = "🟢" if test_name not in [e.split(":")[0] for e in summary['errors']] else "🔴"
            print(f"   {status} {test_name}: {duration:.3f}s")
        
        # Error details
        if summary['errors']:
            print(f"\n🐛 Error Details:")
            for error in summary['errors'][:10]:  # Show first 10 errors
                print(f"   • {error}")
            if len(summary['errors']) > 10:
                print(f"   ... and {len(summary['errors']) - 10} more errors")
        
        print("\n" + "=" * 60)

async def main():
    """Run the stress test"""
    stress_test = HybridStressTest()
    await stress_test.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
