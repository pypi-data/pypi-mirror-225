# Usefulgram

### Installation:
`pip install usefulgram`

### A little history:
angiogram is a wonderful framework. However, when working with it, 
I came across the fact that I transfer many functions and 
classes from project to project. First, common classes were created 
for convenient transportation, then it grew
into a shared folder, and now into a separate project. I hope that this
small add-in will become a useful tool not only for me, but also for you

### What it includes:
- LazyEditor - this is a class aimed at handling any editing-related 
errors. For example, the expiration of time, as well as much, much more. 
Also, it unifies work with media (currently only photo and video are supported)
- LazySender - A class that unifies sending for callback and message types. 
Partially similar in functionality to LazyEditing
- Builder, Row, Button and its Reply analogs - classes for representing the keyboard
in a array-like form
- BasePydanticFilter - Base class, a somewhat developed version
the Callback Factory capable of type hints, supporting inheritance, 
date time and pedantic classes within itself. It is indispensable 
when used together with a plugin for pydantic hints in your IDE
- TrottlingMiddleware - A class that allows you to prevent spam. 
A slightly modified version of 
[this code](https://github.com/wakaree/simple_echo_bot/blob/main/middlewares/throttling.py)
- StackerMiddleware - The class that adds all these classes to handlers
- calendar_menager - A simple calendar menu built on library functions
- And much more!

#### Usage examples:
Along the path 
[**examples -> fully_example**](https://github.com/Sethis/usefulgram/tree/master/examples) 
you will find most of the examples 
of using the library. Over time, they will get bigger

#### Documentation: 
_In development and will be available soon_

### Roadmap:
- Improve the code ✔️
- Add more usage examples ✔️(~75% done)
- Translate all texts in the library into English ✔️(it can be painful in some places)
- Add documentation 🔨🔨🔨 (in progress)
- Add more comments to the code 🔨🔨🔨 (in progress)