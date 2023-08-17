# Documentation extraction

## Purpose

Lupin-danquin CLI allow to create SDD documentation from source code.

## Run it

- Default command
1. Go to current directory.
2. Execute
`danq valdocs "app1, app2, app3, ..."`
3. Result is available in "./val3_documentation.md"  

- With `--beginning-file-path` option

    You can add the content of a third party file before the application documentation.

1. Execute the above command with `--beginning-file-path` or `-b` flag with path to file  
`danq valdocs "app1, app2, app3, ..." -b "path/file"`

- With `--end-file-path` option

    You can add the content of a third party file after the application documentation.
1. Execute the above command with `--end-file-path` or `-e` flag with path to file  
`danq valdocs "app1, app2, app3, ..." -e "path/file"`

- With environnement variables

    You can set environment variables:
    - VAL3_APPLICATIONS=app1, app2, ...
    - VAL3_BEGINNING_FILE_PATH=path/to/file
    - VAL3_END_FILE_PATH=path/to/file

- help command
1. Execute `danq valdocs --help`


## Add documentation

### For a program (pgx file)

Edit your program and add one or more lines of comments the line after "begin" keyword.

### For an application

Create a text file named "README.md" at the same level as "pjx" file. And add one or more lines of description.

## Improvements oportunities

- Improve table for sockets
- Allow to end docstring with 10 * "/"

## Other ideas

To create a sanitizer:

- detect unused variables (private, public?): already done for local variables and parameters (not global variables)
- detect wrongly named variables (l_, x_, s/b/n/st, t, Out): DONE
- validate plantuml diagram from pjx files
- code coverage ? find if all return values are tested
