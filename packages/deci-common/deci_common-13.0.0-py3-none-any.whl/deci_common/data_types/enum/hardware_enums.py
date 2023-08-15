from enum import Enum
from typing import Optional

UNKNOWN = "UNKNOWN"


class HardwareType(str, Enum):
    """
    The type of the hardware to run on (CPU/GPU Names)
    """

    K80 = "K80"
    V100 = "V100"
    T4 = "T4"
    A10G = "A10G"
    G4DN_XLARGE = "g4dn.xlarge"
    G5_XLARGE = "g5.xlarge"
    A100_80G = "A100 80GB GCP"
    A100_40G = "A100 40GB GCP"
    EPYC = "EPYC"
    EPYC_7002 = "EPYC 7002"
    EPYC_7003 = "EPYC 7003"
    XAVIER = "Jetson Xavier"
    NANO = "Jetson Nano"
    XAVIER_AGX = "Jetson Xavier AGX"
    ORIN = "Jetson Orin"
    ORIN_NX = "Jetson Orin NX"
    ORIN_NANO = "Jetson Orin Nano"
    ORIN_NANO_4G = "Jetson Orin Nano 4GB"
    CASCADE_LAKE = "Cascade Lake"
    SKYLAKE = "Skylake"
    Broadwell = "Broadwell"
    Icelake = "Icelake"
    NUC_TIGER_LAKE = "Intel NUC Tiger Lake"
    SKYLAKE_SP = "Skylake-SP"
    CASCADE_LAKE_GCP = "Cascade Lake GCP"
    IMX8 = "NXP i.MX 8M mini"
    C5_2XLARGE = "c5.2xlarge"
    SAPPHIRE_RAPIDS_GCP = "Sapphire Rapids"
    L4_GCP = "L4"
    M5_4XLARGE = "m5.4xlarge"

    @property
    def is_deprecated(self) -> bool:
        return self in [HardwareType.K80, HardwareType.EPYC]


class HardwareGroup(str, Enum):
    CPU = "CPU"
    GPU = "GPU"
    COMMERCIAL_EDGE = "Commercial Edge"
    CONSUMER_EDGE = "Consumer Edge"


class HardwareMachineModel(str, Enum):
    K80 = "p2.xlarge"
    V100 = "p3.2xlarge"
    T4 = "g4dn.2xlarge"
    A10G = "g5.2xlarge"
    G4DN_XLARGE = "g4dn.xlarge"
    G5_XLARGE = "g5.xlarge"
    EPYC = "c5a.2xlarge"
    CASCADE_LAKE = "c5.4xlarge"
    SKYLAKE = "c5n.4xlarge"
    Broadwell = "m4.4xlarge"
    Icelake = "m6i.4xlarge"
    EPYC_7002 = "c5a.4xlarge"
    EPYC_7003 = "m6a.4xlarge"
    SKYLAKE_SP = "m5.2xlarge"
    A100_40G = "a2-highgpu-1g"
    A100_80G = "a2-ultragpu-1g"
    CASCADE_LAKE_GCP = "n2-standard-4"
    C5_2XLARGE = "c5.2xlarge"
    SAPPHIRE_RAPIDS_GCP = "c3-highcpu-8"
    L4_GCP = "g2-standard-8"
    M5_4XLARGE = "m5.4xlarge"

    NANO = HardwareType.NANO.value
    XAVIER = HardwareType.XAVIER.value
    XAVIER_AGX = HardwareType.XAVIER_AGX.value
    ORIN = HardwareType.ORIN.value
    ORIN_NX = HardwareType.ORIN_NX.value
    ORIN_NANO = HardwareType.ORIN_NANO.value
    ORIN_NANO_4G = HardwareType.ORIN_NANO_4G.value
    NUC_TIGER_LAKE = HardwareType.NUC_TIGER_LAKE.value
    IMX8 = HardwareType.IMX8.value


