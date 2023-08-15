import setuptools

DESCRIPTION = 'SecurityGPT, GPT for security practioners'
LONG_DESCRIPTION = """ 
# What is securitygpt ? 
securitygpt is a package that makes makes common tasks that a
security engineer does easy using generative LLMs.  

As a security engineer, you dont want to worry about writing correct prompts, we have taken care of that for you.

# Examples

## VulnGPT

### Summarize CVEs

```
from vulngpt.cve_gpt import summmarize_cve
summmarize_cve("CVE-2021-36934")

{
  "base_score": 7.8,
  "severity": "High",
  "attack_vector": "Local",
  "attack_complexity": "Low",
  "product_name": "Unknown",
  "company_name": "Unknown",
  "cwe_name": "CWE-269",
  "versions_affected": "Unknown",
  "versions_not_affected": "Unknown",
  "applicable_operating_systems": "Unknown",
  "application_configuration_needed": "Unknown",
  "versions_fixed": "Unknown",
  "remediation": {
    "patch_remediation": "Unknown",
    "network_remediation": "Unknown",
    "host_remediation": "Unknown",
    "application_remediation": "Unknown",
    "database_remediation": "Unknown",
    "operating_system_remediation": "Unknown"
  },
  "summary": "This is a potential security issue. Please refer to the provided links for more information."
}

```


"""

setuptools.setup(
    name="securitygpt",                     # This is the name of the package
    version="0.0.1.5",                        # The initial release version
    author="rkreddyp",                     # Full name of the author
    description="SecurityGPT, GPT for security practioners",
    long_description=LONG_DESCRIPTION,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["securitygpt"],             # Name of the python package
    install_requires=[]                     # Install other dependencies if any
)
