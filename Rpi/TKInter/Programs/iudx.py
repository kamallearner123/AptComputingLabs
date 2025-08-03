import subprocess
import yaml
import psutil
import requests
import time
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("iudx_deployment.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class IUDXDeployer:
    def __init__(self, config_file: str):
        """Initialize with configuration file."""
        self.config = self._load_config(config_file)
        self.kubectl_cmd = "kubectl"
        self.helm_cmd = "helm"
        self.monitoring_endpoint = self.config.get("monitoring", {}).get("endpoint", "http://localhost:8080/status")
        self.min_requirements = self.config.get("node_requirements", {
            "cpu_cores": 4,
            "memory_gb": 8,
            "disk_gb": 50
        })

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
            logger.info("Configuration loaded successfully from %s", config_file)
            return config
        except Exception as e:
            logger.error("Failed to load config file %s: %s", config_file, str(e))
            raise

    def check_node_readiness(self) -> bool:
        """Check if nodes meet minimum requirements."""
        logger.info("Checking node readiness...")
        try:
            # Check CPU, memory, and disk
            cpu_cores = psutil.cpu_count()
            memory_gb = psutil.virtual_memory().total / (1024 ** 3)
            disk_gb = psutil.disk_usage("/").free / (1024 ** 3)

            if (cpu_cores < self.min_requirements["cpu_cores"] or
                memory_gb < self.min_requirements["memory_gb"] or
                disk_gb < self.min_requirements["disk_gb"]):
                logger.error(
                    "Node does not meet requirements: CPU %d/%d, Memory %.2f/%.2f GB, Disk %.2f/%.2f GB",
                    cpu_cores, self.min_requirements["cpu_cores"],
                    memory_gb, self.min_requirements["memory_gb"],
                    disk_gb, self.min_requirements["disk_gb"]
                )
                return False
            logger.info("Node meets requirements: CPU %d, Memory %.2f GB, Disk %.2f GB",
                        cpu_cores, memory_gb, disk_gb)

            # Check kubectl connectivity
            result = subprocess.run([self.kubectl_cmd, "get", "nodes"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("kubectl failed to connect to cluster: %s", result.stderr)
                return False
            logger.info("kubectl connected to cluster successfully")
            return True
        except Exception as e:
            logger.error("Node readiness check failed: %s", str(e))
            return False

    def validate_config(self) -> bool:
        """Validate IUDX component configurations."""
        logger.info("Validating configuration...")
        required_keys = ["rancher", "components", "monitoring"]
        for key in required_keys:
            if key not in self.config:
                logger.error("Missing configuration section: %s", key)
                return False
        logger.info("Configuration validated successfully")
        return True

    def deploy_rancher_kubernetes(self) -> bool:
        """Deploy Rancher and Kubernetes cluster."""
        logger.info("Deploying Rancher and Kubernetes cluster...")
        try:
            rancher_config = self.config.get("rancher", {})
            helm_repo = rancher_config.get("helm_repo", "https://releases.rancher.com/server-charts/stable")
            chart_name = rancher_config.get("chart_name", "rancher")
            namespace = rancher_config.get("namespace", "cattle-system")

            # Add Rancher Helm repo
            subprocess.run([self.helm_cmd, "repo", "add", "rancher-stable", helm_repo], check=True)
            subprocess.run([self.helm_cmd, "repo", "update"], check=True)

            # Install Rancher
            helm_install_cmd = [
                self.helm_cmd, "install", "rancher", f"rancher-stable/{chart_name}",
                "--namespace", namespace, "--create-namespace",
                "--set", f"hostname={rancher_config.get('hostname', 'rancher.local')}",
                "--wait"
            ]
            subprocess.run(helm_install_cmd, check=True)
            logger.info("Rancher deployed successfully in namespace %s", namespace)

            # Wait for Kubernetes cluster readiness
            time.sleep(30)  # Wait for Rancher to initialize
            result = subprocess.run([self.kubectl_cmd, "get", "nodes", "-o", "wide"],
                                  capture_output=True, text=True)
            logger.info("Kubernetes nodes: %s", result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Failed to deploy Rancher/Kubernetes: %s", e.stderr)
            return False
        except Exception as e:
            logger.error("Unexpected error during Rancher deployment: %s", str(e))
            return False

    def deploy_component(self, component: Dict) -> Tuple[bool, str]:
        """Deploy a single component (e.g., immudb, PostgreSQL, IUDX services)."""
        name = component.get("name")
        logger.info("Deploying component: %s", name)
        try:
            if component.get("type") == "helm":
                helm_cmd = [
                    self.helm_cmd, "install", name,
                    component.get("chart"),
                    "--namespace", component.get("namespace", "default"),
                    "--create-namespace",
                    "--set", ",".join([f"{k}={v}" for k, v in component.get("values", {}).items()]),
                    "--wait"
                ]
                subprocess.run(helm_cmd, check=True)
            elif component.get("type") == "kubectl":
                subprocess.run([self.kubectl_cmd, "apply", "-f", component.get("manifest")], check=True)
            logger.info("Component %s deployed successfully", name)
            return True, f"{name} deployed"
        except subprocess.CalledProcessError as e:
            logger.error("Failed to deploy %s: %s", name, e.stderr)
            return False, f"{name} deployment failed: {e.stderr}"
        except Exception as e:
            logger.error("Unexpected error deploying %s: %s", name, str(e))
            return False, f"{name} deployment failed: {str(e)}"

    def deploy_components(self) -> List[Tuple[str, bool, str]]:
        """Deploy all dependent and IUDX components."""
        logger.info("Deploying all components...")
        components = self.config.get("components", [])
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_component = {executor.submit(self.deploy_component, comp): comp["name"]
                                 for comp in components}
            for future in future_to_component:
                component_name = future_to_component[future]
                success, message = future.result()
                results.append((component_name, success, message))
        return results

    def start_monitoring(self) -> None:
        """Start monitoring module in a separate thread."""
        logger.info("Starting monitoring module...")
        def monitor():
            while True:
                try:
                    response = requests.get(self.monitoring_endpoint, timeout=5)
                    if response.status_code == 200:
                        logger.info("Monitoring endpoint %s is healthy: %s",
                                   self.monitoring_endpoint, response.json())
                    else:
                        logger.warning("Monitoring endpoint %s returned status %d",
                                      self.monitoring_endpoint, response.status_code)
                except requests.RequestException as e:
                    logger.error("Monitoring endpoint %s failed: %s", self.monitoring_endpoint, str(e))
                time.sleep(60)  # Check every minute
        ThreadPoolExecutor().submit(monitor)

    def get_component_status(self) -> Dict[str, str]:
        """Get status of all PaaS, third-party, and IUDX components."""
        logger.info("Checking component statuses...")
        status = {}
        try:
            # Check Rancher/Kubernetes
            result = subprocess.run([self.kubectl_cmd, "get", "nodes", "-o", "jsonpath={.items[*].status.conditions[?(@.type=='Ready')].status}"],
                                  capture_output=True, text=True)
            status["rancher_kubernetes"] = "Ready" if "True" in result.stdout else "NotReady"

            # Check components
            for component in self.config.get("components", []):
                name = component.get("name")
                namespace = component.get("namespace", "default")
                result = subprocess.run([self.kubectl_cmd, "get", "pods", "-n", namespace,
                                       "-l", f"app={name}", "-o", "jsonpath={.items[*].status.phase}"],
                                      capture_output=True, text=True)
                status[name] = result.stdout or "Unknown"
            logger.info("Component statuses: %s", status)
            return status
        except Exception as e:
            logger.error("Failed to get component statuses: %s", str(e))
            return status

    def deploy(self) -> bool:
        """Main deployment function."""
        logger.info("Starting IUDX deployment...")
        # Step 1: Check readiness
        if not self.check_node_readiness():
            logger.error("Node readiness check failed. Aborting deployment.")
            return False

        # Step 2: Validate configuration
        if not self.validate_config():
            logger.error("Configuration validation failed. Aborting deployment.")
            return False

        # Step 3: Deploy Rancher and Kubernetes
        if not self.deploy_rancher_kubernetes():
            logger.error("Rancher/Kubernetes deployment failed. Aborting deployment.")
            return False

        # Step 4: Deploy components
        results = self.deploy_components()
        for name, success, message in results:
            if not success:
                logger.error("Component deployment failed: %s", message)
                return False

        # Step 5: Start monitoring
        self.start_monitoring()

        # Step 6: Report final status
        status = self.get_component_status()
        logger.info("Final deployment status: %s", status)
        return all(status.values()) and all(s == "Running" for s in status.values())

if __name__ == "__main__":
    config_file = "iudx_config.yaml"
    deployer = IUDXDeployer(config_file)
    success = deployer.deploy()
    logger.info("IUDX deployment %s", "successful" if success else "failed")