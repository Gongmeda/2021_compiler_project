import sys

from parser import Parser
from scanner import Scanner

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
    parser = Parser(scanner.tokens, GRAMMAR_PATH)
    parser.print_grammar()
    # LL-Parser
        # FIRST & FOLLOW 구하기
        # make LL Grammar
            # 모호성 해결
            # left-factoring
            # left-recursion 제거
        # parsing table 생성
        # AST 생성

    # Semantic Analyzer

    # Intermediate Code Generator
    # Code Generator


if __name__ == '__main__':
    main()
