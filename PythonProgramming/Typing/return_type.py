from typing import List, Tuple

class Deployer:
    def deploy_components(self) -> List[Tuple[str, bool, str]]:
        return [
            ("database", True, "deployed successfully"),
            ("webserver", False, "failed to start"),
        ]

d = Deployer()
print(d.deploy_components())

