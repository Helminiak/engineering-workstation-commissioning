# Native Bionic verification — operator required

The API/MCP local-agent path passes independent tests. Native Bionic projects and tool approval remain unverified because no native UI surface is available to this session. Do not infer native support from API tests.

1. Open the installed Bionic interface. Record the actual displayed version, if available, and the selected model/context. Do not include credentials or account settings screenshots.
2. Inspect the actual project/tool controls. If they provide a workspace selection, select `/home/joe/LLM-Workspace`. Record available controls and approval behavior rather than assuming a coding mode exists.
3. Submit the prompt below to the native agent. Approve only normal-user commands in the named scratch directory. Do not approve sudo, external uploads, new repositories, or pushes.
4. Save the native transcript locally to `evidence/bionic-native-transcript.txt`, excluding credentials. Preserve command exit codes and errors. Run the independent commands below in a terminal; record output and exits in `evidence/bionic-native-verification.txt`.
5. Have the commissioning runner record verification only after the artifacts and transcript are independently checked. If tools are unavailable, keep MANUAL_REQUIRED or BLOCKED and describe the actual error.

## Native agent prompt

Execute actual tools. Only write inside `/home/joe/LLM-Workspace/scratch/bionic-native-proof`. Run whoami, pwd and nvidia-smi. Create the directory if needed. Write and read probe.txt containing native-bionic-verified. Create check.sh that prints bash-ok and execute it. Create calculation.py that asserts sum(i*i for i in range(1,11)) == 385 and prints PYTHON_RESULT=385; execute it. Inspect Git status and current branch of `/home/joe/LLM-Workspace` without modifying Git. Write report.md in the scratch directory with each command, actual result and exit code. Do not claim success without execution. Do not use sudo, network, secrets, new repositories, commits or pushes.

## Independent terminal checks

```bash
cd /home/joe/LLM-Workspace
cat scratch/bionic-native-proof/probe.txt
bash scratch/bionic-native-proof/check.sh
python3 scratch/bionic-native-proof/calculation.py
cat scratch/bionic-native-proof/report.md
git status --short
git branch --show-current
```

Inspect source before running the generated Bash/Python files. Matching output alone is insufficient to prove native execution: review the native transcript and tool exit codes. Existing files are not proof of a fresh run.
