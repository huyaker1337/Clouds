$permissions = Get-Content "policy.txt" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
foreach ($permission in $permissions) {
    $result = aws iam simulate-principal-policy `
        --policy-source-arn arn:aws:iam::058264439561:user/DevAppUser `
        --action-names $permission `
        --profile <Your_Profile>
    Write-Output "Permission: $permission"
    Write-Output $result
    Write-Output "`n"
}
