import sys

from parser import LLParser as Parser
from scanner import Scanner
from semantic import Semantic

GRAMMAR_PATH = "grammar.txt"


def main():
    # 명령어 입력 오류 체크
    if len(sys.argv) != 2:
        sys.exit("Usage: Compiler2021 <input_file_name>")

    with open(f'./{sys.argv[1]}', 'r') as file:
        code = file.read()

    # Lexical analyzer (Scanner)
    scanner = Scanner(code)
    scanner.print_tokens()

    # Syntax Analyzer (Parser)
    # LL-Parser
    # 1. make LL Grammar - 모호성 해결 (left-factoring, left-recursion 제거)
    # 2. FIRST & FOLLOW 구하기
    # 3. parsing table 생성
    # 4. AST 생성
    # 5. symbol table 생성
    parser = Parser(scanner.tokens, GRAMMAR_PATH)
    parser.print_grammar()
    parser.print_first_follow()
    parser.print_parsing_table()
    parser.print_ast()
    parser.write_symbol_table(open(f'./{sys.argv[1].split(".")[0]}.symbol', 'w'))

    # Semantic Analyzer
    semantic = Semantic(parser.ast, parser.symbol_table)

    # Intermediate Code Generator
    # Code Generator


if __name__ == '__main__':
    main()
