import importlib.util
import json
import pickle
import functools
import os
import re
import platform
import subprocess
import sys
import configparser
from typing import List, Any

### Helpful python functions

def read_config( path ):

    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_int_input( lower: int, upper: int, prompt: str = 'Enter an number: ', exceptions: List[str] = [], show_range: bool = True ) -> str:

    """prompts the user to input an integer between two bounds, gives the option to break if answer is found in the list of exceptions """

    if show_range:
        prompt += ' ({lower}-{upper}): '.format(lower=lower, upper=upper)

    while True:
        ans = input(prompt)

        try:
            ans = int(ans)
        except:
            if ans in exceptions:
                return ans

            print ('Enter an integer')
            continue

        if ans < lower or ans > upper:
            print ('Enter a number between {lower}-{upper}'.format(lower=lower, upper=upper))
            continue

        return ans

def smart_format( string: str, formatting_dict: dict, trigger_beg: str = '{{', trigger_end: str = '}}' ) -> str:

    """Formatting strings that have curly braces in them is hard, this makes it easy"""

    for key in formatting_dict:
        value = formatting_dict[ key ]

        to_replace = trigger_beg + key + trigger_end # {{first_name}}
        string = string.replace( to_replace, value )

    return string

def find_string_formatting( string: str, trigger_beg: str = '{{', trigger_end: str = '}}' ) -> List[str]:

    """Looks for string formatted with certain triggers
    Returns list of all string occurences where the triggers surround a string """

    return re.findall( r'\{trigger_beg}.*?\{trigger_end}'.format( trigger_beg=trigger_beg, trigger_end=trigger_end ), string )

def strip_trigger( string: str, trigger_beg: str = '{{', trigger_end: str = '}}' ) -> str:

    a = len(trigger_beg)
    b = -1*len(trigger_end)

    assert string[ : a ] == trigger_beg
    assert string[ b : ] == trigger_end
    
    return string[ a:b ]

def format( string: str, formatting_dict: dict={}, trigger_beg: str = '{{', trigger_end: str = '}}', **formatting_kwargs ) -> str:

    """Given a string with variables hidden inside triggers, replace these variables with values defined in `formatted_dict` or `formatting_kwargs`
    Similar to Python's builtin str.format( **kwargs ), with the ability to define your own triggers
    """

    d = { **formatting_dict, **formatting_kwargs } #kwargs take preference

    for key in d: #{ 'first_name': 'Joe' }  
        to_replace = trigger_beg + key + trigger_end # '{{first_name}}'
        string = string.replace( to_replace, d[key] ) # '{{first_name}}' -> 'Joe
    return string

def find_format_triggers( string: str, trigger_beg: str = '{{', trigger_end: str = '}}', include_triggers:bool=True ) -> List[str]:

    """
    Given string="Hello, this is {{first_name}} {{last_name}}" returns
    ["{{first_name}}", "{{last_name}}"] when include_triggers=True
    ["first_name", "last_name"] when include_triggers=False
    """

    capture_key = '.*?'
    if not include_triggers:
        capture_key = '(' + capture_key + ')'

    return re.findall( r'{trigger_beg}{capture_key}{trigger_end}'.format( trigger_beg=re.escape(trigger_beg), 
                                                                          capture_key=capture_key,
                                                                          trigger_end=re.escape(trigger_end) 
                                                                        ), string )

def command_line( string: str, print_off: bool = False ) -> None:

    """inputs the given string to the terminal"""

    if print_off:
        print_command_line( string )

    subprocess.run( string.split() )

def print_command_line( string: str ) -> None:

    print ('>>> ' + string)

def set_env_var( var: str, value: str ) -> None:

    """sets an environment variable with a given value"""

    if platform.system() == 'Windows':
        command_line( 'setx {var} {value}'.format( var = var, value = value ) )
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        command_line( 'export {var}={value}'.format( var = var, value = value ) )

def open_url( url: str, new = 2, **webbrowser_get_kwargs ) -> Any:

    """opens up the URL in a browser"""

    import webbrowser

    try:
        return webbrowser.get( **webbrowser_get_kwargs ).open( url, new=new )
    except:
        print('Could not open webbrowser')
        return None

def merge_dicts( *dicts: dict, ascending: bool = True ) -> dict:

    """Given N-number of dictionaries (with ascending priority), merge all together to one"""

    d = {}
    if ascending:
        inds = list(range( len(dicts) ))
    else:
        inds = list(range( len(dicts)-1, -1, -1 ))

    for ind in inds:
        d = { **d, **dicts[ind] }

    return d

def print_for_loop( iterable ) -> None:
    
    """prints a list in numercal list format"""

    for i in range(len( iterable )):
        print( str(i+1) + '. ' + str(iterable[i]))

