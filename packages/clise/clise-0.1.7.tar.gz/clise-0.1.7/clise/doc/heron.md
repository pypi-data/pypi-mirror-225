### CLISe: Command Line Input Setter

Command liner for python routines using JSON based input parameter files. It
dives into a module with CLI and execute a routine just as herons dive into
water and catch fish. It also uses JSON text to create task lists to automatize
multiple executions of the routine: ver 0.1.7 by Jaesub Hong
(jhong@cfa.harvard.edu)

       Usage: clise JSON_input_file1 -options_for_file1 ... \
            [json_input_file2 -options_for_file2 ...] \
            [--with common_json_files -common_options ...] \
            [--WITH common_json_files -common_options ...]

       clise --help [keys]
       clise [json_files ...] --Help 
       clise --main module.routine --Help 

### Table of Contents
- [Quick overview of the basic concept](#quick-overview-of-the-basic-concept)
- [Installation and startup](#installation-and-startup)
- [Features and limitation](#features-and-limitation)
- [Parameter Setting with JSON files](#parameter-setting-with-json-files)
- [Parameter Setting in CLI](#parameter-setting-in-cli)
- [Sequential and Iterative calling](#sequential-and-iterative-calling)
- [Sequential calling in CLI](#sequential-calling-in-cli)
- [Parameter list](#parameter-list)
- [Logging](#logging)
- [More](#more-to-explain)
- [Changes](#changes)

### Quick overview of the basic concept

There are many command line interface tools for python (e.g., pyCLI, clize,
etc.). They usually provide decorators and other useful functions to deal with
arguments. They also provide routines to generate the executable scripts for
the user routines. While these are great for developing a large code or
project, it can be a bit redundant for a quick test of a routine in a code you
don't have access to modify. In the latter, you may have to write your own
wrapper to bypass that. CLISe takes a different approach, perhaps suitable for
small or moderate size projects.

CLISe enables executions of any routine as a command script only with command
line options and input files (in an extended JSON format). CLISe dynamically
make a decorator for the called routine, handling the input and output
parameters of the routine, so the user doesn't need to modify the original
routine. One of the input parameters required for CLISe is the routine and
module names. So when the input parameter is stored in a file (recommended),
the user doesn't need to remember the routine name in future runs. For more
complex operations, CLISe allows sequential calls of multiple routines, and
provide a simple mechanics to generate multiple calls of multiple routines.

The main objective of CLISe is an efficient separation and maintenance of
essential input parameters of a task or tasks from the programming part for the
task(s). While CLISe enables a few simple variables and math operations in
setting input parameters for convenience, their features are (subjectively)
limited to leave out the programming part: i.e., "rabbit.py" provides the
routines that enables the auto task repetition with variations in input
parameters, but it doesn't provide, for instance, a range-based for-loop
functionality, which belongs to the programming.

The input parameter files contain the name of the routine to call: e.g.,
"-main": "module.routine".  Assume that a python script example.py has

      def my_sum(name, x, y):
           """ This is my sum. """
           print(name+':', x+y)

Then with a JSON file input.json,

      "-main": "example.my_sum",
          "x": 5,
          "y": 7,
       "name": "answer",

One can execute the routine 'my_sum' in a shell command prompt like

      % clise input.json
      answer: 12

Keys starting with alphabets (x, y, and name in the above example) are assumed
to be fed into the main routine set by "-main" key.  In principle, all the
contents in the JSON files can be fed as a long string in the command line or
as optional parameters for individual keys with "-". So the above example is
equivalent to the followings even without the JSON file input.json.

      %  clise --main example.my_sum -#x 5 -#y 7 -name "answer"
      %  clise '{"-main":"example.my_sum","x":5,"y":7,"name":"answer"}'

or some combination of all three examples:

      %  clise '{"-main":"example.my_sum","name":"answer"}' -#x 5 -#y 7
      %  clise input.json '{"name":"answer"}' -#x 15 -#y 27

When both JSON files and command line input options are available for the same
key, the command line options take a priority.  In the last example,
'input.json' has x of 5, which is replaced by the command line option x=15.
Note # in -#x ensures it is a number but not a string.  See more details with
'clise --help cli'. Note --Help (capital H) prints out the doc string of
the routine.

      % clise input.json --Help
      This is my sum.

Calling multiple JSON files execute them in sequence.

      % clise input.json input.json
      answer: 12
      answer: 12

      % clise input.json -#x 7 input.json -#x 6
      answer: 14
      answer: 13

As you may have guessed it by now, in the command line, "--" is reserved for
options for clise itself, and "-" is reserved for options and keys of the
user routine. In JSON files, the parameters lose one "-", so "-var" are 
for the clise, and "var" without "-" is for the user routine.

Find out what kind of parameters are needed to call the routine using --show
func option.

      % clise --main os.path.isfile --show func
       main: os.path.isfile
       path

The above example shows isfile expect a parameter called path.

      % clise --main os.path.isfile -path clise.py --show output
      True

Can check how the parameters get fed to the routine.

      % clise --main os.path.isfile -path clise.py --show feed
       main: os.path.isfile
       path << str .py

      % clise input.json --show feed
       main: example.my_sum
       name << str answer
          x << int 5
          y << int 7

Can call a routine needing no input parameters.

      % clise --main datetime.datetime.now --show output
      2022-04-27 22:11:52.983532

One can force the parameters to a function with --pars option.

      % clise --main math.sin --pars x --show output -#x 1.0
      0.8414709848078965

In the case of the built-in functions: e.g.,

      % clise --main eval --pars x --show output -x 3+3
      6

      % clise --main pow -*-pars x,y --show output -#x 1.5 -#y 3
      3.375

      % clise --main eval --pars x --show output -x 'pow(1.5,3)'
      3.375

### Installation and startup

Install the  package using pip,

      % pip install 

then assign an alias for easy use: e.g., in bash,

      % alias ="python -m clise"

Alternatively, this program can be used without installation: simply
place clise.py in the python path and use

      % alias ="python clise.py"

For a common parameter configuration, assign an environmental variable
CLISE_STARTUP to a JSON file with the common parameters: e.g.,
in bash,

      % export CLISE_STARTUP="~/my_startup.json"

The parameters in this file will be loaded as well.

By default,  will attempt to pass parameters starting only with alphabets
to the routine in call, but one can accept the full parameter sets
(including -main) by adding an optional parameter named _heron_ in your function:

      def my_routine(..., _heron_, ...):
            ...

One can change the name of the parameter to something else by "-roundup".
(i.e., by default, "-roundup": "_heron_").

then, all the input parameters (both from JSON files and CLI) will be passed to
this parameter as collections.OrderedDict. This may be useful for debugging.

One can also use  inside python or ipython for a single task: e.g.,

      >>> from clise import heron, rabbit, jsontool
      >>> cfg = jsontool.load_cli('command line input string')
      >>> out = heron.go(*cfg)

### Features and limitation

There are many excellent packages that handle input parameters of
routines and link them to matching command line tools. The main purpose
of this program is, though, to facilitate a command line call of an arbitrary
python routine without additional wrapper script for the routine. At
the same time, for some tasks, the input parameters themselves are part
of the important data to keep and track.  CLISe encourages the use
of an input file in JSON format for input parameters, so that the input
parameters are available for later review, modification and rerun.  Since
the input parameters contain the name of the main routine to call (i.e.,
poor man's objective oriented programming), there is no need for
additional wrapper script.  For simple routines that don't really need
the input parameter files, a simple alias can be used for easy repetitive
call instead of a wrapper script (try --help startup). Some of
the main features are:

- Calling a python routine from a command line without any wrappers
- Enable somewhat a clean separation between the routine (program) and
  the input parameters (data).
- Support iterative routine calling with minimal parameter setting
- Support calling multiple routines sequentially
- Provide flexible command line options for easy on-the-fly modification
  of parameter changes
- Support automatic logging of the input parameters and run condition
  through hashing
- Support rudimentary extension of JSON format including commenting,
  simple math, and variable substitution.
- Provide recursive file search function with basic regex for the cases
  that the same routine has to deal with lots of similar-type but
  different files.
- Provide the check of the mod time of files to process and enable an
  easy option to what to process and what not to process.
- Allow an option to pass the complete set of the input parameters for
  routines that are written specifically for 
- When the called routine returns another routine, the new routine is
  also called.

In regarding the data type of input parameters,  provides a few tools
to ensure proper types, but not as strict as some of other tools. The motto is
"quickish and dirtish" is good enough, although we don't want to go as far as
"quick and dirty.

The current limitations of the program are:
- Type checking of the parameters: since CLISe doesn't impose any changes in
  the original functions, it doesn't provide a solid way to type check input
  parameters. However, one can use '--enforce_format' to set the type
  explicitly. In addition, '#', '##','\*','\*#', and '\*\*' can be used to
  specify the data type in the command line and JSON files: e.g., in a command
  line, '-x 1' means "x" is a string of "1", while '-#x 1' means "x" is an
  integer of 1.

- Routines of a class: this should work in principle and it does under a
  limited circumstances. For instance, the 2nd-to-last item of the -main
  parameter can be a class name. If so, the class will be initialized.
  e.g., with "-main": "plottool.plottool.collect_data",  will
  initialize the class "plottool" of the module "plottool" with an object
  and call the function "collect_data" under the same object.  If
  a following routine is "plottool.plottool.mplot1d", then CLISe will call the
  function "mplot1d" under the same object of the class. In this way, one
  can pass parameters among multiple functions through the class
  definition, requiring no additional parameter settings in the JSON input file.

- Routines with decorators or processed by function manipulators often end up
  with unclear arguments and keyword arguments when called from the outside,
  sometimes split over the original routine and decorators/manipulators.  In
  this case, the user has to manually make sure what parameters are fed (in
  what order for non-keyword parameters). Use -collect and -discard to
  efficiently facilitate this. The -collect parameter is set True by default
  for routines with *par, **kwpars since their full parameter sets are unknown.

### Parameter Setting with JSON files

In, the JSON format is used for input parameter files. There may be other
more popular or capable formats, but JSON seems to be one of the most compatible
formats with the python dictionary, which is versatile and easy to handle, even
though it tends to be a bit verbose.

Unlike the standard JSON, commenting is allowed in  with the c-style
notation of //. The outermost "{" and "}" can be omitted to simulate a more
configuration-file like feel. String-only variables are allowed for tagging &
replacing by calling the "key" in the "{key}" format: e.g.,

      "key1": "Abcdef", "key2": "{key1} & more" is equivalent to
      "key1": "Abcdef", "key2": "Abcdef & more"

Enclosures "{>" and "}" allow a similar subsititution, but the substitution
occurs after all other variables are substituted.

      "k1": "Abcd", "k2": "{k1}!", "k3": "{k2}?" is equivalent to
      "k1": "Abcd", "k2": "Abcd!", "k3": "{k1}!?"

      "k1": "Abcd", "k2": "{k1}!", "k3": "{>k2}?" is equivalent to
      "k1": "Abcd", "k2": "Abcd!", "k3": "Abcd!?"

For non-string variables, use {= and }: e.g.,

      "key1": [1.5, 20], "key2": "{=key1}"  is equivalent to
      "key1": [1.5, 20], "key2": [1.5, 20]

Basic math expressions can be achieved using "#" or "##".

      "#key" : "3+4*5"  changes to "key": 23
      "#key" : "3+4*5." changes to "key": 23.0
      "##key": "3+4*5"  changes to "key": 23.0

List and dict (OrderedDict) can be set from string.

      "*key"  : "3,a,4.0"  changes to "key": ["3","a"]
      "*#key" : "3,a,4.0"  changes to "key": [3,"a", 4.0]
      "*##key": "3,a,4.0"  changes to "key": [3.0,"a", 4.0]
      "**key" : "'a':1,'b':'x'"  changes to "key": { "a":1, "b":"x" },

These options are handy in CLI.

      "*#key" : "3,a,4.0"  equivalent to -*#key 3,a,4.0 in CLI

Trailing commas are allowed: e.g.,

      "key": [1,2,3,] is the same as "key": [1,2,3].

The built-in keys like infile can be used with wild cards, which automatically
generate a matching file list and successively call the main routine with each
file.  {1}, {2}, ... {key:1}, {key:2}, ... are reserved for tagging and
replacing by regex in infile and other parameters for iterations: e.g.,

      "infile": "(.*)([0-9]+).txt", "outfile": "{1}__{2}.txt"

If the infile parameter encounters files named hello3000.txt, hiThere2000.txt
..., the main routine will be iteratively called with

      "infile": "hello3000.txt",   "outfile": "hello__3000.txt"
      "infile": "hiThere2000.txt", "outfile": "hiThere__2000.txt"
     ...

These features are desirable for convenience, but semi-intentionally limited in
order to keep JSON file mainly for input parameters without over-stepping into
the programming side.  Given the rather relaxed rules for JSON in ,
recommend avoiding multi-line parameters, which can conflict with commenting and
others. Nested variables (dictionary or hash) are ok to use.

Parameters with ==, ~=, !=, ~!= in their keys can be used for a pattern matching to
make exceptions through built-in  functions like combine_tags: e.g.,

      e.g., "infile~=.txt$" : { "x-value": 90, ... }.

What this can do is that when the parameter infile meet files ending with
".txt", x-value is set to 90, superceding other possible settings for x-value.

### Parameter Setting in CLI

All the parameters can be used either in a JSON file or as a command line
option: e.g., {"infile":"filename"} in the JSON file is equivalent to
-infile filename in the command line.  The full content in JSON
can be used in the command line through JSON syntax albeit complex: e.g.,
'{"key":value,... }'.

There is no automatic type checking, but a few options to enforce numeric or
list are available.  See below.  When there are multiple instances of a same
key, the last assignment is used except when it is given after --with
parameter: the command line option of the same parameter is used over the same
of the JSON file.

- Keys without any value mean a boolean variable: e.g.,

        -key in command line is equivalent to {"key": true} in JSON
       -^key is equivalent to { "key": false}
      --^key is equivalent to {"-key": false}
      -^-key is equivalent to {"-key": false}

- Keys starting with # and ## will be enforced
  as numbers and floats, respectively: e.g.,

        -key 1   is equivalent to {"key": "1"}
       -#key 1   is equivalent to {"key": 1}
       -#key 1.0 is equivalent to {"key": 1.0}
      -##key 1   is equivalent to {"key": 1.0}

  Use "-enforce_format" key in JSON files which enables formatting without
  prefix: e.g., in a JSON file,

      "-enforce_format" : {
              "x" : "float",
              "y" : "complex",
              ...
            }

  Then, the command line option -x 1 will keep x as a float instead of str.

- Keys starting with * will be treated as list: e.g.,

         -key 5,Ab,6.1 is equivalent to {"key": "5,Ab,6.1"}
        -*key 5,Ab,6.1 is equivalent to {"key": ["5","Ab","6.1"]}
       -*#key 5,Ab,6.1 is equivalent to {"key": [5,"Ab",6.1]}
      -*##key 5,Ab,6.1 is equivalent to {"key": [5.0,"Ab",6.1]}

- Keys starting with : will be treated as a nested dict: e.g.,

      -key1:key2 abc is equivalent to {"key1": {"key2":"abc"}}

      See demo*.json5 files in example/ directory, which use a few simple
      routines in demo.py.

Several handy command line options are:

      --Help  bool false    display the doc text of the user routine

      --help  bool false    display the main section of the help string
              str  keys     list options of the help contents (from heron.md)
                   all      display all the help text

      --show  bool false    show information about the parameters and jobs
              str         * indicates exit without calling the routine
                   hidden * show also the hidden variables
                   func   * expected function's parameter
                   input  * parameters prepared
                   feed   * how the parameters are fed to the function
                   output   output of the function
                   job      job progress
                   time     run time for each job
                   files    input and output file status
             e.g., --show          shows the basic input parameters and exit
                   --show job,time shows both the job prgress and run time

      --raw   bool false show the input parameters in the standard JSON format
      --with  list None  JSON input files used with all other JSON input files.
      --WITH  list None  Same as --with but supercede the setting earlier, while
                         settings by --with will be superceded by other settings
      --parse bool true  parse *.json files instead of treating them as
                              parameter values.

### Sequential and Iterative calling 

A single input JSON file can set up multiple calls to a routine or a set of
routines. The package includes "demo.py" and JSON files in examples to
illustrate this feature. In "demo_by_file.json5",

      "-main" : "demo.check_file",
      "infile" : "cmd.sh",
      "outfile": "test.sh",

This example can be called

      % clise demo_by_file.json5
      cmd.sh               >> test.sh              is ok.

or the routine "check_file" in "demo.py" can be directly called.

      % clise --main demo.check_file -infile cmd.sh -outfile test.sh
      cmd.sh               >> test.sh              is ok.

One can set up multiple calls as shown in "demo_by_files.json5", which has:

      {
            "-main" : "demo.check_file",
            "infile" : "cmd.sh",
            "outfile": "test.sh",
            "-return" : "a,b",
      },
      {
            "-main" : "demo.check_file",
            "infile" : "cmd.sh",
            "outfile": "cmd.sh",
            "-return" : "a,b",
      },
      {
            "-main" : "demo.show",
            "-inherit" : {
                  "x": "a",
                  "y": "b",
                  "-list": ["a","b"],
            },
      },

Each task (routine) is in a block with enclosing brackets {}.
The "-return" and "-inherit" parameters are used to pass output of routines
to the input of other routine.
      
      % clise demo_by_files.json5
      cmd.sh               >> test.sh              is ok.
      cmd.sh               >> cmd.sh               is ok.
      receiving
            x list ['cmd.sh', 'cmd.sh']
            y list ['test.sh', 'cmd.sh']

In this case, the infile and outfile parameters of the routines are set manually.
A block containing the "-main" parameter is considered as a separate task to be executed.
A block without the "-main" parameter can be used to set common input parameters form
multiple blocks or a designated set of blocks with the "-apply to ..." parameter. 
For instance, 

      {
            "infile": "hello.sh",
            ...
            "-apply to -main": "demo.check_file",
      }

The "infile" parameter here will be assigned to any blocks with "-main" :
"demo.check_file",  However, the designated block has the same parameter, then
this global assignment will be replaced by it. The "-apply to ..." parameter is a 
group of parameters, which can set to any other parameters. For instance, to designate 
a routine or task, one can do something like

      {
            "infile": "hello.sh",
            "-apply to -id": "this only",
      },
      ...
      {
            "-id" :"this only",
            ...
      },
      ...

where the common parameter block will be applied to the block with the "-id"
parameter of "this only".  The "-apply to ..." parameter can be used with matching
types like

      "-apply to -id" : "this"		equiv. to ">> -id"    : "this"
							equiv. to ">> -id ==" : "this"
      "-apply to -id except"  : "this"	equiv. to ">> -id !=" : "this"
      "-apply to -id contains": "this"	equiv. to ">> -id ~=" : "this"
      "-apply to -id without" : "this"	equiv. to ">> -id ~!=": "this"

One can skip a task all together by using the "-skip ..." parameter in the
common block.

      "-skip -id" : "this"		equiv. to "<< -id"    : "this"
						equiv. to "<< -id ==" : "this"
      "-skip -id except"  : "this"	equiv. to "<< -id !=" : "this"
	...

These parameters can be set in CLI in principle, albeit complex: e.g.,

       -"-apply to -id" this 
       -">> -id" this 

One can use regular expression (regex) to pick multiple files matching the
description and set multiple tasks.

      % clise --main demo.check_file -infile '(.*).(py)' -outfile '{1}_{2}.sh'
      (.*).(py)            >> {1}_{2}.sh               is ok.

In this example, clise feeds the string '(.*).py' to the "infile" parameter
of the routine "check_file" as it is (the same for "outfile"). Now with "--loop"
parameter, this turns into multiple runs.

      % clise --main demo.check_file -infile '(.*).(py)' -outfile '{1}_{2}.txt' \
            --loop:*appkeys outfile
      demo.py              >> demo_py.txt          is ok.
      __main__.py          >> __main___py.txt      is ok.
      jsontool.py          >> jsontool_py.txt      is ok.
      heron.py             >> heron_py.txt         is ok.
      __init__.py          >> __init___py.txt      is ok.
      rabbit.py            >> rabbit_py.txt        is ok.
      cmdscript.py         >> cmdscript_py.txt     is ok.
      plottool.py          >> plottool_py.txt      is ok.

The optional parameter "--loop" (dict) indicates the "infile" parameter to be
interpreted as a regex, and match the expressions in the file names of the
directory, and calls the routine multiple times for each matching file. The
"appkeys" parameter indicates the {1}, {2}, ... in the "outfile" parameter to
inherit the matching regex from the "infile" parameter, which in this case is
"(.*)". The same thing can be achieved using a JSON file containing

      "-main" : "demo.check_file",
      "infile" : "(.*).(py)",
      "outfile": "{1}_{2}.txt",
      "-loop"  : {
            "appkeys":  ["outfile"],
      },

Having both "-main" and "-loop" command, in fact, triggers a call to the
routine "multiply_by_file" in "rabbit.py" as a default routine generator, which 
generates a series of tasks matching the "infile" parameter, and then execute
one by one. This is equivalent to 

      "-main" : "demo.check_file",
      "infile" : "(.*).(py)",
      "outfile": "{1}_{2}.sh",
      "-loop"  : {
            "-main"  :  "rabbit.multiply_by_file",
            "appkeys":  ["outfile"],
      },

The user can use their own generator routine and specify in the "-main" of
the "-loop" dictionary parameter. If the user's own generator is not given, then
"rabbit.multiply_by_file" is called by default. There are 4 routines for task generators
are given in "rabbit.py". 

      multiply_by_id          : obsolete, to provide backward compatibility to cjpy
      multiply_by_id_multi    : obsolete, to provide backward compatibility to cjpy
      multiply_by_file        : generator for a single routine
      multiply_by_file_multi  : generator for multiple routines

The "multiply_by_id(_multi)" routines are obsolete in clise since one can simply
set multiple tasks with individual routine blocks and common blocks. They are there
to allow recycle of the old cjpy JSON files.

The "multiply_by_file(_multi)" enables the filename based multiple runs. For
example, in order to call a set of routines for many files, use
"multiply_by_file_multi". In this case, given the complexity of the parameter
settings to multiple files, setting this up as a CLI would be challenging, so
using a JSON file is recommended. The routines like "multiply_by_id(_multi" is
now obsolete since one can set up a set of routines sequentially in a JSON file
using the enclosure {}.

One can set some variations of the parameters using matching options like

      "infile==..." : { ... },
      "infile!=..." : { ... },
      "infile~=..." : { ... },
      "infile~!=...": { ... },

The "-infile.key==#" is reserved for setting options for selected infile
parameter, useful when the same file is used more than once. # indicates the
index of the "infile" parameter.

      "infile" : ["(.*).py","(.*).py","(.*).sh"],
          ...
            "-infile.key==0" : { "x":1, "y":2 },
            "-infile.key==1" : { "x":2, "y":3 },
            "-infile.key==2" : { "x":3, "y":0 },

The files named "*.py" will have two runs each: first with input
parameters being x=1 & y=2 and the 2nd run with x=2 & y=3.
The files named "*.sh" will have a single run with x=3 & y=0.
One can also mark a certain files with " >?", where ? is a non-numeric
character.

      "infile" : ["(.*).py","(.*).py >a","(.*).sh"],
          ...
            "-infile.key==0" : { "x":1, "y":2 },
            "-infile.key==a" : { "x":2, "y":3 },
            "-infile.key==2" : { "x":3, "y":0 },

In this example, the 2nd run with files named "*.py" is labeled "a",
whose parameters can be set with "-infile.key==a".

In principle, one can set up the above tasks of "demo.check_file" by simply calling
"multiply_by_file" without the "-loop" parameter. 

      "-main"  :  "rabbit.multiply_by_file",
      "appkeys":  ["outfile"],
      "seed"  : {
            "-main" : "demo.check_file",
            "infile" : "(.*).(py)",
            "outfile": "{1}_{2}.sh",
      },
      "-block"  : "rabbit",

The "multiply_by_file" routine generate a set of task based on the "seed"
dictionary input. The "-block" parameter being "rabbit" indicates that the output
of this routine is a set of tasks to be executed. Otherwise this will simply
return a set of tasks without their execution.

When multiple tasks need to be repeated with wild card file names, one can use 
"multiply_by_file_multi".

      {
            "-main" : "rabbit.multiply_by_file_multi", // one can call user's own routine 
            ...

            "-apply until -block" : "end of taskgen", 
            // this indicates this block is a task gen block
            // and which block is the end for the seed
      },
      {
            "-main" : "demo.check_file",
            "infile" : "(.*).(py)",
            "outfile": "{1}_{2}.sh",
      },
      {
            "-main" : "module2.routine2", // the 2nd routine to multiply
            ...
      },
      ....
      {
            "-main" : "moduleN.routineN", // the Nth routine to multiply
            ...
      },
      {
            // pars in a block without "-main" will be fed to all the routines above
            "common_par1" : "val1", 
            "common_par2" : "val2", 
            ...

            "-block" : "end of taskgen", // this indicates the ending block for task gen
      },

In this example, routines from "demo.check_file" to "moduleN.routineN" will be
repeated based on the "infile" parameter, and the common block will be also
used. Basically the blocks until "-block": "end of taskgen" will be fed as the
"seed" parameter to "multiply_by_file_multi", which will generate the matching tasks
and clise will execute them.

The "multiply_by_file(_multi)" also allows a few options parameters to filter
file selections such as "include", "exclude", "sortby", "after", "before", "larger",
"smaller". See the parameter list below for more.

To use user's own task generation routine, clise expects to feed the "seed"
parameter to the user routine as the main input providing all the necessary
information to generate the tasks. The user routine is expected to return a
list of OrderedDicts, each of which contains the full set of parameters
including the "-main" parameter for an execution.

### Sequential calling

Multiple jobs can be executed in sequence by simply listing them: e.g.,

      %  job1.json job2.json ...

By default, they get executed independently, so this is equivalent to

      %  job1.json
      %  job2.json
      ...

The output of the one job in the first example can be fed to the input
of the next job. This feature hasn't been tested extensively.

      %  job1.json -par "a" job2.json -par "b" ...

Note in this example, par is set to "a" for job1.json and "b"
for job2.json

      %  job1.json -par "a" -par "b"

In this example, par is simply set to be "b".

      %  job1.json job2.json --with job3.json

In this example, each job is first combined with job3.json and executed, which
is equivalent to:

      %  job1.json --load job3.json
      %  job2.json --load job3.json

### Parameter list:

For command line parameters, add the additional prefix -:i.e., "-main" in a JSON
file is equivalent to --main as a command line option.  Parameters starting with
alphabets can be potentially fed into the routine called.

For clise (heron.py)

      -main       str   None  the main module and routine to call
      -load       str*  None  load other JSON file: same as --with option in the
                              command line
      -loop       dict  None  routine for looping to define the task list
      -id         str   auto/manual   short term ID for the run
                              auto: routine name
                              manual: set by a user for loop. See multiiply_manual_by_id
      -nid        int   auto  number ID for the run
      -fid        str   auto  full ID for the run
      -block      str   None  indicates the routine being for task generation
                              ''                : regular routine, 
                              rabbit            : task generator
                              rabbit:release    : task generator, and the next block is the
                                                  starting point of the searched
                              rabbit:capture    : the last block for the seed

      -include    str   None  only choose input files with matching string: regex
      -exclude    str   None  do not choose input files with matching string: regex
      -after      str   None  run only for outfile (default) modified after this time
      -before     str   None  run only for outfile (default) modified before this time
      -clobber    bool  false overwrite the existing results

      -hisfile    str   none  copy of input JSON file and command line option,
                              automatically generated if set to be "_auto_".
      -logfile    str   none  log file
      -save_cli_ony_run bool  false save log for cmdline tools

      -roudnup    str   _heron_ input keyword name to pass all the parameters to a user function

      -global     str*  none  global variables
      -pars       str*  none  input parameters of the function called; must set
                              this for invisible non-keyword parameters: e.g.,
                              decorated functions
      -kwpars     str*  none  input keyword parameters of the function called;
                              set this for invisible keywords or simply set
                              -collect true
      -collect    bool  false set this true to feed all the unassigned
                              parameters starting with alphabets as keyword
                              paramters when the routine's keyword parameters
                              are not visible. Use --show feed to check how the
                              parameters are passed.
      -discard    str*  none  discard these parameters before calling the routine
      -nonify     str*  none  set these parameters None and feed to the routine

      -init       dict  none  define parameters needed to initialize the class
      -object     str   none  object name to define and reuse when multiple objects under the same
                              class name are required. Each class will load an object and the routines
                              under the same class share the object unless the object name is given under
                              the -object parameter.

      -return     list  None  name of outputs for a routine, which can be used
                              for the input for the later routines
                              e.g., "-return": ["x", "y"]
                              each variable will be OrderedDict with key being
                              the routine's "-id".

      -inherit    dict  None  pairs of receiving and input parameters for routines that
                              inherit outputs of earlier routines. The input parameters
                              can be an expression, evaluated by 'eval'.
                              e.g., "-inherit" : {
                                          "input1" : "x", 
                                          "input2": "x*y",
                                          "scalar": ["x","y"],
                                    }
                              This will grab the first element of output variables "x" and "y",
                              and feed the "x" value to "input1", and the "x*y" value to "input2".

      -enforce_numeric str #  a prefix to specify cmdline par being a number
                              instead of string; "" to disable it
      -enforce_floats  str ## a prefix to specify cmdline par being a float
                              instead of string; "" to disable it
      -enforce_format  dict   a full dict for data format enforcer, int,
                              float, complex, bool, str
      -expand_nested   str ,  a separator to indicate the nested key or
                              parameter; "" to disable it

      -dict_pre   str   **    a prefix to indicate a list in string variable; ""
                              to disable it
      -list_pre   str   *     a prefix to indicate a list in string variable; ""
                              to disable it
      -list_sep   str   ,     a separator to indicate a list in string variable;
                              "" to disable it
      -pop_modifier bool true remove the modifier keys like -enforce_numeric afterwards

      -onlyfor module.routine dict none settings that only apply to a
                              particular module.routine

      -apply to key (op)      assign parameters in a "-main"less block to other blocks,
                              use to define parameters common for multiple tasks.
                              "key" can be "-id", "-main", or others. Available operators arguments:

                              (None), except, contains, without

                              e.g., "apply to -id" : ["Task1", Task2"]

                              will apply the parameters in this block to blocks that have
                              the "-id" values of "Task1" or "Task2". A short form can be used

                              "-apply to key"          is equivalent to ">> key"  or ">> key =="
                              "-apply to key except"   is equivalent to ">> key !="
                              "-apply to key contains" is equivalent to ">> key ~="
                              "-apply to key without"  is equivalent to ">> key ~!="

                              "==" and "!=" operators can take either string or string list.
                              "~=" and "~!=" operators can take a regex string.

      -apply until -block     To indicate the end of the seed for task generator block.
                              The matching end block should have the same value for the "-block" key.

                              "-apply until -block"   is equivalent to ">> -block"
                              
      -skip key (op)          assign blocks to skip: the same mechanics as "-apply to ..."

                              "-skip -id"  is equivalent to "<< -id"

      -verbose    int  0      chatter level for clise (or heron.py)

      -accept
      -reject                 set the accept and reject list for CLI to a block
                              regex string list

In rabbit.py
      For multiply_by_id(_multi): obsolete under the new task management

      -id         str*        Setting "-id" to a string list will make the block into
                              task generator, calling "rabbit.multiply_by_id".
                              This routine can be called explicitly, and the
                              routine and its parameters can be fed as the
                              "seed" variable. This routine generate the repeat listing
                              for a single routine. The parameter change can be implemented
                              by conditional dict: e.g.,

                                    "-id" : ["first", "second"]
                                    "-id==first" : { "x":3, "y":4 },
                                    "-id==second": { "x":5, "y":6 },

                              "==","!=","~=","~!=" are available for conditioning.

                              To repeat the multiple routines in a set, use
                              rabbit.multiply_by_id_multi


      For multiiply_by_file(_multi):
                              To repeat the multiple routines in a set, use
                              rabbit.multiply_by_file_multi

      infile      str*  None  regex of input files, any regex should be in (),
                              which can be tagged as {1}, {2},...
      outfile     str   None  output file, one can use tags in input file

      indir       str   None  input directory root, needed for recursive search,
                              otherwise optional
      outdir      str   None  output directory root, needed for recursive output
                              matching input, otherwise optional
      outsubdir   str   None  when an additional subdirectory name is needed to
                              be added
      mkoutdir    bool  true  make output dir if not exists

      sort        str   None  Sort by name, basename, modtime, or size. The
                              default changes to modtime if -after/-before is
                              set, or to size if -larger/-smaller is set.

      recursive   bool  true  recursive input file search, requires indir
      mirror      bool  true  when input files are searched recursively, does
                              output follow the same directory structure?
                              required outdir
      swapsub     dict  None  when mirroring indir, if certain subdirectory
                              names needed to be changed

      tagkeys     str*  None  list of file parameters to grab tags
      appkeys     str*  None  list of parameters to apply tags

      include     str   None  only include cases with inkey having this phrase
                              this is different from -include key for clise (or heron.py)
      exclude     str   None  exclude cases with inkey having this phrase
                              this is different from -exclude key for clise (or heron.py)

      sortby      str         sorting key for the files and the method: mtime,
                              size, name, fullname: e.g., -sortby infile:mtime
                              will sort the task list by modified time of infile

      after       str   None this automatically set the sortby key to infile:mtime, 
                             in the ascending order
      before      str   None this automatically set the sortby key to infile:mtime, 
                             in the descending order
      larger      str   None this automatically set the sortby key to outfile:size, 
                             in the ascending order
      smaller     str   None this automatically set the sortby key to outfile:size,
                             in the descending order

      inkey      str infile  the main input file key name
      outkey     str outfile the main output file key name
      checkin    str* infile the input files to check if exists before run
      checkout   str* infile the output files to check if exists before run;
                             "-clobber" setting in heron.py
                             setting will decide whether skip the run or not

      rel2indir   str*  None list of file variables whose path is set relative
                             to the input file
      rel2outdir  str*  None list of file variables whose path is set relative
                             to the output file
      rel2nodir   str*  None list of file variables whose path is not set relative
                             to either the input or the output file

      verbose     int   0     chatter level for multiple_by_file(_multi)

### Logging 

The automatic logging of each run and a copy of the input parameters are
enabled through -logfile and -hisfile = "_auto_".
The log file contains the SHA1 has result of the input parameters, so
that one can tell the same run has been run or not.

22-04-28 11:27:58 0:00:00.000100 \
SHA1:81e37f0fee49f9729aaebe684e9853544664972b example.show_new_name  meco

When some of the routines are used frequently as a command line tool
instead of tasks, the logging and copying can be disabled. In general,
key --^parse sets the auto log off, which can be set by key -save_cmdline_log.

### More to explain

- Regex for infile and other files

      "infile==..." and "-infile.key==..." conditioning 

      "infile" : ["file1","file2","file1",...]

      how to refer the same file more than once in repetition of the same task(s)
      with different parameters: use "-infile.key..." option

- Priority order in parameter value assignment 
  (the latter supercede the former):

      --with < STARTUP < --load inside json_files 
            < input_json_files < input cli pars 
            < pars set by task generators < conditional_input_parameters
            < --WITH

            difference btw using cmdline.json5 vs cmdline_noswap.json5
            when 
                  alias search1='clise --^parse cmdline.json5 -infile'
                  alias search2='clise --^parse cmdline_noswap.json5 -infile'

                  A) search1 '(.*).py' -after somefile
                  B) search2 '(.*).py' -after somefile
                  C) search1 '(.*).py' --with -after somefile
                  D) search2 '(.*).py' --WITH -after somefile

                  A = C = D, but in B, the -after option is ignored.

- How to define multiple calls in serial using JSON

      in a single file (file.json):
            {
                  "-main" : "module1.routine1",
                  ...
            },
            {
                  "-main" : "module2.routine2",
                  ...
            },
            ....
            {
                  "-main" : "moduleN.routineN",
                  ...
            },

      % clise file.json

      Note a single task doesn't require the outer {}.

      When having multiple files

      % clise file1.json file2.json ... fileN.json

      each file can have multiple calls.
      JSON file without "-main" is considered as additional options
      for other calls.


- Common blocks
            {
                  // pars in a block without "-main" will be fed to other blocks
                  "common_par1" : "val1", 
                  "common_par2" : "val2", 
                  ...

                  "-apply to -main" : ["moduleB.routineB""], 
			// the parameters in this block applied to blocks with -main==moduleB.routineB
            },
            {
                  "-main" : "moduleB.routineB", //  
                  ...

            },
            {
                  "-main" : "moduleB.routineB", //  
                  ...

            },
            {
                  "-main" : "moduleC.routineC", //  
                  ...

            },
            .....

- Task generator features in rabbit.py: 
      esp. for repeating a set of multiple calls
            {
                  "-main" : "moduleA.taskgen", // example "rabbit.multiply_by_id_multi"
                  ...

                  "-apply until -block" : "end of taskgen", 
			// this indicates this block is a task gen block
			// and which block is the end for the seed
            },
            {
                  "-main" : "module1.routine1", // the first routine to multiply
                  ...
            },
            {
                  "-main" : "module2.routine2", // the 2nd routine to multiply
                  ...
            },
            ....
            {
                  "-main" : "moduleN.routineN", // the Nth routine to multiply
                  ...
            },
            {
                  // pars in a block without "-main" will be fed to all the routines above
                  "common_par1" : "val1", 
                  "common_par2" : "val2", 
                  ...

                  "-block" : "end of taskgen", // this indicates the ending block for task gen
            },

	The whole task gen block should be in a single file.	

      how to write custom generator: 

            - basically return a list of OrderedDict array,
              where each contains all the parameters for a routine call.

            - The generator will receive the list of the OrderedDict from
              routine1 to routineN as an input parameter "seed".

            - One can redefine the name of the par "seed" with "-seedkey". 
              (not be implemented yet)

      4 task gen routines are provided in rabbit.py
            "multiply_by_id"
            "multiply_by_id_multi"
            "multiply_by_file"
            "multiply_by_file_multi"

            in the latter two, file wild card vs regex
                  * <=> (.*)

            *.* in the shell prompt (e.g., % ls *.*) is equivalent to

                        "infile": "(.*).(.*)"

                  the first and second (.*) can be refered to {1}, {2}
                  in other parameters

                        "outfile" : "{1}.png"

                  "tagkeys" enables phrase grab from other keys
                        requires more explanation...

- JSON compatibility

      using hjson module: accepted extension:
	ext ='(json|json5|hjson|jsonc)'

      Normal key consisting of [a-zA-Z] doesn't require "".
            e.g.,
                  x : 1,    <=>    "x": 1,

      For others and string values, it's recommended to use "":
            e.g., 
                  "-main": "module.routine",
            
- Block type

       -main       -apply ...          -block           type

       yes         no                  -                regular task block
       no          yes/no              -                common parameter block for regular tasks

       yes         yes w. end phrase   -                task generation block
       yes/no      no                  end phrase       the end of the task gen seed
       no          -                   "rabbit"         common parameter block for the task gen seed

### Changes

v0.1.7 2023/08
      - add time axis on plottool

v0.1.6 2023/06
      - add wcs  to dplot  in plottool: 
                        e.g., -attr wcs
                        range set by degrees
      - add time to plot1d in plottool: 
                        e.g., -attr xtime,ytime
      - add rebin.py  and update plottool.py with rebin

v0.1.5 2023/03
      - add read_mca in tabletool

v0.1.4 2023/03
      - adhoc fix of a bug in loading clise's own modules

v0.1.3 2023/03
      - add tabletool.py

v0.1.2 2023/03
      - add xray_mirror.py

v0.1.1 2023/03
      - Lower python requirement to 3.8 instead of 3.9

v0.1.0 2023/03
      - Initial version
      - Forked from cjpy
      - Implemented sequential executions of routines with JSON blocks {}
      - Implemented custom routine for iterative calls
