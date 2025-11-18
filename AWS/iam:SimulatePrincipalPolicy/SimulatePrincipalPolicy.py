#!/usr/bin/env python3
import boto3
import json
import sys
import argparse
from botocore.exceptions import ClientError

def parse_args():
    parser = argparse.ArgumentParser(description="simulate-principal-policy с галочками")
    parser.add_argument("--user-name", required=True)
    parser.add_argument("--account", required=True)
    parser.add_argument("--profile", default="default")
    parser.add_argument("--file", default="policy.txt")
    return parser.parse_args()

def read_actions(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        sys.exit(1)

def main():
    args = parse_args()
    arn = f"arn:aws:iam::{args.account}:user/{args.user_name}"
    session = boto3.Session(profile_name=args.profile)
    client = session.client("iam")

    print(f"Проверка для: {arn}")
    print(f"Профиль: {args.profile} | Файл: {args.file}")
    print("=" * 90)

    for action in read_actions(args.file):
        try:
            response = client.simulate_principal_policy(
                PolicySourceArn=arn,
                ActionNames=[action]
            )
            result = response["EvaluationResults"][0]
            decision = result["EvalDecision"]

            if decision == "allowed":
                # РАЗРЕШЕНО — с большой зелёной галочкой сразу после действия
                print(f"Permission: {action}      РАЗРЕШЕНО")
                print(json.dumps(response["EvaluationResults"], indent=2, ensure_ascii=False))
            else:
                # ЗАПРЕЩЕНО — коротко и без JSON
                print(f"{action}")
                if decision == "explicitDeny":
                    print("   ЗАПРЕЩЕНО (явно)")
                else:
                    print("   ЗАПРЕЩЕНО (неявно)")

            print("-" * 90)

        except ClientError as e:
            code = e.response['Error']['Code']
            if code == "InvalidInput":
                print(f"{action}")
                print("   ОШИБКА: Некорректное имя действия")
            else:
                print(f"{action} → Ошибка: {code}")
            print("-" * 90)

if __name__ == "__main__":
    main()
