import sys

from scanner import Scanner


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
    # LR-Parser vs LL-Parser
    # parser table
    # AST

    # Semantic Analyzer

    # Intermediate Code Generator
    # Code Generator


if __name__ == '__main__':
    main()
