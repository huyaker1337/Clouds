# AWS IAM Permission Checker (simulate-principal-policy)

### What this script does

It answers one simple question:  
**"What can this IAM user (or role) actually do in this AWS account?"**  
—even if the user himself has no permission to view his own policies.

### Why you need it

AWS does not have a button that says “Show me all effective permissions”.  
But it has a secret API called `iam:SimulatePrincipalPolicy` that can answer “Is this action allowed for this user?”.

This script uses that secret API to check a whole list of actions and shows you the real result.

### What you will see in the output

- Actions that are ALLOWED → full JSON + the word РАЗРЕШЕНО right next to the permission  
  You immediately see which policy gave the permission (very useful for audits and pentests)

- Actions that are DENIED → just one short line “ЗАПРЕЩЕНО (неявно)” or “ЗАПРЕЩЕНО (явно)”  

### How to use it (Unix)

1. Save the script as `SimulatePrincipalPolicy.py`
2. Create a file `policy.txt` with actions you want to test (one per line), example:
```text
iam:PutUserPolicy
iam:PutRolePolicy
iam:CreatePolicy
iam:AttachUserPolicy
iam:CreateAccessKey
sts:AssumeRole
lambda:UpdateFunctionCode
lambda:InvokeFunction
iam:UpdateAssumeRolePolicy
s3:ListBucket
s3:GetObject
iam:CreateUser
ec2:StartInstance
```
3. Run it (you need a profile that has iam:SimulatePrincipalPolicy permission — usually SecurityAudit or admin works):
```bash
python3 SimulatePrincipalPolicy.py --user-name DevAppUser --account 058264439561 --profile mirage --file policy.txt
```
<img width="868" height="510" alt="image" src="https://github.com/user-attachments/assets/558a3d5b-ad2a-4601-ab96-bc9315fd2e60" />

### How to use it (Windows)

1. Save the script as `SimulatePrincipalPolicy.ps1`
2. Create a file `policy.txt` with actions you want to test (one per line), example:
```text
iam:PutUserPolicy
iam:PutRolePolicy
iam:CreatePolicy
iam:AttachUserPolicy
iam:CreateAccessKey
sts:AssumeRole
lambda:UpdateFunctionCode
lambda:InvokeFunction
iam:UpdateAssumeRolePolicy
s3:ListBucket
s3:GetObject
iam:CreateUser
ec2:StartInstance
```
3. Run it (you need a profile that has iam:SimulatePrincipalPolicy permission — usually SecurityAudit or admin works):
```powershell
.\SimulatePrincipalPolicy.ps1
```
<img width="510" height="878" alt="image" src="https://github.com/user-attachments/assets/e382c6b6-9213-4336-853e-4b8165d7f410" />
