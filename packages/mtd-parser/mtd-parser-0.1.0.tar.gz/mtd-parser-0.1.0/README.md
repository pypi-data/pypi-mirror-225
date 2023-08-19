# Executable UML Class Method Parser

Parses an *.mtd file (method) to yield an abstract syntax tree using python named tuples

### Why you need this

You need to process an *.mtd file in preparation for populating a database or some other purpose

### Installation

Create or use a python 3.11+ environment. Then

% pip install mtd-parser

At this point you can invoke the parser via the command line or from your python script.

#### From your python script

You need this import statement at a minimum:

    from mtd-parser.parser import MethodParser

You then specify a path as shown:

    result = MethodParser.parse_file(file_input=path_to_file, debug=False)

In either case, `result` will be a list of parsed scrall statements. You may find the header of the `visitor.py`
file helpful in interpreting these results.

#### From the command line

This is not the intended usage scenario, but may be helpful for testing or exploration. Since the parser
may generate some diagnostic info you may want to create a fresh working directory and cd into it
first. From there...

    % mtd ping.mtd

The .mtd extension is not necessary, but the file must contain mtd text. See this repository's wiki for
more about the xsm language. The grammar is defined in the [method.peg](https://github.com/modelint/mtd-parser/blob/main/src/mtd_parser/method.peg) file. (if the link breaks after I do some update to the code, 
just browse through the code looking for the method.peg file, and let me know so I can fix it)

You can also specify a debug option like this:

    % mtd ping.mtd -D

This will create a diagnostics folder in your current working directory and deposit a couple of PDFs defining
the parse of both the state model grammar: `method_tree.pdf` and your supplied text: `method.pdf`.

You should also see a file named `mtd-parser.log` in a diagnostics directory within your working directory