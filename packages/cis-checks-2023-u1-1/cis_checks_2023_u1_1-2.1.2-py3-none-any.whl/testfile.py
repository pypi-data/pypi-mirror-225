from cis_checks_2023_u1 import aws_client
import pandas as pd

if __name__ == "__main__":
    # Client_ID = ['AKIA57XTQP6U7LIRSXTF']
    # Client_Secret = ['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']

    # Rahul Kumar Sharma
    # Client_ID = ['AKIA4OSEB3QCJAQBSHEW']
    # Client_Secret = ['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']

    # profile_name = ['impetus_aws']
    # Client_ID = ['AKIATI4F7L7F2MNJAI6B']
    # Client_Secret = ['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']

    # Impetus-Transility-Awsfocus
    # Client_ID = ['AKIAYJJKAJNDIWLPGA5N']
    # Client_Secret = ['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']

    #     661044823565
    # Client_ID = ['AKIAZT2KXQYGUIRSCWHL']
    # Client_Secret = ['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']

    #     661044823565
    # Client_ID = ['AKIAWKR37JZ4QVJ3SRNJ']
    # Client_Secret = ['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']

    #     129084737846-Impetus-SanjaySharma
    # Client_ID = ['AKIAR4DQMZE3LUAOYNLF']
    # Client_Secret = ['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']

    profile_name = ['dheeraj']
    Client_ID = ['AKIA2S6ZYCT746FPNIXE']
    Client_Secret = ['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']

    client = aws_client(iam_role_to_assume='arn:aws:iam::727916745983:role/iamread', aws_access_key_id=Client_ID[0],
                        aws_secret_access_key=Client_Secret[0])

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)

    # client = aws_client(profile_name=profile_name[0])
    # client = aws_client(profile_name=profile_name[0])

    # regions = client.get_regions()
    # cloudtrails = client.get_cloudtrails(regions)
    # credsreport = client.get_cred_report()
    # password_policy = client.get_account_password_policy()

    data = client.get_compliance()

    kleradict = {}
    for compliance_data in data:
        kleradict.setdefault('ScoredControl', []).append(compliance_data['ScoredControl'])
        kleradict.setdefault('Result', []).append(compliance_data['Result'])
        kleradict.setdefault('failReason', []).append(compliance_data['failReason'])
        kleradict.setdefault('Offenders', []).append(str(compliance_data['Offenders']))
        kleradict.setdefault('ControlId', []).append(compliance_data['ControlId'])
        kleradict.setdefault('Description', []).append(compliance_data['Description'])

    # print(data['Offenders'])

    outdict = {'Compliance': pd.DataFrame(data=kleradict)}

    klera_dst = [outdict]
    print(klera_dst)
