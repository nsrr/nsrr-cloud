output "iam_account_alias" {
  description = "Lists the account alias"
  value       =  aws_iam_account_alias.alias.account_alias
}

output "iam_account_password_max_age" {
  description = "Lists the max age of password"
  value       =  aws_iam_account_password_policy.strict.max_password_age
}