class InferenceHardware(str, Enum):
    """
    Hardware that can be used for deep learning inference.
    """

    CPU = "cpu"
    GPU = "gpu"


class InferyVersion(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    JETSON = "jetson"
    JETSON_PY36 = "jetson_py36"
    JETSON_PY38 = "jetson_py38"


class HardwareEnvironment(str, Enum):
    GCP = "gcp"
    AWS = "aws"
    Azure = "azure"
    PREMISE = "on premise"


class HardwareVendor(str, Enum):
    INTEL = "intel"
    NVIDIA = "nvidia"
    AMD = "amd"
    NXP = "nxp"


class HardwareImageRepository(str, Enum):
    INTEL = "intel"
    JETSON = "jetson"


class HardwareImageDistribution(str, Enum):
    J46 = "j46"
    J50 = "j50"
    J502 = "j502"

    @property
    def python_version(self) -> str:
        dist_to_version = {
            HardwareImageDistribution.J46: "3.6",
            HardwareImageDistribution.J50: "3.8",
            HardwareImageDistribution.J502: "3.8",
        }
        return dist_to_version[self]


def type_with_model(model: HardwareMachineModel, override_label: Optional[str] = None) -> str:
    return f"{override_label or HardwareType[model.name].value} ({model})"


class HardwareTypeLabel(str, Enum):
    XAVIER = "Jetson Xavier NX 16GB"
    NANO = "Jetson Nano 4GB"
    XAVIER_AGX = "Jetson AGX Xavier 32GB"
    ORIN = "Jetson AGX Orin Development Kit"
    ORIN_NX = "Jetson Orin NX 16GB"
    ORIN_NANO = "Jetson Orin Nano 8GB"
    ORIN_NANO_4G = "Jetson Orin Nano 4GB"
    EPYC = type_with_model(HardwareMachineModel.EPYC)
    EPYC_7002 = type_with_model(HardwareMachineModel.EPYC_7002, f"AMD Rome {HardwareType.EPYC_7002.value}")
    EPYC_7003 = type_with_model(HardwareMachineModel.EPYC_7003, f"AMD Milan {HardwareType.EPYC_7003.value}")
    CASCADE_LAKE = type_with_model(HardwareMachineModel.CASCADE_LAKE)
    SKYLAKE = type_with_model(HardwareMachineModel.SKYLAKE, "Sky Lake")
    Broadwell = type_with_model(HardwareMachineModel.Broadwell)
    Icelake = type_with_model(HardwareMachineModel.Icelake, "Ice Lake")
    K80 = type_with_model(HardwareMachineModel.K80)
    V100 = type_with_model(HardwareMachineModel.V100)
    SKYLAKE_SP = type_with_model(HardwareMachineModel.SKYLAKE_SP)
    T4 = type_with_model(HardwareMachineModel.T4)
    A10G = type_with_model(HardwareMachineModel.A10G)
    A100_40G = type_with_model(HardwareMachineModel.A100_40G, "A100 40GB")
    A100_80G = type_with_model(HardwareMachineModel.A100_80G, "A100 80GB")
    CASCADE_LAKE_GCP = type_with_model(HardwareMachineModel.CASCADE_LAKE_GCP, "Cascade Lake")
    SAPPHIRE_RAPIDS_GCP = type_with_model(HardwareMachineModel.SAPPHIRE_RAPIDS_GCP, "Sapphire Rapids")
    L4_GCP = type_with_model(HardwareMachineModel.L4_GCP, "L4")

    NUC_TIGER_LAKE = HardwareType.NUC_TIGER_LAKE.value
    IMX8 = HardwareType.IMX8.value
    C5_2XLARGE = HardwareType.C5_2XLARGE.value
    M5_4XLARGE = HardwareType.M5_4XLARGE.value
    G4DN_XLARGE = HardwareType.G4DN_XLARGE.value
    G5_XLARGE = HardwareType.G5_XLARGE.value