def import_from_pickle( file_path: str ) -> Any:

    """Given a file_path to a pickle object, return the loaded Object"""

    f = open(file_path, 'rb')
    Obj = pickle.load( f )
    f.close()
    return Obj

def export_to_pickle( Obj: Any, file_path: str ) -> None:   

    """Export the Object to a file_path with pickle library"""

    f = open(file_path, 'wb')
    pickle.dump( Obj, f )
    f.close()

def json_to_object( string: str, object_hook ):

    """Given a json string, turn it into an object"""

    return json.loads( string, object_hook=object_hook)

def import_module_from_path(f: os.PathLike, module_name: str = 'new_module'):

    """Given a path to a python module, load and return the module"""

    spec = importlib.util.spec_from_file_location( module_name, f )
    module = importlib.util.module_from_spec( spec )
    spec.loader.exec_module( module )
    return module

def find_kwargs_in_strings( strings: List[str] ):

    args = []
    kwargs = {}

    for string in strings:
        vals = string.split('=')

        if len(vals) == 1:
            args.append(vals[0])
        if len(vals) > 1:
            key = '='.join(vals[:-1])
            value = vals[-1]
            kwargs[key] = value
    
    return args, kwargs

def get_selection_from_iterable( iterable, prompt: str = 'Select one', print_off: bool = True, allow_null: bool = False ) -> Any:

    """Returns the Object from iterable that the user selected"""

    if len(iterable) > 0:
        if len(iterable) == 1:
            return iterable[0]
        else:
            if print_off:
                print_for_loop( [ str(i) for i in iterable ] )

            if allow_null:
                ind = get_int_input( 1, len(iterable), prompt=prompt, exceptions=[''] ) 
                if ind == '':
                    return None
            else:
                ind = get_int_input( 1, len(iterable), prompt=prompt ) 

            return iterable[ ind-1 ]
    else:
        return None

def get_selections_from_iterable( iterable, 
                                    prompt: str = '', 
                                    exceptions: List[str] = [], 
                                    allow_all: bool = True, 
                                    print_off: bool = True 
                                ) -> List[int]:

    """Returns a list of indices pertaining to what the user selected from a list of options"""
    if print_off:
        print_for_loop( iterable )

    exceptions.append( '' ) # for breaking out of the loop

    if prompt == '':
        prompt = 'Make your selection - enter to exit'
        if allow_all:
            prompt += ', type "all" to select all'
            exceptions.append('all')

    inds = []
    while True:
        index = get_int_input( 1, len(iterable), prompt = prompt, exceptions = exceptions, show_range=True )

        if index == '':
            break
        elif index == 'all':
            inds = list(range(len(iterable)))
            print ('all items added to the queue')
            continue
        else: # index is a regular number
            index = index - 1

        if index not in inds:
            print ( str(iterable[index]) + ' added to the queue')
            inds.append( index )
        else:
            inds.remove( index )
            print ( str(iterable[index]) + ' removed from the queue')

    return [ iterable[ind] for ind in inds ]

def get_system_input_arguments():

    """parse system inputs, send back args and kwargs"""

    system_inputs = sys.argv[1:]

    on_args = True

    args = []
    kwargs = {}

    for arg in system_inputs:
        if '=' in arg:
            on_args = False #on_kwargs

        if on_args:
            args.append( arg )
        else:
            att, value = arg.split( '=' ) 
            value = get_special_string( value )
            kwargs[att] = value

    return args, kwargs

def get_special_string( string ):

    mapping = {
        "True": True,
        "False": False
    }

    if string in mapping:
        return mapping[string]
    return string


def confirm_raw( string: str = ''  ) -> bool:

    """Returns a boolean stating whether 'yes' was entered in response to the prompt"""

    string_to_print = string + ' Enter "yes" to continue: '
    if input(string_to_print) == 'yes':
        return True
    return False

def confirm_wrap(string, *dec_args, **dec_kwargs):

    """given a string, returns a decorator """

    def confirm_decorator(func):

        @functools.wraps(func)
        def wrapper(*called_args, **called_kwargs):

            if confirm_raw( string = string ):
                return func( *called_args, **called_kwargs )
            return None

        return wrapper

    return confirm_decorator


def try_operation_wrap( *dec_args, debug = False, **dec_kwargs):

    """can pass in debug True or False"""

    def try_operation_decorator( func ):

        """Any function decorated with this will return a boolean successful attempt"""

        @functools.wraps(func)
        def wrapper( *called_args, **called_kwargs ):

            if debug:

                _ = func( *called_args, **called_kwargs )

            if not debug:
               
                try:
                    _ = func( *called_args, **called_kwargs )
                except:
                    return False
    
            return True

        return wrapper

    return try_operation_decorator


