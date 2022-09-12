import ansible_runner
r = ansible_runner.run(private_data_dir='/home/agrishin/python/ans_py', playbook='test.yml')
print(r.stdout)
for evnt in r.events:
    try:
        print(evnt['event_data']['res']['result']['rendered'])
    except KeyError as e:
        continue
