"""Original Idea File. I need it for development!"""


import inspect

import g4f


print('Start initialisation g4f models')

providers = [cls_obj for _, cls_obj in inspect.getmembers(g4f.Provider) if inspect.ismodule(cls_obj)]

print(f'Detected {len(providers)} providers')
print('Start testing providers')


work_providers = []
for provider in providers:
    try:
        response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, provider=provider, messages=[
                                     {"role": "user", "content": "Hello world"}], stream=True)
        for i in response:
            if not i:
                print('Null')
                raise
        if 'is not working' in response:
            print('Not working')
            raise
        work_providers.append(provider)
    except:  # pylint: disable=bare-except
        print('error')

print(f'End! Find {len(work_providers)}!')
[print(i.__name__) for i in work_providers]  # pylint: disable=expression-not-assigned

print('=' * 100)


use_poviders = []
for prov in work_providers:
    response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, provider=prov, messages=[
                            {"role": "user", "content": "Hello world"}], stream=True)
    res = ''
    for i in response:
        res.join(i)
    if '"error"' not in res:
        use_poviders.append(prov)

for prov in use_poviders:
    response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, provider=prov, messages=[
                            {"role": "user", "content": "Hello world"}])
    print(response)
# response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, provider=g4f.Provider.Bing, messages=[
#                                      {"role": "user", "content": "Hello world"}], stream=True)

# for message in response:
#     print(message)



# print(inspect.getmembers(g4f.Provider))
